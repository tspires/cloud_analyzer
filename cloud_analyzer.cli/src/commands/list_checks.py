"""List available optimization checks."""

from typing import Optional

import click
from rich.console import Console
from rich.table import Table

from checks.registry import check_registry
from models import CheckType, CloudProvider
from cli_constants import (
    PROVIDER_CHOICES_WITH_ALL,
    DEFAULT_PROVIDER,
    ERROR_INVALID_CHECK_TYPE,
    ERROR_NO_CHECKS_FOUND,
)

console = Console()


@click.command("list-checks")
@click.option(
    "--provider",
    type=click.Choice(PROVIDER_CHOICES_WITH_ALL, case_sensitive=False),
    default=DEFAULT_PROVIDER,
    help="Filter checks by cloud provider",
)
@click.option(
    "--type",
    "check_type",
    help="Filter checks by type (e.g., idle_resource, right_sizing)",
)
def list_checks(provider: str, check_type: Optional[str]) -> None:
    """List all available optimization checks.
    
    This command shows all the checks that can be run to identify
    cost optimization opportunities in your cloud infrastructure.
    """
    # Get all registered checks
    all_checks = check_registry.list_all()
    
    # Filter by provider if specified
    if provider != "all":
        provider_enum = CloudProvider(provider)
        all_checks = [
            check for check in all_checks
            if provider_enum in check.supported_providers
        ]
    
    # Filter by type if specified
    if check_type:
        try:
            check_type_enum = CheckType(check_type)
            all_checks = [
                check for check in all_checks
                if check.check_type == check_type_enum
            ]
        except ValueError:
            console.print(f"[red]Error:[/red] {ERROR_INVALID_CHECK_TYPE.format(check_type)}")
            console.print("\nValid check types:")
            for ct in CheckType:
                console.print(f"  • {ct.value}")
            return
    
    if not all_checks:
        console.print(f"[yellow]{ERROR_NO_CHECKS_FOUND}[/yellow]")
        return
    
    # Create table
    table = Table(title="Available Optimization Checks")
    table.add_column("Check Name", style="cyan", no_wrap=True)
    table.add_column("Type", style="magenta")
    table.add_column("Providers", style="green")
    table.add_column("Description", style="white")
    
    # Add checks to table
    for check in sorted(all_checks, key=lambda c: (c.check_type.value, c.name)):
        providers = ", ".join(p.value.upper() for p in sorted(check.supported_providers, key=lambda x: x.value))
        table.add_row(
            check.name,
            check.check_type.value,
            providers,
            check.description,
        )
    
    console.print(table)
    
    # Show summary
    console.print(f"\nTotal checks: {len(all_checks)}")
    
    # Show check types if not filtered
    if not check_type:
        check_types = set(check.check_type for check in all_checks)
        console.print(f"Check types: {len(check_types)}")
        for ct in sorted(check_types, key=lambda x: x.value):
            count = sum(1 for check in all_checks if check.check_type == ct)
            console.print(f"  • {ct.value}: {count} checks")