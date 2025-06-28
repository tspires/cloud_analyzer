"""Registry for optimization checks."""

from typing import Dict, List, Optional, Set

from models import CheckType, CloudProvider
from checks.base import Check


class CheckRegistry:
    """Registry for managing optimization checks."""
    
    def __init__(self) -> None:
        """Initialize check registry."""
        self._checks: Dict[str, Check] = {}
        self._checks_by_type: Dict[CheckType, List[Check]] = {}
        self._checks_by_provider: Dict[CloudProvider, List[Check]] = {}
    
    def register(self, check: Check) -> None:
        """Register a check.
        
        Args:
            check: Check instance to register
            
        Raises:
            ValueError: If check with same name already registered
        """
        if check.name in self._checks:
            raise ValueError(f"Check '{check.name}' already registered")
        
        self._checks[check.name] = check
        
        # Index by type
        if check.check_type not in self._checks_by_type:
            self._checks_by_type[check.check_type] = []
        self._checks_by_type[check.check_type].append(check)
        
        # Index by provider
        for provider in check.supported_providers:
            if provider not in self._checks_by_provider:
                self._checks_by_provider[provider] = []
            self._checks_by_provider[provider].append(check)
    
    def get(self, name: str) -> Optional[Check]:
        """Get a check by name.
        
        Args:
            name: Check name
            
        Returns:
            Check instance or None
        """
        return self._checks.get(name)
    
    def list_all(self) -> List[Check]:
        """List all registered checks.
        
        Returns:
            List of all checks
        """
        return list(self._checks.values())
    
    def list_by_type(self, check_type: CheckType) -> List[Check]:
        """List checks by type.
        
        Args:
            check_type: Type of check
            
        Returns:
            List of checks of given type
        """
        return self._checks_by_type.get(check_type, [])
    
    def list_by_provider(self, provider: CloudProvider) -> List[Check]:
        """List checks by provider.
        
        Args:
            provider: Cloud provider
            
        Returns:
            List of checks supporting given provider
        """
        return self._checks_by_provider.get(provider, [])
    
    def list_by_types(self, check_types: Set[CheckType]) -> List[Check]:
        """List checks by multiple types.
        
        Args:
            check_types: Set of check types
            
        Returns:
            List of checks matching any of the given types
        """
        checks = []
        for check_type in check_types:
            checks.extend(self.list_by_type(check_type))
        return list(set(checks))  # Remove duplicates


# Global registry instance
check_registry = CheckRegistry()