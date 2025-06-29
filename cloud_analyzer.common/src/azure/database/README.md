# Azure Database Metrics Wrapper

A comprehensive Python wrapper for collecting utilization metrics from all Azure database services including SQL Database, PostgreSQL, and MySQL.

## Features

- **Unified Interface**: Single wrapper client for all Azure database types
- **Comprehensive Metrics**: CPU, memory, storage, IO, and database-specific metrics
- **Error Handling**: Robust error handling with retries and timeout support
- **Async Support**: Fully asynchronous implementation for better performance
- **Optimization Recommendations**: Built-in analysis for cost optimization and performance
- **Clean Code**: Follows Python best practices and clean code principles

## Installation

```bash
pip install azure-identity azure-mgmt-monitor azure-mgmt-sql azure-mgmt-rdbms
```

## Quick Start

```python
import asyncio
from azure.identity import DefaultAzureCredential
from src.azure.database import AzureDatabaseMetricsWrapper

async def main():
    # Initialize the wrapper
    wrapper = AzureDatabaseMetricsWrapper(
        credential=DefaultAzureCredential(),
        subscription_id="your-subscription-id"
    )
    
    # Get metrics for a specific database
    metrics = await wrapper.get_database_metrics(
        resource_id="/subscriptions/.../databases/mydb"
    )
    
    print(f"CPU Usage: {metrics.cpu_percent_avg:.2f}%")
    print(f"Memory Usage: {metrics.memory_percent_avg:.2f}%")
    
    # Get metrics for all databases
    all_metrics = await wrapper.get_all_database_metrics()
    
    # Get optimization recommendations
    recommendations = await wrapper.get_optimization_recommendations(
        include_all=True
    )
    
    await wrapper.close()

asyncio.run(main())
```

## Supported Database Types

### Azure SQL Database
- DTU-based (Basic, Standard, Premium)
- vCore-based (General Purpose, Business Critical)
- Metrics: CPU, Memory, DTU, Storage, Sessions, Workers

### Azure Database for PostgreSQL
- Single Server
- Flexible Server
- Metrics: CPU, Memory, Storage, IO, Connections, Network

### Azure Database for MySQL
- Single Server
- Flexible Server
- Metrics: CPU, Memory, Storage, IO, Connections, Queries, Replication

## Architecture

```
src/azure/database/
├── __init__.py          # Package exports
├── base.py              # Base classes and interfaces
├── sql_database.py      # SQL Database implementation
├── postgresql.py        # PostgreSQL implementation
├── mysql.py             # MySQL implementation
├── client.py            # Unified wrapper client
├── example.py           # Usage examples
└── README.md            # This file
```

## Key Classes

### AzureDatabaseMetricsWrapper
The main wrapper class that provides a unified interface for all database types.

**Key Methods:**
- `get_database_metrics()`: Get metrics for a specific database
- `list_all_databases()`: List all databases in the subscription
- `get_all_database_metrics()`: Get metrics for all databases
- `get_optimization_recommendations()`: Get cost and performance recommendations

### DatabaseMetrics
Data class containing all collected metrics:
- Resource identification (ID, name, type)
- CPU utilization (average and maximum)
- Memory utilization
- Storage utilization
- Database-specific metrics (DTU, IO, connections, etc.)

## Error Handling

The wrapper includes comprehensive error handling:
- Automatic retries with exponential backoff
- Timeout protection for long-running operations
- Specific handling for authentication and resource errors
- Detailed logging for debugging

## Best Practices

1. **Use async/await**: The wrapper is fully asynchronous for better performance
2. **Handle errors gracefully**: Always wrap calls in try-except blocks
3. **Set appropriate timeouts**: Configure timeout based on your needs
4. **Use connection pooling**: Reuse wrapper instances when possible
5. **Monitor at appropriate intervals**: Don't over-poll metrics

## Configuration

```python
wrapper = AzureDatabaseMetricsWrapper(
    credential=your_credential,
    subscription_id="subscription-id",
    retry_count=3,              # Number of retries
    retry_delay=1.0,            # Initial retry delay in seconds
    timeout=30.0                # Operation timeout in seconds
)
```

## Testing

Run the unit tests:

```bash
pytest tests/azure/database/test_client.py -v
```

## License

This wrapper follows the same license as the parent project.