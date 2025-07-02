"""Metrics collection service with async processing and error handling."""

import asyncio
import uuid
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
from concurrent.futures import ThreadPoolExecutor, as_completed
import logging
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

from azure.core.exceptions import AzureError, HttpResponseError

from ..providers.base import CloudProviderBase
from ..models.base import CloudResource, ResourceFilter
from ..models.metrics import (
    MetricDefinition, MetricData, CollectionRun, CollectionStatus,
    MetricsCollectionConfig, MetricAggregationType
)
from ..database.connection import DatabaseConnection
from ..database.repository import MetricsRepository
from .resource_discovery import ResourceDiscoveryService

logger = logging.getLogger(__name__)


class MetricsCollectionService:
    """Service for collecting Azure metrics with async processing."""

    def __init__(
        self,
        provider: CloudProviderBase,
        db_connection: DatabaseConnection,
        discovery_service: ResourceDiscoveryService,
        config: MetricsCollectionConfig
    ):
        """Initialize metrics collection service."""
        self.provider = provider
        self.db_connection = db_connection
        self.discovery_service = discovery_service
        self.config = config
        self.logger = logging.getLogger(f"{__name__}.{self.__class__.__name__}")

        # Initialize thread pool for parallel processing
        self.executor = ThreadPoolExecutor(max_workers=config.parallel_workers)

    async def collect_all_metrics(
        self,
        resource_filter: Optional[ResourceFilter] = None,
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None,
        dry_run: bool = False
    ) -> CollectionRun:
        """Collect metrics for all resources matching the filter."""

        # Set default time range (last 24 hours)
        if not end_time:
            end_time = datetime.utcnow()
        if not start_time:
            start_time = end_time - timedelta(hours=24)

        # Create collection run
        collection_run = CollectionRun(
            id=str(uuid.uuid4()),
            start_time=datetime.utcnow(),
            end_time=None,
            status=CollectionStatus.RUNNING,
            resource_filters=resource_filter.__dict__ if resource_filter else {},
            metrics_collected=0,
            resources_processed=0,
            errors_count=0,
            error_details=[],
            config=self.config.__dict__
        )

        try:
            if not dry_run:
                # Persist collection run to database
                with self.db_connection.get_session() as session:
                    repository = MetricsRepository(session)
                    repository.create_collection_run(collection_run)

            self.logger.info(f"Starting metrics collection run {collection_run.id}")

            # Get resources to process
            resources = self.discovery_service.get_resources_from_db(
                resource_types=resource_filter.resource_types if resource_filter else None,
                resource_groups=resource_filter.resource_groups if resource_filter else None,
                subscription_ids=resource_filter.subscription_ids if resource_filter else None
            )

            if not resources:
                self.logger.warning("No resources found for metrics collection")
                collection_run.mark_completed()
                return collection_run

            self.logger.info(f"Collecting metrics for {len(resources)} resources")

            # Process resources in batches with parallelization
            all_metrics = []
            batch_size = self.config.batch_size

            for i in range(0, len(resources), batch_size):
                batch = resources[i:i + batch_size]

                if dry_run:
                    self.logger.info(f"DRY RUN: Would collect metrics for batch {i//batch_size + 1} ({len(batch)} resources)")
                    collection_run.resources_processed += len(batch)
                    continue

                batch_metrics = await self._process_batch(
                    batch, start_time, end_time, collection_run
                )
                all_metrics.extend(batch_metrics)

                # Update collection run statistics
                collection_run.resources_processed += len(batch)
                collection_run.metrics_collected += len(batch_metrics)

                self.logger.info(
                    f"Processed batch {i//batch_size + 1}/{(len(resources) + batch_size - 1)//batch_size}, "
                    f"collected {len(batch_metrics)} metrics"
                )

            if not dry_run and all_metrics:
                # Bulk insert metrics data
                self._persist_metrics_data(all_metrics, collection_run.id)

            # Mark collection run as completed
            collection_run.mark_completed()

            if not dry_run:
                # Update collection run in database
                with self.db_connection.get_session() as session:
                    repository = MetricsRepository(session)
                    repository.update_collection_run(collection_run)

            self.logger.info(
                f"Metrics collection completed. "
                f"Processed {collection_run.resources_processed} resources, "
                f"collected {collection_run.metrics_collected} metrics, "
                f"errors: {collection_run.errors_count}"
            )

            return collection_run

        except Exception as e:
            self.logger.error(f"Metrics collection failed: {e}")
            collection_run.mark_failed(str(e))

            if not dry_run:
                try:
                    with self.db_connection.get_session() as session:
                        repository = MetricsRepository(session)
                        repository.update_collection_run(collection_run)
                except Exception as db_error:
                    self.logger.error(f"Failed to update collection run in database: {db_error}")

            raise

    async def _process_batch(
        self,
        resources: List[CloudResource],
        start_time: datetime,
        end_time: datetime,
        collection_run: CollectionRun
    ) -> List[MetricData]:
        """Process a batch of resources for metrics collection."""
        batch_metrics = []

        # Create tasks for parallel processing
        tasks = []
        for resource in resources:
            task = asyncio.create_task(
                self._collect_resource_metrics(resource, start_time, end_time, collection_run)
            )
            tasks.append(task)

        # Wait for all tasks to complete
        results = await asyncio.gather(*tasks, return_exceptions=True)

        # Process results
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                self.logger.error(f"Failed to collect metrics for {resources[i].name}: {result}")
                collection_run.errors_count += 1
                collection_run.error_details.append({
                    'timestamp': datetime.utcnow().isoformat(),
                    'resource_id': resources[i].id,
                    'error': str(result)
                })
            else:
                batch_metrics.extend(result)

        return batch_metrics

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=10),
        retry=retry_if_exception_type((HttpResponseError, AzureError))
    )
    async def _collect_resource_metrics(
        self,
        resource: CloudResource,
        start_time: datetime,
        end_time: datetime,
        collection_run: CollectionRun
    ) -> List[MetricData]:
        """Collect metrics for a single resource with retry logic."""
        try:
            # Get available metrics for this resource type
            available_metrics = await self.provider.get_available_metrics(resource.resource_type)

            if not available_metrics:
                self.logger.debug(f"No metrics available for resource type {resource.resource_type}")
                return []

            # Collect metrics from Azure Monitor
            metric_names = [metric.name for metric in available_metrics]
            metrics_data = await self.provider.collect_metrics(
                resource=resource,
                metric_names=metric_names,
                start_time=start_time,
                end_time=end_time,
                aggregation_interval=f"PT{self.config.interval_minutes}M"
            )

            # Set collection run ID for all metrics
            for metric_data in metrics_data:
                metric_data.collection_run_id = collection_run.id

            self.logger.debug(f"Collected {len(metrics_data)} metrics for {resource.name}")
            return metrics_data

        except Exception as e:
            self.logger.error(f"Failed to collect metrics for {resource.name}: {e}")
            raise

    def _persist_metrics_data(self, metrics_data: List[MetricData], collection_run_id: str):
        """Persist metrics data to database in batches."""
        try:
            with self.db_connection.get_session() as session:
                repository = MetricsRepository(session)

                # Process in batches to avoid memory issues
                batch_size = 1000
                for i in range(0, len(metrics_data), batch_size):
                    batch = metrics_data[i:i + batch_size]
                    repository.bulk_insert_metric_data(batch)

                    self.logger.debug(f"Persisted batch {i//batch_size + 1} of metrics data")

        except Exception as e:
            self.logger.error(f"Failed to persist metrics data: {e}")
            raise

    async def collect_resource_metrics(
        self,
        resource_id: str,
        metric_names: Optional[List[str]] = None,
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None
    ) -> List[MetricData]:
        """Collect specific metrics for a single resource."""
        try:
            # Get resource
            resource = await self.discovery_service.get_resource_by_id(resource_id)
            if not resource:
                raise ValueError(f"Resource {resource_id} not found")

            # Set default time range
            if not end_time:
                end_time = datetime.utcnow()
            if not start_time:
                start_time = end_time - timedelta(hours=1)

            # Get available metrics if not specified
            if not metric_names:
                available_metrics = await self.provider.get_available_metrics(resource.resource_type)
                metric_names = [metric.name for metric in available_metrics]

            # Collect metrics
            metrics_data = await self.provider.collect_metrics(
                resource=resource,
                metric_names=metric_names,
                start_time=start_time,
                end_time=end_time
            )

            self.logger.info(f"Collected {len(metrics_data)} metrics for resource {resource.name}")
            return metrics_data

        except Exception as e:
            self.logger.error(f"Failed to collect metrics for resource {resource_id}: {e}")
            raise

    def get_collection_history(
        self,
        limit: Optional[int] = 10
    ) -> List[CollectionRun]:
        """Get history of collection runs."""
        try:
            with self.db_connection.get_session() as session:
                repository = MetricsRepository(session)
                db_runs = repository.get_collection_runs(limit=limit)

                # Convert database models to domain models
                collection_runs = []
                for db_run in db_runs:
                    collection_run = CollectionRun(
                        id=db_run.id,
                        start_time=db_run.start_time,
                        end_time=db_run.end_time,
                        status=db_run.status,
                        resource_filters=db_run.resource_filters,
                        metrics_collected=db_run.metrics_collected,
                        resources_processed=db_run.resources_processed,
                        errors_count=db_run.errors_count,
                        error_details=db_run.error_details,
                        config=db_run.config,
                        created_at=db_run.created_at
                    )
                    collection_runs.append(collection_run)

                return collection_runs

        except Exception as e:
            self.logger.error(f"Failed to get collection history: {e}")
            raise

    def cleanup_old_data(self, retention_days: Optional[int] = None) -> int:
        """Clean up old metrics data."""
        try:
            retention_days = retention_days or self.config.retention_days

            with self.db_connection.get_session() as session:
                repository = MetricsRepository(session)
                deleted_count = repository.cleanup_old_data(retention_days)

                self.logger.info(f"Cleaned up {deleted_count} old metrics records")
                return deleted_count

        except Exception as e:
            self.logger.error(f"Failed to cleanup old data: {e}")
            raise

    def cleanup(self):
        """Cleanup resources."""
        if hasattr(self, 'executor') and self.executor:
            self.executor.shutdown(wait=True)
            self.executor = None

    def __del__(self):
        """Cleanup resources."""
        try:
            self.cleanup()
        except Exception:
            # Ignore errors during cleanup
            pass
