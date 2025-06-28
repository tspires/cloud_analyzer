# Cloud Cost Efficiency Analyzer

A comprehensive multi-cloud cost optimization platform that provides intelligent analysis and actionable recommendations for AWS, Azure, and Google Cloud Platform.

## Overview

Cloud Cost Efficiency Analyzer helps organizations optimize their cloud spending by providing:
- **Multi-Cloud Support**: Unified cost analysis across AWS, Azure, and GCP
- **Real-time Insights**: Up-to-date cost monitoring and anomaly detection
- **Actionable Recommendations**: AI-driven optimization suggestions with ROI calculations
- **Resource Efficiency**: Identify idle, underutilized, and oversized resources
- **Executive Reporting**: Comprehensive dashboards and customizable reports

## Documentation

- [Product Specification](./PRODUCT_SPEC.md) - Detailed product vision, features, and user journeys
- [Technical Specification](./TECHNICAL_SPEC.md) - Architecture, implementation details, and technical requirements

## Key Features

### 🔐 Secure Multi-Cloud Authentication
- AWS IAM roles and SSO integration
- Azure Service Principal authentication
- GCP Service Account support
- Encrypted credential storage with automatic rotation

### 📊 Advanced Cost Analysis
- Real-time cost monitoring with hourly updates
- Historical trend analysis and forecasting
- Tag-based cost allocation and chargeback
- Budget tracking with alerts

### 🎯 Intelligent Optimization
- Right-sizing recommendations based on actual usage
- Reserved Instance and Savings Plan optimization
- Idle resource detection and cleanup suggestions
- Automated cost anomaly detection

### 📈 Comprehensive Reporting
- Executive dashboards with KPIs
- Detailed cost breakdowns by service, team, or project
- Custom report builder with scheduling
- Export to PDF, CSV, or API integration

## Project Structure

```
cloud_analyzer/
├── common/                 # Shared library for checks and providers
│   └── src/
│       ├── models/        # Data models (resources, checks, etc.)
│       ├── providers/     # Cloud provider interfaces
│       ├── checks/        # Optimization check implementations
│       └── utils/         # Common utilities
├── cli/                   # Command-line interface
│   └── src/
│       ├── commands/      # CLI commands
│       ├── formatters/    # Output formatters
│       └── utils/         # CLI utilities
├── backend/               # API backend (future)
├── frontend/              # Web UI (future)
└── tests/                 # Test suites

```

## Getting Started

### Prerequisites

- Python 3.11 or higher
- Poetry for dependency management
- Cloud provider CLI tools (aws, az, gcloud) installed and configured

### Installation

1. Clone the repository:
```bash
git clone https://github.com/tspires/cloud_analyzer.git
cd cloud_analyzer
```

2. Install dependencies:
```bash
poetry install
```

3. Configure cloud providers:
```bash
poetry run cloud-analyzer configure --provider aws
poetry run cloud-analyzer configure --provider azure
poetry run cloud-analyzer configure --provider gcp
```

### Basic Usage

1. List available checks:
```bash
poetry run cloud-analyzer list-checks
```

2. Run analysis:
```bash
# Analyze all configured providers
poetry run cloud-analyzer analyze

# Analyze specific provider
poetry run cloud-analyzer analyze --provider aws

# Analyze specific region
poetry run cloud-analyzer analyze --provider aws --region us-east-1

# Filter by severity
poetry run cloud-analyzer analyze --severity high
```

3. Generate report:
```bash
poetry run cloud-analyzer report --format html --output report.html
```

## Available Checks

### Compute
- **Idle Instance Detection**: Identifies instances with low CPU/network usage
- **Right-sizing**: Recommends smaller instance types for overprovisioned resources
- **Spot Instance Opportunities**: Identifies workloads suitable for spot instances

### Storage
- **Unattached Volumes**: Finds storage volumes not attached to any instance
- **Storage Tier Optimization**: Recommends moving data to cheaper storage tiers
- **Old Snapshots**: Identifies snapshots that can be deleted

### Database
- **Idle Databases**: Finds database instances with minimal connections
- **Multi-AZ Overuse**: Identifies non-production databases with unnecessary HA
- **Backup Retention**: Optimizes backup retention policies

### Logging & Monitoring
- **Log Retention**: Identifies excessive log retention periods
- **Verbose Logging**: Finds production systems with debug logging enabled
- **Metrics Overuse**: Identifies excessive custom metrics collection

See [CHECKS.md](CHECKS.md) for a complete list of optimization checks.

## Technology Stack

- **Backend**: Python 3.11+, FastAPI, SQLAlchemy
- **Frontend**: Vue.js 3, TypeScript, Vite, Tailwind CSS
- **Database**: PostgreSQL (Amazon RDS), Redis (ElastiCache)
- **Infrastructure**: AWS (ECS Fargate, API Gateway, CloudFront)
- **Cloud Providers**: AWS, Azure, Google Cloud Platform
- **IaC**: AWS CDK (Python) or Terraform

## License

Copyright (c) 2024 Cloud Analyzer. All rights reserved.