#!/bin/bash

# Cloud Analyzer Backend Setup Script
# Based on Technical Specification

set -e

echo "==================================="
echo "Cloud Analyzer Backend Setup"
echo "==================================="

# Check Python version
PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
REQUIRED_VERSION="3.11"

if ! python3 -c "import sys; exit(0 if sys.version_info >= (3, 11) else 1)"; then
    echo "Error: Python 3.11+ is required. Current version: $PYTHON_VERSION"
    exit 1
fi

echo "✓ Python version check passed: $PYTHON_VERSION"

# Create virtual environment
echo "Creating virtual environment..."
python3 -m venv venv
source venv/bin/activate

echo "✓ Virtual environment created"

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

# Install core dependencies from tech spec
echo "Installing core dependencies..."

# Backend Framework (FastAPI)
pip install fastapi==0.104.1
pip install uvicorn[standard]==0.24.0
pip install pydantic==2.5.0
pip install pydantic-settings==2.1.0
pip install python-jose[cryptography]==3.3.0
pip install python-multipart==0.0.6
pip install httpx==0.25.2

# Database
pip install sqlalchemy==2.0.23
pip install alembic==1.12.1
pip install asyncpg==0.29.0
pip install psycopg2-binary==2.9.9

# Task Queue
pip install celery==5.3.4
pip install redis==5.0.1
pip install flower==2.0.1

# Cloud Provider SDKs (AWS)
pip install boto3==1.34.0
pip install botocore==1.34.0

# Cloud Provider SDKs (Azure)
pip install azure-mgmt-compute==30.0.0
pip install azure-mgmt-storage==21.0.0
pip install azure-mgmt-resource==23.0.0
pip install azure-identity==1.15.0
pip install azure-mgmt-costmanagement==4.0.1
pip install azure-mgmt-consumption==10.0.0
pip install msal==1.26.0

# Cloud Provider SDKs (GCP)
pip install google-cloud-compute==1.14.0
pip install google-cloud-storage==2.13.0
pip install google-cloud-resource-manager==1.11.0
pip install google-cloud-billing==1.11.0
pip install google-auth==2.25.0
pip install google-auth-oauthlib==1.2.0
pip install google-auth-httplib2==0.2.0
pip install google-api-python-client==2.111.0

# Security & Authentication
pip install authlib==1.3.0
pip install cryptography==41.0.7
pip install bcrypt==4.1.2
pip install passlib==1.7.4

# Utilities
pip install python-dateutil==2.8.2
pip install typing-extensions==4.9.0
pip install pyyaml==6.0.1
pip install python-dotenv==1.0.0

# HTTP & API
pip install aiohttp==3.9.1
pip install requests==2.31.0

# Development Tools
pip install pytest==7.4.3
pip install pytest-asyncio==0.21.1
pip install pytest-cov==4.1.0
pip install black==23.12.0
pip install flake8==6.1.0
pip install mypy==1.7.1
pip install isort==5.13.0
pip install pre-commit==3.6.0

# Additional utilities for optimization engine
pip install numpy==1.26.2
pip install pandas==2.1.4

echo "✓ All dependencies installed"

# Create project structure based on tech spec
echo "Creating project structure..."

mkdir -p app/{api/v1/endpoints,core,models,services/providers/{aws,azure,gcp}}
mkdir -p tests
mkdir -p alembic

# Create __init__.py files
touch app/__init__.py
touch app/api/__init__.py
touch app/api/v1/__init__.py
touch app/api/v1/endpoints/__init__.py
touch app/core/__init__.py
touch app/models/__init__.py
touch app/services/__init__.py
touch app/services/providers/__init__.py
touch app/services/providers/aws/__init__.py
touch app/services/providers/azure/__init__.py
touch app/services/providers/gcp/__init__.py
touch tests/__init__.py

echo "✓ Project structure created"

# Create .env.example file
cat > .env.example << EOF
# Environment
ENVIRONMENT=development
DEBUG=True

# API Settings
API_V1_STR=/api/v1
PROJECT_NAME="Cloud Analyzer Backend"
BACKEND_CORS_ORIGINS=["http://localhost:3000","http://localhost:5173"]

# Security
SECRET_KEY=your-secret-key-here-change-in-production
ACCESS_TOKEN_EXPIRE_MINUTES=15
REFRESH_TOKEN_EXPIRE_DAYS=7

# Database
DATABASE_URL=postgresql://user:password@localhost/cloud_analyzer
DATABASE_POOL_SIZE=20
DATABASE_MAX_OVERFLOW=0

# Redis
REDIS_URL=redis://localhost:6379/0

# AWS Configuration (Optional - for testing)
AWS_ACCESS_KEY_ID=
AWS_SECRET_ACCESS_KEY=
AWS_DEFAULT_REGION=us-east-1

# Azure Configuration (Optional - for testing)
AZURE_CLIENT_ID=
AZURE_CLIENT_SECRET=
AZURE_TENANT_ID=
AZURE_SUBSCRIPTION_ID=

# GCP Configuration (Optional - for testing)
GOOGLE_APPLICATION_CREDENTIALS=
GCP_PROJECT_ID=

# Monitoring
SENTRY_DSN=
LOG_LEVEL=INFO

# Celery
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/0
EOF

echo "✓ Created .env.example file"

# Create a basic FastAPI main.py
cat > app/main.py << EOF
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
)

# Set all CORS enabled origins
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.get("/")
async def root():
    return {"message": "Cloud Analyzer Backend API"}
EOF

echo "✓ Created main.py"

# Create basic config file
cat > app/core/config.py << EOF
from typing import List, Union
from pydantic_settings import BaseSettings
from pydantic import AnyHttpUrl, field_validator

class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Cloud Analyzer Backend"
    
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []

    @field_validator("BACKEND_CORS_ORIGINS", mode='before')
    @classmethod
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)
    
    DATABASE_URL: str = "postgresql://user:password@localhost/cloud_analyzer"
    
    class Config:
        case_sensitive = True
        env_file = ".env"

settings = Settings()
EOF

echo "✓ Created config.py"

# Create requirements.txt for easy reference
pip freeze > requirements.txt

echo "✓ Created requirements.txt"

# Create README for backend
cat > README.md << EOF
# Cloud Analyzer Backend

Multi-cloud cost optimization analyzer backend service.

## Setup

1. Install Python 3.11+
2. Run the setup script:
   \`\`\`bash
   chmod +x setup.sh
   ./setup.sh
   \`\`\`

3. Configure environment variables:
   \`\`\`bash
   cp .env.example .env
   # Edit .env with your configuration
   \`\`\`

4. Set up PostgreSQL database:
   \`\`\`bash
   createdb cloud_analyzer
   alembic upgrade head
   \`\`\`

5. Run the development server:
   \`\`\`bash
   source venv/bin/activate
   uvicorn app.main:app --reload
   \`\`\`

## Tech Stack

- **Runtime**: Python 3.11+
- **Framework**: FastAPI
- **ORM**: SQLAlchemy 2.0
- **Task Queue**: Celery with Redis
- **Cloud SDKs**: boto3 (AWS), azure-mgmt (Azure), google-cloud (GCP)

## Testing

\`\`\`bash
pytest tests/ -v
\`\`\`

## Code Quality

\`\`\`bash
# Format code
black app/ tests/

# Lint
flake8 app/ tests/

# Type checking
mypy app/
\`\`\`
EOF

echo "✓ Created README.md"

# Create pre-commit configuration
cat > .pre-commit-config.yaml << EOF
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.5.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-added-large-files
      - id: check-json
      - id: check-merge-conflict

  - repo: https://github.com/psf/black
    rev: 23.12.0
    hooks:
      - id: black
        language_version: python3.11

  - repo: https://github.com/pycqa/isort
    rev: 5.13.0
    hooks:
      - id: isort
        args: ["--profile", "black"]

  - repo: https://github.com/pycqa/flake8
    rev: 6.1.0
    hooks:
      - id: flake8
        args: ["--max-line-length=88", "--extend-ignore=E203"]
EOF

echo "✓ Created pre-commit configuration"

# Initialize pre-commit
pre-commit install

echo "✓ Initialized pre-commit hooks"

# Create pytest configuration
cat > pytest.ini << EOF
[pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts = -v --tb=short
asyncio_mode = auto
EOF

echo "✓ Created pytest configuration"

# Final instructions
echo ""
echo "==================================="
echo "Setup Complete!"
echo "==================================="
echo ""
echo "Next steps:"
echo "1. Copy .env.example to .env and configure your settings"
echo "2. Set up PostgreSQL database"
echo "3. Run 'source venv/bin/activate' to activate virtual environment"
echo "4. Run 'uvicorn app.main:app --reload' to start the server"
echo ""
echo "The API will be available at http://localhost:8000"
echo "API documentation at http://localhost:8000/docs"