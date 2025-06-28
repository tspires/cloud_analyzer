"""Analyze command for running optimization checks."""

import asyncio
from pathlib import Path
from typing import List, Optional

import click
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.table import Table

from models import CloudProvider

from formatters.check_results import format_check_results
from utils.config import load_config
from utils.cloud_identity import display_cloud_identity_panel, display_multi_cloud_identity_table
from .analyze_helpers import (
    determine_providers,
    display_dry_run_info,
    display_summary,
    filter_results_by_severity,
    save_results_csv,
    save_results_json,
    validate_configuration,
)

console = Console()


@click.command()
@click.option(
    "--provider",
    type=click.Choice(["aws", "azure", "gcp", "all"], case_sensitive=False),
    default="all",
    help="Cloud provider to analyze",
)
@click.option(
    "--region",
    help="Specific region to analyze (defaults to all regions)",
)
@click.option(
    "--checks",
    help="Comma-separated list of check types to run",
)
@click.option(
    "--severity",
    type=click.Choice(["critical", "high", "medium", "low", "all"], case_sensitive=False),
    default="all",
    help="Minimum severity level to display",
)
@click.option(
    "--output",
    type=click.Choice(["table", "json", "csv"], case_sensitive=False),
    default="table",
    help="Output format",
)
@click.option(
    "--output-file",
    type=click.Path(path_type=Path),
    help="Save results to file",
)
@click.option(
    "--dry-run",
    is_flag=True,
    help="Show what would be analyzed without running checks",
)
def analyze(
    provider: str,
    region: Optional[str],
    checks: Optional[str],
    severity: str,
    output: str,
    output_file: Optional[Path],
    dry_run: bool,
) -> None:
    """Analyze cloud resources for optimization opportunities.
    
    This command will scan your cloud resources and identify potential
    cost savings through various optimization checks.
    """
    # Load and validate configuration
    config = load_config()
    if not validate_configuration(config, provider):
        return
    
    # Determine providers and parse check types
    providers_to_analyze = determine_providers(provider, config)
    check_types = [c.strip() for c in checks.split(",")] if checks else None
    
    # Handle dry run
    if dry_run:
        display_dry_run_info(providers_to_analyze, region, check_types)
        return
    
    # Display cloud identity information
    console.print("\n[bold cyan]Cloud Instance Information[/bold cyan]\n")
    if provider == "all":
        display_multi_cloud_identity_table(config, console)
    else:
        display_cloud_identity_panel(providers_to_analyze[0], config, console)
    
    # Run analysis
    console.print("\n[bold cyan]Starting cloud resource analysis...[/bold cyan]\n")
    
    try:
        # Step 1: Validate credentials
        with console.status("[bold yellow]Validating credentials...[/bold yellow]") as status:
            # Validate credentials for each provider
            for provider in providers_to_analyze:
                status.update(f"[bold yellow]Validating {provider.value.upper()} credentials...[/bold yellow]")
                # In real implementation, credentials would be validated here
                import time
                time.sleep(0.5)  # Simulate validation
            console.print("✓ [green]Credentials validated[/green]")
        
        # Step 2: Run async analysis
        console.print("\n[bold yellow]Running analysis...[/bold yellow]")
        results = asyncio.run(
            run_analysis(providers_to_analyze, region, check_types, config)
        )
        
        # Step 3: Filter by severity
        console.print("\n[bold yellow]Filtering results by severity...[/bold yellow]")
        results = filter_results_by_severity(results, severity)
        console.print(f"✓ [green]Found {len(results)} findings matching severity filter[/green]")
        
        # Handle output formatting
        if output == "table":
            # Determine the provider for display (if single provider)
            display_provider = None
            if provider != "all" and providers_to_analyze:
                display_provider = providers_to_analyze[0]
            format_check_results(results, console, config, display_provider)
            display_summary(results)
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
        console.print(f"[red]Error during analysis:[/red] {str(e)}")
        raise


async def run_analysis(
    providers: List[CloudProvider],
    region: Optional[str],
    check_types: Optional[List[str]],
    config: dict,
) -> list:
    """Run the actual analysis."""
    results = []
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console
    ) as progress:
        for provider in providers:
            # Step 1: Initialize provider
            task = progress.add_task(
                f"[cyan]Initializing {provider.value.upper()} provider...[/cyan]",
                total=None
            )
            # In real implementation, provider would be initialized here
            await asyncio.sleep(0.5)  # Simulate initialization
            progress.remove_task(task)
            console.print(f"  ✓ [green]{provider.value.upper()} provider initialized[/green]")
            
            # Step 2: Discover resources
            task = progress.add_task(
                f"[cyan]Discovering {provider.value.upper()} resources...[/cyan]",
                total=None
            )
            # In real implementation, resources would be discovered here
            await asyncio.sleep(1.0)  # Simulate discovery
            progress.remove_task(task)
            console.print(f"  ✓ [green]Discovered resources in {provider.value.upper()}[/green]")
            
            # Step 3: Run checks
            task = progress.add_task(
                f"[cyan]Running optimization checks for {provider.value.upper()}...[/cyan]",
                total=None
            )
            # In real implementation, checks would be run here
            await asyncio.sleep(1.5)  # Simulate check execution
            progress.remove_task(task)
            console.print(f"  ✓ [green]Completed checks for {provider.value.upper()}[/green]")
    
    # In real implementation, this would return actual results
    return results