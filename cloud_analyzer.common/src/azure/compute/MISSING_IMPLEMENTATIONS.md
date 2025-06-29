# Missing Compute Resource Implementations

## Priority 1: VM Scale Sets

### Key Metrics Needed
- Instance count (current, minimum, maximum)
- CPU percentage per instance
- Network in/out per instance
- Disk operations per instance
- Scale-in/out events
- Health probe status

### Implementation Skeleton
```python
class VMScaleSetMetricsClient(AzureComputeMetricsClient):
    """Client for collecting Azure VM Scale Set metrics."""
    
    async def get_compute_metrics(self, resource_id: str, ...) -> ComputeMetrics:
        # Get VMSS details
        # Collect instance-level metrics
        # Aggregate metrics across instances
        # Include scaling metrics
        pass
```

## Priority 2: Azure Kubernetes Service (AKS)

### Key Metrics Needed
- Node count and health
- Pod count and status
- CPU/Memory per node
- Network traffic
- Container restarts
- Cluster autoscaler metrics

### Challenges
- Multi-level metrics (cluster, node, pod)
- Integration with Kubernetes metrics
- Container-specific monitoring

## Priority 3: Container Instances

### Key Metrics Needed
- CPU usage
- Memory usage
- Network bytes transmitted/received
- Container group status
- Restart count

### Implementation Notes
- Simpler than AKS
- Direct container metrics
- No orchestration overhead

## Priority 4: Azure Functions

### Key Metrics Needed
- Function execution count
- Function execution units
- Average execution duration
- Function failures
- HTTP trigger response times
- Queue/Event trigger latencies

### Special Considerations
- Consumption vs Premium plans
- Cold start metrics
- Trigger-specific metrics

## Priority 5: Azure Batch

### Key Metrics Needed
- Active node count
- Idle node count
- Task completion rate
- Failed task count
- Node state transitions
- Pool utilization

### Complexity
- Job-level aggregation
- Pool management metrics
- Task scheduling metrics

## Implementation Template

```python
# Template for new resource implementations
class <ResourceType>MetricsClient(AzureComputeMetricsClient):
    """Client for collecting Azure <ResourceType> metrics."""
    
    def __init__(self, credential, subscription_id, monitor_client=None, resource_client=None):
        super().__init__(credential, subscription_id, monitor_client)
        self._resource_client = resource_client
    
    @property
    def resource_client(self):
        """Get or create the resource management client."""
        if not self._resource_client:
            self._resource_client = <ResourceManagementClient>(
                credential=self.credential,
                subscription_id=self.subscription_id
            )
        return self._resource_client
    
    async def get_compute_metrics(self, resource_id, time_range=None, 
                                  aggregation="Average", interval=None,
                                  include_capacity_metrics=True) -> ComputeMetrics:
        """Get utilization metrics for <ResourceType>."""
        # 1. Parse resource information
        # 2. Get resource details from ARM
        # 3. Define resource-specific metrics
        # 4. Fetch metrics from Azure Monitor
        # 5. Process and aggregate metrics
        # 6. Build ComputeMetrics object
        # 7. Add resource-specific information
        pass
    
    async def list_resources(self) -> List[Dict[str, Any]]:
        """List all <ResourceType> in the subscription."""
        # Use resource client to list all resources
        pass
    
    async def get_recommendations(self, resource_id, metrics=None, 
                                  pricing_tier=None) -> List[ComputeRecommendation]:
        """Get optimization recommendations for <ResourceType>."""
        # Analyze metrics for optimization opportunities
        pass
```

## Required Azure SDK Clients

1. **VM Scale Sets**: `azure.mgmt.compute.ComputeManagementClient`
2. **AKS**: `azure.mgmt.containerservice.ContainerServiceClient`
3. **Container Instances**: `azure.mgmt.containerinstance.ContainerInstanceManagementClient`
4. **Functions**: `azure.mgmt.web.WebSiteManagementClient`
5. **Batch**: `azure.mgmt.batch.BatchManagementClient`
6. **Service Fabric**: `azure.mgmt.servicefabric.ServiceFabricManagementClient`

## Testing Requirements

Each implementation needs:
1. Unit tests with mocked Azure clients
2. Metric calculation tests
3. Recommendation logic tests
4. Error handling tests
5. Integration test examples