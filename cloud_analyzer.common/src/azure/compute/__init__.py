"""Azure compute metrics collection package."""
from .app_services import AppServiceMetricsClient
from .base import (
    AzureComputeMetricsClient,
    ComputeMetrics,
    ComputeRecommendation,
    ComputeResourceType,
)
from .client import AzureComputeMetricsWrapper
from .virtual_machines import VirtualMachineMetricsClient

__all__ = [
    'AzureComputeMetricsClient',
    'AzureComputeMetricsWrapper',
    'ComputeMetrics',
    'ComputeRecommendation',
    'ComputeResourceType',
    'VirtualMachineMetricsClient',
    'AppServiceMetricsClient',
]