"""Models for optimization checks and results."""

from datetime import datetime, timezone
from decimal import Decimal
from enum import Enum
from typing import Any, Dict, List, Optional, Set

from pydantic import BaseModel, Field

from models.base import CloudProvider, Resource


class CheckType(str, Enum):
    """Types of optimization checks."""
    
    # Compute
    IDLE_RESOURCE = "idle_resource"
    RIGHT_SIZING = "right_sizing"
    INSTANCE_GENERATION = "instance_generation"
    SPOT_OPPORTUNITY = "spot_opportunity"
    
    # Storage
    UNATTACHED_VOLUME = "unattached_volume"
    STORAGE_TIER = "storage_tier"
    OLD_SNAPSHOT = "old_snapshot"
    
    # Database
    IDLE_DATABASE = "idle_database"
    MULTI_AZ_OVERUSE = "multi_az_overuse"
    BACKUP_RETENTION = "backup_retention"
    
    # Logging
    LOG_RETENTION = "log_retention"
    LOG_VERBOSITY = "log_verbosity"
    METRICS_OVERUSE = "metrics_overuse"
    
    # Network
    UNUSED_IP = "unused_ip"
    IDLE_LOAD_BALANCER = "idle_load_balancer"
    DATA_TRANSFER = "data_transfer"
    
    # Scheduling
    ALWAYS_ON_NON_PROD = "always_on_non_prod"
    
    # Licensing
    LICENSE_OPTIMIZATION = "license_optimization"
    OPEN_SOURCE_ALTERNATIVE = "open_source_alternative"
    
    # Cost Optimization
    RESERVED_INSTANCE_OPTIMIZATION = "reserved_instance_optimization"
    SAVINGS_PLAN_OPTIMIZATION = "savings_plan_optimization"


class CheckSeverity(str, Enum):
    """Severity levels for check results."""
    
    CRITICAL = "critical"  # > 50% potential savings
    HIGH = "high"  # 30-50% potential savings
    MEDIUM = "medium"  # 15-30% potential savings
    LOW = "low"  # < 15% potential savings
    INFO = "info"  # Informational only


class CheckInfo(BaseModel):
    """Information about an available check."""
    
    name: str = Field(..., description="Check name")
    check_type: CheckType = Field(..., description="Type of check")
    description: str = Field(..., description="Check description")
    supported_providers: List[CloudProvider] = Field(..., description="Supported providers")
    
    model_config = {
        "use_enum_values": True
    }


class CheckResult(BaseModel):
    """Result of running an optimization check."""
    
    id: str = Field(..., description="Unique check result ID")
    check_type: CheckType = Field(..., description="Type of check performed")
    severity: CheckSeverity = Field(..., description="Severity of the finding")
    
    # Resource information
    resource: Resource = Field(..., description="Resource checked")
    related_resources: List[Resource] = Field(
        default_factory=list, description="Related resources"
    )
    
    # Finding details
    title: str = Field(..., description="Short title of the finding")
    description: str = Field(..., description="Detailed description")
    impact: str = Field(..., description="Business impact description")
    
    # Cost impact
    current_cost: Decimal = Field(..., description="Current monthly cost")
    optimized_cost: Decimal = Field(..., description="Optimized monthly cost")
    monthly_savings: Decimal = Field(..., description="Potential monthly savings")
    annual_savings: Decimal = Field(..., description="Potential annual savings")
    savings_percentage: float = Field(..., description="Percentage savings")
    
    # Implementation
    effort_level: str = Field(..., description="Implementation effort (low/medium/high)")
    risk_level: str = Field(..., description="Risk level (low/medium/high)")
    implementation_steps: List[str] = Field(
        default_factory=list, description="Steps to implement optimization"
    )
    
    # Metadata
    confidence_score: float = Field(
        1.0, description="Confidence in the recommendation (0-1)"
    )
    check_metadata: Dict[str, Any] = Field(
        default_factory=dict, description="Additional check-specific data"
    )
    
    # Timestamps
    checked_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc), description="When check was performed"
    )
    
    @property
    def priority_score(self) -> float:
        """Calculate priority score based on savings and effort."""
        effort_multiplier = {"low": 1.0, "medium": 0.7, "high": 0.4}.get(
            self.effort_level, 0.5
        )
        severity_multiplier = {
            "critical": 2.0,
            "high": 1.5,
            "medium": 1.0,
            "low": 0.5,
            "info": 0.1,
        }.get(self.severity, 1.0)
        
        return float(self.monthly_savings) * effort_multiplier * severity_multiplier
    
    model_config = {
        "use_enum_values": True,
        "arbitrary_types_allowed": True
    }