"""Validation utilities for Azure metrics collection."""
from datetime import datetime, timedelta
from typing import Optional, Tuple


def validate_resource_id(resource_id: str) -> None:
    """Validate Azure resource ID format.
    
    Args:
        resource_id: Azure resource ID to validate
        
    Raises:
        ValueError: If resource ID is invalid
    """
    if not resource_id:
        raise ValueError("Resource ID cannot be empty")
    
    if not resource_id.startswith('/'):
        raise ValueError("Resource ID must start with '/'")
    
    parts = resource_id.split('/')
    if len(parts) < 9:
        raise ValueError("Invalid resource ID format")
    
    required_parts = ['subscriptions', 'resourceGroups', 'providers']
    for part in required_parts:
        if part not in parts:
            raise ValueError(f"Resource ID missing required part: {part}")


def validate_time_range(time_range: Optional[Tuple[datetime, datetime]]) -> None:
    """Validate time range for metrics collection.
    
    Args:
        time_range: Optional tuple of (start, end) datetimes
        
    Raises:
        ValueError: If time range is invalid
    """
    if time_range is None:
        return
    
    if not isinstance(time_range, tuple) or len(time_range) != 2:
        raise ValueError("Time range must be a tuple of (start, end)")
    
    start, end = time_range
    
    if not isinstance(start, datetime) or not isinstance(end, datetime):
        raise ValueError("Time range must contain datetime objects")
    
    if start >= end:
        raise ValueError("Start time must be before end time")
    
    # Check if time range is not too large (e.g., max 90 days)
    max_days = 90
    if (end - start) > timedelta(days=max_days):
        raise ValueError(f"Time range cannot exceed {max_days} days")


def validate_aggregation(aggregation: str) -> None:
    """Validate aggregation type.
    
    Args:
        aggregation: Aggregation type to validate
        
    Raises:
        ValueError: If aggregation type is invalid
    """
    valid_aggregations = {"Average", "Maximum", "Minimum", "Total", "Count"}
    
    if aggregation not in valid_aggregations:
        raise ValueError(f"Invalid aggregation type. Must be one of: {valid_aggregations}")


def validate_retry_config(retry_count: int, retry_delay: float, timeout: float) -> None:
    """Validate retry configuration parameters.
    
    Args:
        retry_count: Number of retries
        retry_delay: Delay between retries in seconds
        timeout: Operation timeout in seconds
        
    Raises:
        ValueError: If any parameter is invalid
    """
    if retry_count < 0 or retry_count > 10:
        raise ValueError("Retry count must be between 0 and 10")
    
    if retry_delay < 0 or retry_delay > 60:
        raise ValueError("Retry delay must be between 0 and 60 seconds")
    
    if timeout < 1 or timeout > 300:
        raise ValueError("Timeout must be between 1 and 300 seconds")