# Cloud Cost Optimization Analysis Prompt Plan

## Overview
This document provides detailed prompts for implementing cost optimization analysis for each cloud service across AWS, Azure, and GCP using their respective CLI tools.

## Currently Supported Services

### 1. Virtual Machines / Compute Instances

**AWS EC2**
```bash
# Get instance utilization metrics
aws cloudwatch get-metric-statistics \
  --namespace AWS/EC2 \
  --metric-name CPUUtilization \
  --dimensions Name=InstanceId,Value=i-1234567890abcdef0 \
  --statistics Average,Maximum \
  --start-time 2024-01-01T00:00:00Z \
  --end-time 2024-01-08T00:00:00Z \
  --period 3600

# List all instances with pricing info
aws ec2 describe-instances \
  --query 'Reservations[*].Instances[*].[InstanceId,InstanceType,State.Name,LaunchTime,Tags]' \
  --output json

# Get instance recommendations
aws compute-optimizer get-ec2-instance-recommendations \
  --instance-arns arn:aws:ec2:region:account:instance/i-xxxxx
```

**Azure VMs**
```bash
# Get VM list with size and state
az vm list --query "[].{name:name, size:hardwareProfile.vmSize, state:powerState, location:location}" -o json

# Get CPU metrics
az monitor metrics list \
  --resource /subscriptions/{sub-id}/resourceGroups/{rg}/providers/Microsoft.Compute/virtualMachines/{vm-name} \
  --metric "Percentage CPU" \
  --aggregation Average Maximum \
  --interval PT1H \
  --start-time 2024-01-01 \
  --end-time 2024-01-08

# Get VM pricing
az vm list-skus --location eastus --size Standard_D --output table
```

**GCP Compute Engine**
```bash
# List instances with machine type
gcloud compute instances list --format="json(name,machineType,status,creationTimestamp)"

# Get CPU utilization
gcloud monitoring read \
  'compute.googleapis.com/instance/cpu/utilization' \
  --project=PROJECT_ID \
  --filter='resource.instance_id="INSTANCE_ID"' \
  --start-time='2024-01-01T00:00:00Z' \
  --end-time='2024-01-08T00:00:00Z'

# Get sizing recommendations
gcloud recommender recommendations list \
  --project=PROJECT_ID \
  --location=ZONE \
  --recommender=google.compute.instance.MachineTypeRecommender
```

### 2. Storage Volumes / Disks

**AWS EBS**
```bash
# List unattached volumes
aws ec2 describe-volumes \
  --filters "Name=status,Values=available" \
  --query 'Volumes[*].[VolumeId,Size,VolumeType,CreateTime,State]'

# Get volume metrics (requires CloudWatch agent)
aws cloudwatch get-metric-statistics \
  --namespace AWS/EBS \
  --metric-name VolumeReadOps \
  --dimensions Name=VolumeId,Value=vol-xxxxx \
  --statistics Sum \
  --start-time 2024-01-01T00:00:00Z \
  --end-time 2024-01-08T00:00:00Z
```

**Azure Managed Disks**
```bash
# List all disks with attachment status
az disk list --query "[].{name:name, size:diskSizeGb, state:diskState, attached:managedBy}" -o json

# Get disk metrics (IOPS)
az monitor metrics list \
  --resource /subscriptions/{sub-id}/resourceGroups/{rg}/providers/Microsoft.Compute/disks/{disk-name} \
  --metric "Composite Disk Read Operations/sec" \
  --aggregation Average
```

**GCP Persistent Disks**
```bash
# List unattached disks
gcloud compute disks list --filter="users:[]" --format="json(name,sizeGb,type,creationTimestamp)"

# Get disk utilization metrics
gcloud monitoring read \
  'compute.googleapis.com/instance/disk/read_ops_count' \
  --project=PROJECT_ID \
  --filter='resource.instance_id="INSTANCE_ID"'
```

### 3. Snapshots

**AWS Snapshots**
```bash
# List snapshots with age
aws ec2 describe-snapshots \
  --owner-ids self \
  --query 'Snapshots[*].[SnapshotId,StartTime,VolumeSize,Description,Tags]' \
  --output json

# Check AMI associations
aws ec2 describe-images \
  --owners self \
  --query 'Images[*].BlockDeviceMappings[*].Ebs.SnapshotId' \
  --output json
```

**Azure Snapshots**
```bash
# List all snapshots
az snapshot list --query "[].{name:name, size:diskSizeGb, created:timeCreated, source:creationData.sourceResourceId}" -o json
```

**GCP Snapshots**
```bash
# List snapshots with creation time
gcloud compute snapshots list --format="json(name,diskSizeGb,creationTimestamp,sourceDisk)"

# Check if snapshot is used by an image
gcloud compute images list --format="json(name,sourceSnapshot)"
```

### 4. Databases

**AWS RDS**
```bash
# List RDS instances
aws rds describe-db-instances \
  --query 'DBInstances[*].[DBInstanceIdentifier,DBInstanceClass,Engine,AllocatedStorage,DBInstanceStatus]'

# Get RDS metrics
aws cloudwatch get-metric-statistics \
  --namespace AWS/RDS \
  --metric-name CPUUtilization \
  --dimensions Name=DBInstanceIdentifier,Value=mydb-instance \
  --statistics Average,Maximum \
  --start-time 2024-01-01T00:00:00Z \
  --end-time 2024-01-08T00:00:00Z
```

**Azure SQL Database**
```bash
# List databases
az sql db list --server myserver --resource-group myrg \
  --query "[].{name:name, tier:currentServiceObjectiveName, size:maxSizeBytes}" -o json

# Get DTU/CPU metrics
az monitor metrics list \
  --resource /subscriptions/{sub-id}/resourceGroups/{rg}/providers/Microsoft.Sql/servers/{server}/databases/{db} \
  --metric "cpu_percent" "dtu_consumption_percent" \
  --aggregation Average Maximum
```

**GCP Cloud SQL**
```bash
# List instances
gcloud sql instances list --format="json(name,tier,diskSize,state)"

# Get CPU/Memory metrics
gcloud monitoring read \
  'cloudsql.googleapis.com/database/cpu/utilization' \
  --project=PROJECT_ID \
  --filter='resource.database_id="PROJECT_ID:INSTANCE_ID"'
```

### 5. Reserved Instances / Commitments

**AWS Reserved Instances**
```bash
# Get RI utilization
aws ce get-reservation-utilization \
  --time-period Start=2024-01-01,End=2024-01-31 \
  --granularity DAILY

# Get RI coverage
aws ce get-reservation-coverage \
  --time-period Start=2024-01-01,End=2024-01-31 \
  --granularity MONTHLY

# Get RI recommendations
aws ce get-reservation-purchase-recommendation \
  --service "Amazon Elastic Compute Cloud - Compute" \
  --account-scope PAYER
```

**Azure Reservations**
```bash
# List reservations
az reservations reservation list --query "[].{name:name, term:term, state:provisioningState, expiry:expiryDate}" -o json

# Get reservation utilization (via REST API)
az rest --method GET \
  --uri "https://management.azure.com/providers/Microsoft.Capacity/reservationorders/{order-id}/reservations/{reservation-id}/providers/Microsoft.Consumption/reservationSummaries?api-version=2021-10-01"
```

**GCP Committed Use Discounts**
```bash
# List commitments
gcloud compute commitments list --format="json(name,type,startTimestamp,endTimestamp,status)"

# Get commitment utilization (requires BigQuery export)
bq query --use_legacy_sql=false '
SELECT 
  commitment_name,
  SUM(usage_amount) as total_usage,
  SUM(commitment_amount) as total_commitment,
  (SUM(usage_amount) / SUM(commitment_amount)) * 100 as utilization_percent
FROM `PROJECT.DATASET.gcp_billing_export`
WHERE commitment_name IS NOT NULL
GROUP BY commitment_name'
```

## Services Not Yet Implemented

### 6. Object Storage

**AWS S3**
```bash
# List buckets with size
aws s3api list-buckets --query 'Buckets[*].[Name,CreationDate]'
aws cloudwatch get-metric-statistics \
  --namespace AWS/S3 \
  --metric-name BucketSizeBytes \
  --dimensions Name=BucketName,Value=my-bucket Name=StorageType,Value=StandardStorage \
  --statistics Average \
  --start-time 2024-01-01T00:00:00Z \
  --end-time 2024-01-08T00:00:00Z

# Get lifecycle policies
aws s3api get-bucket-lifecycle-configuration --bucket my-bucket

# Get storage class distribution
aws s3api list-objects-v2 --bucket my-bucket --query 'Contents[*].StorageClass' | sort | uniq -c
```

**Azure Blob Storage**
```bash
# List storage accounts
az storage account list --query "[].{name:name, sku:sku.name, kind:kind}" -o json

# Get blob containers and size
az storage container list --account-name mystorageaccount --query "[].{name:name, properties:properties}" -o json

# Get metrics
az monitor metrics list \
  --resource /subscriptions/{sub-id}/resourceGroups/{rg}/providers/Microsoft.Storage/storageAccounts/{account} \
  --metric "UsedCapacity" \
  --aggregation Average
```

**GCP Cloud Storage**
```bash
# List buckets with storage class
gsutil ls -L -b | grep -E "StorageClass|TimeCreated"

# Get bucket size
gsutil du -s gs://bucket-name

# Get lifecycle rules
gsutil lifecycle get gs://bucket-name
```

### 7. Container Services

**AWS ECS/EKS**
```bash
# ECS: List clusters and services
aws ecs list-clusters
aws ecs list-services --cluster my-cluster
aws ecs describe-services --cluster my-cluster --services my-service \
  --query 'services[*].[serviceName,desiredCount,runningCount,launchType]'

# EKS: Get node utilization
kubectl top nodes
kubectl get nodes -o json | jq '.items[].status.allocatable'

# Get container insights
aws cloudwatch get-metric-statistics \
  --namespace ECS/ContainerInsights \
  --metric-name CpuUtilized \
  --dimensions Name=ClusterName,Value=my-cluster
```

**Azure Container Instances / AKS**
```bash
# AKS: List node pools
az aks nodepool list --cluster-name myAKSCluster --resource-group myRG \
  --query "[].{name:name, count:count, vmSize:vmSize}" -o json

# Get node metrics
kubectl top nodes

# Container Instances
az container list --query "[].{name:name, cpu:containers[0].resources.requests.cpu, memory:containers[0].resources.requests.memoryInGb}" -o json
```

**GCP GKE / Cloud Run**
```bash
# GKE: List node pools
gcloud container node-pools list --cluster=my-cluster --zone=us-central1-a

# Get node utilization
kubectl top nodes

# Cloud Run services
gcloud run services list --format="json(metadata.name,spec.template.spec.containers[0].resources)"
```

### 8. Serverless Functions

**AWS Lambda**
```bash
# List functions with memory and timeout
aws lambda list-functions --query 'Functions[*].[FunctionName,MemorySize,Timeout,CodeSize]'

# Get invocation metrics
aws cloudwatch get-metric-statistics \
  --namespace AWS/Lambda \
  --metric-name Invocations \
  --dimensions Name=FunctionName,Value=my-function \
  --statistics Sum

# Get cost allocation
aws ce get-cost-and-usage \
  --time-period Start=2024-01-01,End=2024-01-31 \
  --granularity MONTHLY \
  --filter '{"Dimensions":{"Key":"SERVICE","Values":["Lambda"]}}'
```

**Azure Functions**
```bash
# List function apps
az functionapp list --query "[].{name:name, plan:appServicePlanId, state:state}" -o json

# Get execution count
az monitor metrics list \
  --resource /subscriptions/{sub-id}/resourceGroups/{rg}/providers/Microsoft.Web/sites/{function-app} \
  --metric "FunctionExecutionCount" \
  --aggregation Total
```

**GCP Cloud Functions**
```bash
# List functions
gcloud functions list --format="json(name,availableMemoryMb,timeout,status)"

# Get invocation metrics
gcloud monitoring read \
  'cloudfunctions.googleapis.com/function/execution_count' \
  --project=PROJECT_ID \
  --filter='resource.function_name="FUNCTION_NAME"'
```

### 9. Load Balancers

**AWS ELB/ALB/NLB**
```bash
# List load balancers
aws elbv2 describe-load-balancers \
  --query 'LoadBalancers[*].[LoadBalancerName,Type,State.Code,CreatedTime]'

# Get request count
aws cloudwatch get-metric-statistics \
  --namespace AWS/ApplicationELB \
  --metric-name RequestCount \
  --dimensions Name=LoadBalancer,Value=app/my-load-balancer/50dc6c495c0c9188 \
  --statistics Sum

# Check target health
aws elbv2 describe-target-health --target-group-arn arn:aws:elasticloadbalancing:...
```

**Azure Load Balancer / Application Gateway**
```bash
# List load balancers
az network lb list --query "[].{name:name, sku:sku.name, location:location}" -o json

# Application Gateway
az network application-gateway list --query "[].{name:name, tier:sku.tier, capacity:sku.capacity}" -o json

# Get metrics
az monitor metrics list \
  --resource /subscriptions/{sub-id}/resourceGroups/{rg}/providers/Microsoft.Network/loadBalancers/{lb-name} \
  --metric "ByteCount" \
  --aggregation Total
```

**GCP Load Balancers**
```bash
# List forwarding rules (LB frontend)
gcloud compute forwarding-rules list --format="json(name,loadBalancingScheme,target)"

# Get request count metrics
gcloud monitoring read \
  'loadbalancing.googleapis.com/https/request_count' \
  --project=PROJECT_ID \
  --filter='resource.forwarding_rule_name="RULE_NAME"'
```

### 10. Databases (NoSQL)

**AWS DynamoDB**
```bash
# List tables with billing mode
aws dynamodb list-tables | xargs -I {} aws dynamodb describe-table --table-name {} \
  --query 'Table.[TableName,BillingModeSummary.BillingMode,ProvisionedThroughput]'

# Get consumed capacity
aws cloudwatch get-metric-statistics \
  --namespace AWS/DynamoDB \
  --metric-name ConsumedReadCapacityUnits \
  --dimensions Name=TableName,Value=my-table \
  --statistics Sum,Average
```

**Azure Cosmos DB**
```bash
# List Cosmos DB accounts
az cosmosdb list --query "[].{name:name, kind:kind, locations:locations[0].locationName}" -o json

# Get RU consumption
az monitor metrics list \
  --resource /subscriptions/{sub-id}/resourceGroups/{rg}/providers/Microsoft.DocumentDB/databaseAccounts/{account} \
  --metric "TotalRequestUnits" \
  --aggregation Total
```

**GCP Firestore / Bigtable**
```bash
# Firestore: Get document reads/writes
gcloud monitoring read \
  'firestore.googleapis.com/document/read_count' \
  --project=PROJECT_ID

# Bigtable: List instances
gcloud bigtable instances list --format="json(name,nodeCount,storageType)"
```

### 11. Caching Services

**AWS ElastiCache**
```bash
# List cache clusters
aws elasticache describe-cache-clusters \
  --query 'CacheClusters[*].[CacheClusterId,CacheNodeType,Engine,NumCacheNodes,CacheClusterStatus]'

# Get CPU utilization
aws cloudwatch get-metric-statistics \
  --namespace AWS/ElastiCache \
  --metric-name CPUUtilization \
  --dimensions Name=CacheClusterId,Value=my-cache-cluster
```

**Azure Cache for Redis**
```bash
# List Redis caches
az redis list --query "[].{name:name, sku:sku.name, capacity:sku.capacity}" -o json

# Get cache metrics
az monitor metrics list \
  --resource /subscriptions/{sub-id}/resourceGroups/{rg}/providers/Microsoft.Cache/Redis/{cache-name} \
  --metric "percentProcessorTime" "usedmemorypercentage"
```

**GCP Memorystore**
```bash
# List Redis instances
gcloud redis instances list --format="json(name,tier,memorySizeGb,state)"

# Get metrics
gcloud monitoring read \
  'redis.googleapis.com/stats/cpu_utilization' \
  --project=PROJECT_ID \
  --filter='resource.instance_id="INSTANCE_ID"'
```

### 12. CDN Services

**AWS CloudFront**
```bash
# List distributions
aws cloudfront list-distributions \
  --query 'DistributionList.Items[*].[Id,DomainName,PriceClass,Enabled]'

# Get request metrics
aws cloudwatch get-metric-statistics \
  --namespace AWS/CloudFront \
  --metric-name Requests \
  --dimensions Name=DistributionId,Value=ABCDEFG123456 \
  --statistics Sum
```

**Azure CDN**
```bash
# List CDN profiles and endpoints
az cdn profile list --query "[].{name:name, sku:sku.name}" -o json
az cdn endpoint list --profile-name myprofile --resource-group myrg

# Get metrics
az monitor metrics list \
  --resource /subscriptions/{sub-id}/resourceGroups/{rg}/providers/Microsoft.Cdn/profiles/{profile}/endpoints/{endpoint} \
  --metric "ByteHitRatio" "RequestCount"
```

**GCP Cloud CDN**
```bash
# List backend services with CDN enabled
gcloud compute backend-services list --format="json(name,cdnPolicy.cacheMode,enableCDN)"

# Get cache hit ratio
gcloud monitoring read \
  'loadbalancing.googleapis.com/https/backend_latencies' \
  --project=PROJECT_ID \
  --filter='metric.cache_result="HIT"'
```

## Cost Optimization Analysis Framework

### General Approach for Each Service:

1. **Discovery Phase**
   ```bash
   # List all resources of the type
   # Get basic configuration and state
   # Identify creation time and tags
   ```

2. **Utilization Analysis**
   ```bash
   # Collect performance metrics (CPU, memory, requests, etc.)
   # Analyze patterns over 7-30 days
   # Identify peak vs average usage
   ```

3. **Cost Analysis**
   ```bash
   # Get current pricing/billing information
   # Calculate monthly/annual costs
   # Identify cost allocation tags
   ```

4. **Optimization Recommendations**
   ```bash
   # Compare utilization vs capacity
   # Identify rightsizing opportunities
   # Check for unused resources
   # Analyze commitment/reservation options
   ```

### Implementation Pattern:

```python
class ServiceOptimizationCheck:
    async def discover_resources(self):
        # Use CLI to list resources
        pass
    
    async def analyze_utilization(self, resource):
        # Use metrics APIs to get usage data
        pass
    
    async def calculate_savings(self, resource, utilization):
        # Compare current cost vs optimized cost
        pass
    
    async def generate_recommendations(self, resource, analysis):
        # Create specific action items
        pass
```

## Priority Implementation Order

Based on typical cloud spend patterns:

1. **Compute Instances** (30-40% of cloud spend)
2. **Databases** (20-30% of cloud spend)  
3. **Storage & Snapshots** (10-20% of cloud spend)
4. **Reserved Instances/Commitments** (savings opportunity)
5. **Load Balancers & Networking** (5-10% of cloud spend)
6. **Container Services** (growing spend category)
7. **Serverless & Functions** (usage-based optimization)
8. **CDN & Edge Services** (bandwidth costs)
9. **Caching Services** (memory optimization)
10. **Logging & Monitoring** (data retention costs)

## Notes

- Each service requires specific metrics and thresholds
- Consider cloud-native recommendation services (AWS Compute Optimizer, Azure Advisor, GCP Recommender)
- Account for service-specific pricing models (on-demand, reserved, spot, committed use)
- Include tag-based cost allocation analysis
- Consider multi-region and cross-AZ data transfer costs
- Account for service limits and quotas in recommendations