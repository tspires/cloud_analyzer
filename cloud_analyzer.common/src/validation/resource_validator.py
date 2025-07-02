"""Resource data validation utilities."""

import logging
from typing import List, Dict, Any, Optional, Tuple
import re

from ..models.base import CloudResource, CloudProvider, ResourceType

logger = logging.getLogger(__name__)


class ResourceValidator:
    """Validator for cloud resource data quality and consistency."""
    
    def __init__(self):
        """Initialize validator."""
        self.validation_errors = []
        self.validation_warnings = []
    
    def validate_resource(self, resource: CloudResource) -> Tuple[bool, List[str]]:
        """Validate a cloud resource."""
        errors = []
        
        # Validate required fields
        if not resource.id:
            errors.append("Missing resource ID")
        elif not self._is_valid_azure_resource_id(resource.id):
            errors.append(f"Invalid Azure resource ID format: {resource.id}")
        
        if not resource.name:
            errors.append("Missing resource name")
        elif not self._is_valid_resource_name(resource.name):
            errors.append(f"Invalid resource name format: {resource.name}")
        
        if not resource.resource_type:
            errors.append("Missing resource type")
        elif not self._is_valid_resource_type(resource.resource_type):
            errors.append(f"Unsupported resource type: {resource.resource_type}")
        
        if not resource.location:
            errors.append("Missing location")
        elif not self._is_valid_azure_location(resource.location):
            errors.append(f"Invalid Azure location: {resource.location}")
        
        if not resource.resource_group:
            errors.append("Missing resource group")
        elif not self._is_valid_resource_group_name(resource.resource_group):
            errors.append(f"Invalid resource group name: {resource.resource_group}")
        
        if not resource.subscription_id:
            errors.append("Missing subscription ID")
        elif not self._is_valid_subscription_id(resource.subscription_id):
            errors.append(f"Invalid subscription ID format: {resource.subscription_id}")
        
        # Validate provider
        if resource.provider != CloudProvider.AZURE:
            errors.append(f"Expected Azure provider, got {resource.provider}")
        
        # Validate tags
        if resource.tags:
            tag_errors = self._validate_tags(resource.tags)
            errors.extend(tag_errors)
        
        # Validate properties
        if resource.properties and not isinstance(resource.properties, dict):
            errors.append("Properties must be a dictionary")
        
        is_valid = len(errors) == 0
        return is_valid, errors
    
    def validate_resource_batch(self, resources: List[CloudResource]) -> Dict[str, Any]:
        """Validate a batch of resources."""
        results = {
            'total_count': len(resources),
            'valid_count': 0,
            'invalid_count': 0,
            'errors': [],
            'warnings': [],
            'validation_summary': {}
        }
        
        if not resources:
            results['warnings'].append("Empty resource batch")
            return results
        
        # Track for duplicate detection
        seen_ids = set()
        duplicate_count = 0
        
        # Validate individual resources
        for i, resource in enumerate(resources):
            is_valid, errors = self.validate_resource(resource)
            
            if is_valid:
                results['valid_count'] += 1
            else:
                results['invalid_count'] += 1
                for error in errors:
                    results['errors'].append(f"Resource {i} ({resource.name}): {error}")
            
            # Check for duplicates
            if resource.id in seen_ids:
                duplicate_count += 1
                results['warnings'].append(f"Duplicate resource ID: {resource.id}")
            else:
                seen_ids.add(resource.id)
        
        # Batch-level validation
        batch_warnings = self._validate_batch_consistency(resources)
        results['warnings'].extend(batch_warnings)
        
        # Generate summary
        results['validation_summary'] = {
            'success_rate': results['valid_count'] / results['total_count'] if results['total_count'] > 0 else 0,
            'duplicate_count': duplicate_count,
            'has_errors': results['invalid_count'] > 0,
            'has_warnings': len(results['warnings']) > 0,
            'resource_types': len(set(r.resource_type for r in resources)),
            'resource_groups': len(set(r.resource_group for r in resources)),
            'subscriptions': len(set(r.subscription_id for r in resources))
        }
        
        return results
    
    def _is_valid_azure_resource_id(self, resource_id: str) -> bool:
        """Validate Azure resource ID format."""
        # Azure resource ID pattern: /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/{resourceProviderNamespace}/{resourceType}/{resourceName}
        pattern = r'^/subscriptions/[a-f0-9\-]{36}/resourceGroups/[^/]+/providers/[^/]+/[^/]+/.+$'
        return bool(re.match(pattern, resource_id, re.IGNORECASE))
    
    def _is_valid_resource_name(self, name: str) -> bool:
        """Validate resource name format."""
        # Azure resource names: 1-64 characters, alphanumeric, hyphens, underscores, periods, parentheses
        if not name or len(name) > 64:
            return False
        
        pattern = r'^[a-zA-Z0-9\-_\.\(\)]+$'
        return bool(re.match(pattern, name))
    
    def _is_valid_resource_type(self, resource_type: str) -> bool:
        """Validate resource type."""
        try:
            # Check if it's a known resource type
            known_types = [rt.value for rt in ResourceType]
            return resource_type in known_types
        except:
            # Fallback to basic format validation
            pattern = r'^[A-Za-z0-9\.]+/[A-Za-z0-9\.]+$'
            return bool(re.match(pattern, resource_type))
    
    def _is_valid_azure_location(self, location: str) -> bool:
        """Validate Azure location."""
        # Common Azure locations (not exhaustive, but covers most cases)
        common_locations = {
            'eastus', 'eastus2', 'westus', 'westus2', 'westus3', 'centralus', 'northcentralus', 'southcentralus',
            'westcentralus', 'canadacentral', 'canadaeast', 'brazilsouth', 'northeurope', 'westeurope',
            'uksouth', 'ukwest', 'francecentral', 'francesouth', 'germanywestcentral', 'germanynorth',
            'norwayeast', 'norwaywest', 'switzerlandnorth', 'switzerlandwest', 'swedencentral', 'swedensouth',
            'eastasia', 'southeastasia', 'japaneast', 'japanwest', 'australiaeast', 'australiasoutheast',
            'australiacentral', 'australiacentral2', 'koreacentral', 'koreasouth', 'southindia', 'centralindia',
            'westindia', 'southafricanorth', 'southafricawest', 'uaenorth', 'uaecentral'
        }
        
        return location.lower() in common_locations or self._is_valid_location_format(location)
    
    def _is_valid_location_format(self, location: str) -> bool:
        """Validate location format (fallback for new regions)."""
        # Basic validation: lowercase letters and numbers, reasonable length
        pattern = r'^[a-z0-9]+$'
        return bool(re.match(pattern, location)) and 2 <= len(location) <= 50
    
    def _is_valid_resource_group_name(self, rg_name: str) -> bool:
        """Validate resource group name."""
        # Azure RG names: 1-90 characters, alphanumeric, hyphens, underscores, periods, parentheses
        # Cannot end with period
        if not rg_name or len(rg_name) > 90 or rg_name.endswith('.'):
            return False
        
        pattern = r'^[a-zA-Z0-9\-_\.\(\)]+$'
        return bool(re.match(pattern, rg_name))
    
    def _is_valid_subscription_id(self, subscription_id: str) -> bool:
        """Validate Azure subscription ID (GUID format)."""
        pattern = r'^[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}$'
        return bool(re.match(pattern, subscription_id, re.IGNORECASE))
    
    def _validate_tags(self, tags: Dict[str, str]) -> List[str]:
        """Validate resource tags."""
        errors = []
        
        if len(tags) > 50:  # Azure limit
            errors.append("Too many tags (max 50)")
        
        for key, value in tags.items():
            if not isinstance(key, str) or not isinstance(value, str):
                errors.append(f"Tag key/value must be strings: {key}={value}")
                continue
                
            if len(key) > 512:  # Azure limit
                errors.append(f"Tag key too long (max 512 chars): {key}")
            
            if len(value) > 256:  # Azure limit
                errors.append(f"Tag value too long (max 256 chars): {key}={value}")
            
            # Check for reserved tag prefixes
            reserved_prefixes = ['microsoft', 'azure', 'windows']
            if any(key.lower().startswith(prefix) for prefix in reserved_prefixes):
                errors.append(f"Tag key uses reserved prefix: {key}")
        
        return errors
    
    def _validate_batch_consistency(self, resources: List[CloudResource]) -> List[str]:
        """Check for consistency issues within a batch."""
        warnings = []
        
        if len(resources) > 1000:  # Large batch warning
            warnings.append(f"Large batch size ({len(resources)} resources) may impact performance")
        
        # Check subscription consistency
        subscriptions = set(r.subscription_id for r in resources)
        if len(subscriptions) > 5:
            warnings.append(f"Resources span many subscriptions ({len(subscriptions)})")
        
        # Check for unusual resource type distribution
        type_counts = {}
        for resource in resources:
            type_counts[resource.resource_type] = type_counts.get(resource.resource_type, 0) + 1
        
        if len(type_counts) > 20:
            warnings.append(f"Many different resource types in batch ({len(type_counts)})")
        
        # Check for resources without tags (governance warning)
        untagged_count = sum(1 for r in resources if not r.tags)
        if untagged_count > len(resources) * 0.5:  # More than 50% untagged
            warnings.append(f"Many resources lack tags ({untagged_count}/{len(resources)})")
        
        return warnings
    
    def get_resource_quality_score(self, validation_result: Dict[str, Any]) -> float:
        """Calculate a resource data quality score (0-1)."""
        if validation_result['total_count'] == 0:
            return 0.0
        
        base_score = validation_result['validation_summary']['success_rate']
        
        # Bonus for good tagging practices
        if validation_result['total_count'] > 0:
            # Assuming we can infer tagging quality from warnings
            tagging_bonus = 0.1 if 'resources lack tags' not in str(validation_result['warnings']) else 0.0
        else:
            tagging_bonus = 0.0
        
        # Penalty for duplicates
        duplicate_penalty = min(validation_result['validation_summary']['duplicate_count'] * 0.05, 0.2)
        
        # Penalty for warnings
        warning_penalty = min(len(validation_result['warnings']) * 0.05, 0.2)
        
        final_score = max(0.0, min(1.0, base_score + tagging_bonus - duplicate_penalty - warning_penalty))
        return round(final_score, 2)