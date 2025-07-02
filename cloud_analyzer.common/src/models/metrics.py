"""Models for Azure metrics collection and storage."""

from dataclasses import dataclass
from typing import Dict, Any, List, Optional, Union
from datetime import datetime
from enum import Enum
import uuid

from .base import CloudResource


class MetricAggregationType(Enum):
    """Azure Monitor metric aggregation types."""
    AVERAGE = "Average"
    MAXIMUM = "Maximum"
    MINIMUM = "Minimum"
    TOTAL = "Total"
    COUNT = "Count"


class CollectionStatus(Enum):
    """Status of metrics collection runs."""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    PARTIAL = "partial"


@dataclass
class MetricDefinition:
    """Definition of an available metric for a resource type."""
    id: str
    name: str
    display_name: str
    description: str
    resource_type: str
    unit: str
    aggregation_types: List[MetricAggregationType]
    dimensions: List[str]
    is_enabled: bool = True
    retention_days: int = 30
    collection_interval_minutes: int = 15

    def __post_init__(self):
        """Generate ID if not provided."""
        if not self.id:
            self.id = str(uuid.uuid4())


@dataclass
class MetricData:
    """Time series metric data point."""
    id: str
    resource_id: str
    metric_name: str
    timestamp: datetime
    value: Union[float, int]
    aggregation_type: MetricAggregationType
    dimensions: Dict[str, str]
    unit: str
    collection_run_id: str
    created_at: Optional[datetime] = None

    def __post_init__(self):
        """Set created_at if not provided and generate ID."""
        if not self.id:
            self.id = str(uuid.uuid4())
        if self.created_at is None:
            self.created_at = datetime.utcnow()


@dataclass
class CollectionRun:
    """Tracking information for metrics collection runs."""
    id: str
    start_time: datetime
    end_time: Optional[datetime]
    status: CollectionStatus
    resource_filters: Dict[str, Any]
    metrics_collected: int
    resources_processed: int
    errors_count: int
    error_details: List[Dict[str, Any]]
    config: Dict[str, Any]
    created_at: Optional[datetime] = None

    def __post_init__(self):
        """Set created_at and generate ID if not provided."""
        if not self.id:
            self.id = str(uuid.uuid4())
        if self.created_at is None:
            self.created_at = datetime.utcnow()

    def mark_completed(self):
        """Mark the collection run as completed."""
        self.end_time = datetime.utcnow()
        self.status = CollectionStatus.COMPLETED

    def mark_failed(self, error_message: str):
        """Mark the collection run as failed."""
        self.end_time = datetime.utcnow()
        self.status = CollectionStatus.FAILED
        self.errors_count += 1
        self.error_details.append({
            'timestamp': datetime.utcnow().isoformat(),
            'error': error_message
        })

    @property
    def duration_minutes(self) -> Optional[float]:
        """Calculate duration of the collection run in minutes."""
        if self.end_time:
            delta = self.end_time - self.start_time
            return delta.total_seconds() / 60
        return None


@dataclass
class MetricsCollectionConfig:
    """Configuration for metrics collection."""
    interval_minutes: int = 15
    retention_days: int = 30
    batch_size: int = 100
    parallel_workers: int = 4
    timeout_seconds: int = 300
    retry_attempts: int = 3
    retry_delay_seconds: int = 5
    enable_data_validation: bool = True
    resource_filters: Optional[Dict[str, Any]] = None