"""Resource discovery service for Azure resources."""

import asyncio
from typing import List, Dict, Any, Optional, AsyncIterator
from datetime import datetime
import logging

from ..providers.base import CloudProviderBase
from ..providers.azure import AzureProvider
from ..models.base import CloudResource, ResourceFilter, CloudProvider
from ..database.connection import DatabaseConnection
from ..database.repository import MetricsRepository

logger = logging.getLogger(__name__)


class ResourceDiscoveryService:
    """Service for discovering and managing cloud resources."""
    
    def __init__(
        self, 
        provider: CloudProviderBase, 
        db_connection: DatabaseConnection
    ):
        """Initialize resource discovery service."""
        self.provider = provider
        self.db_connection = db_connection
        self.logger = logging.getLogger(f"{__name__}.{self.__class__.__name__}")
    
    async def discover_resources(
        self, 
        resource_filter: Optional[ResourceFilter] = None,
        persist_to_db: bool = True
    ) -> List[CloudResource]:
        """Discover resources and optionally persist to database."""
        discovered_resources = []
        
        try:
            self.logger.info("Starting resource discovery")
            
            if not self.provider.is_authenticated:
                await self.provider.authenticate()
            
            # Discover resources
            async for resource in self.provider.discover_resources(resource_filter):
                discovered_resources.append(resource)
                
                if persist_to_db:
                    self._persist_resource(resource)
                
                self.logger.debug(f"Discovered resource: {resource.name} ({resource.resource_type})")
            
            self.logger.info(f"Discovery completed. Found {len(discovered_resources)} resources")
            return discovered_resources
            
        except Exception as e:
            self.logger.error(f"Resource discovery failed: {e}")
            raise
    
    def _persist_resource(self, resource: CloudResource):
        """Persist a discovered resource to the database."""
        try:
            with self.db_connection.get_session() as session:
                repository = MetricsRepository(session)
                repository.upsert_resource(resource)
                
        except Exception as e:
            self.logger.error(f"Failed to persist resource {resource.id}: {e}")
            # Don't raise - continue with discovery
    
    def get_resources_from_db(
        self,
        resource_types: Optional[List[str]] = None,
        resource_groups: Optional[List[str]] = None,
        subscription_ids: Optional[List[str]] = None
    ) -> List[CloudResource]:
        """Get resources from database with optional filtering."""
        try:
            with self.db_connection.get_session() as session:
                repository = MetricsRepository(session)
                db_resources = repository.get_resources(
                    resource_types=resource_types,
                    resource_groups=resource_groups,
                    subscription_ids=subscription_ids
                )
                
                # Convert database models to domain models
                resources = []
                for db_resource in db_resources:
                    resource = CloudResource(
                        id=db_resource.id,
                        name=db_resource.name,
                        resource_type=db_resource.resource_type,
                        location=db_resource.location,
                        resource_group=db_resource.resource_group,
                        subscription_id=db_resource.subscription_id,
                        provider=CloudProvider.AZURE,
                        tags=db_resource.tags,
                        properties=db_resource.properties,
                        created_at=db_resource.created_at,
                        updated_at=db_resource.updated_at
                    )
                    resources.append(resource)
                
                return resources
                
        except Exception as e:
            self.logger.error(f"Failed to get resources from database: {e}")
            raise
    
    async def get_resource_by_id(self, resource_id: str) -> Optional[CloudResource]:
        """Get a specific resource by ID from database or provider."""
        try:
            # First try database
            with self.db_connection.get_session() as session:
                repository = MetricsRepository(session)
                db_resource = repository.get_resource_by_id(resource_id)
                
                if db_resource:
                    return CloudResource(
                        id=db_resource.id,
                        name=db_resource.name,
                        resource_type=db_resource.resource_type,
                        location=db_resource.location,
                        resource_group=db_resource.resource_group,
                        subscription_id=db_resource.subscription_id,
                        provider=CloudProvider.AZURE,
                        tags=db_resource.tags,
                        properties=db_resource.properties,
                        created_at=db_resource.created_at,
                        updated_at=db_resource.updated_at
                    )
            
            # If not in database, try provider
            if not self.provider.is_authenticated:
                await self.provider.authenticate()
            
            return await self.provider.get_resource_by_id(resource_id)
            
        except Exception as e:
            self.logger.error(f"Failed to get resource {resource_id}: {e}")
            raise
    
    async def refresh_resource_cache(
        self, 
        resource_filter: Optional[ResourceFilter] = None
    ) -> int:
        """Refresh the resource cache by re-discovering resources."""
        try:
            self.logger.info("Refreshing resource cache")
            
            discovered_resources = await self.discover_resources(
                resource_filter=resource_filter,
                persist_to_db=True
            )
            
            self.logger.info(f"Resource cache refreshed with {len(discovered_resources)} resources")
            return len(discovered_resources)
            
        except Exception as e:
            self.logger.error(f"Failed to refresh resource cache: {e}")
            raise