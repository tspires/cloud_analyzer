"""Utilities for displaying cloud identity information."""

from typing import Dict, Optional, Tuple
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from models import CloudProvider


def get_cloud_identity_info(provider: CloudProvider, config: Dict) -> Dict[str, str]:
    """Extract cloud identity information from configuration.
    
    Args:
        provider: Cloud provider
        config: Configuration dictionary
        
    Returns:
        Dictionary with identity information
    """
    provider_config = config.get(provider.value, {})
    info = {}
    
    if provider == CloudProvider.AZURE:
        info["Tenant ID"] = provider_config.get("tenant_id", "Not configured")
        info["Subscription ID"] = provider_config.get("subscription_id", "Not configured")
        info["Environment"] = provider_config.get("cloud_environment", "Public")
        
    elif provider == CloudProvider.AWS:
        info["Account ID"] = provider_config.get("account_id", "Not configured")
        info["Region"] = provider_config.get("region", "Not configured")
        # Check for role/profile info
        if provider_config.get("profile"):
            info["Profile"] = provider_config["profile"]
        if provider_config.get("role_arn"):
            info["Role ARN"] = provider_config["role_arn"]
            
    elif provider == CloudProvider.GCP:
        info["Project ID"] = provider_config.get("project_id", "Not configured")
        info["Region"] = provider_config.get("region", "Not configured")
        if provider_config.get("service_account_email"):
            info["Service Account"] = provider_config["service_account_email"]
    
    return info


def display_cloud_identity_panel(provider: CloudProvider, config: Dict, console: Console) -> None:
    """Display cloud identity information in a formatted panel.
    
    Args:
        provider: Cloud provider
        config: Configuration dictionary
        console: Rich console instance
    """
    identity_info = get_cloud_identity_info(provider, config)
    
    # Create content for panel
    content_lines = []
    for key, value in identity_info.items():
        if value != "Not configured":
            content_lines.append(f"[bold cyan]{key}:[/bold cyan] {value}")
        else:
            content_lines.append(f"[bold cyan]{key}:[/bold cyan] [yellow]{value}[/yellow]")
    
    content = "\n".join(content_lines)
    
    # Create panel with provider-specific color
    color_map = {
        CloudProvider.AWS: "yellow",
        CloudProvider.AZURE: "blue",
        CloudProvider.GCP: "red"
    }
    
    panel = Panel(
        content,
        title=f"[bold]{provider.value.upper()} Cloud Instance[/bold]",
        border_style=color_map.get(provider, "white"),
        padding=(1, 2)
    )
    
    console.print(panel)


def display_multi_cloud_identity_table(config: Dict, console: Console) -> None:
    """Display identity information for all configured providers in a table.
    
    Args:
        config: Configuration dictionary
        console: Rich console instance
    """
    table = Table(
        title="Cloud Provider Identity Information",
        show_header=True,
        header_style="bold magenta"
    )
    
    table.add_column("Provider", style="cyan", width=10)
    table.add_column("Primary ID", style="white")
    table.add_column("Secondary ID", style="white")
    table.add_column("Environment/Region", style="dim")
    
    for provider in CloudProvider:
        if provider.value in config:
            info = get_cloud_identity_info(provider, config)
            
            if provider == CloudProvider.AZURE:
                primary = info.get("Tenant ID", "N/A")
                secondary = info.get("Subscription ID", "N/A")
                env = info.get("Environment", "N/A")
            elif provider == CloudProvider.AWS:
                primary = info.get("Account ID", "N/A")
                secondary = info.get("Profile", info.get("Role ARN", "Default"))
                env = info.get("Region", "N/A")
            elif provider == CloudProvider.GCP:
                primary = info.get("Project ID", "N/A")
                secondary = info.get("Service Account", "Default")
                env = info.get("Region", "N/A")
            else:
                continue
                
            table.add_row(
                provider.value.upper(),
                primary if primary != "Not configured" else "[yellow]Not configured[/yellow]",
                secondary if secondary != "Not configured" else "[yellow]Not configured[/yellow]",
                env if env != "Not configured" else "[yellow]Not configured[/yellow]"
            )
    
    console.print(table)


def format_identity_line(provider: CloudProvider, config: Dict) -> str:
    """Format a single line summary of cloud identity.
    
    Args:
        provider: Cloud provider
        config: Configuration dictionary
        
    Returns:
        Formatted identity string
    """
    info = get_cloud_identity_info(provider, config)
    
    if provider == CloudProvider.AZURE:
        tenant = info.get("Tenant ID", "Unknown")
        subscription = info.get("Subscription ID", "Unknown")
        return f"Azure Tenant: {tenant} | Subscription: {subscription}"
        
    elif provider == CloudProvider.AWS:
        account = info.get("Account ID", "Unknown")
        region = info.get("Region", "Unknown")
        return f"AWS Account: {account} | Region: {region}"
        
    elif provider == CloudProvider.GCP:
        project = info.get("Project ID", "Unknown")
        return f"GCP Project: {project}"
    
    return f"{provider.value.upper()}: Unknown"