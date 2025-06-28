"""Configure command for setting up cloud provider credentials."""

import asyncio
from pathlib import Path
from typing import Dict, Optional

import click
from rich.console import Console
from rich.prompt import Confirm, Prompt
from rich.table import Table

from auth import AuthManager
from models import CloudProvider
from utils.config import load_config, save_config
from utils.cloud_identity import display_cloud_identity_panel, display_multi_cloud_identity_table

console = Console()


@click.command()
@click.option(
    "--provider",
    type=click.Choice(["aws", "azure", "gcp"], case_sensitive=False),
    help="Cloud provider to configure",
)
@click.option(
    "--show",
    is_flag=True,
    help="Show current configuration",
)
@click.option(
    "--clear",
    is_flag=True,
    help="Clear configuration for a provider",
)
@click.option(
    "--auth-type",
    type=click.Choice(["browser", "credentials", "profile", "cli"], case_sensitive=False),
    help="Authentication type to use",
)
def configure(provider: Optional[str], show: bool, clear: bool, auth_type: Optional[str]) -> None:
    """Configure cloud provider credentials.
    
    This command sets up authentication credentials for AWS, Azure, or GCP.
    Credentials are stored securely in your home directory.
    
    Browser authentication is supported for interactive login.
    """
    # Handle async operations
    asyncio.run(_configure_async(provider, show, clear, auth_type))


async def _configure_async(provider: Optional[str], show: bool, clear: bool, auth_type: Optional[str]) -> None:
    """Async implementation of configure command."""
    auth_manager = AuthManager()
    
    if show:
        await show_configuration(auth_manager)
        return
    
    if clear:
        if not provider:
            console.print("[red]Error:[/red] --provider is required with --clear")
            return
        
        provider_enum = CloudProvider(provider)
        if Confirm.ask(f"Clear configuration for {provider.upper()}?"):
            await auth_manager.remove_credentials(provider_enum)
            console.print(f"[green]Configuration cleared for {provider.upper()}[/green]")
        return
    
    if not provider:
        # Interactive mode - ask which provider to configure
        provider = Prompt.ask(
            "Which provider would you like to configure?",
            choices=["aws", "azure", "gcp"],
        )
    
    console.print(f"\n[bold]Configuring {provider.upper()}[/bold]\n")
    
    provider_enum = CloudProvider(provider)
    
    if provider == "aws":
        await configure_aws(auth_manager, auth_type)
    elif provider == "azure":
        await configure_azure(auth_manager, auth_type)
    elif provider == "gcp":
        await configure_gcp(auth_manager, auth_type)
    
    console.print(f"\n[green]✓ Configuration saved for {provider.upper()}[/green]")


async def configure_aws(auth_manager: AuthManager, auth_type: Optional[str] = None) -> None:
    """Configure AWS credentials."""
    console.print("AWS authentication options:")
    console.print("  1. Browser (SSO) - Recommended for interactive use")
    console.print("  2. Profile - Use existing AWS CLI profile")
    console.print("  3. Credentials - Direct access key configuration")
    console.print()
    
    if not auth_type:
        auth_choice = Prompt.ask(
            "Select authentication method",
            choices=["1", "2", "3"],
            default="1"
        )
        auth_type = ["browser", "profile", "credentials"][int(auth_choice) - 1]
    
    try:
        if auth_type == "browser":
            start_url = Prompt.ask("AWS SSO Start URL")
            region = Prompt.ask("AWS Region", default="us-east-1")
            
            console.print("\n[yellow]Opening browser for authentication...[/yellow]")
            console.print("Please complete the authentication in your browser.\n")
            
            await auth_manager.authenticate(
                CloudProvider.AWS,
                auth_type="sso",
                start_url=start_url,
                region=region
            )
            
        elif auth_type == "profile":
            profile = Prompt.ask("AWS Profile name", default="default")
            region = Prompt.ask("AWS Region", default="us-east-1")
            
            await auth_manager.authenticate(
                CloudProvider.AWS,
                auth_type="profile",
                profile=profile,
                region=region
            )
            
        else:  # credentials
            access_key_id = Prompt.ask("AWS Access Key ID")
            secret_access_key = Prompt.ask("AWS Secret Access Key", password=True)
            region = Prompt.ask("Default region", default="us-east-1")
            
            # For direct credentials, we'll need to implement a direct auth provider
            # For now, save to config file
            config = load_config() or {}
            config["aws"] = {
                "access_key_id": access_key_id,
                "secret_access_key": secret_access_key,
                "region": region
            }
            save_config(config)
            
    except Exception as e:
        console.print(f"[red]Authentication failed:[/red] {e}")
        raise click.Abort()


async def configure_azure(auth_manager: AuthManager, auth_type: Optional[str] = None) -> None:
    """Configure Azure credentials."""
    console.print("Azure authentication options:")
    console.print("  1. Azure CLI - Use existing Azure CLI credentials (Recommended)")
    console.print("  2. Browser - Interactive login")
    console.print("  3. Service Principal - For automation")
    console.print()
    
    if not auth_type:
        auth_choice = Prompt.ask(
            "Select authentication method",
            choices=["1", "2", "3"],
            default="1"
        )
        auth_type = ["cli", "browser", "service_principal"][int(auth_choice) - 1]
    
    try:
        if auth_type == "cli":
            console.print("\n[yellow]Using Azure CLI credentials...[/yellow]")
            console.print("Make sure you are logged in with 'az login'\n")
            
            # Optionally ask for subscription ID
            subscription_id = Prompt.ask(
                "Azure Subscription ID (optional, will auto-detect)", 
                default=""
            )
            
            await auth_manager.authenticate(
                CloudProvider.AZURE,
                auth_type="cli",
                subscription_id=subscription_id if subscription_id else None
            )
            
        elif auth_type == "browser":
            console.print("\n[yellow]Opening browser for authentication...[/yellow]")
            console.print("Please complete the authentication in your browser.\n")
            
            await auth_manager.authenticate(
                CloudProvider.AZURE,
                auth_type="browser",
                tenant_id="common"
            )
            
        else:  # service_principal
            subscription_id = Prompt.ask("Azure Subscription ID")
            tenant_id = Prompt.ask("Azure Tenant ID")
            client_id = Prompt.ask("Azure Client ID (App ID)")
            client_secret = Prompt.ask("Azure Client Secret", password=True)
            
            await auth_manager.authenticate(
                CloudProvider.AZURE,
                auth_type="service_principal",
                subscription_id=subscription_id,
                tenant_id=tenant_id,
                client_id=client_id,
                client_secret=client_secret
            )
            
    except Exception as e:
        console.print(f"[red]Authentication failed:[/red] {e}")
        raise click.Abort()


async def configure_gcp(auth_manager: AuthManager, auth_type: Optional[str] = None) -> None:
    """Configure GCP credentials."""
    console.print("GCP authentication options:")
    console.print("  1. Browser - Interactive OAuth login (Recommended)")
    console.print("  2. Service Account - Using key file")
    console.print()
    
    if not auth_type:
        auth_choice = Prompt.ask(
            "Select authentication method",
            choices=["1", "2"],
            default="1"
        )
        auth_type = ["browser", "service_account"][int(auth_choice) - 1]
    
    try:
        if auth_type == "browser":
            project_id = Prompt.ask("GCP Project ID (optional, will auto-detect)", default="")
            
            console.print("\n[yellow]Opening browser for authentication...[/yellow]")
            console.print("Please complete the authentication in your browser.\n")
            
            await auth_manager.authenticate(
                CloudProvider.GCP,
                auth_type="browser",
                project_id=project_id if project_id else None
            )
            
        else:  # service_account
            project_id = Prompt.ask("GCP Project ID")
            key_file_path = Prompt.ask(
                "Service Account key file path",
                default="~/.config/gcloud/service-account.json",
            )
            
            # Expand the path
            key_file_path = str(Path(key_file_path).expanduser())
            
            # Verify file exists
            if not Path(key_file_path).exists():
                console.print(
                    f"[yellow]Warning: File not found at {key_file_path}[/yellow]"
                )
                if not Confirm.ask("Continue anyway?"):
                    raise click.Abort()
            
            await auth_manager.authenticate(
                CloudProvider.GCP,
                auth_type="service_account",
                key_file_path=key_file_path,
                project_id=project_id
            )
            
    except Exception as e:
        console.print(f"[red]Authentication failed:[/red] {e}")
        raise click.Abort()


async def show_configuration(auth_manager: AuthManager) -> None:
    """Display current configuration."""
    providers = auth_manager.list_providers()
    config = load_config()
    
    if not any(status == "configured" for status in providers.values()):
        console.print("[yellow]No providers configured[/yellow]")
        return
    
    # Display cloud identity information
    console.print("\n[bold cyan]Cloud Instance Information[/bold cyan]\n")
    if config:
        display_multi_cloud_identity_table(config, console)
    
    console.print("\n[bold]Provider Configuration Details[/bold]\n")
    
    table = Table(title="Authentication Status")
    table.add_column("Provider", style="cyan")
    table.add_column("Status", style="white")
    table.add_column("Auth Method", style="dim")
    
    for provider, status in providers.items():
        details = ""
        if status == "configured":
            # Try to load credentials to get more info
            try:
                creds = await auth_manager.load_credentials(provider)
                if creds:
                    # Show authentication method
                    if provider == CloudProvider.AWS:
                        if creds.profile:
                            details = f"Profile: {creds.profile}"
                        elif creds.metadata.get("sso_session"):
                            details = "SSO Authentication"
                        else:
                            details = "Access Keys"
                    elif provider == CloudProvider.AZURE:
                        if creds.client_id:
                            details = "Service Principal"
                        else:
                            details = "Browser/CLI Auth"
                    elif provider == CloudProvider.GCP:
                        if creds.service_account_key:
                            details = "Service Account"
                        else:
                            details = "Browser Auth"
                    
                    if creds.expires_in_minutes is not None:
                        if creds.expires_in_minutes < 60:
                            details += f" ([yellow]expires in {creds.expires_in_minutes}m[/yellow])"
                        else:
                            hours = creds.expires_in_minutes // 60
                            details += f" (expires in {hours}h)"
            except Exception:
                pass
        
        status_display = "[green]Configured[/green]" if status == "configured" else "[dim]Not configured[/dim]"
        table.add_row(provider.value.upper(), status_display, details)
    
    console.print(table)