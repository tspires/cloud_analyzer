"""Main CLI entry point."""

import logging
import sys

import click
from rich.console import Console

from commands import analyze, auth_status, configure, list_checks, report, run_check
from cli_constants import (
    VERSION,
    EXIT_SUCCESS,
    EXIT_ERROR,
    EXIT_KEYBOARD_INTERRUPT,
    INFO_OPERATION_CANCELLED,
    ERROR_UNEXPECTED,
    INFO_RUN_WITH_DEBUG,
)

console = Console()
logger = logging.getLogger(__name__)


@click.group()
@click.version_option(version=VERSION, prog_name="cloud-analyzer")
@click.pass_context
def cli(ctx: click.Context) -> None:
    """Cloud Analyzer - Azure cloud cost optimization tool.
    
    Analyze your Azure cloud infrastructure to identify
    cost optimization opportunities.
    """
    ctx.ensure_object(dict)


# Register commands
cli.add_command(configure.configure)
cli.add_command(auth_status.auth_status)
cli.add_command(analyze.analyze)
cli.add_command(list_checks.list_checks)
cli.add_command(report.report)
cli.add_command(run_check.run_check)


def main() -> None:
    """Main entry point."""
    try:
        cli()
    except click.ClickException:
        # Click will handle its own exceptions
        raise
    except KeyboardInterrupt:
        console.print(f"\n[yellow]{INFO_OPERATION_CANCELLED}[/yellow]")
        sys.exit(EXIT_KEYBOARD_INTERRUPT)
    except Exception as e:
        logger.exception("Unexpected error in CLI")
        console.print(f"[red]{ERROR_UNEXPECTED.format(str(e))}[/red]")
        console.print(f"[dim]{INFO_RUN_WITH_DEBUG}[/dim]")
        sys.exit(EXIT_ERROR)


if __name__ == "__main__":
    main()