"""Repository pattern for database operations."""

from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, desc, func
import logging

from .models import (
    Resource, MetricDefinitionModel, MetricDataModel, 
    CollectionRunModel, CollectionStatusEnum
)
from ..models.base import CloudResource, CloudProvider
from ..models.metrics import (
    MetricDefinition, MetricData, CollectionRun, 
    MetricAggregationType, CollectionStatus
)

logger = logging.getLogger(__name__)


class MetricsRepository:
    """Repository for metrics data operations."""
    
    def __init__(self, session: Session):
        """Initialize repository with database session."""
        self.session = session
    
    # Resource operations
    def upsert_resource(self, resource: CloudResource) -> Resource:
        """Insert or update a cloud resource."""
        try:
            db_resource = self.session.query(Resource).filter(
                Resource.id == resource.id
            ).first()
            
            if db_resource:
                # Update existing resource
                db_resource.name = resource.name
                db_resource.resource_type = resource.resource_type
                db_resource.location = resource.location
                db_resource.resource_group = resource.resource_group
                db_resource.subscription_id = resource.subscription_id
                db_resource.tags = resource.tags
                db_resource.properties = resource.properties
                db_resource.updated_at = datetime.utcnow()
                db_resource.last_discovered = datetime.utcnow()
            else:
                # Create new resource
                db_resource = Resource(
                    id=resource.id,
                    name=resource.name,
                    resource_type=resource.resource_type,
                    location=resource.location,
                    resource_group=resource.resource_group,
                    subscription_id=resource.subscription_id,
                    tags=resource.tags,
                    properties=resource.properties,
                    last_discovered=datetime.utcnow()
                )
                self.session.add(db_resource)
            
            self.session.commit()
            return db_resource
            
        except Exception as e:
            self.session.rollback()
            logger.error(f"Failed to upsert resource {resource.id}: {e}")
            raise
    
    def get_resources(
        self, 
        resource_types: Optional[List[str]] = None,
        resource_groups: Optional[List[str]] = None,
        subscription_ids: Optional[List[str]] = None
    ) -> List[Resource]:
        """Get resources with optional filtering."""
        try:
            query = self.session.query(Resource)
            
            # Apply filters
            if resource_types:
                query = query.filter(Resource.resource_type.in_(resource_types))
            
            if resource_groups:
                query = query.filter(Resource.resource_group.in_(resource_groups))
            
            if subscription_ids:
                query = query.filter(Resource.subscription_id.in_(subscription_ids))
            
            return query.all()
            
        except Exception as e:
            logger.error(f"Failed to get resources: {e}")
            raise
    
    def get_resource_by_id(self, resource_id: str) -> Optional[Resource]:
        """Get a resource by ID."""
        try:
            return self.session.query(Resource).filter(
                Resource.id == resource_id
            ).first()
        except Exception as e:
            logger.error(f"Failed to get resource {resource_id}: {e}")
            raise
    
    # Metric definition operations
    def upsert_metric_definition(self, metric_def: MetricDefinition) -> MetricDefinitionModel:
        """Insert or update a metric definition."""
        try:
            db_metric_def = self.session.query(MetricDefinitionModel).filter(
                and_(
                    MetricDefinitionModel.name == metric_def.name,
                    MetricDefinitionModel.resource_type == metric_def.resource_type
                )
            ).first()
            
            if db_metric_def:
                # Update existing definition
                db_metric_def.display_name = metric_def.display_name
                db_metric_def.description = metric_def.description
                db_metric_def.unit = metric_def.unit
                db_metric_def.aggregation_types = [agg.value for agg in metric_def.aggregation_types]
                db_metric_def.dimensions = metric_def.dimensions
                db_metric_def.is_enabled = metric_def.is_enabled
                db_metric_def.retention_days = metric_def.retention_days
                db_metric_def.collection_interval_minutes = metric_def.collection_interval_minutes
                db_metric_def.updated_at = datetime.utcnow()
            else:
                # Create new definition
                db_metric_def = MetricDefinitionModel(
                    id=metric_def.id,
                    name=metric_def.name,
                    display_name=metric_def.display_name,
                    description=metric_def.description,
                    resource_type=metric_def.resource_type,
                    unit=metric_def.unit,
                    aggregation_types=[agg.value for agg in metric_def.aggregation_types],
                    dimensions=metric_def.dimensions,
                    is_enabled=metric_def.is_enabled,
                    retention_days=metric_def.retention_days,
                    collection_interval_minutes=metric_def.collection_interval_minutes
                )
                self.session.add(db_metric_def)
            
            self.session.commit()
            return db_metric_def
            
        except Exception as e:
            self.session.rollback()
            logger.error(f"Failed to upsert metric definition {metric_def.name}: {e}")
            raise
    
    def get_metric_definitions(self, resource_type: Optional[str] = None) -> List[MetricDefinitionModel]:
        """Get metric definitions, optionally filtered by resource type."""
        try:
            query = self.session.query(MetricDefinitionModel).filter(
                MetricDefinitionModel.is_enabled == True
            )
            
            if resource_type:
                query = query.filter(MetricDefinitionModel.resource_type == resource_type)
            
            return query.all()
            
        except Exception as e:
            logger.error(f"Failed to get metric definitions: {e}")
            raise
    
    # Metric data operations
    def bulk_insert_metric_data(self, metrics_data: List[MetricData]) -> int:
        """Bulk insert metric data points."""
        try:
            db_metrics = []
            for metric_data in metrics_data:
                db_metric = MetricDataModel(
                    id=metric_data.id,
                    resource_id=metric_data.resource_id,
                    metric_name=metric_data.metric_name,
                    timestamp=metric_data.timestamp,
                    value=metric_data.value,
                    aggregation_type=metric_data.aggregation_type,
                    dimensions=metric_data.dimensions,
                    unit=metric_data.unit,
                    collection_run_id=metric_data.collection_run_id
                )
                db_metrics.append(db_metric)
            
            self.session.bulk_save_objects(db_metrics)
            self.session.commit()
            
            return len(db_metrics)
            
        except Exception as e:
            self.session.rollback()
            logger.error(f"Failed to bulk insert metric data: {e}")
            raise
    
    def get_metric_data(
        self,
        resource_id: Optional[str] = None,
        metric_names: Optional[List[str]] = None,
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None,
        limit: Optional[int] = None
    ) -> List[MetricDataModel]:
        """Get metric data with optional filtering."""
        try:
            query = self.session.query(MetricDataModel)
            
            # Apply filters
            if resource_id:
                query = query.filter(MetricDataModel.resource_id == resource_id)
            
            if metric_names:
                query = query.filter(MetricDataModel.metric_name.in_(metric_names))
            
            if start_time:
                query = query.filter(MetricDataModel.timestamp >= start_time)
            
            if end_time:
                query = query.filter(MetricDataModel.timestamp <= end_time)
            
            # Order by timestamp (most recent first)
            query = query.order_by(desc(MetricDataModel.timestamp))
            
            if limit:
                query = query.limit(limit)
            
            return query.all()
            
        except Exception as e:
            logger.error(f"Failed to get metric data: {e}")
            raise
    
    # Collection run operations
    def create_collection_run(self, collection_run: CollectionRun) -> CollectionRunModel:
        """Create a new collection run record."""
        try:
            db_run = CollectionRunModel(
                id=collection_run.id,
                start_time=collection_run.start_time,
                status=collection_run.status,
                resource_filters=collection_run.resource_filters,
                config=collection_run.config,
                metrics_collected=collection_run.metrics_collected,
                resources_processed=collection_run.resources_processed,
                errors_count=collection_run.errors_count,
                error_details=collection_run.error_details
            )
            
            self.session.add(db_run)
            self.session.commit()
            
            return db_run
            
        except Exception as e:
            self.session.rollback()
            logger.error(f"Failed to create collection run: {e}")
            raise
    
    def update_collection_run(self, collection_run: CollectionRun) -> CollectionRunModel:
        """Update an existing collection run."""
        try:
            db_run = self.session.query(CollectionRunModel).filter(
                CollectionRunModel.id == collection_run.id
            ).first()
            
            if not db_run:
                raise ValueError(f"Collection run {collection_run.id} not found")
            
            db_run.end_time = collection_run.end_time
            db_run.status = collection_run.status
            db_run.metrics_collected = collection_run.metrics_collected
            db_run.resources_processed = collection_run.resources_processed
            db_run.errors_count = collection_run.errors_count
            db_run.error_details = collection_run.error_details
            
            self.session.commit()
            return db_run
            
        except Exception as e:
            self.session.rollback()
            logger.error(f"Failed to update collection run {collection_run.id}: {e}")
            raise
    
    def get_collection_runs(
        self, 
        status: Optional[CollectionStatus] = None,
        limit: Optional[int] = None
    ) -> List[CollectionRunModel]:
        """Get collection runs with optional filtering."""
        try:
            query = self.session.query(CollectionRunModel)
            
            if status:
                query = query.filter(CollectionRunModel.status == status)
            
            query = query.order_by(desc(CollectionRunModel.created_at))
            
            if limit:
                query = query.limit(limit)
            
            return query.all()
            
        except Exception as e:
            logger.error(f"Failed to get collection runs: {e}")
            raise
    
    # Data cleanup operations
    def cleanup_old_data(self, retention_days: int = 30) -> int:
        """Clean up old metric data based on retention policy."""
        try:
            cutoff_date = datetime.utcnow() - timedelta(days=retention_days)
            
            deleted_count = self.session.query(MetricDataModel).filter(
                MetricDataModel.timestamp < cutoff_date
            ).count()
            
            self.session.query(MetricDataModel).filter(
                MetricDataModel.timestamp < cutoff_date
            ).delete()
            
            self.session.commit()
            
            logger.info(f"Cleaned up {deleted_count} old metric data records")
            return deleted_count
            
        except Exception as e:
            self.session.rollback()
            logger.error(f"Failed to cleanup old data: {e}")
            raise