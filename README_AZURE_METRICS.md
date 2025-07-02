# Azure Metrics CLI Application

A comprehensive Python CLI application that discovers Azure resources and collects their instrumentation metrics via the Azure REST API, storing the data in a local PostgreSQL database.

## Features

- **Resource Discovery**: Automatically discover Azure resources across subscriptions and resource groups
- **Metrics Collection**: Collect comprehensive metrics from Azure Monitor for various resource types
- **Database Storage**: Store metrics data in PostgreSQL with efficient indexing and partitioning
- **Async Processing**: High-performance async collection with configurable parallelization
- **Data Validation**: Built-in data quality checks and validation
- **Rich CLI**: Beautiful command-line interface with progress indicators and formatted output
- **Configuration Management**: Secure configuration with encrypted credential storage

## Supported Azure Resource Types

- **Virtual Machines** (CPU, memory, disk, network metrics)
- **App Services** (request metrics, response times, error rates)
- **SQL Databases** (DTU usage, connections, storage)
- **Storage Accounts** (transaction metrics, capacity, availability)
- **Application Insights** (custom metrics, performance counters)
- **Load Balancers** (data path availability, health probe status)
- **Azure Functions** (execution count, duration, errors)
- **Key Vault** (service API hits, availability)
- **Cosmos DB** (request units, storage, availability)

## Installation

### Prerequisites

- Python 3.8+
- PostgreSQL 12+
- Azure CLI (for authentication) or Azure service principal credentials

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Required Python Packages

- `azure-mgmt-monitor>=6.0.0` - Azure Monitor management
- `azure-mgmt-resource>=23.0.0` - Azure Resource management
- `azure-identity>=1.15.0` - Azure authentication
- `sqlalchemy>=2.0.0` - Database ORM
- `psycopg2-binary>=2.9.0` - PostgreSQL adapter
- `click>=8.1.7` - CLI framework
- `rich>=13.7.0` - Rich text and formatting
- `tenacity>=8.2.0` - Retry logic
- `pydantic>=2.5.0` - Data validation
- `cryptography>=41.0.0` - Configuration encryption

## Quick Start

### 1. Database Setup

Set up PostgreSQL database:

```bash
# Create database
sudo -u postgres createdb azure_metrics

# Configure database connection
cloud-analyzer setup-db configure --host localhost --port 5432 --database azure_metrics --username postgres

# Initialize database schema
cloud-analyzer setup-db init

# Test connection
cloud-analyzer setup-db test
```

### 2. Azure Authentication

Configure Azure credentials:

```bash
# Option 1: Use Azure CLI authentication
az login

# Option 2: Configure service principal
cloud-analyzer configure
```

For service principal authentication, you'll need:
- `tenant_id` - Azure AD tenant ID
- `client_id` - Application (client) ID
- `client_secret` - Client secret
- `subscription_id` - Azure subscription ID

### 3. Discover Resources

```bash
# Discover all resources
cloud-analyzer metrics discover

# Discover specific resource group
cloud-analyzer metrics discover --resource-group myResourceGroup

# Discover specific resource types
cloud-analyzer metrics discover --resource-type "Microsoft.Compute/virtualMachines"

# Dry run to see what would be discovered
cloud-analyzer metrics discover --dry-run
```

### 4. Collect Metrics

```bash
# Collect metrics for all discovered resources
cloud-analyzer metrics collect

# Collect metrics for specific time range
cloud-analyzer metrics collect --start-time 2024-01-01T00:00:00 --end-time 2024-01-02T00:00:00

# Collect with custom settings
cloud-analyzer metrics collect --interval-minutes 15 --batch-size 50 --parallel-workers 8
```

## CLI Commands

### Resource Discovery

```bash
# Discover and store resources
cloud-analyzer metrics discover [OPTIONS]

Options:
  -g, --resource-group TEXT    Filter by resource group (multiple allowed)
  -t, --resource-type TEXT     Filter by resource type (multiple allowed)
  -s, --subscription-id TEXT   Filter by subscription ID (multiple allowed)
  --dry-run                    Show what would be discovered without persisting
  -o, --output-format [table|json|csv]  Output format (default: table)
  -v, --verbose                Verbose output
```

### Metrics Collection

```bash
# Collect metrics from Azure Monitor
cloud-analyzer metrics collect [OPTIONS]

Options:
  -g, --resource-group TEXT    Filter by resource group
  -t, --resource-type TEXT     Filter by resource type
  -s, --subscription-id TEXT   Filter by subscription ID
  --start-time DATETIME        Start time (YYYY-MM-DD or YYYY-MM-DDTHH:MM:SS)
  --end-time DATETIME          End time (YYYY-MM-DD or YYYY-MM-DDTHH:MM:SS)
  --interval-minutes INTEGER   Collection interval in minutes (default: 15)
  --batch-size INTEGER         Batch size for processing (default: 100)
  --parallel-workers INTEGER   Number of parallel workers (default: 4)
  --dry-run                    Show what would be collected without persisting
  -v, --verbose                Verbose output
```

### Resource Management

```bash
# List discovered resources
cloud-analyzer metrics list-resources [OPTIONS]

Options:
  -t, --resource-type TEXT     Filter by resource type
  -g, --resource-group TEXT    Filter by resource group
  -s, --subscription-id TEXT   Filter by subscription ID
  -o, --output-format [table|json|csv]  Output format (default: table)
  -v, --verbose                Verbose output
```

### Collection History

```bash
# View collection run history
cloud-analyzer metrics collection-history [OPTIONS]

Options:
  -l, --limit INTEGER          Number of recent runs to show (default: 10)
  -v, --verbose                Verbose output
```

### Data Cleanup

```bash
# Clean up old metrics data
cloud-analyzer metrics cleanup [OPTIONS]

Options:
  --retention-days INTEGER     Number of days to retain (default from config)
  --dry-run                    Show what would be cleaned up
  -v, --verbose                Verbose output
```

### Database Management

```bash
# Configure database connection
cloud-analyzer setup-db configure [OPTIONS]

Options:
  -h, --host TEXT              Database host (default: localhost)
  -p, --port INTEGER           Database port (default: 5432)
  -d, --database TEXT          Database name (default: azure_metrics)
  -u, --username TEXT          Database username (default: postgres)
  --password TEXT              Database password
  --test-connection            Test connection after setup

# Initialize database schema
cloud-analyzer setup-db init

# Test database connection
cloud-analyzer setup-db test

# Show database status
cloud-analyzer setup-db status
```

## Configuration

### Configuration File Location

Configuration is stored in `~/.cloud-analyzer/config.json` with sensitive values encrypted.

### Configuration Structure

```json
{
  "azure": {
    "subscription_id": "your-subscription-id",
    "tenant_id": "your-tenant-id",
    "client_id": "your-client-id",
    "client_secret": {
      "encrypted": true,
      "value": "encrypted-secret"
    }
  },
  "database": {
    "host": "localhost",
    "port": "5432",
    "database": "azure_metrics",
    "username": "postgres",
    "password": {
      "encrypted": true,
      "value": "encrypted-password"
    }
  }
}
```

### Environment Variables

You can override configuration using environment variables:

```bash
export AZURE_SUBSCRIPTION_ID="your-subscription-id"
export AZURE_TENANT_ID="your-tenant-id"
export AZURE_CLIENT_ID="your-client-id"
export AZURE_CLIENT_SECRET="your-client-secret"

export DB_HOST="localhost"
export DB_PORT="5432"
export DB_DATABASE="azure_metrics"
export DB_USERNAME="postgres"
export DB_PASSWORD="your-password"
```

## Database Schema

### Key Tables

- **`resources`** - Azure resource metadata
- **`metric_definitions`** - Available metrics per resource type
- **`metric_data`** - Time series metric values (partitioned by date)
- **`collection_runs`** - Collection run tracking and statistics

### Performance Features

- **Indexes** - Optimized for time series queries
- **Partitioning** - Automatic partitioning by date for large datasets
- **Connection Pooling** - Efficient database connection management
- **Bulk Operations** - Batch inserts for high throughput

## Performance Tuning

### Collection Settings

```bash
# High throughput configuration
cloud-analyzer metrics collect \
  --batch-size 200 \
  --parallel-workers 8 \
  --interval-minutes 5

# Conservative configuration
cloud-analyzer metrics collect \
  --batch-size 50 \
  --parallel-workers 2 \
  --interval-minutes 60
```

### Database Optimization

```sql
-- Manual index creation for specific query patterns
CREATE INDEX CONCURRENTLY idx_metric_data_custom 
ON metric_data (resource_id, metric_name, timestamp DESC);

-- Partition maintenance (for large datasets)
SELECT cleanup_old_metric_data(90); -- Keep 90 days
```

## Error Handling

### Retry Logic

The application includes automatic retry logic for:
- Azure API rate limits (exponential backoff)
- Transient network errors
- Database connection issues

### Error Recovery

- **Partial failures** - Continue processing other resources if some fail
- **Graceful degradation** - Skip problematic metrics while collecting others
- **Detailed logging** - Comprehensive error tracking and reporting

## Monitoring

### Collection Run Status

```bash
# Check recent collection runs
cloud-analyzer metrics collection-history --limit 5

# Database statistics
cloud-analyzer setup-db status
```

### Logging

Logs are written to console with configurable verbosity:

```bash
# Enable verbose logging
cloud-analyzer metrics collect --verbose

# Enable debug logging (set environment variable)
export LOG_LEVEL=DEBUG
```

## Examples

### Basic Workflow

```bash
# 1. Set up database
cloud-analyzer setup-db configure --test-connection
cloud-analyzer setup-db init

# 2. Configure Azure credentials
cloud-analyzer configure

# 3. Discover resources
cloud-analyzer metrics discover --resource-group production

# 4. Collect metrics for last 24 hours
cloud-analyzer metrics collect --start-time 2024-01-01T00:00:00

# 5. View results
cloud-analyzer metrics list-resources
cloud-analyzer metrics collection-history
```

### Advanced Usage

```bash
# Collect metrics for specific resource types
cloud-analyzer metrics discover \
  --resource-type "Microsoft.Compute/virtualMachines" \
  --resource-type "Microsoft.Web/sites"

# High-frequency collection with custom timeframe
cloud-analyzer metrics collect \
  --start-time "2024-01-01T00:00:00" \
  --end-time "2024-01-01T23:59:59" \
  --interval-minutes 5 \
  --parallel-workers 10

# Export resource list to CSV
cloud-analyzer metrics list-resources --output-format csv > resources.csv

# Clean up old data (keep 30 days)
cloud-analyzer metrics cleanup --retention-days 30
```

### Automation Examples

```bash
#!/bin/bash
# Daily metrics collection script

# Collect yesterday's metrics
yesterday=$(date -d "yesterday" +%Y-%m-%d)
cloud-analyzer metrics collect \
  --start-time "${yesterday}T00:00:00" \
  --end-time "${yesterday}T23:59:59" \
  --batch-size 100 \
  --parallel-workers 4

# Clean up old data (keep 90 days)
cloud-analyzer metrics cleanup --retention-days 90

# Check collection status
cloud-analyzer metrics collection-history --limit 1
```

## Troubleshooting

### Common Issues

**Authentication Errors**
```bash
# Check Azure CLI authentication
az account show

# Test configuration
cloud-analyzer auth-status
```

**Database Connection Issues**
```bash
# Test database connection
cloud-analyzer setup-db test

# Check PostgreSQL service
sudo systemctl status postgresql
```

**Performance Issues**
```bash
# Reduce batch size and workers
cloud-analyzer metrics collect --batch-size 50 --parallel-workers 2

# Check database performance
cloud-analyzer setup-db status
```

### Debug Mode

```bash
# Enable detailed logging
export LOG_LEVEL=DEBUG
cloud-analyzer metrics collect --verbose
```

## Contributing

Please see the main project README for contribution guidelines.

## License

This project is part of the Cloud Analyzer suite. See LICENSE for details.