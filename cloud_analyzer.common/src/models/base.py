"""Base models for cloud resources."""

from abc import ABC
from datetime import datetime, timezone
from decimal import Decimal
from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class CloudProvider(str, Enum):
    """Supported cloud providers."""
    
    AZURE = "azure"


class ResourceType(str, Enum):
    """Types of cloud resources."""
    
    # Compute
    INSTANCE = "instance"
    CONTAINER = "container"
    FUNCTION = "function"
    RESERVED_INSTANCE = "reserved_instance"
    
    # Storage
    VOLUME = "volume"
    SNAPSHOT = "snapshot"
    BUCKET = "bucket"
    
    # Database
    DATABASE = "database"
    CACHE = "cache"
    
    # Network
    LOAD_BALANCER = "load_balancer"
    NAT_GATEWAY = "nat_gateway"
    IP_ADDRESS = "ip_address"
    
    # Analytics
    CLUSTER = "cluster"
    WAREHOUSE = "warehouse"
    PIPELINE = "pipeline"
    
    # Logging
    LOG_GROUP = "log_group"
    METRIC = "metric"


class Resource(BaseModel):
    """Base model for cloud resources."""
    
    id: str = Field(..., description="Unique resource identifier")
    name: str = Field(..., description="Resource name")
    type: ResourceType = Field(..., description="Type of resource")
    provider: CloudProvider = Field(..., description="Cloud provider")
    region: str = Field(..., description="Region/location")
    
    # Cost information
    monthly_cost: Decimal = Field(
        default=Decimal("0"), description="Estimated monthly cost"
    )
    hourly_cost: Optional[Decimal] = Field(
        None, description="Hourly cost if applicable"
    )
    currency: str = Field(default="USD", description="Currency code")
    
    # Metadata
    created_at: Optional[datetime] = Field(None, description="Resource creation time")
    last_seen: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc), description="Last time resource was observed"
    )
    tags: Dict[str, str] = Field(
        default_factory=dict, description="Resource tags/labels"
    )
    
    # State
    state: str = Field(..., description="Current resource state")
    is_active: bool = Field(True, description="Whether resource is active/running")
    
    # Additional provider-specific data
    metadata: Dict[str, Any] = Field(
        default_factory=dict, description="Provider-specific metadata"
    )
    
    model_config = {
        "use_enum_values": True,
        "arbitrary_types_allowed": True
    }