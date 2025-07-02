"""Database setup and management commands."""

import click
from rich.console import Console
from rich.panel import Panel
from rich import print as rprint
from typing import Optional

import sys
import os
# Add the common module to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..', 'cloud_analyzer.common', 'src'))

from database.connection import DatabaseConnection, get_database_url
from ..utils.config import get_config

console = Console()


@click.group()
def setup_db():
    """Database setup and management commands."""
    pass


@setup_db.command()
@click.option('--host', '-h', help='Database host (default: localhost)')
@click.option('--port', '-p', type=int, help='Database port (default: 5432)')
@click.option('--database', '-d', help='Database name (default: azure_metrics)')
@click.option('--username', '-u', help='Database username (default: postgres)')
@click.option('--password', help='Database password')
@click.option('--test-connection', is_flag=True, help='Test database connection after setup')
def configure(
    host: Optional[str],
    port: Optional[int],
    database: Optional[str],
    username: Optional[str],
    password: Optional[str],
    test_connection: bool
):
    """Configure database connection settings."""
    try:
        config = get_config()
        
        # Get current database config or set defaults
        db_config = config.get('database', {
            'host': 'localhost',
            'port': '5432',
            'database': 'azure_metrics',
            'username': 'postgres',
            'password': ''
        })
        
        # Update with provided values
        if host:
            db_config['host'] = host
        if port:
            db_config['port'] = str(port)
        if database:
            db_config['database'] = database
        if username:
            db_config['username'] = username
        if password:
            db_config['password'] = password
        
        # Save updated configuration
        config['database'] = db_config
        
        from ..utils.config import save_config
        save_config(config)
        
        rprint("[green]Database configuration saved successfully![/green]")
        
        # Display current configuration (without password)
        display_config = db_config.copy()
        display_config['password'] = '***' if display_config.get('password') else 'Not set'
        
        config_text = "\n".join([f"{k}: {v}" for k, v in display_config.items()])
        console.print(Panel(config_text, title="Database Configuration", border_style="blue"))
        
        # Test connection if requested
        if test_connection:
            rprint("\n[blue]Testing database connection...[/blue]")
            db_connection = DatabaseConnection(config)
            
            if db_connection.test_connection():
                rprint("[green]✓ Database connection successful![/green]")
            else:
                rprint("[red]✗ Database connection failed. Please check your settings.[/red]")
                return
        
    except Exception as e:
        rprint(f"[red]Failed to configure database: {e}[/red]")
        raise click.ClickException(str(e))


@setup_db.command()
def init():
    """Initialize database schema (create tables)."""
    try:
        config = get_config()
        
        rprint("[blue]Initializing database schema...[/blue]")
        
        # Test connection first
        db_connection = DatabaseConnection(config)
        if not db_connection.test_connection():
            rprint("[red]Failed to connect to database. Please check your configuration.[/red]")
            rprint("Run 'cloud-analyzer setup-db configure' to set up database connection.")
            return
        
        # Create tables
        db_connection.create_tables()
        
        rprint("[green]✓ Database schema initialized successfully![/green]")
        rprint("You can now run metrics collection commands.")
        
    except Exception as e:
        rprint(f"[red]Failed to initialize database: {e}[/red]")
        raise click.ClickException(str(e))


@setup_db.command()
def test():
    """Test database connection."""
    try:
        config = get_config()
        
        rprint("[blue]Testing database connection...[/blue]")
        
        # Show current configuration (without password)
        db_config = config.get('database', {})
        display_config = db_config.copy()
        display_config['password'] = '***' if display_config.get('password') else 'Not set'
        
        config_text = "\n".join([f"{k}: {v}" for k, v in display_config.items()])
        console.print(Panel(config_text, title="Current Database Configuration", border_style="blue"))
        
        # Test connection
        db_connection = DatabaseConnection(config)
        
        if db_connection.test_connection():
            rprint("\n[green]✓ Database connection successful![/green]")
            
            # Show database URL (without password)
            db_url = get_database_url(config)
            safe_url = db_url.split('@')[0].split(':')[:-1] + ['***@'] + db_url.split('@')[1:]
            safe_url = ''.join(safe_url) if len(safe_url) > 1 else db_url
            rprint(f"[dim]Connection URL: {safe_url}[/dim]")
            
        else:
            rprint("\n[red]✗ Database connection failed![/red]")
            rprint("Please check your database configuration and ensure PostgreSQL is running.")
            rprint("Run 'cloud-analyzer setup-db configure' to update settings.")
            
    except Exception as e:
        rprint(f"[red]Database connection test failed: {e}[/red]")
        raise click.ClickException(str(e))


@setup_db.command()
def status():
    """Show database status and statistics."""
    try:
        config = get_config()
        
        # Test connection
        db_connection = DatabaseConnection(config)
        if not db_connection.test_connection():
            rprint("[red]✗ Cannot connect to database[/red]")
            return
        
        rprint("[green]✓ Database connection successful[/green]")
        
        # Get database statistics
        try:
            db_connection.initialize()
            
            session = db_connection.get_sync_session()
            try:
                # Import models to get table info
                from database.models import Resource, MetricDataModel, CollectionRunModel
                
                # Get counts
                resource_count = session.query(Resource).count()
                metrics_count = session.query(MetricDataModel).count()
                collection_runs_count = session.query(CollectionRunModel).count()
                
                # Get latest collection run
                latest_run = session.query(CollectionRunModel).order_by(
                    CollectionRunModel.created_at.desc()
                ).first()
                
                status_info = f"""
[bold]Resources:[/bold] {resource_count:,}
[bold]Metric Data Points:[/bold] {metrics_count:,}
[bold]Collection Runs:[/bold] {collection_runs_count:,}
[bold]Latest Collection:[/bold] {latest_run.created_at.strftime('%Y-%m-%d %H:%M:%S') if latest_run else 'None'}
"""
                
                console.print(Panel(status_info, title="Database Statistics", border_style="green"))
                
            finally:
                session.close()
                
        except Exception as e:
            rprint(f"[yellow]Could not get database statistics: {e}[/yellow]")
            
    except Exception as e:
        rprint(f"[red]Failed to get database status: {e}[/red]")
        raise click.ClickException(str(e))