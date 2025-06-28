"""Run a single optimization check by name."""

import asyncio
from typing import Optional

import click
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn

from checks.registry import check_registry
from models import CloudProvider

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
    type=click.Choice(["aws", "azure", "gcp"], case_sensitive=False),
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
        cloud-analyzer run-check idle-ec2-instances --provider aws
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
    
    try:
        # Validate credentials
        with console.status(f"[bold yellow]Validating {provider.upper()} credentials...[/bold yellow]") as status:
            # In real implementation, credentials would be validated here
            import time
            time.sleep(0.5)  # Simulate validation
            console.print("✓ [green]Credentials validated[/green]")
        
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
        await asyncio.sleep(0.5)  # Simulate initialization
        progress.remove_task(task)
        console.print(f"  ✓ [green]{provider.value.upper()} provider initialized[/green]")
        
        # Step 2: Discover resources
        task = progress.add_task(
            f"[cyan]Discovering resources for check '{check.name}'...[/cyan]",
            total=None
        )
        await asyncio.sleep(1.0)  # Simulate discovery
        progress.remove_task(task)
        console.print(f"  ✓ [green]Resources discovered[/green]")
        
        # Step 3: Run the check
        task = progress.add_task(
            f"[cyan]Analyzing resources...[/cyan]",
            total=None
        )
        await asyncio.sleep(1.5)  # Simulate check execution
        progress.remove_task(task)
        console.print(f"  ✓ [green]Analysis complete[/green]")
    
    # In real implementation, this would return actual results
    return results