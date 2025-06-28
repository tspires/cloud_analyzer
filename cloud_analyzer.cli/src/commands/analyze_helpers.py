"""Helper functions for the analyze command."""

from pathlib import Path
from typing import List, Optional, Dict, Any, Set, Tuple
import json
import csv

from rich.console import Console

from models import CheckResult, CheckSeverity, CloudProvider
from constants import SEVERITY_ORDER
from cli_constants import ERROR_NO_CONFIG, ERROR_NO_PROVIDER_CONFIG

console = Console()


def validate_configuration(config: Optional[Dict], provider: str) -> bool:
    """Validate that configuration exists for the specified provider.
    
    Args:
        config: Configuration dictionary
        provider: Provider name or 'all'
        
    Returns:
        True if configuration is valid
    """
    if not config:
        console.print(f"[red]Error:[/red] {ERROR_NO_CONFIG}")
        return False
    
    if provider != "all" and provider not in config:
        console.print(f"[red]Error:[/red] {ERROR_NO_PROVIDER_CONFIG.format(provider)}")
        return False
    
    return True


def determine_providers(provider: str, config: Dict) -> List[CloudProvider]:
    """Determine which providers to analyze based on input and config.
    
    Args:
        provider: Provider name or 'all'
        config: Configuration dictionary
        
    Returns:
        List of CloudProvider enums to analyze
    """
    if provider == "all":
        return [p for p in CloudProvider if p.value in config]
    else:
        return [CloudProvider(provider)]


def filter_results_by_severity(
    results: List[CheckResult], 
    severity: str
) -> List[CheckResult]:
    """Filter check results by minimum severity level.
    
    Args:
        results: List of check results
        severity: Minimum severity level or 'all'
        
    Returns:
        Filtered list of results
    """
    if severity == "all":
        return results
    
    min_severity = CheckSeverity(severity)
    min_index = SEVERITY_ORDER.index(min_severity.value)
    
    return [
        r for r in results
        if SEVERITY_ORDER.index(r.severity.value if hasattr(r.severity, 'value') else r.severity) >= min_index
    ]


def save_results_json(results: List[CheckResult], output_file: Path) -> None:
    """Save results to JSON file.
    
    Args:
        results: List of check results
        output_file: Path to output file
        
    Raises:
        IOError: If file cannot be written
    """
    try:
        output_data = [r.dict() for r in results]
        output_file.parent.mkdir(parents=True, exist_ok=True)
        with open(output_file, "w") as f:
            json.dump(output_data, f, indent=2, default=str)
        console.print(f"\n[green]Results saved to {output_file}[/green]")
    except IOError as e:
        console.print(f"[red]Error:[/red] Failed to save results to {output_file}: {e}")
        raise


def save_results_csv(results: List[CheckResult], output_file: Path) -> None:
    """Save results to CSV file.
    
    Args:
        results: List of check results
        output_file: Path to output file
        
    Raises:
        IOError: If file cannot be written
    """
    if not results:
        console.print("[yellow]No results to save[/yellow]")
        return
    
    try:
        output_file.parent.mkdir(parents=True, exist_ok=True)
        with open(output_file, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=results[0].dict().keys())
            writer.writeheader()
            for r in results:
                writer.writerow(r.dict())
        console.print(f"\n[green]Results saved to {output_file}[/green]")
    except IOError as e:
        console.print(f"[red]Error:[/red] Failed to save results to {output_file}: {e}")
        raise


def display_summary(results: List[CheckResult]) -> None:
    """Display summary statistics for analysis results.
    
    Args:
        results: List of check results
    """
    if not results:
        return
    
    console.print(f"\n[bold]Summary:[/bold]")
    console.print(f"Total findings: {len(results)}")
    
    # Calculate total savings
    total_monthly = sum(r.monthly_savings for r in results)
    total_annual = sum(r.annual_savings for r in results)
    
    console.print(
        f"Potential monthly savings: [green]${total_monthly:,.2f}[/green]"
    )
    console.print(
        f"Potential annual savings: [green]${total_annual:,.2f}[/green]"
    )


def display_dry_run_info(
    providers: List[CloudProvider],
    region: Optional[str],
    check_types: Optional[List[str]]
) -> None:
    """Display what would be analyzed in a dry run.
    
    Args:
        providers: List of providers to analyze
        region: Optional region filter
        check_types: Optional list of check types
    """
    console.print("\n[bold]Dry Run - Would analyze:[/bold]")
    for p in providers:
        console.print(f"  • {p.value.upper()}")
        if region:
            console.print(f"    Region: {region}")
        else:
            console.print("    Regions: All configured regions")
        if check_types:
            console.print(f"    Checks: {', '.join(check_types)}")
        else:
            console.print("    Checks: All available checks")


def get_provider_identity_info(provider: CloudProvider, config: Dict) -> Tuple[str, List[str]]:
    """Get tenant/account ID and subscription/project IDs for a provider.
    
    Args:
        provider: Cloud provider
        config: Configuration dictionary
        
    Returns:
        Tuple of (tenant/account ID, list of subscription/project IDs)
    """
    provider_config = config.get(provider.value, {})
    
    if provider == CloudProvider.AZURE:
        tenant_id = provider_config.get("tenant_id", "Unknown")
        subscription_ids = []
        if "subscription_id" in provider_config:
            subscription_ids = [provider_config["subscription_id"]]
        return tenant_id, subscription_ids
    
    elif provider == CloudProvider.AWS:
        # For AWS, the account ID might be in metadata after authentication
        account_id = provider_config.get("account_id", "Unknown")
        regions = []
        if "region" in provider_config:
            regions = [provider_config["region"]]
        return account_id, regions
    
    elif provider == CloudProvider.GCP:
        # For GCP, use project ID as the primary identifier
        project_id = provider_config.get("project_id", "Unknown")
        return project_id, [project_id] if project_id != "Unknown" else []
    
    return "Unknown", []