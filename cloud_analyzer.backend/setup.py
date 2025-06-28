from setuptools import setup, find_packages

setup(
    name="cloud-analyzer-backend",
    version="0.1.0",
    description="Multi-cloud cost optimization analyzer - Backend API",
    author="Cloud Analyzer Team",
    packages=find_packages(),
    python_requires=">=3.11",
    install_requires=[
        # Web Framework
        "fastapi>=0.104.1",
        "uvicorn[standard]>=0.24.0",
        "python-multipart>=0.0.6",
        "httpx>=0.25.2",
        
        # Database
        "sqlalchemy>=2.0.23",
        "alembic>=1.12.1",
        "asyncpg>=0.29.0",
        "psycopg2-binary>=2.9.9",
        
        # Task Queue
        "celery>=5.3.4",
        "redis>=5.0.1",
        "flower>=2.0.1",
        
        # Cloud SDKs - AWS
        "boto3>=1.34.0",
        "botocore>=1.34.0",
        
        # Cloud SDKs - Azure
        "azure-mgmt-compute>=30.0.0",
        "azure-mgmt-storage>=21.0.0",
        "azure-mgmt-resource>=23.0.0",
        "azure-identity>=1.15.0",
        "azure-mgmt-costmanagement>=4.0.1",
        "azure-mgmt-consumption>=10.0.0",
        "msal>=1.26.0",
        
        # Cloud SDKs - GCP
        "google-cloud-compute>=1.14.0",
        "google-cloud-storage>=2.13.0",
        "google-cloud-resource-manager>=1.11.0",
        "google-cloud-billing>=1.11.0",
        "google-auth>=2.25.0",
        "google-auth-oauthlib>=1.2.0",
        "google-auth-httplib2>=0.2.0",
        "google-api-python-client>=2.111.0",
        
        # Security & Auth
        "python-jose[cryptography]>=3.3.0",
        "passlib>=1.7.4",
        "bcrypt>=4.1.2",
        "authlib>=1.3.0",
        "cryptography>=41.0.7",
        
        # Data Processing
        "pydantic>=2.5.0",
        "pydantic-settings>=2.1.0",
        "python-dateutil>=2.8.2",
        "typing-extensions>=4.9.0",
        "numpy>=1.26.2",
        "pandas>=2.1.4",
        
        # HTTP & Utilities
        "aiohttp>=3.9.1",
        "requests>=2.31.0",
        "pyyaml>=6.0.1",
        "python-dotenv>=1.0.0",
    ],
)