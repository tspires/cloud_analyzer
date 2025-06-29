"""Unit tests for Azure compute metrics wrapper with mocked Azure imports."""
import pytest
from unittest.mock import AsyncMock, MagicMock, patch
import sys
import os
from datetime import datetime, timedelta, timezone
from enum import Enum

# Add the src directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..', 'src'))

# Mock Azure modules before importing our code
sys.modules['azure.core'] = MagicMock()
sys.modules['azure.core.exceptions'] = MagicMock()
sys.modules['azure.core.credentials'] = MagicMock()
sys.modules['azure.identity'] = MagicMock()
sys.modules['azure.mgmt.monitor'] = MagicMock()
sys.modules['azure.mgmt.monitor.models'] = MagicMock()
sys.modules['azure.mgmt.compute'] = MagicMock()
sys.modules['azure.mgmt.web'] = MagicMock()

# Create mock exceptions
class MockAzureError(Exception):
    pass

class MockClientAuthenticationError(MockAzureError):
    pass

class MockResourceNotFoundError(MockAzureError):
    pass

# Set up the exceptions
sys.modules['azure.core.exceptions'].AzureError = MockAzureError
sys.modules['azure.core.exceptions'].ClientAuthenticationError = MockClientAuthenticationError
sys.modules['azure.core.exceptions'].ResourceNotFoundError = MockResourceNotFoundError

# Now we can import our modules
from src.azure.compute import (
    AzureComputeMetricsWrapper,
    ComputeMetrics,
    ComputeRecommendation,
    ComputeResourceType,
)


class TestAzureComputeMetricsWrapper:
    """Test cases for the unified compute metrics wrapper."""
    
    @pytest.fixture
    def wrapper(self):
        """Create wrapper instance for testing."""
        wrapper = AzureComputeMetricsWrapper(
            subscription_id="test-subscription",
            retry_count=2,
            retry_delay=0.1,
            timeout=5.0,
            concurrent_requests=5
        )
        return wrapper
    
    @pytest.fixture
    def sample_vm_metrics(self):
        """Create sample VM metrics data."""
        return ComputeMetrics(
            resource_id="/subscriptions/test/resourceGroups/rg/providers/Microsoft.Compute/virtualMachines/vm1",
            resource_name="vm1",
            resource_type=ComputeResourceType.VIRTUAL_MACHINE,
            resource_group="test-rg",
            location="eastus",
            time_range=(datetime.now(timezone.utc) - timedelta(days=7), datetime.now(timezone.utc)),
            cpu_percent_avg=15.5,
            cpu_percent_max=45.0,
            cpu_percent_p95=35.0,
            memory_percent_avg=60.0,
            memory_percent_max=75.0,
            network_in_bytes_total=1000000.0,
            network_out_bytes_total=500000.0,
            tags={"env": "prod", "owner": "team1"},
            sku={"size": "Standard_D2s_v3", "tier": "Standard"},
            state="running"
        )
    
    @pytest.fixture
    def sample_app_metrics(self):
        """Create sample App Service metrics data."""
        return ComputeMetrics(
            resource_id="/subscriptions/test/resourceGroups/rg/providers/Microsoft.Web/sites/app1",
            resource_name="app1",
            resource_type=ComputeResourceType.APP_SERVICE,
            resource_group="test-rg",
            location="eastus",
            time_range=(datetime.now(timezone.utc) - timedelta(days=7), datetime.now(timezone.utc)),
            cpu_percent_avg=25.0,
            cpu_percent_max=60.0,
            memory_percent_avg=40.0,
            memory_percent_max=55.0,
            request_count=10000,
            error_count=50,
            response_time_avg=250.0,
            tags={"env": "prod"},
            sku={"tier": "Standard", "size": "S1"},
            state="Running"
        )
    
    def test_initialization(self):
        """Test wrapper initialization."""
        wrapper = AzureComputeMetricsWrapper(
            subscription_id="test-sub",
            retry_count=5,
            retry_delay=2.0,
            timeout=60.0,
            concurrent_requests=20
        )
        
        assert wrapper.subscription_id == "test-sub"
        assert wrapper.retry_count == 5
        assert wrapper.retry_delay == 2.0
        assert wrapper.timeout == 60.0
        assert wrapper.concurrent_requests == 20
    
    def test_set_subscription(self, wrapper):
        """Test setting subscription ID."""
        new_sub = "new-subscription-id"
        wrapper.set_subscription(new_sub)
        
        assert wrapper.subscription_id == new_sub
        assert wrapper._vm_client is None
        assert wrapper._app_service_client is None
    
    def test_get_resource_type(self, wrapper):
        """Test resource type detection."""
        # Virtual Machine
        vm_id = "/subscriptions/test/resourceGroups/rg/providers/Microsoft.Compute/virtualMachines/vm1"
        assert wrapper._get_resource_type(vm_id) == ComputeResourceType.VIRTUAL_MACHINE
        
        # App Service
        app_id = "/subscriptions/test/resourceGroups/rg/providers/Microsoft.Web/sites/app1"
        assert wrapper._get_resource_type(app_id) == ComputeResourceType.APP_SERVICE
        
        # Unknown type should raise error
        unknown_id = "/subscriptions/test/resourceGroups/rg/providers/Microsoft.Unknown/resources/res1"
        with pytest.raises(ValueError):
            wrapper._get_resource_type(unknown_id)
    
    def test_validate_subscription_error(self):
        """Test validation when subscription not set."""
        wrapper = AzureComputeMetricsWrapper()
        
        with pytest.raises(ValueError, match="Subscription ID not set"):
            wrapper._validate_subscription()
    
    @pytest.mark.asyncio
    async def test_retry_operation_success(self, wrapper):
        """Test retry operation with immediate success."""
        async def mock_operation():
            return "success"
        
        result = await wrapper._retry_operation(mock_operation)
        assert result == "success"
    
    @pytest.mark.asyncio
    async def test_retry_operation_eventual_success(self, wrapper):
        """Test retry operation that succeeds after failure."""
        attempt_count = 0
        
        async def mock_operation():
            nonlocal attempt_count
            attempt_count += 1
            if attempt_count < 2:
                raise Exception("Temporary failure")
            return "success"
        
        result = await wrapper._retry_operation(mock_operation)
        assert result == "success"
        assert attempt_count == 2
    
    @pytest.mark.asyncio
    async def test_error_handler_authentication_error(self, wrapper):
        """Test error handler with authentication error."""
        with pytest.raises(MockAzureError, match="Authentication failed"):
            async with wrapper._error_handler("test_op", "test_resource"):
                raise MockClientAuthenticationError("Invalid credentials")
    
    @pytest.mark.asyncio
    async def test_get_compute_metrics_vm(self, wrapper, sample_vm_metrics):
        """Test getting VM metrics."""
        # Mock the VM client
        mock_client = MagicMock()
        mock_client.get_compute_metrics = AsyncMock(return_value=sample_vm_metrics)
        
        with patch.object(type(wrapper), 'vm_metrics_client', new_callable=lambda: property(lambda self: mock_client)):
            result = await wrapper.get_compute_metrics(sample_vm_metrics.resource_id)
            
            assert result == sample_vm_metrics
            mock_client.get_compute_metrics.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_get_compute_metrics_app_service(self, wrapper, sample_app_metrics):
        """Test getting App Service metrics."""
        # Mock the App Service client
        mock_client = MagicMock()
        mock_client.get_compute_metrics = AsyncMock(return_value=sample_app_metrics)
        
        with patch.object(type(wrapper), 'app_service_metrics_client', new_callable=lambda: property(lambda self: mock_client)):
            result = await wrapper.get_compute_metrics(sample_app_metrics.resource_id)
            
            assert result == sample_app_metrics
            mock_client.get_compute_metrics.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_list_all_compute_resources(self, wrapper):
        """Test listing all compute resources."""
        mock_vms = [{"id": "vm1", "name": "vm1", "location": "eastus"}]
        mock_apps = [{"id": "app1", "name": "app1", "location": "westus"}]
        
        # Mock clients
        mock_vm_client = MagicMock()
        mock_vm_client.list_resources = AsyncMock(return_value=mock_vms)
        mock_app_client = MagicMock()
        mock_app_client.list_resources = AsyncMock(return_value=mock_apps)
        
        with patch.object(type(wrapper), 'vm_metrics_client', new_callable=lambda: property(lambda self: mock_vm_client)):
            with patch.object(type(wrapper), 'app_service_metrics_client', new_callable=lambda: property(lambda self: mock_app_client)):
                result = await wrapper.list_all_compute_resources()
                
                assert result['virtual_machines'] == mock_vms
                assert result['app_services'] == mock_apps
    
    @pytest.mark.asyncio
    async def test_get_all_compute_metrics(self, wrapper, sample_vm_metrics, sample_app_metrics):
        """Test getting metrics for all compute resources."""
        mock_resources = {
            'virtual_machines': [{"id": sample_vm_metrics.resource_id}],
            'app_services': [{"id": sample_app_metrics.resource_id}]
        }
        
        with patch.object(wrapper, 'list_all_compute_resources', AsyncMock(return_value=mock_resources)):
            with patch.object(wrapper, 'get_compute_metrics') as mock_get_metrics:
                # Set up side effects for different resource IDs
                mock_get_metrics.side_effect = [sample_vm_metrics, sample_app_metrics]
                
                result = await wrapper.get_all_compute_metrics()
                
                assert len(result) == 2
                assert result[0] == sample_vm_metrics
                assert result[1] == sample_app_metrics
    
    @pytest.mark.asyncio
    async def test_get_all_compute_metrics_with_filters(self, wrapper, sample_vm_metrics):
        """Test getting metrics with resource filters."""
        mock_resources = {
            'virtual_machines': [
                {"id": sample_vm_metrics.resource_id, "resource_group": "test-rg", "tags": {"env": "prod"}},
                {"id": "vm2", "resource_group": "other-rg", "tags": {"env": "dev"}}
            ],
            'app_services': []
        }
        
        resource_filter = {
            'resource_groups': ['test-rg'],
            'tags': {'env': 'prod'}
        }
        
        with patch.object(wrapper, 'list_all_compute_resources', AsyncMock(return_value=mock_resources)):
            with patch.object(wrapper, 'get_compute_metrics', AsyncMock(return_value=sample_vm_metrics)):
                result = await wrapper.get_all_compute_metrics(resource_filter=resource_filter)
                
                # Should only get metrics for the filtered resource
                assert len(result) == 1
                assert result[0] == sample_vm_metrics
    
    @pytest.mark.asyncio
    async def test_get_optimization_recommendations_single(self, wrapper, sample_vm_metrics):
        """Test getting recommendations for single resource."""
        mock_recommendations = [
            ComputeRecommendation(
                resource_id=sample_vm_metrics.resource_id,
                resource_name="vm1",
                recommendation_type="resize",
                severity="high",
                description="Low CPU usage",
                impact="cost"
            )
        ]
        
        # Mock VM client
        mock_client = MagicMock()
        mock_client.get_recommendations = AsyncMock(return_value=mock_recommendations)
        
        with patch.object(type(wrapper), 'vm_metrics_client', new_callable=lambda: property(lambda self: mock_client)):
            result = await wrapper.get_optimization_recommendations(
                resource_id=sample_vm_metrics.resource_id,
                metrics=sample_vm_metrics
            )
            
            assert result == mock_recommendations
    
    @pytest.mark.asyncio
    async def test_get_cost_optimization_summary(self, wrapper, sample_vm_metrics):
        """Test getting cost optimization summary."""
        mock_recommendations = {
            "vm1": [
                ComputeRecommendation(
                    resource_id=sample_vm_metrics.resource_id,
                    resource_name="vm1",
                    recommendation_type="resize",
                    severity="high",
                    description="Low CPU usage",
                    impact="cost",
                    estimated_monthly_savings=50.0,
                    estimated_annual_savings=600.0
                )
            ]
        }
        
        with patch.object(wrapper, 'get_optimization_recommendations', AsyncMock(return_value=mock_recommendations)):
            with patch.object(wrapper, 'get_all_compute_metrics', AsyncMock(return_value=[sample_vm_metrics])):
                summary = await wrapper.get_cost_optimization_summary()
                
                assert summary['total_resources_analyzed'] == 1
                assert summary['resources_with_recommendations'] == 1
                assert summary['total_recommendations'] == 1
                assert summary['estimated_annual_savings'] == 600.0
                assert summary['recommendations_by_type']['resize'] == 1
                assert summary['recommendations_by_severity']['high'] == 1
                assert len(summary['top_opportunities']) == 1
    
    @pytest.mark.asyncio
    async def test_close(self, wrapper):
        """Test closing the wrapper."""
        await wrapper.close()  # Should not raise any errors


class TestComputeMetrics:
    """Test cases for ComputeMetrics dataclass."""
    
    def test_compute_metrics_creation(self):
        """Test creating ComputeMetrics with all fields."""
        now = datetime.now(timezone.utc)
        week_ago = now - timedelta(days=7)
        
        metrics = ComputeMetrics(
            resource_id="/subscriptions/test/resourceGroups/rg/providers/Microsoft.Compute/virtualMachines/vm1",
            resource_name="vm1",
            resource_type=ComputeResourceType.VIRTUAL_MACHINE,
            resource_group="test-rg",
            location="eastus",
            time_range=(week_ago, now),
            cpu_percent_avg=45.5,
            cpu_percent_max=78.9,
            cpu_percent_p95=65.0,
            memory_percent_avg=32.1,
            memory_percent_max=45.6,
            network_in_bytes_total=1000000.0,
            network_out_bytes_total=500000.0,
            disk_read_bytes_total=2000000.0,
            disk_write_bytes_total=1500000.0,
            availability_percent=99.9,
            instance_count=2,
            tags={"env": "prod"},
            sku={"size": "Standard_D2s_v3"},
            state="running",
            additional_metrics={"custom": "value"}
        )
        
        assert metrics.resource_name == "vm1"
        assert metrics.cpu_percent_avg == 45.5
        assert metrics.memory_percent_avg == 32.1
        assert metrics.network_in_bytes_total == 1000000.0
        assert metrics.tags == {"env": "prod"}
        assert metrics.additional_metrics == {"custom": "value"}
    
    def test_compute_metrics_minimal(self):
        """Test creating ComputeMetrics with minimal fields."""
        now = datetime.now(timezone.utc)
        
        metrics = ComputeMetrics(
            resource_id="test-id",
            resource_name="test-resource",
            resource_type=ComputeResourceType.VIRTUAL_MACHINE,
            resource_group="test-rg",
            location="eastus",
            time_range=(now, now),
            cpu_percent_avg=50.0,
            cpu_percent_max=60.0
        )
        
        assert metrics.cpu_percent_avg == 50.0
        assert metrics.cpu_percent_max == 60.0
        assert metrics.memory_percent_avg is None
        assert metrics.tags == {}
        assert metrics.additional_metrics == {}


class TestComputeRecommendation:
    """Test cases for ComputeRecommendation dataclass."""
    
    def test_recommendation_creation(self):
        """Test creating ComputeRecommendation."""
        rec = ComputeRecommendation(
            resource_id="test-id",
            resource_name="test-vm",
            recommendation_type="resize",
            severity="high",
            description="VM has low CPU utilization",
            impact="cost",
            estimated_monthly_savings=100.0,
            estimated_annual_savings=1200.0,
            action_details={"current_size": "D4s_v3", "recommended_size": "D2s_v3"}
        )
        
        assert rec.resource_name == "test-vm"
        assert rec.recommendation_type == "resize"
        assert rec.severity == "high"
        assert rec.estimated_annual_savings == 1200.0
        assert rec.action_details["recommended_size"] == "D2s_v3"