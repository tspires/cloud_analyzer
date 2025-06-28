"""Base classes for optimization checks."""

from abc import ABC, abstractmethod
from typing import List, Optional, Set

from models.checks import CheckResult, CheckType
from models.base import CloudProvider, Resource
from providers.base import CloudProviderInterface


class Check(ABC):
    """Abstract base class for optimization checks."""
    
    @property
    @abstractmethod
    def check_type(self) -> CheckType:
        """Return the type of check."""
        pass
    
    @property
    @abstractmethod
    def name(self) -> str:
        """Return human-readable name of the check."""
        pass
    
    @property
    @abstractmethod
    def description(self) -> str:
        """Return description of what this check does."""
        pass
    
    @property
    @abstractmethod
    def supported_providers(self) -> Set[CloudProvider]:
        """Return set of providers this check supports."""
        pass
    
    @abstractmethod
    async def run(
        self, 
        provider: CloudProviderInterface, 
        resources: List[Resource],
        region: Optional[str] = None
    ) -> List[CheckResult]:
        """Run the check against provided resources.
        
        Args:
            provider: Cloud provider interface
            resources: List of resources to check
            region: Optional region filter
            
        Returns:
            List of check results
        """
        pass
    
    def filter_resources(self, resources: List[Resource]) -> List[Resource]:
        """Filter resources relevant to this check.
        
        Override this method to filter resources before checking.
        
        Args:
            resources: All resources
            
        Returns:
            Filtered resources
        """
        return resources


class CheckRunner:
    """Runner for executing checks."""
    
    def __init__(self, provider: CloudProviderInterface) -> None:
        """Initialize check runner.
        
        Args:
            provider: Cloud provider interface
        """
        self.provider = provider
    
    async def run_check(
        self, 
        check: Check, 
        resources: List[Resource],
        region: Optional[str] = None
    ) -> List[CheckResult]:
        """Run a single check.
        
        Args:
            check: Check to run
            resources: Resources to check
            region: Optional region filter
            
        Returns:
            List of check results
        """
        if self.provider.provider not in check.supported_providers:
            return []
        
        filtered_resources = check.filter_resources(resources)
        if not filtered_resources:
            return []
        
        return await check.run(self.provider, filtered_resources, region)
    
    async def run_checks(
        self, 
        checks: List[Check], 
        resources: List[Resource],
        region: Optional[str] = None
    ) -> List[CheckResult]:
        """Run multiple checks.
        
        Args:
            checks: List of checks to run
            resources: Resources to check
            region: Optional region filter
            
        Returns:
            Combined list of check results
        """
        results = []
        
        for check in checks:
            check_results = await self.run_check(check, resources, region)
            results.extend(check_results)
        
        return results