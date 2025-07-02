"""CLI commands for Azure metrics collection."""

import asyncio
from typing import Optional, List
from datetime import datetime, timedelta
import click
from rich.console import Console
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn
from rich.panel import Panel
from rich import print as rprint

import sys
import os
# Add the common module to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..', 'cloud_analyzer.common', 'src'))

from models.base import ResourceFilter, CloudProvider
from models.metrics import MetricsCollectionConfig
from providers.azure import AzureProvider
from database.connection import DatabaseConnection, get_database_url
from services.resource_discovery import ResourceDiscoveryService
from services.metrics_collector import MetricsCollectionService
from ..utils.config import get_config, get_azure_credentials

console = Console()


@click.group()
def metrics():
    """Azure metrics collection commands."""
    pass


@metrics.command()
@click.option('--resource-group', '-g', multiple=True,
              help='Filter by resource group (can be specified multiple times)')
@click.option('--resource-type', '-t', multiple=True,
              help='Filter by resource type (can be specified multiple times)')
@click.option('--subscription-id', '-s', multiple=True,
              help='Filter by subscription ID (can be specified multiple times)')
@click.option('--dry-run', is_flag=True, help='Show what would be discovered without persisting')
@click.option('--output-format', '-o', type=click.Choice(['table', 'json', 'csv']),
              default='table', help='Output format')
@click.option('--verbose', '-v', is_flag=True, help='Verbose output')
async def discover(
    resource_group: tuple,
    resource_type: tuple,
    subscription_id: tuple,
    dry_run: bool,
    output_format: str,
    verbose: bool
):
    """Discover Azure resources."""
    try:
        config = get_config()

        # Create resource filter
        resource_filter = ResourceFilter(
            resource_groups=list(resource_group) if resource_group else None,
            resource_types=list(resource_type) if resource_type else None,
            subscription_ids=list(subscription_id) if subscription_id else None
        )

        # Initialize Azure provider
        azure_config = get_azure_credentials(config)
        provider = AzureProvider(azure_config)

        # Initialize database connection
        db_connection = DatabaseConnection(config)
        if not dry_run:
            db_connection.initialize()
            if not db_connection.test_connection():
                rprint("[red]Failed to connect to database. Please check your configuration.[/red]")
                return

        # Initialize discovery service
        discovery_service = ResourceDiscoveryService(provider, db_connection)

        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TaskProgressColumn(),
            console=console
        ) as progress:

            task = progress.add_task("Discovering resources...", total=None)

            # Discover resources
            resources = await discovery_service.discover_resources(
                resource_filter=resource_filter,
                persist_to_db=not dry_run
            )

            progress.update(task, completed=len(resources), total=len(resources))

        if dry_run:
            rprint(f"[yellow]DRY RUN: Would discover {len(resources)} resources[/yellow]")
        else:
            rprint(f"[green]Discovered {len(resources)} resources[/green]")

        # Display results
        if output_format == 'table':
            _display_resources_table(resources, verbose)
        elif output_format == 'json':
            _display_resources_json(resources)
        elif output_format == 'csv':
            _display_resources_csv(resources)

    except Exception as e:
        rprint(f"[red]Discovery failed: {e}[/red]")
        if verbose:
            console.print_exception()
        raise click.ClickException(str(e))


@metrics.command()
@click.option('--resource-group', '-g', multiple=True,
              help='Filter by resource group (can be specified multiple times)')
@click.option('--resource-type', '-t', multiple=True,
              help='Filter by resource type (can be specified multiple times)')
@click.option('--subscription-id', '-s', multiple=True,
              help='Filter by subscription ID (can be specified multiple times)')
@click.option('--start-time', type=click.DateTime(['%Y-%m-%d', '%Y-%m-%dT%H:%M:%S']),
              help='Start time for metrics collection (YYYY-MM-DD or YYYY-MM-DDTHH:MM:SS)')
@click.option('--end-time', type=click.DateTime(['%Y-%m-%d', '%Y-%m-%dT%H:%M:%S']),
              help='End time for metrics collection (YYYY-MM-DD or YYYY-MM-DDTHH:MM:SS)')
@click.option('--interval-minutes', type=int, default=15,
              help='Collection interval in minutes (default: 15)')
@click.option('--batch-size', type=int, default=100,
              help='Batch size for processing (default: 100)')
@click.option('--parallel-workers', type=int, default=4,
              help='Number of parallel workers (default: 4)')
@click.option('--dry-run', is_flag=True, help='Show what would be collected without persisting')
@click.option('--verbose', '-v', is_flag=True, help='Verbose output')
async def collect(
    resource_group: tuple,
    resource_type: tuple,
    subscription_id: tuple,
    start_time: Optional[datetime],
    end_time: Optional[datetime],
    interval_minutes: int,
    batch_size: int,
    parallel_workers: int,
    dry_run: bool,
    verbose: bool
):
    """Collect Azure metrics for resources."""
    try:
        config = get_config()

        # Create resource filter
        resource_filter = ResourceFilter(
            resource_groups=list(resource_group) if resource_group else None,
            resource_types=list(resource_type) if resource_type else None,
            subscription_ids=list(subscription_id) if subscription_id else None
        )

        # Create metrics collection config
        metrics_config = MetricsCollectionConfig(
            interval_minutes=interval_minutes,
            batch_size=batch_size,
            parallel_workers=parallel_workers
        )

        # Initialize services
        azure_config = get_azure_credentials(config)
        provider = AzureProvider(azure_config)

        db_connection = DatabaseConnection(config)
        if not dry_run:
            db_connection.initialize()
            if not db_connection.test_connection():
                rprint("[red]Failed to connect to database. Please check your configuration.[/red]")
                return

        discovery_service = ResourceDiscoveryService(provider, db_connection)
        metrics_service = MetricsCollectionService(
            provider, db_connection, discovery_service, metrics_config
        )

        # Set default time range if not provided
        if not end_time:
            end_time = datetime.utcnow()
        if not start_time:
            start_time = end_time - timedelta(hours=24)

        rprint(f"[blue]Collecting metrics from {start_time} to {end_time}[/blue]")

        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:

            task = progress.add_task("Collecting metrics...", total=None)

            # Collect metrics
            collection_run = await metrics_service.collect_all_metrics(
                resource_filter=resource_filter,
                start_time=start_time,
                end_time=end_time,
                dry_run=dry_run
            )

            progress.update(task, completed=1, total=1)

        # Display results
        _display_collection_results(collection_run, dry_run)

    except Exception as e:
        rprint(f"[red]Metrics collection failed: {e}[/red]")
        if verbose:
            console.print_exception()
        raise click.ClickException(str(e))


@metrics.command()
@click.option('--resource-type', '-t', help='Filter by resource type')
@click.option('--resource-group', '-g', help='Filter by resource group')
@click.option('--subscription-id', '-s', help='Filter by subscription ID')
@click.option('--output-format', '-o', type=click.Choice(['table', 'json', 'csv']),
              default='table', help='Output format')
@click.option('--verbose', '-v', is_flag=True, help='Verbose output')
async def list_resources(
    resource_type: Optional[str],
    resource_group: Optional[str],
    subscription_id: Optional[str],
    output_format: str,
    verbose: bool
):
    """List discovered resources from database."""
    try:
        config = get_config()

        # Initialize database connection
        db_connection = DatabaseConnection(config)
        db_connection.initialize()

        if not db_connection.test_connection():
            rprint("[red]Failed to connect to database. Please check your configuration.[/red]")
            return

        # Initialize services
        azure_config = get_azure_credentials(config)
        provider = AzureProvider(azure_config)
        discovery_service = ResourceDiscoveryService(provider, db_connection)

        # Get resources from database
        resources = discovery_service.get_resources_from_db(
            resource_types=[resource_type] if resource_type else None,
            resource_groups=[resource_group] if resource_group else None,
            subscription_ids=[subscription_id] if subscription_id else None
        )

        rprint(f"[green]Found {len(resources)} resources in database[/green]")

        # Display results
        if output_format == 'table':
            _display_resources_table(resources, verbose)
        elif output_format == 'json':
            _display_resources_json(resources)
        elif output_format == 'csv':
            _display_resources_csv(resources)

    except Exception as e:
        rprint(f"[red]Failed to list resources: {e}[/red]")
        if verbose:
            console.print_exception()
        raise click.ClickException(str(e))


@metrics.command()
@click.option('--limit', '-l', type=int, default=10, help='Number of recent runs to show')
@click.option('--verbose', '-v', is_flag=True, help='Verbose output')
async def collection_history(limit: int, verbose: bool):
    """Show metrics collection history."""
    try:
        config = get_config()

        # Initialize services
        azure_config = get_azure_credentials(config)
        provider = AzureProvider(azure_config)

        db_connection = DatabaseConnection(config)
        db_connection.initialize()

        discovery_service = ResourceDiscoveryService(provider, db_connection)
        metrics_config = MetricsCollectionConfig()
        metrics_service = MetricsCollectionService(
            provider, db_connection, discovery_service, metrics_config
        )

        # Get collection history
        collection_runs = metrics_service.get_collection_history(limit=limit)

        if not collection_runs:
            rprint("[yellow]No collection runs found[/yellow]")
            return

        # Display collection history table
        _display_collection_history(collection_runs, verbose)

    except Exception as e:
        rprint(f"[red]Failed to get collection history: {e}[/red]")
        if verbose:
            console.print_exception()
        raise click.ClickException(str(e))


@metrics.command()
@click.option('--retention-days', type=int, help='Number of days to retain (default from config)')
@click.option('--dry-run', is_flag=True, help='Show what would be cleaned up')
@click.option('--verbose', '-v', is_flag=True, help='Verbose output')
async def cleanup(retention_days: Optional[int], dry_run: bool, verbose: bool):
    """Clean up old metrics data."""
    try:
        config = get_config()

        # Initialize services
        azure_config = get_azure_credentials(config)
        provider = AzureProvider(azure_config)

        db_connection = DatabaseConnection(config)
        db_connection.initialize()

        discovery_service = ResourceDiscoveryService(provider, db_connection)
        metrics_config = MetricsCollectionConfig()
        metrics_service = MetricsCollectionService(
            provider, db_connection, discovery_service, metrics_config
        )

        if dry_run:
            rprint("[yellow]DRY RUN: Would clean up old metrics data[/yellow]")
            return

        # Clean up old data
        deleted_count = metrics_service.cleanup_old_data(retention_days)

        rprint(f"[green]Cleaned up {deleted_count} old metrics records[/green]")

    except Exception as e:
        rprint(f"[red]Cleanup failed: {e}[/red]")
        if verbose:
            console.print_exception()
        raise click.ClickException(str(e))


def _display_resources_table(resources: List, verbose: bool):
    """Display resources in table format."""
    table = Table(title="Discovered Resources")

    table.add_column("Name", style="cyan")
    table.add_column("Type", style="magenta")
    table.add_column("Resource Group", style="green")
    table.add_column("Location", style="blue")

    if verbose:
        table.add_column("Subscription ID", style="yellow")
        table.add_column("Tags", style="white")

    for resource in resources[:50]:  # Limit to first 50 for readability
        row = [
            resource.name,
            resource.resource_type.split('/')[-1],  # Show only the last part
            resource.resource_group,
            resource.location
        ]

        if verbose:
            row.append(resource.subscription_id[:8] + "...")  # Truncate subscription ID
            row.append(str(len(resource.tags)) + " tags" if resource.tags else "No tags")

        table.add_row(*row)

    if len(resources) > 50:
        table.caption = f"Showing first 50 of {len(resources)} resources"

    console.print(table)


def _display_resources_json(resources: List):
    """Display resources in JSON format."""
    import json

    resource_data = []
    for resource in resources:
        resource_data.append({
            'id': resource.id,
            'name': resource.name,
            'type': resource.resource_type,
            'resource_group': resource.resource_group,
            'location': resource.location,
            'subscription_id': resource.subscription_id,
            'tags': resource.tags
        })

    print(json.dumps(resource_data, indent=2, default=str))


def _display_resources_csv(resources: List):
    """Display resources in CSV format."""
    import csv
    import sys

    writer = csv.writer(sys.stdout)
    writer.writerow(['Name', 'Type', 'ResourceGroup', 'Location', 'SubscriptionId', 'Tags'])

    for resource in resources:
        writer.writerow([
            resource.name,
            resource.resource_type,
            resource.resource_group,
            resource.location,
            resource.subscription_id,
            ';'.join([f"{k}={v}" for k, v in resource.tags.items()]) if resource.tags else ''
        ])


def _display_collection_results(collection_run, dry_run: bool):
    """Display metrics collection results."""
    if dry_run:
        status_color = "yellow"
        status_text = "DRY RUN"
    else:
        status_color = "green" if collection_run.status.value == "completed" else "red"
        status_text = collection_run.status.value.upper()

    duration = collection_run.duration_minutes
    duration_text = f"{duration:.2f} minutes" if duration else "In progress"

    panel_content = f"""
[bold]Collection Run ID:[/bold] {collection_run.id}
[bold]Status:[/bold] [{status_color}]{status_text}[/{status_color}]
[bold]Duration:[/bold] {duration_text}
[bold]Resources Processed:[/bold] {collection_run.resources_processed}
[bold]Metrics Collected:[/bold] {collection_run.metrics_collected}
[bold]Errors:[/bold] {collection_run.errors_count}
"""

    if collection_run.error_details:
        panel_content += f"\n[bold]Recent Errors:[/bold]\n"
        for error in collection_run.error_details[-3:]:  # Show last 3 errors
            panel_content += f"  • {error.get('error', 'Unknown error')}\n"

    console.print(Panel(panel_content, title="Collection Results", border_style="blue"))


def _display_collection_history(collection_runs: List, verbose: bool):
    """Display collection history in table format."""
    table = Table(title="Collection History")

    table.add_column("Run ID", style="cyan")
    table.add_column("Status", style="magenta")
    table.add_column("Start Time", style="blue")
    table.add_column("Duration", style="green")
    table.add_column("Resources", style="yellow")
    table.add_column("Metrics", style="white")
    table.add_column("Errors", style="red")

    for run in collection_runs:
        duration = f"{run.duration_minutes:.1f}m" if run.duration_minutes else "N/A"
        status_style = "green" if run.status.value == "completed" else "red"

        table.add_row(
            run.id[:8] + "...",
            f"[{status_style}]{run.status.value}[/{status_style}]",
            run.start_time.strftime("%Y-%m-%d %H:%M"),
            duration,
            str(run.resources_processed),
            str(run.metrics_collected),
            str(run.errors_count)
        )

    console.print(table)


# Make the async commands work with Click
def async_command(f):
    """Decorator to run async commands with asyncio."""
    def wrapper(*args, **kwargs):
        try:
            return asyncio.run(f(*args, **kwargs))
        except Exception as e:
            if hasattr(e, '__cause__') and isinstance(e.__cause__, click.ClickException):
                raise e.__cause__
            raise click.ClickException(str(e))
    return wrapper

# Apply async decorator to all async commands
discover.callback = async_command(discover.callback)
collect.callback = async_command(collect.callback)
list_resources.callback = async_command(list_resources.callback)
collection_history.callback = async_command(collection_history.callback)
cleanup.callback = async_command(cleanup.callback)
