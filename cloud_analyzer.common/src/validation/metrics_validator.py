"""Metrics data validation utilities."""

import logging
from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime, timedelta
import re

from ..models.metrics import MetricData, MetricDefinition, MetricAggregationType
from ..models.base import CloudResource

logger = logging.getLogger(__name__)


class MetricsValidator:
    """Validator for metrics data quality and consistency."""
    
    def __init__(self, enable_strict_validation: bool = True):
        """Initialize validator."""
        self.enable_strict_validation = enable_strict_validation
        self.validation_errors = []
        self.validation_warnings = []
    
    def validate_metric_data(self, metric_data: MetricData) -> Tuple[bool, List[str]]:
        """Validate a single metric data point."""
        errors = []
        
        # Validate required fields
        if not metric_data.resource_id:
            errors.append("Missing resource_id")
        
        if not metric_data.metric_name:
            errors.append("Missing metric_name")
        
        if metric_data.timestamp is None:
            errors.append("Missing timestamp")
        
        if metric_data.value is None:
            errors.append("Missing value")
        
        # Validate value ranges
        if metric_data.value is not None:
            if not isinstance(metric_data.value, (int, float)):
                errors.append(f"Value must be numeric, got {type(metric_data.value)}")
            elif metric_data.value < 0 and not self._is_negative_allowed(metric_data.metric_name):
                errors.append(f"Negative value not allowed for metric {metric_data.metric_name}")
            elif abs(metric_data.value) > 1e15:  # Reasonable upper limit
                errors.append(f"Value {metric_data.value} exceeds reasonable range")
        
        # Validate timestamp
        if metric_data.timestamp:
            now = datetime.utcnow()
            if metric_data.timestamp > now + timedelta(minutes=5):
                errors.append("Timestamp is in the future")
            elif metric_data.timestamp < now - timedelta(days=365):
                errors.append("Timestamp is more than 1 year old")
        
        # Validate metric name format
        if metric_data.metric_name and not self._is_valid_metric_name(metric_data.metric_name):
            errors.append(f"Invalid metric name format: {metric_data.metric_name}")
        
        # Validate unit consistency
        if metric_data.unit and not self._is_valid_unit(metric_data.unit):
            errors.append(f"Invalid unit: {metric_data.unit}")
        
        # Validate dimensions
        if metric_data.dimensions:
            dimension_errors = self._validate_dimensions(metric_data.dimensions)
            errors.extend(dimension_errors)
        
        is_valid = len(errors) == 0
        return is_valid, errors
    
    def validate_metric_batch(self, metrics_batch: List[MetricData]) -> Dict[str, Any]:
        """Validate a batch of metric data points."""
        results = {
            'total_count': len(metrics_batch),
            'valid_count': 0,
            'invalid_count': 0,
            'errors': [],
            'warnings': [],
            'validation_summary': {}
        }
        
        if not metrics_batch:
            results['warnings'].append("Empty metrics batch")
            return results
        
        # Validate individual metrics
        for i, metric_data in enumerate(metrics_batch):
            is_valid, errors = self.validate_metric_data(metric_data)
            
            if is_valid:
                results['valid_count'] += 1
            else:
                results['invalid_count'] += 1
                for error in errors:
                    results['errors'].append(f"Metric {i}: {error}")
        
        # Check for batch-level issues
        batch_warnings = self._validate_batch_consistency(metrics_batch)
        results['warnings'].extend(batch_warnings)
        
        # Generate summary
        results['validation_summary'] = {
            'success_rate': results['valid_count'] / results['total_count'] if results['total_count'] > 0 else 0,
            'has_errors': results['invalid_count'] > 0,
            'has_warnings': len(results['warnings']) > 0
        }
        
        return results
    
    def validate_metric_definition(self, metric_def: MetricDefinition) -> Tuple[bool, List[str]]:
        """Validate a metric definition."""
        errors = []
        
        # Required fields
        if not metric_def.name:
            errors.append("Missing metric name")
        
        if not metric_def.resource_type:
            errors.append("Missing resource type")
        
        if not metric_def.unit:
            errors.append("Missing unit")
        
        # Validate aggregation types
        if not metric_def.aggregation_types:
            errors.append("Missing aggregation types")
        else:
            for agg_type in metric_def.aggregation_types:
                if not isinstance(agg_type, MetricAggregationType):
                    errors.append(f"Invalid aggregation type: {agg_type}")
        
        # Validate retention period
        if metric_def.retention_days <= 0:
            errors.append("Retention days must be positive")
        elif metric_def.retention_days > 2555:  # ~7 years
            errors.append("Retention period too long (max 7 years)")
        
        # Validate collection interval
        if metric_def.collection_interval_minutes <= 0:
            errors.append("Collection interval must be positive")
        elif metric_def.collection_interval_minutes > 1440:  # 24 hours
            errors.append("Collection interval too long (max 24 hours)")
        
        is_valid = len(errors) == 0
        return is_valid, errors
    
    def _is_negative_allowed(self, metric_name: str) -> bool:
        """Check if negative values are allowed for a metric."""
        # Some metrics can have negative values
        negative_allowed_patterns = [
            'temperature',
            'change',
            'delta',
            'difference',
            'offset'
        ]
        
        metric_lower = metric_name.lower()
        return any(pattern in metric_lower for pattern in negative_allowed_patterns)
    
    def _is_valid_metric_name(self, metric_name: str) -> bool:
        """Validate metric name format."""
        # Allow alphanumeric, spaces, dashes, underscores, dots, and parentheses
        pattern = r'^[a-zA-Z0-9\s\-_\.\(\)]+$'
        return bool(re.match(pattern, metric_name)) and len(metric_name) <= 255
    
    def _is_valid_unit(self, unit: str) -> bool:
        """Validate unit format."""
        # Common Azure Monitor units
        valid_units = {
            'Percent', 'Count', 'Bytes', 'Seconds', 'Milliseconds', 'BytesPerSecond',
            'CountPerSecond', 'Cores', 'MilliCores', 'NanoCores', 'BitsPerSecond',
            'Unspecified', 'None'
        }
        
        return unit in valid_units or len(unit) <= 50
    
    def _validate_dimensions(self, dimensions: Dict[str, str]) -> List[str]:
        """Validate metric dimensions."""
        errors = []
        
        if len(dimensions) > 10:  # Azure Monitor limit
            errors.append("Too many dimensions (max 10)")
        
        for key, value in dimensions.items():
            if not isinstance(key, str) or not isinstance(value, str):
                errors.append(f"Dimension key/value must be strings: {key}={value}")
            elif len(key) > 100:
                errors.append(f"Dimension key too long: {key}")
            elif len(value) > 100:
                errors.append(f"Dimension value too long: {value}")
        
        return errors
    
    def _validate_batch_consistency(self, metrics_batch: List[MetricData]) -> List[str]:
        """Check for consistency issues within a batch."""
        warnings = []
        
        if len(metrics_batch) > 20000:  # Large batch warning
            warnings.append(f"Large batch size ({len(metrics_batch)} metrics) may impact performance")
        
        # Check for duplicate timestamps for same resource/metric
        seen_combinations = set()
        duplicates = 0
        
        for metric in metrics_batch:
            key = (metric.resource_id, metric.metric_name, metric.timestamp.isoformat())
            if key in seen_combinations:
                duplicates += 1
            else:
                seen_combinations.add(key)
        
        if duplicates > 0:
            warnings.append(f"Found {duplicates} duplicate metric entries")
        
        # Check timestamp spread
        if metrics_batch:
            timestamps = [m.timestamp for m in metrics_batch if m.timestamp]
            if timestamps:
                min_time = min(timestamps)
                max_time = max(timestamps)
                time_span = (max_time - min_time).total_seconds() / 3600  # hours
                
                if time_span > 168:  # 1 week
                    warnings.append(f"Large time span in batch: {time_span:.1f} hours")
        
        # Check for missing collection run IDs
        missing_run_id = sum(1 for m in metrics_batch if not m.collection_run_id)
        if missing_run_id > 0:
            warnings.append(f"{missing_run_id} metrics missing collection_run_id")
        
        return warnings
    
    def get_data_quality_score(self, validation_result: Dict[str, Any]) -> float:
        """Calculate a data quality score (0-1) based on validation results."""
        if validation_result['total_count'] == 0:
            return 0.0
        
        base_score = validation_result['validation_summary']['success_rate']
        
        # Penalize for warnings
        warning_penalty = min(len(validation_result['warnings']) * 0.1, 0.3)
        
        # Penalize for high error rate
        error_rate = validation_result['invalid_count'] / validation_result['total_count']
        error_penalty = error_rate * 0.5
        
        final_score = max(0.0, base_score - warning_penalty - error_penalty)
        return round(final_score, 2)