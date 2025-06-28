# Cloud Cost Optimization Checks

## Overview
This document contains all cloud cost optimization checks implemented by the Cloud Cost Efficiency Analyzer, ranked by potential impact and likelihood of savings.

## 🔴 Critical Impact Checks (40-90% savings)

### 1. Dev/Test Running 24/7
- **Potential Savings**: 65-75%
- **Frequency**: 80% of organizations
- **Effort**: Low
- **Description**: Non-production environments running during nights and weekends
- **Fix**: Implement automated scheduling for shutdown/startup

### 2. Databricks/EMR Cluster Waste
- **Potential Savings**: 60-80%
- **Frequency**: 70% of organizations
- **Effort**: Low
- **Description**: Clusters running without auto-termination, oversized, or using on-demand instead of spot
- **Fix**: Set 10-minute auto-termination, use spot instances, right-size clusters

### 3. Log Over-retention
- **Potential Savings**: 70-90%
- **Frequency**: 90% of organizations
- **Effort**: Low
- **Description**: Debug logs retained for months, all logs kept forever
- **Fix**: Implement tiered retention (7 days debug, 30 days info, 90 days error)

### 4. Data Pipeline Over-frequency
- **Potential Savings**: 50-90%
- **Frequency**: 80% of data pipelines
- **Effort**: Medium
- **Description**: ETL/data pipelines running hourly when daily would suffice
- **Fix**: Analyze actual data freshness requirements, reduce frequency

### 5. Idle/Zombie Resources
- **Potential Savings**: 100%
- **Frequency**: 70% of organizations
- **Effort**: Low
- **Description**: Stopped VMs still billing, unused databases, idle load balancers
- **Fix**: Terminate or deallocate unused resources

## 🟠 High Impact Checks (30-50% savings)

### 6. Spot Instance Underutilization
- **Potential Savings**: 50-90%
- **Frequency**: 85% miss opportunities
- **Effort**: Medium
- **Description**: Batch jobs, dev environments, scaling capacity on on-demand
- **Fix**: Implement spot instances for suitable workloads

### 7. Verbose Production Logging
- **Potential Savings**: 50-80%
- **Frequency**: 85% of organizations
- **Effort**: Low
- **Description**: DEBUG level in production, no log sampling
- **Fix**: Set appropriate log levels, implement sampling

### 8. Unattached Storage Volumes
- **Potential Savings**: 100%
- **Frequency**: 60% of organizations
- **Effort**: Low
- **Description**: EBS volumes, managed disks, persistent disks not attached
- **Fix**: Delete orphaned volumes

### 9. Right-sizing Overprovisioned Instances
- **Potential Savings**: 30-50%
- **Frequency**: 75% of instances
- **Effort**: Medium
- **Description**: CPU/memory utilization under 20-30%
- **Fix**: Downsize to appropriate instance types

### 10. Data Warehouse Oversizing
- **Potential Savings**: 50-70%
- **Frequency**: 60% of organizations
- **Effort**: Medium
- **Description**: Snowflake XL for Small workloads, Redshift always running
- **Fix**: Right-size, implement auto-suspend/resume

## 🟡 Medium Impact Checks (20-40% savings)

### 11. APM/Metrics Over-collection
- **Potential Savings**: 40-60%
- **Frequency**: 70% of organizations
- **Effort**: Low
- **Description**: Every request traced, high-cardinality metrics
- **Fix**: Implement sampling, reduce metric dimensions

### 12. Storage Class Optimization
- **Potential Savings**: 50-80%
- **Frequency**: 60% of organizations
- **Effort**: Low
- **Description**: Old data in hot storage tiers
- **Fix**: Implement lifecycle policies

### 13. Container/Kubernetes Overprovisioning
- **Potential Savings**: 30-50%
- **Frequency**: 70% of organizations
- **Effort**: Medium
- **Description**: Requested resources far exceed actual usage
- **Fix**: Analyze actual usage, implement VPA/HPA

### 14. Database License Migration
- **Potential Savings**: $7-47K per core/year
- **Frequency**: 30% of organizations
- **Effort**: High
- **Description**: SQL Server, Oracle licenses
- **Fix**: Migrate to PostgreSQL/MySQL

### 15. Reserved Instances/Savings Plans
- **Potential Savings**: 20-40%
- **Frequency**: 50% underutilized
- **Effort**: Low
- **Description**: Stable workloads on on-demand pricing
- **Fix**: Purchase appropriate commitments

## 🟢 Lower Impact Checks (5-20% savings)

### 16. Previous Generation Instances
- **Potential Savings**: 20-30%
- **Frequency**: 40% of organizations
- **Effort**: Medium
- **Description**: Running m4, c4 instead of m5, c5
- **Fix**: Upgrade to current generation

### 17. Snapshot/Backup Over-retention
- **Potential Savings**: 30-60%
- **Frequency**: 80% of organizations
- **Effort**: Low
- **Description**: Years of snapshots, redundant backups
- **Fix**: Implement retention policies

### 18. VPC Flow Logs/Network Logs
- **Potential Savings**: 60-80%
- **Frequency**: 50% of organizations
- **Effort**: Low
- **Description**: Logging all accepted traffic
- **Fix**: Log only rejected/suspicious traffic

### 19. Multi-AZ for Non-Critical
- **Potential Savings**: 50%
- **Frequency**: 40% of organizations
- **Effort**: Medium
- **Description**: Dev/test with unnecessary HA
- **Fix**: Single AZ for non-critical workloads

### 20. Container Registry Cleanup
- **Potential Savings**: 60-80%
- **Frequency**: 70% of organizations
- **Effort**: Low
- **Description**: Every build version retained forever
- **Fix**: Lifecycle policies, keep last 10-20 images

## Multi-Cloud Specific Checks

### AWS Specific
- **Unused Elastic IPs**: $3.60/month each
- **NAT Gateway Optimization**: $45/month + data processing
- **S3 Request Optimization**: Batch small files
- **EBS GP2 to GP3**: 20% savings, better performance
- **Lambda Memory Optimization**: 10-30% savings

### Azure Specific
- **Stopped VMs Still Billing**: Deallocate vs stop
- **Azure Hybrid Benefit**: Windows/SQL licensing
- **Blob Access Tiers**: Hot/Cool/Archive optimization
- **Reserved VM Instances**: 1 or 3 year commitments

### GCP Specific
- **Sustained Use Discounts**: Automatic but verify
- **Committed Use Discounts**: Predictable workloads
- **Preemptible VMs**: 80% savings for batch
- **Cloud Storage Classes**: Multi-regional vs regional

## Quick Win Priority List

### Week 1 (Immediate Impact)
1. Set log retention policies
2. Schedule dev/test shutdown
3. Delete unattached volumes
4. Set production log levels to INFO
5. Clean container registries
6. Terminate idle resources
7. Implement S3 lifecycle policies

### Week 2 (Medium Effort)
1. Enable Databricks auto-termination
2. Implement spot instances for batch
3. Right-size data warehouses
4. Reduce pipeline frequency
5. Optimize APM sampling

### Month 1 (Strategic)
1. Purchase Reserved Instances
2. Implement comprehensive tagging
3. Migrate to current gen instances
4. Evaluate database migrations
5. Optimize data transfer patterns

## Detection Queries

### AWS
```sql
-- Find idle EC2 instances
SELECT instance_id, instance_type, launch_time
FROM ec2_instances
WHERE cpu_utilization < 5 
  AND network_in < 1000000
  AND state = 'running'
  AND launch_time < NOW() - INTERVAL '7 days'
```

### Databricks
```sql
-- Find clusters without auto-termination
SELECT cluster_id, cluster_name, autotermination_minutes
FROM clusters
WHERE autotermination_minutes = 0 
   OR autotermination_minutes > 120
```

### CloudWatch Logs
```bash
# Find large log groups
aws logs describe-log-groups \
  --query 'logGroups[?storedBytes > `1073741824`].[logGroupName, storedBytes]' \
  --output table
```

## Expected Savings by Category

- **Logging/Telemetry**: 25-40% of total bill
- **Compute**: 20-30% of total bill  
- **Storage**: 15-25% of total bill
- **Database**: 10-20% of total bill
- **Network**: 5-10% of total bill
- **Analytics/Big Data**: 20-40% of analytics spend

## Red Flags

1. **Logging costs > Compute costs**: Major logging problem
2. **Databricks > 30% of cloud bill**: Cluster management issues
3. **Zero spot instances**: Missing major savings opportunity
4. **No Reserved Instances**: Overpaying for stable workloads
5. **Storage growing faster than compute**: Data retention issues

## Implementation Notes

- Focus on top 10 checks for 80% of potential savings
- Automate detection and alerting for continuous optimization
- Track savings monthly to demonstrate ROI
- Consider effort vs reward for prioritization
- Start with quick wins to build momentum