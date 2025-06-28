# Flywheel Prompt Plans for Cloud Cost Optimization

## Overview

This repository contains flywheel-compatible prompt plans for comprehensive cloud cost optimization analysis across AWS, Azure, and GCP.

## Available Plans

### 1. Main Optimization Plan
**File**: `flywheel_prompt_plan.yaml`
**Purpose**: Comprehensive analysis of core cloud services
**Services Covered**:
- Compute instances (EC2, VMs, GCE)
- Storage volumes (EBS, Managed Disks, Persistent Disks)  
- Snapshots
- Databases (RDS, SQL Database, Cloud SQL)
- Reserved Instances/Commitments

### 2. Specialized Plans

#### Cosmos DB Optimization
**File**: `flywheel_specialized_plans/cosmos_db_optimization.yaml`
**Purpose**: Deep analysis of Azure Cosmos DB costs
**Focus Areas**:
- RU/s utilization analysis
- Consistency level optimization
- Regional deployment optimization
- Serverless vs provisioned recommendations

#### Container Services Optimization  
**File**: `flywheel_specialized_plans/container_optimization.yaml`
**Purpose**: Optimize container clusters (EKS, AKS, GKE)
**Focus Areas**:
- Node pool right-sizing
- Workload resource optimization
- Spot/preemptible instance usage
- Autoscaling configuration

#### Multi-Cloud Storage Optimization
**File**: `flywheel_specialized_plans/multi_cloud_storage.yaml`  
**Purpose**: Optimize object storage across S3, Blob, and GCS
**Focus Areas**:
- Lifecycle policy optimization
- Storage class transitions
- Access pattern analysis
- Cross-region optimization

## Usage

### Basic Execution

```bash
# Run the main optimization plan for AWS
flywheel run flywheel_prompt_plan.yaml \
  -v cloud_provider=aws \
  -v region=us-east-1 \
  -v days_to_analyze=30

# Run for Azure
flywheel run flywheel_prompt_plan.yaml \
  -v cloud_provider=azure \
  -v region=eastus \
  -v days_to_analyze=30

# Run for GCP
flywheel run flywheel_prompt_plan.yaml \
  -v cloud_provider=gcp \
  -v region=us-central1 \
  -v days_to_analyze=30
```

### Specialized Plans

```bash
# Cosmos DB optimization
flywheel run flywheel_specialized_plans/cosmos_db_optimization.yaml \
  -v subscription_id=YOUR_SUBSCRIPTION_ID \
  -v resource_group=YOUR_RG \
  -v days_to_analyze=30

# Container optimization for EKS
flywheel run flywheel_specialized_plans/container_optimization.yaml \
  -v cloud_provider=aws \
  -v cluster_name=my-eks-cluster \
  -v namespace=production

# Storage optimization  
flywheel run flywheel_specialized_plans/multi_cloud_storage.yaml \
  -v analyze_lifecycle=true \
  -v analyze_access_patterns=true \
  -v days_to_analyze=90
```

### Advanced Options

```bash
# Use a specific Claude model
flywheel run flywheel_prompt_plan.yaml \
  -m claude-3-opus-20240229 \
  -v cloud_provider=aws

# Save output to file
flywheel run flywheel_prompt_plan.yaml \
  -v cloud_provider=azure \
  -o optimization_report_$(date +%Y%m%d).json

# Increase token limit for detailed analysis
flywheel run flywheel_prompt_plan.yaml \
  -t 8192 \
  -v cloud_provider=gcp
```

## Variables

### Main Plan Variables
- `cloud_provider`: aws, azure, or gcp
- `region`: Cloud region to analyze
- `days_to_analyze`: Historical period for metrics (default: 30)

### Cosmos DB Variables
- `subscription_id`: Azure subscription ID
- `resource_group`: Resource group name
- `days_to_analyze`: Metric analysis period

### Container Variables
- `cloud_provider`: aws, azure, or gcp
- `cluster_name`: Kubernetes cluster name
- `namespace`: Kubernetes namespace (default: default)

### Storage Variables
- `analyze_lifecycle`: Include lifecycle analysis (true/false)
- `analyze_access_patterns`: Include access pattern analysis (true/false)
- `days_to_analyze`: Historical period for access analysis

## Output Structure

Each plan generates structured outputs that can be saved and processed:

```json
{
  "compute_analysis": "Detailed compute findings...",
  "storage_analysis": "Storage optimization opportunities...",
  "optimization_report": "Comprehensive markdown report...",
  "implementation_scripts": "Ready-to-run CLI commands..."
}
```

## Prerequisites

1. **Cloud CLI Tools**: Ensure you have the appropriate CLI tools installed:
   - AWS: `aws cli`
   - Azure: `az cli`  
   - GCP: `gcloud`

2. **Authentication**: Be authenticated to your cloud provider:
   ```bash
   # AWS
   aws configure
   
   # Azure
   az login
   
   # GCP
   gcloud auth login
   ```

3. **Permissions**: Ensure you have read access to:
   - Compute resources
   - Storage resources
   - Billing/cost data
   - CloudWatch/Monitor metrics

## Best Practices

1. **Start Small**: Test on a single region or resource group first
2. **Review Output**: Always review recommendations before implementing
3. **Test Changes**: Use dev/test environments to validate optimizations
4. **Track Savings**: Monitor actual vs projected savings
5. **Iterate**: Run monthly to identify new optimization opportunities

## Extending the Plans

To add new services or checks:

1. Add new steps to existing plans
2. Create specialized plans for complex services
3. Use the `saveOutput` feature to chain analyses
4. Include specific CLI commands for accuracy

## Integration with Cloud Analyzer

These flywheel plans complement the Cloud Analyzer codebase by:
1. Providing analysis for services not yet implemented
2. Offering interactive, step-by-step optimization workflows
3. Generating implementation scripts automatically
4. Creating monitoring plans for tracking savings

## Troubleshooting

1. **API Key Issues**: Set `ANTHROPIC_API_KEY` environment variable
2. **CLI Not Found**: Ensure cloud CLI tools are in your PATH
3. **Permission Errors**: Check cloud IAM permissions
4. **Rate Limits**: Add delays between API calls if needed

## Contributing

To contribute new optimization plans:
1. Follow the existing YAML structure
2. Include comprehensive CLI commands
3. Add clear descriptions for each step
4. Test with `flywheel validate`
5. Document new variables and usage