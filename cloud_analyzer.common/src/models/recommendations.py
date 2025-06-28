"""Models for optimization recommendations."""

from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, Field

from models.checks import CheckResult


class RecommendationType(str, Enum):
    """Types of recommendations."""
    
    TERMINATE = "terminate"
    RESIZE = "resize"
    SCHEDULE = "schedule"
    MIGRATE = "migrate"
    PURCHASE = "purchase"
    CONFIGURE = "configure"
    DELETE = "delete"
    ARCHIVE = "archive"


class RecommendationStatus(str, Enum):
    """Status of a recommendation."""
    
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    DISMISSED = "dismissed"
    FAILED = "failed"


class Recommendation(BaseModel):
    """Actionable recommendation based on check results."""
    
    id: str = Field(..., description="Unique recommendation ID")
    type: RecommendationType = Field(..., description="Type of recommendation")
    status: RecommendationStatus = Field(
        default=RecommendationStatus.PENDING, description="Current status"
    )
    
    # Source checks
    check_results: List[CheckResult] = Field(
        ..., description="Check results that generated this recommendation"
    )
    
    # Summary
    title: str = Field(..., description="Recommendation title")
    summary: str = Field(..., description="Executive summary")
    
    # Impact
    total_monthly_savings: float = Field(
        ..., description="Total potential monthly savings"
    )
    implementation_cost: Optional[float] = Field(
        None, description="One-time implementation cost"
    )
    payback_months: Optional[float] = Field(
        None, description="Months to payback implementation cost"
    )
    
    # Actions
    automated: bool = Field(
        False, description="Whether this can be automated"
    )
    requires_downtime: bool = Field(
        False, description="Whether implementation requires downtime"
    )
    rollback_possible: bool = Field(
        True, description="Whether changes can be rolled back"
    )
    
    # Tracking
    notes: Optional[str] = Field(None, description="Implementation notes")
    implemented_by: Optional[str] = Field(None, description="User who implemented")
    implemented_at: Optional[str] = Field(None, description="Implementation timestamp")
    
    model_config = {
        "use_enum_values": True,
        "arbitrary_types_allowed": True
    }