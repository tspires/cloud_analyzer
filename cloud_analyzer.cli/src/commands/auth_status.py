"""Auth status command for checking authentication status."""

import asyncio
from typing import Optional

import click
from rich.console import Console
from rich.table import Table

from auth import AuthManager
from models import CloudProvider
from cli_constants import PROVIDER_CHOICES
from utils.config import load_config
from utils.cloud_identity import display_cloud_identity_panel, display_multi_cloud_identity_table
from .auth_helpers import (
    get_or_create_provider,
    format_status_details,
    validate_provider,
)

console = Console()


@click.command("auth-status")
@click.option(
    "--provider",
    type=click.Choice(PROVIDER_CHOICES, case_sensitive=False),
    help="Check status for specific provider",
)
@click.option(
    "--validate",
    is_flag=True,
    help="Validate credentials by making API calls",
)
def auth_status(provider: Optional[str], validate: bool) -> None:
    """Check authentication status for cloud providers.
    
    Shows which providers are configured and optionally validates
    that the credentials are still valid.
    """
    asyncio.run(_auth_status_async(provider, validate))


async def _auth_status_async(provider: Optional[str], validate: bool) -> None:
    """Async implementation of auth status command."""
    auth_manager = AuthManager()
    config = load_config()
    
    # Display cloud identity information first
    console.print("\n[bold cyan]Cloud Instance Information[/bold cyan]\n")
    if provider:
        # Check specific provider
        provider_enum = CloudProvider(provider)
        if config and provider_enum.value in config:
            display_cloud_identity_panel(provider_enum, config, console)
        await check_provider_status(auth_manager, provider_enum, validate)
    else:
        # Display identity info for all configured providers
        if config:
            display_multi_cloud_identity_table(config, console)
        
        # Check all providers
        console.print("\n[bold]Cloud Provider Authentication Status[/bold]\n")
        
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Provider", style="cyan", width=12)
        table.add_column("Status", width=15)
        table.add_column("Details", style="dim")
        if validate:
            table.add_column("Validation", width=12)
        
        for provider_enum in CloudProvider:
            status, details, validation = await get_provider_status(
                auth_manager, provider_enum, validate
            )
            
            row = [provider_enum.value.upper(), status, details]
            if validate:
                row.append(validation)
            table.add_row(*row)
        
        console.print(table)


async def check_provider_status(
    auth_manager: AuthManager,
    provider: CloudProvider,
    validate: bool
) -> None:
    """Check status for a specific provider."""
    status, details, validation = await get_provider_status(
        auth_manager, provider, validate
    )
    
    console.print(f"\n[bold]{provider.value.upper()} Status[/bold]")
    console.print(f"Status: {status}")
    console.print(f"Details: {details}")
    
    if validate:
        console.print(f"Validation: {validation}")


async def get_provider_status(
    auth_manager: AuthManager,
    provider: CloudProvider,
    validate: bool
) -> tuple[str, str, str]:
    """Get status information for a provider.
    
    Returns:
        Tuple of (status, details, validation)
    """
    try:
        creds = await auth_manager.load_credentials(provider)
        
        if not creds:
            return "[yellow]Not configured[/yellow]", "No credentials found", ""
        
        # Format status and details
        status, details = format_status_details(creds)
        
        # Validate if requested
        validation = ""
        if validate:
            auth_provider = get_or_create_provider(provider, auth_manager, creds)
            validation = await validate_provider(auth_provider, creds)
        
        return status, details, validation
        
    except Exception as e:
        return "[red]Error[/red]", str(e), ""