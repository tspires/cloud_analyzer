"""Analyze command for running optimization checks."""

import asyncio
import json
import sys
from pathlib import Path
from typing import Dict, List, Optional

import click
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn

# Add parent directory to path to import from cloud_analyzer.common
sys.path.append(str(Path(__file__).parent.parent.parent.parent / 'cloud_analyzer.common' / 'src'))

from models.base import CloudProvider
from models.checks import CheckResult
from checks.registry import check_registry
from checks.register_checks import register_all_checks
from providers.azure import AzureProvider

from formatters.check_results import format_check_results
from utils.config import load_config
from utils.cloud_identity import (
    display_cloud_identity_panel,
    display_multi_cloud_identity_table,
)
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


class AnalysisContext:
    """Context object to hold analysis state and configuration."""
    
    def __init__(
        self,
        providers: List[CloudProvider],
        region: Optional[str],
        check_types: Optional[List[str]],
        config: Dict,
    ):
        self.providers = providers
        self.region = region
        self.check_types = check_types
        self.config = config
        self.results: List[CheckResult] = []


class ProviderAnalyzer:
    """Handles analysis for cloud providers."""
    
    def __init__(self, context: AnalysisContext):
        self.context = context
    
    async def analyze_provider(self, provider: CloudProvider, provider_config: Dict) -> None:
        """Analyze resources for a cloud provider."""
        # Create provider instance
        provider_instance = None
        
        if provider == CloudProvider.AZURE:
            # Handle multiple subscriptions for Azure
            subscription_ids = self._get_azure_subscription_ids(provider_config)
            if not subscription_ids:
                self._display_no_subscriptions_warning()
                return
            
            subscription_names = provider_config.get('subscription_names', {})
            
            for idx, subscription_id in enumerate(subscription_ids, 1):
                sub_display = subscription_names.get(subscription_id, subscription_id)
                self._display_subscription_header(sub_display, idx, len(subscription_ids))
                
                provider_instance = AzureProvider(subscription_id=subscription_id)
                await self._analyze_with_provider(provider_instance, provider)
        
    
    def _get_azure_subscription_ids(self, provider_config: Dict) -> List[str]:
        """Extract and validate Azure subscription IDs from configuration."""
        subscription_ids = provider_config.get('subscription_ids', [])
        
        if not subscription_ids and 'subscription_id' in provider_config:
            subscription_ids = [provider_config['subscription_id']]
        
        return [sid for sid in subscription_ids if sid and isinstance(sid, str)]
    
    def _display_no_subscriptions_warning(self) -> None:
        """Display warning when no subscriptions are configured."""
        console.print(
            f"[yellow]Warning: No subscriptions configured for Azure[/yellow]"
        )
        console.print(
            "[dim]Run 'cloud-analyzer configure --provider azure' to set up subscriptions[/dim]"
        )
    
    def _display_subscription_header(self, display_name: str, idx: int, total: int) -> None:
        """Display subscription analysis header."""
        if total > 1:
            console.print(
                f"\n[bold cyan]Checking Subscription ({idx}/{total}): {display_name}[/bold cyan]"
            )
        else:
            console.print(f"\n[bold cyan]Checking Subscription: {display_name}[/bold cyan]")
    
    async def _analyze_with_provider(self, provider_instance, provider: CloudProvider) -> None:
        """Run analysis with a specific provider instance."""
        try:
            # Initialize provider
            console.print(f"  Initializing {provider.value} provider...")
            await provider_instance.initialize()
            
            # Get resources
            console.print("  Fetching resources...")
            regions = [self.context.region] if self.context.region else None
            resources = await provider_instance.list_resources(regions=regions)
            
            console.print(f"  Found {len(resources)} resources")
            
            # Run checks
            await self._run_checks(provider_instance, resources)
            
        except Exception as e:
            console.print(f"  [red]Error analyzing {provider.value}: {str(e)}[/red]")
    
    async def _run_checks(self, provider_instance, resources) -> None:
        """Run registered checks against resources."""
        # Get all registered checks
        checks = check_registry.list_all()
        
        # Filter checks if specific types requested
        if self.context.check_types:
            checks = [c for c in checks if c.id in self.context.check_types]
        
        # Filter checks by provider compatibility
        provider_checks = [c for c in checks if provider_instance.provider in c.supported_providers]
        
        console.print(f"\n  Running {len(provider_checks)} checks...")
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
        ) as progress:
            task = progress.add_task("Running checks...", total=len(provider_checks))
            
            for check in provider_checks:
                progress.update(task, description=f"Running {check.name}...")
                
                try:
                    # Run the check
                    results = await check.run(provider_instance, resources)
                    
                    # Add results to context
                    self.context.results.extend(results)
                    
                except Exception as e:
                    console.print(f"    [yellow]Warning: Check '{check.name}' failed: {str(e)}[/yellow]")
                
                progress.advance(task)




class OutputFormatter:
    """Handles formatting and output of analysis results."""
    
    def __init__(self, console: Console):
        self.console = console
    
    def format_output(
        self,
        results: List[CheckResult],
        output_format: str,
        output_file: Optional[Path],
        config: Dict,
        display_provider: Optional[CloudProvider]
    ) -> None:
        """Format and output results based on specified format."""
        formatters = {
            "table": self._format_table,
            "json": self._format_json,
            "csv": self._format_csv,
        }
        
        formatter = formatters.get(output_format)
        if formatter:
            formatter(results, output_file, config, display_provider)
    
    def _format_table(
        self,
        results: List[CheckResult],
        output_file: Optional[Path],
        config: Dict,
        display_provider: Optional[CloudProvider]
    ) -> None:
        """Format results as a table."""
        format_check_results(results, self.console, config, display_provider)
        display_summary(results)
    
    def _format_json(
        self,
        results: List[CheckResult],
        output_file: Optional[Path],
        config: Dict,
        display_provider: Optional[CloudProvider]
    ) -> None:
        """Format results as JSON."""
        if output_file:
            save_results_json(results, output_file)
        else:
            self.console.print(
                json.dumps([r.dict() for r in results], indent=2, default=str)
            )
    
    def _format_csv(
        self,
        results: List[CheckResult],
        output_file: Optional[Path],
        config: Dict,
        display_provider: Optional[CloudProvider]
    ) -> None:
        """Format results as CSV."""
        if output_file:
            save_results_csv(results, output_file)
        else:
            self.console.print("[red]Error:[/red] CSV output requires --output-file")


async def validate_credentials(providers: List[CloudProvider], config: Dict) -> None:
    """Validate credentials for all providers."""
    with console.status("[bold yellow]Validating credentials...[/bold yellow]") as status:
        for provider in providers:
            status.update(
                f"[bold yellow]Validating {provider.value.upper()} credentials...[/bold yellow]"
            )
            
            # Create provider instance and validate
            provider_config = config.get(provider.value, {})
            provider_instance = None
            
            try:
                if provider == CloudProvider.AZURE:
                    subscription_id = provider_config.get('subscription_id')
                    if subscription_id:
                        provider_instance = AzureProvider(subscription_id=subscription_id)
                
                if provider_instance:
                    await provider_instance.initialize()
                    if not await provider_instance.validate_credentials():
                        console.print(f"✗ [red]{provider.value.upper()} credentials invalid[/red]")
                        raise click.ClickException(f"Invalid {provider.value} credentials")
                        
            except Exception as e:
                console.print(f"✗ [red]{provider.value.upper()} validation failed: {str(e)}[/red]")
                raise
                
        console.print("✓ [green]Credentials validated[/green]")


async def run_analysis(
    providers: List[CloudProvider],
    region: Optional[str],
    check_types: Optional[List[str]],
    config: dict,
) -> List[CheckResult]:
    """Run the actual analysis."""
    # Ensure checks are registered
    register_all_checks()
    
    context = AnalysisContext(providers, region, check_types, config)
    analyzer = ProviderAnalyzer(context)
    
    for provider_enum in providers:
        provider_config = config.get(provider_enum.value, {})
        await analyzer.analyze_provider(provider_enum, provider_config)
    
    return context.results


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
    _display_cloud_identity(provider, providers_to_analyze, config)
    
    # Run analysis
    console.print("\n[bold cyan]Starting cloud resource analysis...[/bold cyan]\n")
    
    try:
        asyncio.run(validate_credentials(providers_to_analyze, config))
        
        console.print("\n[bold yellow]Running analysis...[/bold yellow]")
        results = asyncio.run(
            run_analysis(providers_to_analyze, region, check_types, config)
        )
        
        # Filter results by severity
        results = _filter_results(results, severity)
        
        # Format and output results
        display_provider = _get_display_provider(provider, providers_to_analyze)
        formatter = OutputFormatter(console)
        formatter.format_output(results, output, output_file, config, display_provider)
        
    except Exception as e:
        console.print(f"[red]Error during analysis:[/red] {str(e)}")
        raise


def _display_cloud_identity(
    provider: str,
    providers_to_analyze: List[CloudProvider],
    config: Dict
) -> None:
    """Display cloud identity information."""
    console.print("\n[bold cyan]Cloud Instance Information[/bold cyan]\n")
    
    if provider == "all":
        display_multi_cloud_identity_table(config, console)
    else:
        display_cloud_identity_panel(providers_to_analyze[0], config, console)


def _filter_results(results: List[CheckResult], severity: str) -> List[CheckResult]:
    """Filter results by severity level."""
    console.print("\n[bold yellow]Filtering results by severity...[/bold yellow]")
    filtered_results = filter_results_by_severity(results, severity)
    console.print(f"✓ [green]Found {len(filtered_results)} findings matching severity filter[/green]")
    return filtered_results


def _get_display_provider(
    provider: str,
    providers_to_analyze: List[CloudProvider]
) -> Optional[CloudProvider]:
    """Get the provider for display purposes."""
    if provider != "all" and providers_to_analyze:
        return providers_to_analyze[0]
    return None