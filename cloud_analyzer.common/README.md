# Azure Database Metrics Wrapper

A comprehensive Python wrapper client for collecting utilization metrics from all Azure database services (SQL Database, PostgreSQL, and MySQL). Built with clean code principles and Python best practices.

## Features

- **Unified Interface**: Single wrapper client for all Azure database types
- **Comprehensive Metrics Collection**: 
  - CPU, memory, storage, and IO utilization
  - Database-specific metrics (DTU for SQL, connections for PostgreSQL/MySQL)
  - Support for both single server and flexible server architectures
- **Robust Error Handling**: 
  - Automatic retries with exponential backoff
  - Timeout protection
  - Detailed error context and logging
- **Async/Await Support**: Fully asynchronous for optimal performance
- **Cost Optimization**: Built-in recommendations for right-sizing and cost savings
- **Clean Architecture**: Follows SOLID principles and clean code standards

## Project Structure

```
src/azure/database/
├── __init__.py           # Package exports
├── base.py               # Abstract base classes and data models
├── client.py             # Unified wrapper client with error handling
├── sql_database.py       # Azure SQL Database implementation
├── postgresql.py         # PostgreSQL implementation
├── mysql.py              # MySQL implementation
├── example.py            # Usage examples
└── README.md             # Detailed documentation

tests/azure/database/
├── test_wrapper_mocked.py  # Unit tests with mocked Azure imports
├── test_base.py           # Base class tests
├── test_sql_database.py   # SQL Database specific tests
└── test_simple.py         # Simple test to verify environment
```

## Installation

```bash
pip install -r requirements.txt
```

Required packages:
- azure-identity
- azure-mgmt-monitor
- azure-mgmt-sql
- azure-mgmt-rdbms
- azure-core

## Usage

### Basic Example

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
    
    await wrapper.close()

asyncio.run(main())
```

### Advanced Usage

```python
# Get metrics for all databases with optimization recommendations
all_recommendations = await wrapper.get_optimization_recommendations(
    include_all=True
)

for db_name, recommendations in all_recommendations.items():
    print(f"\nDatabase: {db_name}")
    for rec in recommendations:
        print(f"  - [{rec['severity']}] {rec['description']}")
        print(f"    Action: {rec['action']}")
```

## Key Components

### DatabaseMetrics
Data class containing all collected metrics:
- Resource identification
- CPU, memory, storage utilization
- Database-specific metrics (DTU, IO, connections)
- Time range and aggregation details

### AzureDatabaseMetricsWrapper
Main wrapper class providing:
- Unified interface for all database types
- Automatic database type detection
- Retry logic and error handling
- Concurrent metric collection
- Optimization recommendations

### Database-Specific Clients
- **SqlDatabaseMetricsClient**: Handles SQL Database (DTU and vCore models)
- **PostgreSQLMetricsClient**: Handles PostgreSQL (Single and Flexible servers)
- **MySQLMetricsClient**: Handles MySQL (Single and Flexible servers)

## Design Principles

1. **Single Responsibility**: Each class has one clear purpose
2. **Open/Closed**: Easy to extend for new database types
3. **Dependency Inversion**: Interfaces defined in base classes
4. **DRY**: Common functionality in base classes
5. **Error Handling**: Comprehensive error handling with context
6. **Testability**: Designed for easy unit testing

## Testing

Run all tests:
```bash
python -m pytest tests/azure/database/ -v
```

The test suite includes:
- Unit tests with mocked Azure dependencies
- Async operation testing
- Error handling scenarios
- Full coverage of wrapper functionality

## Best Practices Implemented

1. **Type Hints**: Full type annotations throughout
2. **Docstrings**: Comprehensive documentation
3. **Logging**: Structured logging with appropriate levels
4. **Async/Await**: Proper async context managers and error handling
5. **Configuration**: Configurable retry and timeout settings
6. **Resource Cleanup**: Proper cleanup in async context
7. **Validation**: Input validation and error messages

## Configuration Options

```python
wrapper = AzureDatabaseMetricsWrapper(
    credential=your_credential,        # Azure credential
    subscription_id="sub-id",          # Azure subscription
    retry_count=3,                     # Number of retries
    retry_delay=1.0,                   # Initial retry delay (seconds)
    timeout=30.0                       # Operation timeout (seconds)
)
```

## Error Handling

The wrapper provides comprehensive error handling:
- Authentication errors with clear messages
- Resource not found with context
- Timeout protection for long operations
- Retry logic for transient failures
- Detailed logging for debugging

## Future Enhancements

- Support for Cosmos DB metrics
- Metric streaming and real-time monitoring
- Integration with Azure Cost Management API
- Custom metric definitions
- Export to monitoring systems (Prometheus, Grafana)