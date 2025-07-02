"""Models for optimization checks and results."""

from dataclasses import dataclass
from typing import Dict, Any, List, Optional, Union
from datetime import datetime
from enum import Enum

from .base import CheckStatus, CloudResource


class Severity(Enum):
    """Severity levels for check results."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class RecommendationType(Enum):
    """Types of optimization recommendations."""
    COST_OPTIMIZATION = "cost_optimization"
    PERFORMANCE = "performance"
    SECURITY = "security"
    RELIABILITY = "reliability"
    GOVERNANCE = "governance"


@dataclass
class CheckRecommendation:
    """Recommendation from an optimization check."""
    title: str
    description: str
    severity: Severity
    recommendation_type: RecommendationType
    potential_savings: Optional[float] = None
    effort_level: Optional[str] = None
    implementation_steps: Optional[List[str]] = None
    additional_info: Optional[Dict[str, Any]] = None


@dataclass
class CheckResult:
    """Result of running an optimization check."""
    check_id: str
    check_name: str
    resource: CloudResource
    status: CheckStatus
    timestamp: datetime
    recommendations: List[CheckRecommendation]
    metadata: Dict[str, Any]
    error_message: Optional[str] = None
    execution_time_ms: Optional[int] = None

    def __post_init__(self):
        """Set timestamp if not provided."""
        if not hasattr(self, 'timestamp') or self.timestamp is None:
            self.timestamp = datetime.utcnow()


class CheckRegistry:
    """Registry for managing optimization checks."""
    
    def __init__(self):
        self._checks: Dict[str, Any] = {}
    
    def register(self, check_id: str, check_class: Any):
        """Register a check class."""
        self._checks[check_id] = check_class
    
    def get_check(self, check_id: str) -> Optional[Any]:
        """Get a registered check by ID."""
        return self._checks.get(check_id)
    
    def list_checks(self) -> List[str]:
        """List all registered check IDs."""
        return list(self._checks.keys())
    
    def get_checks_by_resource_type(self, resource_type: str) -> List[str]:
        """Get checks that apply to a specific resource type."""
        applicable_checks = []
        for check_id, check_class in self._checks.items():
            if hasattr(check_class, 'SUPPORTED_RESOURCE_TYPES'):
                if resource_type in check_class.SUPPORTED_RESOURCE_TYPES:
                    applicable_checks.append(check_id)
        return applicable_checks


# Global check registry instance
check_registry = CheckRegistry()