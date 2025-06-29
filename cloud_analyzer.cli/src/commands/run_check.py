"""Run a single optimization check by name."""

import asyncio
import sys
from pathlib import Path
from typing import Optional

import click
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn

# Add parent directory to path to import from cloud_analyzer.common
sys.path.append(str(Path(__file__).parent.parent.parent.parent / 'cloud_analyzer.common' / 'src'))

from checks.registry import check_registry
from checks.register_checks import register_all_checks
from models.base import CloudProvider
from providers.azure import AzureProvider

from formatters.check_results import format_check_results
from utils.config import load_config
from .analyze_helpers import (
    display_summary,
    save_results_csv,
    save_results_json,
    validate_configuration,
)

console = Console()


@click.command("run-check")
@click.argument("check_name")
@click.option(
    "--provider",
    type=click.Choice(["azure"], case_sensitive=False),
    help="Cloud provider (required if check supports multiple providers)",
)
@click.option(
    "--region",
    help="Specific region to analyze (defaults to all regions)",
)
@click.option(
    "--output",
    type=click.Choice(["table", "json", "csv"], case_sensitive=False),
    default="table",
    help="Output format",
)
@click.option(
    "--output-file",
    type=click.Path(),
    help="Save results to file",
)
def run_check(
    check_name: str,
    provider: Optional[str],
    region: Optional[str],
    output: str,
    output_file: Optional[str],
) -> None:
    """Run a single optimization check by name.
    
    Check names can be found using the 'list-checks' command.
    
    Example:
        cloud-analyzer run-check azure-vm-deallocated --provider azure
    """
    # Get the check from registry
    check = check_registry.get(check_name)
    if not check:
        console.print(f"[red]Error:[/red] Check '{check_name}' not found")
        console.print("\nRun 'cloud-analyzer list-checks' to see available checks")
        return
    
    # Determine provider
    if len(check.supported_providers) > 1 and not provider:
        console.print(
            f"[red]Error:[/red] Check '{check_name}' supports multiple providers. "
            "Please specify --provider"
        )
        console.print(f"Supported providers: {', '.join(p.value for p in check.supported_providers)}")
        return
    
    if provider:
        provider_enum = CloudProvider(provider)
        if provider_enum not in check.supported_providers:
            console.print(
                f"[red]Error:[/red] Check '{check_name}' does not support provider '{provider}'"
            )
            console.print(f"Supported providers: {', '.join(p.value for p in check.supported_providers)}")
            return
    else:
        # Use the only supported provider
        provider_enum = list(check.supported_providers)[0]
        provider = provider_enum.value
    
    # Load and validate configuration
    config = load_config()
    if not validate_configuration(config, provider):
        return
    
    # Display check information
    console.print(f"\n[bold cyan]Running check:[/bold cyan] {check.name}")
    console.print(f"[dim]Description: {check.description}[/dim]")
    console.print(f"[dim]Provider: {provider.upper()}[/dim]")
    if region:
        console.print(f"[dim]Region: {region}[/dim]")
    else:
        console.print("[dim]Regions: All configured regions[/dim]")
    console.print()
    
    # Ensure checks are registered
    register_all_checks()
    
    try:
        # Run the check
        console.print(f"\n[bold yellow]Executing check '{check_name}'...[/bold yellow]")
        results = asyncio.run(
            run_single_check(check, provider_enum, region, config)
        )
        
        # Handle output formatting
        if output == "table":
            if results:
                format_check_results(results, console, config, provider_enum)
                display_summary(results)
            else:
                console.print("[yellow]No optimization opportunities found[/yellow]")
        elif output == "json":
            if output_file:
                save_results_json(results, output_file)
            else:
                import json
                console.print(json.dumps([r.dict() for r in results], indent=2, default=str))
        elif output == "csv":
            if output_file:
                save_results_csv(results, output_file)
            else:
                console.print("[red]Error:[/red] CSV output requires --output-file")
        
    except Exception as e:
        console.print(f"[red]Error running check:[/red] {str(e)}")
        raise


async def run_single_check(
    check,
    provider: CloudProvider,
    region: Optional[str],
    config: dict,
) -> list:
    """Run a single check and return results.
    
    Args:
        check: Check instance to run
        provider: Cloud provider
        region: Optional region filter
        config: Configuration dictionary
        
    Returns:
        List of CheckResult instances
    """
    results = []
    
    # Create provider instance
    provider_config = config.get(provider.value, {})
    provider_instance = None
    
    if provider == CloudProvider.AZURE:
        subscription_id = provider_config.get('subscription_id')
        provider_instance = AzureProvider(subscription_id=subscription_id)
    
    if not provider_instance:
        raise Exception(f"Provider {provider.value} not implemented")
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console
    ) as progress:
        # Step 1: Initialize provider
        task = progress.add_task(
            f"[cyan]Initializing {provider.value.upper()} provider...[/cyan]",
            total=None
        )
        await provider_instance.initialize()
        progress.remove_task(task)
        console.print(f"  ✓ [green]{provider.value.upper()} provider initialized[/green]")
        
        # Step 2: Validate credentials
        task = progress.add_task(
            f"[cyan]Validating credentials...[/cyan]",
            total=None
        )
        if not await provider_instance.validate_credentials():
            progress.remove_task(task)
            raise Exception(f"Invalid {provider.value} credentials")
        progress.remove_task(task)
        console.print(f"  ✓ [green]Credentials validated[/green]")
        
        # Step 3: Get resources
        task = progress.add_task(
            f"[cyan]Fetching resources...[/cyan]",
            total=None
        )
        regions = [region] if region else None
        resources = await provider_instance.list_resources(regions=regions)
        progress.remove_task(task)
        console.print(f"  ✓ [green]Found {len(resources)} resources[/green]")
        
        # Step 4: Run the check
        task = progress.add_task(
            f"[cyan]Running check...[/cyan]",
            total=None
        )
        results = await check.run(provider_instance, resources)
        progress.remove_task(task)
        console.print(f"  ✓ [green]Check complete[/green]")
    
    return results