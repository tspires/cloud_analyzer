"""SQLAlchemy database models for Azure metrics."""

from sqlalchemy import (
    Column, String, DateTime, Integer, Float, Text, Boolean, 
    JSON, ForeignKey, Index, BigInteger, Enum as SQLEnum
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from datetime import datetime
import enum

Base = declarative_base()


class ResourceTypeEnum(enum.Enum):
    """Enumeration of Azure resource types."""
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


class CollectionStatusEnum(enum.Enum):
    """Collection run status enumeration."""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    PARTIAL = "partial"


class MetricAggregationTypeEnum(enum.Enum):
    """Metric aggregation type enumeration."""
    AVERAGE = "Average"
    MAXIMUM = "Maximum"
    MINIMUM = "Minimum"
    TOTAL = "Total"
    COUNT = "Count"


class Resource(Base):
    """Azure resource metadata table."""
    __tablename__ = 'resources'
    
    id = Column(String(500), primary_key=True)  # Azure resource ID
    name = Column(String(255), nullable=False)
    resource_type = Column(String(100), nullable=False)
    location = Column(String(50), nullable=False)
    resource_group = Column(String(255), nullable=False)
    subscription_id = Column(String(36), nullable=False)
    tags = Column(JSON, default={})
    properties = Column(JSON, default={})
    
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    last_discovered = Column(DateTime, default=func.now())
    
    # Relationships
    metric_data = relationship("MetricDataModel", back_populates="resource")
    
    # Indexes
    __table_args__ = (
        Index('idx_resource_type', 'resource_type'),
        Index('idx_resource_group', 'resource_group'),
        Index('idx_subscription_id', 'subscription_id'),
        Index('idx_last_discovered', 'last_discovered'),
    )


class MetricDefinitionModel(Base):
    """Metric definitions for resource types."""
    __tablename__ = 'metric_definitions'
    
    id = Column(String(36), primary_key=True)
    name = Column(String(255), nullable=False)
    display_name = Column(String(255), nullable=False)
    description = Column(Text)
    resource_type = Column(String(100), nullable=False)
    unit = Column(String(50), nullable=False)
    aggregation_types = Column(JSON)  # List of supported aggregation types
    dimensions = Column(JSON)  # List of supported dimensions
    
    is_enabled = Column(Boolean, default=True)
    retention_days = Column(Integer, default=30)
    collection_interval_minutes = Column(Integer, default=15)
    
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    # Indexes
    __table_args__ = (
        Index('idx_metric_resource_type', 'resource_type'),
        Index('idx_metric_name', 'name'),
        Index('idx_metric_enabled', 'is_enabled'),
    )


class MetricDataModel(Base):
    """Time series metric data."""
    __tablename__ = 'metric_data'
    
    id = Column(String(36), primary_key=True)
    resource_id = Column(String(500), ForeignKey('resources.id', ondelete='CASCADE'), nullable=False)
    metric_name = Column(String(255), nullable=False)
    timestamp = Column(DateTime, nullable=False)
    value = Column(Float, nullable=False)
    aggregation_type = Column(SQLEnum(MetricAggregationTypeEnum), nullable=False)
    dimensions = Column(JSON, default={})
    unit = Column(String(50))
    collection_run_id = Column(String(36), ForeignKey('collection_runs.id', ondelete='SET NULL'))
    
    created_at = Column(DateTime, default=func.now())
    
    # Relationships
    resource = relationship("Resource", back_populates="metric_data")
    collection_run = relationship("CollectionRunModel", back_populates="metric_data")
    
    # Indexes for time series queries
    __table_args__ = (
        Index('idx_metric_resource_id', 'resource_id'),
        Index('idx_metric_name_timestamp', 'metric_name', 'timestamp'),
        Index('idx_metric_timestamp', 'timestamp'),
        Index('idx_metric_collection_run', 'collection_run_id'),
        # Composite index for common queries
        Index('idx_metric_resource_metric_time', 'resource_id', 'metric_name', 'timestamp'),
    )


class CollectionRunModel(Base):
    """Metrics collection run tracking."""
    __tablename__ = 'collection_runs'
    
    id = Column(String(36), primary_key=True)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime)
    status = Column(SQLEnum(CollectionStatusEnum), nullable=False)
    
    # Configuration and filters
    resource_filters = Column(JSON, default={})
    config = Column(JSON, default={})
    
    # Statistics
    metrics_collected = Column(Integer, default=0)
    resources_processed = Column(Integer, default=0)
    errors_count = Column(Integer, default=0)
    error_details = Column(JSON, default=[])
    
    created_at = Column(DateTime, default=func.now())
    
    # Relationships
    metric_data = relationship("MetricDataModel", back_populates="collection_run")
    
    # Indexes
    __table_args__ = (
        Index('idx_collection_start_time', 'start_time'),
        Index('idx_collection_status', 'status'),
        Index('idx_collection_created_at', 'created_at'),
    )