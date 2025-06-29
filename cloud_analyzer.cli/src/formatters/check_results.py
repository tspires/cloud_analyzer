"""Formatters for check results."""

from typing import List, Optional, Dict
import sys
from pathlib import Path

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text

from models import CloudProvider

# Add parent directory to path to import from cloud_analyzer.common
sys.path.append(str(Path(__file__).parent.parent.parent.parent / 'cloud_analyzer.common' / 'src'))

from models.checks import CheckResult

# Define severity styles
SEVERITY_STYLES = {
    "critical": "bold red",
    "high": "red",
    "medium": "yellow",
    "low": "blue",
    "info": "dim",
}


def format_check_results(results: List[CheckResult], console: Console, config: Optional[Dict] = None, provider: Optional[CloudProvider] = None) -> None:
    """Format and display check results as a table.
    
    Args:
        results: List of check results to display
        console: Rich console instance
        config: Optional configuration dictionary for showing tenant/subscription info
        provider: Optional provider to show identity info for
    """
    if not results:
        console.print("[yellow]No optimization opportunities found.[/yellow]")
        return
    
    # Group results by severity
    results_by_severity = {}
    for result in results:
        if result.severity not in results_by_severity:
            results_by_severity[result.severity] = []
        results_by_severity[result.severity].append(result)
    
    # Display results by severity
    severity_order = ["critical", "high", "medium", "low", "info"]
    
    for severity in severity_order:
        if severity not in results_by_severity:
            continue
        
        severity_results = results_by_severity[severity]
        
        # Create table for this severity level
        table = Table(
            title=f"{severity.upper()} Priority Findings ({len(severity_results)})",
            title_style=get_severity_style(severity),
        )
        
        table.add_column("Resource", style="cyan", no_wrap=True)
        table.add_column("Type", style="magenta")
        table.add_column("Finding", style="white")
        table.add_column("Monthly Savings", justify="right", style="green")
        table.add_column("Annual Savings", justify="right", style="green")
        table.add_column("Effort", style="yellow")
        
        # Sort by savings potential
        severity_results.sort(key=lambda x: x.monthly_savings, reverse=True)
        
        for result in severity_results:
            table.add_row(
                result.resource.name,
                result.resource.type.value if hasattr(result.resource.type, 'value') else str(result.resource.type),
                result.title,
                f"${result.monthly_savings:,.2f}",
                f"${result.annual_savings:,.2f}",
                result.effort_level.value if hasattr(result.effort_level, 'value') else str(result.effort_level),
            )
        
        console.print(table)
        console.print()


def format_detailed_result(result: CheckResult, console: Console, config: Optional[Dict] = None) -> None:
    """Format a single check result with full details.
    
    Args:
        result: Check result to display
        console: Rich console instance
        config: Optional configuration dictionary for showing tenant/subscription info
    """
    # Create severity indicator
    severity_color = get_severity_style(result.severity).split()[0]
    severity_text = Text(
        f" {result.severity.upper()} ",
        style=f"bold white on {severity_color}",
    )
    
    # Get tenant/subscription info if config is provided
    identity_info = ""
    if config and hasattr(result.resource, 'provider'):
        from commands.analyze_helpers import get_provider_identity_info
        provider = result.resource.provider
        tenant_id, subscription_ids = get_provider_identity_info(provider, config)
        
        if provider == CloudProvider.AZURE:
            identity_info = f"\n[bold]Tenant ID:[/bold] {tenant_id}"
            if subscription_ids:
                identity_info += f"\n[bold]Subscription ID:[/bold] {subscription_ids[0]}"
    
    # Create main panel
    panel_content = f"""
[bold]Resource:[/bold] {result.resource.name} ({result.resource.type.value if hasattr(result.resource.type, 'value') else result.resource.type})
[bold]Provider:[/bold] {result.resource.provider.value.upper() if hasattr(result.resource.provider, 'value') else result.resource.provider.upper()}{identity_info}
[bold]Region:[/bold] {result.resource.region}

[bold]Finding:[/bold]
{result.description}

[bold]Impact:[/bold]
{result.impact}

[bold]Cost Analysis:[/bold]
  • Current Cost: ${result.current_cost:,.2f}/month
  • Optimized Cost: ${result.optimized_cost:,.2f}/month
  • Monthly Savings: [green]${result.monthly_savings:,.2f}[/green]
  • Annual Savings: [green]${result.annual_savings:,.2f}[/green]
  • Savings: [green]{result.savings_percentage:.1f}%[/green]

[bold]Implementation:[/bold]
  • Effort: {result.effort_level}
  • Risk: {result.risk_level}
  • Confidence: {result.confidence_score:.0%}
"""
    
    # Add implementation steps
    if result.implementation_steps:
        panel_content += "\n[bold]Steps:[/bold]\n"
        for step in result.implementation_steps:
            panel_content += f"  {step}\n"
    
    panel = Panel(
        panel_content.strip(),
        title=f"{severity_text} {result.title}",
        border_style=get_severity_style(result.severity),
    )
    
    console.print(panel)


def get_severity_style(severity: str) -> str:
    """Get color style for severity level."""
    return SEVERITY_STYLES.get(severity, "white")