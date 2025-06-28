# Azure Resource Type Coverage Analysis

## Currently Supported Resource Types

### ✅ Implemented
1. **Virtual Machines** (Compute)
   - Type: `ResourceType.INSTANCE`
   - Checks: Reserved instance utilization, right-sizing potential

2. **Managed Disks** (Storage) 
   - Type: `ResourceType.VOLUME`
   - Checks: Unattached volume detection

3. **Snapshots** (Storage)
   - Type: `ResourceType.SNAPSHOT`
   - Checks: Old snapshot detection

4. **SQL Databases** (Database)
   - Type: `ResourceType.DATABASE`
   - Checks: Database right-sizing based on CPU/memory utilization

## ❌ Not Yet Supported Azure Resources

### Compute Services
- **App Services** - Web apps, API apps, mobile backends
- **Azure Functions** - Serverless compute
- **Container Instances** - Docker containers
- **Azure Kubernetes Service (AKS)** - Managed Kubernetes
- **Virtual Machine Scale Sets** - Auto-scaling VM groups
- **Azure Batch** - Large-scale parallel compute

### Database Services  
- **Cosmos DB** - Globally distributed NoSQL database
- **Azure Database for PostgreSQL**
- **Azure Database for MySQL**
- **Azure Database for MariaDB**
- **Azure Cache for Redis**
- **Azure Synapse Analytics** (formerly SQL Data Warehouse)

### Storage Services
- **Storage Accounts** - Blob, File, Queue, Table storage
- **Azure Files** - Managed file shares
- **Azure NetApp Files** - Enterprise file storage
- **StorSimple** - Hybrid cloud storage

### Networking
- **Load Balancers**
- **Application Gateways** 
- **Virtual Network Gateways** (VPN)
- **ExpressRoute** circuits
- **Public IP Addresses**
- **Network Security Groups**
- **Azure Firewall**
- **Azure Front Door**
- **CDN Profiles**

### Integration & Messaging
- **Service Bus** - Message queues and topics
- **Event Hubs** - Big data streaming
- **Event Grid** - Event routing service
- **Logic Apps** - Workflow automation
- **API Management**

### Analytics & AI
- **Azure Databricks**
- **HDInsight** - Hadoop/Spark clusters
- **Stream Analytics**
- **Data Factory** - ETL/ELT pipelines
- **Machine Learning** workspaces
- **Cognitive Services**

### Other Key Services
- **SignalR Service** - Real-time messaging
- **Notification Hubs** - Push notifications
- **IoT Hub** - IoT device management
- **Media Services** - Video streaming
- **Azure DevOps** - CI/CD pipelines
- **Key Vault** - Secrets management
- **Application Insights** - APM
- **Log Analytics Workspaces**

## Implementation Recommendations

### High Priority Additions
1. **Cosmos DB** - Often misconfigured with high RU/s
2. **Storage Accounts** - Unused blob containers, wrong access tiers
3. **App Services** - Over-provisioned plans
4. **AKS** - Idle node pools
5. **Public IPs** - Unattached static IPs

### Potential Checks for New Resources

#### Cosmos DB
- RU/s utilization vs provisioned
- Unused containers
- Cross-region replication costs
- Backup policy optimization

#### Storage Accounts
- Blob lifecycle management
- Hot/Cool/Archive tier optimization
- Unused containers
- Cross-region replication

#### App Services
- Plan utilization (CPU/Memory)
- Scaling recommendations
- Unused deployment slots
- Always-on settings for low-traffic apps

#### SignalR Service
- Unit utilization
- Message quota usage
- Scaling tier optimization

## Code Structure for New Resources

To add support for a new resource type:

1. Add to `ResourceType` enum in `models/base.py`
2. Implement discovery in `AzureProvider.list_resources()`
3. Create new check classes for resource-specific optimizations
4. Add cost estimation logic
5. Implement metrics collection where applicable

Example for Cosmos DB:
```python
# In ResourceType enum
COSMOS_DB = "cosmos_db"

# In AzureProvider.list_resources()
if not resource_types or ResourceType.COSMOS_DB in resource_types:
    cosmos_client = CosmosDBManagementClient(self._credential, self._subscription_id)
    for account in cosmos_client.database_accounts.list():
        # Create Resource object with cost estimation
        pass
```