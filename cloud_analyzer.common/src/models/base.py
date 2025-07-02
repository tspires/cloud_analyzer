"""Base models for cloud resources and providers."""

from enum import Enum
from typing import Dict, Any, Optional, List
from dataclasses import dataclass
from datetime import datetime


class CloudProvider(Enum):
    """Supported cloud providers."""
    AZURE = "azure"
    AWS = "aws"
    GCP = "gcp"


class ResourceType(Enum):
    """Azure resource types for metrics collection."""
    VIRTUAL_MACHINE = "Microsoft.Compute/virtualMachines"
    APP_SERVICE = "Microsoft.Web/sites"
    SQL_DATABASE = "Microsoft.Sql/servers/databases"
    STORAGE_ACCOUNT = "Microsoft.Storage/storageAccounts"
    APPLICATION_INSIGHTS = "Microsoft.Insights/components"
    LOAD_BALANCER = "Microsoft.Network/loadBalancers"
    FUNCTION_APP = "Microsoft.Web/sites"
    KEY_VAULT = "Microsoft.KeyVault/vaults"
    COSMOS_DB = "Microsoft.DocumentDB/databaseAccounts"
    MYSQL_SERVER = "Microsoft.DBforMySQL/servers"
    POSTGRESQL_SERVER = "Microsoft.DBforPostgreSQL/servers"
    VM_SCALE_SET = "Microsoft.Compute/virtualMachineScaleSets"


class CheckStatus(Enum):
    """Status of optimization checks."""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    SKIPPED = "skipped"


@dataclass
class CloudResource:
    """Base model for cloud resources."""
    id: str
    name: str
    resource_type: str
    location: str
    resource_group: str
    subscription_id: str
    provider: CloudProvider
    tags: Dict[str, str]
    properties: Dict[str, Any]
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    def __post_init__(self):
        """Set timestamps if not provided."""
        if self.created_at is None:
            self.created_at = datetime.utcnow()
        if self.updated_at is None:
            self.updated_at = datetime.utcnow()


@dataclass
class ResourceFilter:
    """Filter criteria for resource discovery."""
    resource_groups: Optional[List[str]] = None
    resource_types: Optional[List[str]] = None
    tags: Optional[Dict[str, str]] = None
    subscription_ids: Optional[List[str]] = None
    locations: Optional[List[str]] = None
