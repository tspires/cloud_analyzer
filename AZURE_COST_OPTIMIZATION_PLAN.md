# Azure Cost Optimization CLI - Prompt Plan

## Overview
This document outlines the implementation plan for an Azure CLI tool that discovers all resources in an Azure tenant, collects utilization metrics, and stores them in a PostgreSQL database for cost optimization analysis.

## Goals
1. Automatically discover all resources across an Azure tenant
2. Collect utilization metrics for each resource type
3. Store metrics in PostgreSQL for historical analysis
4. Identify cost optimization opportunities based on utilization patterns

## Phase 1: Resource Discovery

### 1.1 Authentication & Setup
- Use Azure SDK for Python (azure-mgmt-resource)
- Implement service principal authentication
- Support for multiple subscriptions within a tenant

### 1.2 Resource Discovery Strategy
```python
# Discover all resource types across subscriptions
resource_types = [
    'Microsoft.Compute/virtualMachines',
    'Microsoft.Compute/virtualMachineScaleSets',
    'Microsoft.Compute/disks',
    'Microsoft.Storage/storageAccounts',
    'Microsoft.Sql/servers/databases',
    'Microsoft.Sql/servers/elasticPools',
    'Microsoft.DBforPostgreSQL/servers',
    'Microsoft.DBforMySQL/servers',
    'Microsoft.DocumentDB/databaseAccounts',
    'Microsoft.Cache/Redis',
    'Microsoft.Web/sites',
    'Microsoft.Web/serverFarms',
    'Microsoft.ContainerService/managedClusters',
    'Microsoft.ContainerInstance/containerGroups',
    'Microsoft.Network/applicationGateways',
    'Microsoft.Network/loadBalancers',
    'Microsoft.Network/publicIPAddresses',
    'Microsoft.Network/virtualNetworkGateways',
    'Microsoft.KeyVault/vaults',
    'Microsoft.EventHub/namespaces',
    'Microsoft.ServiceBus/namespaces',
    'Microsoft.Logic/workflows',
    'Microsoft.DataFactory/factories',
    'Microsoft.Synapse/workspaces',
    'Microsoft.CognitiveServices/accounts'
]
```

### 1.3 Resource Enumeration
- Use Azure Resource Graph for efficient querying
- Batch queries to handle large environments
- Capture resource metadata (tags, location, resource group)

## Phase 2: Metrics Collection

### 2.1 Metrics by Resource Type

#### Virtual Machines
- CPU Percentage (avg, max, p95)
- Available Memory Bytes
- Disk Read/Write Operations/Sec
- Network In/Out
- OS Disk Queue Depth

#### Storage Accounts
- Used Capacity
- Transactions
- Ingress/Egress
- Availability
- Success E2E Latency

#### SQL Databases
- DTU Percentage
- CPU Percentage
- Data IO Percentage
- Log IO Percentage
- Storage Percentage
- Connection Count

#### App Services
- CPU Percentage
- Memory Percentage
- Http Queue Length
- Response Time
- Request Count

#### AKS Clusters
- Node CPU Utilization
- Node Memory Utilization
- Pod Count
- Node Count

### 2.2 Metrics Collection Strategy
```python
# Time ranges for analysis
time_ranges = {
    'real_time': '5 minutes',
    'hourly': '1 hour',
    'daily': '24 hours',
    'weekly': '7 days',
    'monthly': '30 days'
}

# Aggregation types
aggregations = ['Average', 'Maximum', 'Minimum', 'Total', 'Count']
```

### 2.3 Azure Monitor Integration
- Use Azure Monitor Metrics API
- Implement retry logic for API limits
- Batch metric queries for efficiency

## Phase 3: Database Design

### 3.1 PostgreSQL Schema

```sql
-- Resources table
CREATE TABLE resources (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    resource_id TEXT NOT NULL UNIQUE,
    subscription_id TEXT NOT NULL,
    resource_group TEXT NOT NULL,
    resource_name TEXT NOT NULL,
    resource_type TEXT NOT NULL,
    location TEXT NOT NULL,
    tags JSONB,
    sku JSONB,
    properties JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Metrics metadata
CREATE TABLE metric_definitions (
    id SERIAL PRIMARY KEY,
    resource_type TEXT NOT NULL,
    metric_name TEXT NOT NULL,
    unit TEXT NOT NULL,
    aggregation_type TEXT NOT NULL,
    UNIQUE(resource_type, metric_name, aggregation_type)
);

-- Metrics data (partitioned by month)
CREATE TABLE metrics (
    id BIGSERIAL,
    resource_id TEXT NOT NULL,
    metric_definition_id INTEGER NOT NULL,
    timestamp TIMESTAMP NOT NULL,
    value DOUBLE PRECISION NOT NULL,
    time_grain TEXT NOT NULL,
    PRIMARY KEY (timestamp, resource_id, metric_definition_id)
) PARTITION BY RANGE (timestamp);

-- Cost data
CREATE TABLE resource_costs (
    id BIGSERIAL PRIMARY KEY,
    resource_id TEXT NOT NULL,
    billing_period DATE NOT NULL,
    cost DECIMAL(10, 2) NOT NULL,
    currency TEXT DEFAULT 'USD',
    usage_quantity DECIMAL(20, 6),
    usage_unit TEXT,
    meter_name TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Optimization recommendations
CREATE TABLE recommendations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    resource_id TEXT NOT NULL,
    recommendation_type TEXT NOT NULL,
    description TEXT NOT NULL,
    potential_savings DECIMAL(10, 2),
    confidence_score DECIMAL(3, 2),
    metrics_analyzed JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status TEXT DEFAULT 'active'
);

-- Indexes for performance
CREATE INDEX idx_resources_type ON resources(resource_type);
CREATE INDEX idx_resources_subscription ON resources(subscription_id);
CREATE INDEX idx_metrics_resource_timestamp ON metrics(resource_id, timestamp DESC);
CREATE INDEX idx_metrics_timestamp ON metrics(timestamp DESC);
CREATE INDEX idx_recommendations_resource ON recommendations(resource_id);
CREATE INDEX idx_recommendations_status ON recommendations(status);
```

### 3.2 Data Retention Strategy
- Raw metrics: 90 days
- Hourly aggregates: 1 year
- Daily aggregates: 3 years
- Monthly aggregates: Indefinite

## Phase 4: Implementation Architecture

### 4.1 Component Architecture
```
┌─────────────────────┐
│   Azure Tenant      │
│  (Multiple Subs)    │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  Resource Discovery │
│    Component        │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  Metrics Collector  │
│  (Azure Monitor)    │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│   Data Processor    │
│  (Aggregation)      │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  PostgreSQL DB      │
│  (TimescaleDB)      │
└─────────────────────┘
```

### 4.2 Key Python Libraries
```python
# Core dependencies
dependencies = {
    'azure-identity': 'Authentication',
    'azure-mgmt-resource': 'Resource management',
    'azure-mgmt-monitor': 'Metrics collection',
    'azure-mgmt-consumption': 'Cost data',
    'azure-mgmt-advisor': 'Azure Advisor integration',
    'psycopg2-binary': 'PostgreSQL connection',
    'sqlalchemy': 'ORM for database operations',
    'pandas': 'Data processing',
    'asyncio': 'Async operations',
    'aiohttp': 'Async HTTP requests',
    'click': 'CLI framework',
    'python-dotenv': 'Environment configuration'
}
```

## Phase 5: Cost Optimization Analysis

### 5.1 Optimization Rules

#### Compute Optimization
- **Idle VMs**: CPU < 5% for 7+ days
- **Oversized VMs**: CPU < 20% and Memory < 30% for 14+ days
- **Stopped VMs**: VMs stopped but not deallocated
- **Orphaned Disks**: Unattached managed disks

#### Storage Optimization
- **Cold Storage**: Blobs not accessed for 30+ days
- **Duplicate Snapshots**: Multiple snapshots of same disk
- **Oversized Premium Storage**: Low IOPS on premium disks

#### Database Optimization
- **Idle Databases**: Low DTU/vCore usage
- **Backup Retention**: Excessive backup retention
- **Elastic Pool Candidates**: Multiple DBs with complementary usage

#### Network Optimization
- **Idle Load Balancers**: No backend pools or traffic
- **Unused Public IPs**: Unassociated public IPs
- **Idle VPN Gateways**: No connections or traffic

### 5.2 Recommendation Engine
```python
class RecommendationEngine:
    def analyze_vm_utilization(self, metrics):
        # Analyze CPU, memory, disk metrics
        # Generate rightsizing recommendations
        pass
    
    def analyze_storage_patterns(self, metrics):
        # Analyze access patterns
        # Recommend tier changes
        pass
    
    def analyze_database_usage(self, metrics):
        # Analyze DTU/vCore utilization
        # Recommend scaling options
        pass
```

## Phase 6: CLI Interface

### 6.1 Command Structure
```bash
# Discovery commands
azure-cost-optimizer discover --subscription-id <id>
azure-cost-optimizer discover --all-subscriptions

# Metrics collection
azure-cost-optimizer collect-metrics --resource-type <type>
azure-cost-optimizer collect-metrics --all --days 30

# Analysis commands
azure-cost-optimizer analyze --resource-id <id>
azure-cost-optimizer analyze --resource-group <rg>
azure-cost-optimizer analyze --optimization-type <type>

# Reporting commands
azure-cost-optimizer report --format json
azure-cost-optimizer report --format csv --output report.csv
azure-cost-optimizer report --top-opportunities 10

# Database management
azure-cost-optimizer db init
azure-cost-optimizer db migrate
azure-cost-optimizer db cleanup --older-than 90d
```

### 6.2 Configuration File
```yaml
# config.yaml
azure:
  tenant_id: ${AZURE_TENANT_ID}
  client_id: ${AZURE_CLIENT_ID}
  client_secret: ${AZURE_CLIENT_SECRET}
  subscriptions:
    - id: sub1
      name: Production
    - id: sub2
      name: Development

database:
  host: ${DB_HOST}
  port: 5432
  name: azure_metrics
  user: ${DB_USER}
  password: ${DB_PASSWORD}
  
metrics:
  collection_interval: 300  # seconds
  retention_days: 90
  aggregation_intervals:
    - 1h
    - 1d
    - 1w
    - 1m

optimization:
  thresholds:
    vm_idle_cpu: 5
    vm_idle_days: 7
    vm_oversized_cpu: 20
    vm_oversized_memory: 30
    storage_cold_days: 30
```

## Phase 7: Monitoring & Alerting

### 7.1 Application Metrics
- Collection success rate
- API rate limit tracking
- Database performance metrics
- Recommendation generation rate

### 7.2 Alerting Rules
- Failed collections
- Database connection issues
- High potential savings detected
- Resource quota warnings

## Phase 8: Security Considerations

### 8.1 Authentication
- Service Principal with least privilege
- Managed Identity support for Azure VMs
- Key Vault integration for secrets

### 8.2 Data Security
- Encryption at rest for PostgreSQL
- TLS for all connections
- Row-level security for multi-tenant scenarios
- Audit logging for all operations

## Implementation Timeline

### Week 1-2: Foundation
- Set up project structure
- Implement authentication
- Create database schema
- Basic resource discovery

### Week 3-4: Metrics Collection
- Implement metrics collectors
- Test with core resource types
- Database write operations
- Error handling

### Week 5-6: Analysis Engine
- Implement optimization rules
- Create recommendation engine
- Test recommendation accuracy
- Performance optimization

### Week 7-8: CLI & Reporting
- Build CLI interface
- Implement reporting formats
- Add configuration management
- Documentation

### Week 9-10: Testing & Deployment
- Integration testing
- Performance testing
- Security review
- Deployment automation

## Success Metrics
- Resource discovery coverage: >95%
- Metrics collection reliability: >99%
- Recommendation accuracy: >80%
- Cost savings identified: >20% of spend
- Query performance: <1s for common queries