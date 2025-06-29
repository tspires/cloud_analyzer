"""Configure command for setting up cloud provider credentials."""

import asyncio
import json
import subprocess
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import click
from rich.console import Console
from rich.prompt import Confirm, Prompt
from rich.table import Table

from auth import AuthManager
from models import CloudProvider
from utils.config import load_config, save_config
from utils.cloud_identity import (
    display_cloud_identity_panel,
    display_multi_cloud_identity_table,
)

# Constants
AUTH_METHOD_BROWSER = "browser"
AUTH_METHOD_PROFILE = "profile"
AUTH_METHOD_CREDENTIALS = "credentials"
AUTH_METHOD_CLI = "cli"
AUTH_METHOD_SERVICE_PRINCIPAL = "service_principal"
AUTH_METHOD_SERVICE_ACCOUNT = "service_account"

AZURE_AUTH_METHODS = [AUTH_METHOD_CLI, AUTH_METHOD_BROWSER, AUTH_METHOD_SERVICE_PRINCIPAL]


console = Console()


class ProviderConfigurator:
    """Base class for provider configuration."""
    
    def __init__(self, auth_manager: AuthManager):
        self.auth_manager = auth_manager
        self.console = console



class AzureSubscriptionSelector:
    """Handles Azure subscription selection logic."""
    
    def __init__(self, console: Console):
        self.console = console
    
    def select_subscriptions(
        self, 
        subscriptions: List[Dict]
    ) -> Tuple[List[Dict], Dict[str, str]]:
        """Select subscriptions from a list."""
        enabled_subs = [s for s in subscriptions if s.get('state') == 'Enabled']
        
        if not enabled_subs:
            return [], {}
        
        self._display_subscriptions(enabled_subs)
        
        if len(enabled_subs) == 1:
            return enabled_subs, {enabled_subs[0]['id']: enabled_subs[0]['name']}
        
        selected_subs = self._prompt_for_selection(enabled_subs)
        subscription_names = {sub['id']: sub['name'] for sub in selected_subs}
        
        return selected_subs, subscription_names
    
    def _display_subscriptions(self, subscriptions: List[Dict]) -> None:
        """Display available subscriptions."""
        self.console.print("\n[bold]Available Azure Subscriptions:[/bold]")
        for i, sub in enumerate(subscriptions, 1):
            self.console.print(f"  {i}. {sub['name']} ({sub['id']})")
    
    def _prompt_for_selection(self, subscriptions: List[Dict]) -> List[Dict]:
        """Prompt user to select subscriptions."""
        selection = Prompt.ask(
            "\nSelect subscriptions to analyze (comma-separated numbers, or 'all')",
            default="all"
        )
        
        if selection.lower() == 'all':
            return subscriptions
        
        try:
            indices = [int(i.strip()) - 1 for i in selection.split(',')]
            selected = [subscriptions[i] for i in indices if 0 <= i < len(subscriptions)]
            
            if not selected:
                self.console.print("[yellow]Invalid selection, using all subscriptions[/yellow]")
                return subscriptions
            
            return selected
        except ValueError:
            self.console.print("[yellow]Invalid selection format, using all subscriptions[/yellow]")
            return subscriptions


class AzureConfigurator(ProviderConfigurator):
    """Handles Azure-specific configuration."""
    
    def __init__(self, auth_manager: AuthManager):
        super().__init__(auth_manager)
        self.subscription_selector = AzureSubscriptionSelector(self.console)
    
    async def configure(self, auth_type: Optional[str] = None) -> None:
        """Configure Azure credentials."""
        self._display_auth_options()
        
        if not auth_type:
            auth_type = self._get_auth_type()
        
        try:
            if auth_type == AUTH_METHOD_CLI:
                await self._configure_cli_auth()
            elif auth_type == AUTH_METHOD_BROWSER:
                await self._configure_browser_auth()
            else:  # service_principal
                await self._configure_service_principal()
        except Exception as e:
            self.console.print(f"[red]Authentication failed:[/red] {e}")
            raise click.Abort()
    
    def _display_auth_options(self) -> None:
        """Display Azure authentication options."""
        self.console.print("Azure authentication options:")
        self.console.print("  1. Azure CLI - Use existing Azure CLI credentials (Recommended)")
        self.console.print("  2. Browser - Interactive login")
        self.console.print("  3. Service Principal - For automation")
        self.console.print()
    
    def _get_auth_type(self) -> str:
        """Get authentication type from user."""
        auth_choice = Prompt.ask(
            "Select authentication method",
            choices=["1", "2", "3"],
            default="1"
        )
        return AZURE_AUTH_METHODS[int(auth_choice) - 1]
    
    async def _configure_cli_auth(self) -> None:
        """Configure Azure CLI authentication."""
        self.console.print("\n[yellow]Using Azure CLI credentials...[/yellow]")
        self.console.print("Make sure you are logged in with 'az login'\n")
        
        subscriptions = self._get_cli_subscriptions()
        if subscriptions:
            self._save_subscription_config(subscriptions)
            return
        
        # Fall back to single subscription
        await self._configure_single_subscription()
    
    def _get_cli_subscriptions(self) -> Optional[List[Dict]]:
        """Get subscriptions using Azure CLI."""
        try:
            result = subprocess.run(
                ['az', 'account', 'list', '--output', 'json'],
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                return json.loads(result.stdout)
        except Exception as e:
            self.console.print(f"[yellow]Could not list subscriptions: {e}[/yellow]")
        
        return None
    
    def _save_subscription_config(self, subscriptions: List[Dict]) -> None:
        """Save subscription configuration."""
        selected_subs, subscription_names = self.subscription_selector.select_subscriptions(
            subscriptions
        )
        
        if not selected_subs:
            return
        
        config = load_config() or {}
        config['azure'] = {
            'auth_type': 'cli',
            'subscription_ids': [sub['id'] for sub in selected_subs],
            'subscription_names': subscription_names
        }
        save_config(config)
        
        self.console.print(f"\n[green]Configured {len(selected_subs)} subscription(s)[/green]")
    
    async def _configure_single_subscription(self) -> None:
        """Configure single subscription."""
        subscription_id = Prompt.ask(
            "Azure Subscription ID (optional, will auto-detect)", 
            default=""
        )
        
        await self.auth_manager.authenticate(
            CloudProvider.AZURE,
            auth_type="cli",
            subscription_id=subscription_id if subscription_id else None
        )
    
    async def _configure_browser_auth(self) -> None:
        """Configure browser-based authentication."""
        self.console.print("\n[yellow]Opening browser for authentication...[/yellow]")
        self.console.print("Please complete the authentication in your browser.\n")
        
        creds = await self.auth_manager.authenticate(
            CloudProvider.AZURE,
            auth_type="browser",
            tenant_id="common"
        )
        
        # Try to get subscriptions from the provider
        provider = self.auth_manager.get_provider(CloudProvider.AZURE)
        if provider and hasattr(provider, '_subscriptions') and provider._subscriptions:
            self._save_subscription_config(provider._subscriptions)
    
    async def _configure_service_principal(self) -> None:
        """Configure service principal authentication."""
        subscription_id = Prompt.ask("Azure Subscription ID")
        tenant_id = Prompt.ask("Azure Tenant ID")
        client_id = Prompt.ask("Azure Client ID (App ID)")
        client_secret = Prompt.ask("Azure Client Secret", password=True)
        
        await self.auth_manager.authenticate(
            CloudProvider.AZURE,
            auth_type="service_principal",
            subscription_id=subscription_id,
            tenant_id=tenant_id,
            client_id=client_id,
            client_secret=client_secret
        )




class ConfigurationDisplay:
    """Handles display of configuration information."""
    
    def __init__(self, console: Console):
        self.console = console
    
    async def show_configuration(self, auth_manager: AuthManager) -> None:
        """Display current configuration."""
        providers = auth_manager.list_providers()
        config = load_config()
        
        if not any(status == "configured" for status in providers.values()):
            self.console.print("[yellow]No providers configured[/yellow]")
            return
        
        self._display_cloud_identity(config)
        await self._display_provider_details(auth_manager, providers)
    
    def _display_cloud_identity(self, config: Dict) -> None:
        """Display cloud identity information."""
        self.console.print("\n[bold cyan]Cloud Instance Information[/bold cyan]\n")
        if config:
            display_multi_cloud_identity_table(config, self.console)
    
    async def _display_provider_details(
        self, 
        auth_manager: AuthManager, 
        providers: Dict
    ) -> None:
        """Display detailed provider configuration."""
        self.console.print("\n[bold]Provider Configuration Details[/bold]\n")
        
        table = Table(title="Authentication Status")
        table.add_column("Provider", style="cyan")
        table.add_column("Status", style="white")
        table.add_column("Auth Method", style="dim")
        
        for provider, status in providers.items():
            details = await self._get_provider_details(auth_manager, provider, status)
            status_display = self._format_status(status)
            table.add_row(provider.value.upper(), status_display, details)
        
        self.console.print(table)
    
    async def _get_provider_details(
        self, 
        auth_manager: AuthManager, 
        provider: CloudProvider, 
        status: str
    ) -> str:
        """Get detailed information for a provider."""
        if status != "configured":
            return ""
        
        try:
            creds = await auth_manager.load_credentials(provider)
            if not creds:
                return ""
            
            details = self._get_auth_method_details(provider, creds)
            expiry_info = self._get_expiry_info(creds)
            
            return f"{details}{expiry_info}" if expiry_info else details
        except Exception:
            return ""
    
    def _get_auth_method_details(self, provider: CloudProvider, creds) -> str:
        """Get authentication method details."""
        if provider == CloudProvider.AZURE:
            if creds.client_id:
                return "Service Principal"
            else:
                return "Browser/CLI Auth"
        return ""
    
    def _get_expiry_info(self, creds) -> str:
        """Get credential expiry information."""
        if creds.expires_in_minutes is None:
            return ""
        
        if creds.expires_in_minutes < 60:
            return f" ([yellow]expires in {creds.expires_in_minutes}m[/yellow])"
        else:
            hours = creds.expires_in_minutes // 60
            return f" (expires in {hours}h)"
    
    def _format_status(self, status: str) -> str:
        """Format status for display."""
        if status == "configured":
            return "[green]Configured[/green]"
        return "[dim]Not configured[/dim]"


class ConfigureCommand:
    """Main configure command handler."""
    
    def __init__(self):
        self.auth_manager = AuthManager()
        self.display = ConfigurationDisplay(console)
        self.configurators = {
            CloudProvider.AZURE: AzureConfigurator(self.auth_manager),
        }
    
    async def execute(
        self,
        provider: Optional[str],
        show: bool,
        clear: bool,
        auth_type: Optional[str]
    ) -> None:
        """Execute the configure command."""
        if show:
            await self.display.show_configuration(self.auth_manager)
            return
        
        if clear:
            await self._clear_configuration(provider)
            return
        
        provider = self._get_provider(provider)
        await self._configure_provider(provider, auth_type)
    
    async def _clear_configuration(self, provider: Optional[str]) -> None:
        """Clear configuration for a provider."""
        if not provider:
            console.print("[red]Error:[/red] --provider is required with --clear")
            return
        
        provider_enum = CloudProvider(provider)
        if Confirm.ask(f"Clear configuration for {provider.upper()}?"):
            await self.auth_manager.remove_credentials(provider_enum)
            console.print(f"[green]Configuration cleared for {provider.upper()}[/green]")
    
    def _get_provider(self, provider: Optional[str]) -> str:
        """Get provider name, prompting if necessary."""
        if not provider:
            return Prompt.ask(
                "Which provider would you like to configure?",
                choices=["aws", "azure", "gcp"],
            )
        return provider
    
    async def _configure_provider(self, provider: str, auth_type: Optional[str]) -> None:
        """Configure a specific provider."""
        console.print(f"\n[bold]Configuring {provider.upper()}[/bold]\n")
        
        provider_enum = CloudProvider(provider)
        configurator = self.configurators.get(provider_enum)
        
        if configurator:
            await configurator.configure(auth_type)
            console.print(f"\n[green]✓ Configuration saved for {provider.upper()}[/green]")


@click.command()
@click.option(
    "--provider",
    type=click.Choice(["azure"], case_sensitive=False),
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
def configure(
    provider: Optional[str],
    show: bool,
    clear: bool,
    auth_type: Optional[str]
) -> None:
    """Configure cloud provider credentials.
    
    This command sets up authentication credentials for Azure.
    Credentials are stored securely in your home directory.
    
    Browser authentication is supported for interactive login.
    """
    command = ConfigureCommand()
    asyncio.run(command.execute(provider, show, clear, auth_type))