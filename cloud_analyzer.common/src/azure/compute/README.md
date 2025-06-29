# Azure Compute Metrics Wrapper

A comprehensive Python wrapper for collecting utilization metrics from all Azure compute services including Virtual Machines, App Services, VM Scale Sets, Container Instances, and AKS clusters.

## Features

- **Unified Interface**: Single wrapper client for all Azure compute resource types
- **Comprehensive Metrics**: 
  - CPU, memory, network, and disk utilization
  - Service-specific metrics (requests, response times, error rates)
  - Percentile calculations (p95, p99) for better insights
- **Advanced Capabilities**:
  - Concurrent metric collection with rate limiting
  - Resource filtering by tags, resource groups, and locations
  - Cost optimization analysis with savings estimates
  - Performance and reliability recommendations
- **Robust Error Handling**: 
  - Automatic retries with exponential backoff
  - Timeout protection
  - Detailed error context and logging
- **Clean Architecture**: Follows SOLID principles and clean code standards

## Supported Resource Types

### Virtual Machines
- CPU, memory, network, and disk metrics
- Power state monitoring
- OS and storage information
- Availability zone detection

### App Services
- CPU, memory, and response time metrics
- Request counts and error rates
- HTTP status code breakdown
- App Service Plan information

### Coming Soon
- VM Scale Sets
- Container Instances
- AKS Clusters
- Batch Accounts
- Service Fabric Clusters

## Installation

```bash
pip install azure-identity azure-mgmt-monitor azure-mgmt-compute azure-mgmt-web
```

## Quick Start

```python
import asyncio
from azure.identity import DefaultAzureCredential
from src.azure.compute import AzureComputeMetricsWrapper

async def main():
    # Initialize the wrapper
    wrapper = AzureComputeMetricsWrapper(
        credential=DefaultAzureCredential(),
        subscription_id="your-subscription-id"
    )
    
    # Get metrics for a specific VM
    vm_metrics = await wrapper.get_compute_metrics(
        resource_id="/subscriptions/.../virtualMachines/myvm"
    )
    
    print(f"VM CPU Usage: {vm_metrics.cpu_percent_avg:.2f}%")
    print(f"VM Memory Usage: {vm_metrics.memory_percent_avg:.2f}%")
    
    # Get cost optimization recommendations
    recommendations = await wrapper.get_optimization_recommendations(
        resource_id=vm_metrics.resource_id
    )
    
    for rec in recommendations:
        print(f"{rec.severity}: {rec.description}")
    
    await wrapper.close()

asyncio.run(main())
```

## Architecture

```
src/azure/compute/
├── __init__.py              # Package exports
├── base.py                  # Base classes and data models
├── virtual_machines.py      # VM implementation
├── app_services.py          # App Service implementation
├── client.py                # Unified wrapper client
├── example.py               # Usage examples
└── README.md                # This file
```

## Key Classes

### AzureComputeMetricsWrapper
The main wrapper class providing a unified interface for all compute resource types.

**Key Methods:**
- `get_compute_metrics()`: Get metrics for any compute resource
- `list_all_compute_resources()`: List all compute resources
- `get_all_compute_metrics()`: Get metrics for multiple resources
- `get_optimization_recommendations()`: Get cost and performance recommendations
- `get_cost_optimization_summary()`: Get aggregated cost savings opportunities

### ComputeMetrics
Data class containing all collected metrics:
- Resource identification and metadata
- CPU, memory, network, and disk utilization
- Service-specific metrics (requests, errors, etc.)
- Tags, SKU, and state information

### ComputeRecommendation
Optimization recommendation with:
- Type (resize, shutdown, reserved instance, etc.)
- Severity (high, medium, low)
- Impact (cost, performance, availability, security)
- Estimated savings

## Advanced Usage

### Batch Processing with Filters

```python
# Get metrics for production VMs in specific regions
metrics = await wrapper.get_all_compute_metrics(
    resource_types=['virtual_machines'],
    resource_filter={
        'tags': {'environment': 'production'},
        'locations': ['eastus', 'westus'],
        'resource_groups': ['prod-rg1', 'prod-rg2']
    }
)
```

### Cost Optimization Analysis

```python
# Get comprehensive cost optimization summary
summary = await wrapper.get_cost_optimization_summary()

print(f"Total potential savings: ${summary['estimated_annual_savings']:,.0f}")
for opportunity in summary['top_opportunities']:
    print(f"{opportunity['resource_name']}: ${opportunity['annual_savings']:,.0f}/year")
```

### Performance Monitoring

```python
# Monitor performance with hourly granularity
metrics = await wrapper.get_compute_metrics(
    resource_id=vm_id,
    time_range=(datetime.utcnow() - timedelta(days=1), datetime.utcnow()),
    interval=timedelta(hours=1)
)

# Check 95th percentile CPU usage
if metrics.cpu_percent_p95 > 90:
    print("High CPU usage detected!")
```

## Configuration Options

```python
wrapper = AzureComputeMetricsWrapper(
    credential=your_credential,        # Azure credential
    subscription_id="sub-id",          # Azure subscription
    retry_count=3,                     # Number of retries
    retry_delay=1.0,                   # Initial retry delay (seconds)
    timeout=30.0,                      # Operation timeout (seconds)
    concurrent_requests=10             # Max concurrent API requests
)
```

## Error Handling

The wrapper provides comprehensive error handling:
- Authentication errors with clear messages
- Resource not found with context
- Timeout protection for long operations
- Retry logic for transient failures
- Rate limiting to avoid API throttling

## Best Practices

1. **Use Resource Filters**: Filter resources to reduce API calls and improve performance
2. **Batch Operations**: Process multiple resources concurrently for efficiency
3. **Handle Exceptions**: Always wrap calls in try-except blocks
4. **Set Appropriate Timeouts**: Adjust timeout based on resource count
5. **Monitor Rate Limits**: Use concurrent_requests to control API usage

## Recommendations System

The wrapper provides intelligent recommendations:
- **Resize**: Detect over/under-provisioned resources
- **Shutdown**: Identify idle or stopped resources
- **Reserved Instances**: Suggest RI purchases for consistent workloads
- **Performance**: Alert on high utilization
- **Security**: Check for security best practices
- **Governance**: Ensure proper tagging and organization

## Testing

Run the comprehensive test suite:

```bash
python -m pytest tests/azure/compute/ -v
```

The test suite includes:
- Unit tests with mocked Azure dependencies
- Async operation testing
- Error handling scenarios
- Resource filtering tests
- Recommendation generation tests

## Future Enhancements

- Support for additional compute services (AKS, Container Instances)
- Real-time metric streaming
- Integration with Azure Advisor
- Custom metric definitions
- Export to monitoring systems (Prometheus, Grafana)
- Machine learning for anomaly detection
- Automated remediation actions