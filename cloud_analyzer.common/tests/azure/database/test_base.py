"""Unit tests for base database metrics classes."""
from datetime import datetime, timedelta
from unittest.mock import MagicMock, patch

import pytest
from azure.core.exceptions import AzureError
from azure.mgmt.monitor.models import MetricValue

from src.azure.database.base import AzureDatabaseMetricsClient, DatabaseMetrics


class MockDatabaseClient(AzureDatabaseMetricsClient):
    """Mock implementation for testing base class."""
    
    async def get_database_metrics(self, resource_id, time_range=None, aggregation="Average", interval=None):
        return DatabaseMetrics(
            resource_id=resource_id,
            database_name="test-db",
            server_name="test-server",
            resource_group="test-rg",
            database_type="Test Database",
            time_range=time_range or self._get_default_time_range(),
            cpu_percent_avg=50.0,
            cpu_percent_max=80.0
        )
    
    async def list_databases(self):
        return [{"id": "test-db", "name": "test-db"}]


class TestDatabaseMetrics:
    """Test cases for DatabaseMetrics dataclass."""
    
    def test_database_metrics_creation(self):
        """Test creating DatabaseMetrics instance."""
        now = datetime.utcnow()
        week_ago = now - timedelta(days=7)
        
        metrics = DatabaseMetrics(
            resource_id="/subscriptions/test/resourceGroups/rg/providers/Test/databases/db",
            database_name="test-db",
            server_name="test-server",
            resource_group="test-rg",
            database_type="Test Database",
            time_range=(week_ago, now),
            cpu_percent_avg=45.5,
            cpu_percent_max=78.9,
            memory_percent_avg=32.1,
            memory_percent_max=45.6
        )
        
        assert metrics.database_name == "test-db"
        assert metrics.cpu_percent_avg == 45.5
        assert metrics.cpu_percent_max == 78.9
        assert metrics.memory_percent_avg == 32.1
        assert metrics.memory_percent_max == 45.6
    
    def test_database_metrics_optional_fields(self):
        """Test DatabaseMetrics with optional fields."""
        now = datetime.utcnow()
        
        metrics = DatabaseMetrics(
            resource_id="test-id",
            database_name="test-db",
            server_name="test-server",
            resource_group="test-rg",
            database_type="Test",
            time_range=(now, now),
            cpu_percent_avg=50.0,
            cpu_percent_max=60.0,
            additional_metrics={"custom": "value"}
        )
        
        assert metrics.memory_percent_avg is None
        assert metrics.dtu_percent_avg is None
        assert metrics.additional_metrics == {"custom": "value"}


class TestAzureDatabaseMetricsClient:
    """Test cases for AzureDatabaseMetricsClient base class."""
    
    @pytest.fixture
    def mock_credential(self):
        """Create mock credential."""
        return MagicMock()
    
    @pytest.fixture
    def client(self, mock_credential):
        """Create test client instance."""
        return MockDatabaseClient(
            credential=mock_credential,
            subscription_id="test-subscription"
        )
    
    def test_initialization(self, mock_credential):
        """Test client initialization."""
        client = MockDatabaseClient(
            credential=mock_credential,
            subscription_id="test-sub"
        )
        
        assert client.credential == mock_credential
        assert client.subscription_id == "test-sub"
        assert client._monitor_client is None
    
    def test_monitor_client_lazy_initialization(self, client):
        """Test lazy initialization of monitor client."""
        with patch('src.azure.database.base.MonitorManagementClient') as mock_monitor:
            mock_instance = MagicMock()
            mock_monitor.return_value = mock_instance
            
            # First access creates client
            monitor = client.monitor_client
            assert monitor == mock_instance
            mock_monitor.assert_called_once_with(
                credential=client.credential,
                subscription_id=client.subscription_id
            )
            
            # Second access returns cached client
            monitor2 = client.monitor_client
            assert monitor2 == mock_instance
            assert mock_monitor.call_count == 1
    
    def test_get_default_time_range(self, client):
        """Test default time range generation."""
        start, end = client._get_default_time_range(days=7)
        
        assert isinstance(start, datetime)
        assert isinstance(end, datetime)
        assert (end - start).days == 7
        assert end <= datetime.utcnow()
    
    def test_format_timespan(self, client):
        """Test timespan formatting for Azure Monitor API."""
        end = datetime(2024, 1, 1, 12, 0, 0)
        start = end - timedelta(hours=1)
        
        timespan = client._format_timespan((start, end))
        
        assert timespan == "2024-01-01T11:00:00Z/2024-01-01T12:00:00Z"
    
    def test_calculate_metric_aggregates_average(self, client):
        """Test metric aggregation with average values."""
        metric_values = [
            MagicMock(average=10.0, maximum=15.0),
            MagicMock(average=20.0, maximum=25.0),
            MagicMock(average=30.0, maximum=35.0)
        ]
        
        avg, max_val = client._calculate_metric_aggregates(metric_values, "Average")
        
        assert avg == 20.0  # (10 + 20 + 30) / 3
        assert max_val == 30.0  # max of averages
    
    def test_calculate_metric_aggregates_maximum(self, client):
        """Test metric aggregation with maximum values."""
        metric_values = [
            MagicMock(maximum=15.0),
            MagicMock(maximum=25.0),
            MagicMock(maximum=35.0)
        ]
        
        avg, max_val = client._calculate_metric_aggregates(metric_values, "Maximum")
        
        assert avg == 25.0  # (15 + 25 + 35) / 3
        assert max_val == 35.0
    
    def test_calculate_metric_aggregates_empty(self, client):
        """Test metric aggregation with empty values."""
        avg, max_val = client._calculate_metric_aggregates([], "Average")
        
        assert avg == 0.0
        assert max_val == 0.0
    
    def test_parse_resource_id(self, client):
        """Test parsing Azure resource ID."""
        resource_id = "/subscriptions/sub123/resourceGroups/myRg/providers/Microsoft.Sql/servers/myServer/databases/myDb"
        
        parsed = client._parse_resource_id(resource_id)
        
        assert parsed['subscription'] == 'sub123'
        assert parsed['resource_group'] == 'myRg'
        assert parsed['provider'] == 'Microsoft.Sql'
        assert parsed['resource_type'] == 'servers'
        assert parsed['resource_name'] == 'myServer'
    
    @pytest.mark.asyncio
    async def test_fetch_metric_success(self, client):
        """Test successful metric fetching."""
        resource_id = "test-resource"
        metric_name = "cpu_percent"
        time_range = (datetime.utcnow() - timedelta(hours=1), datetime.utcnow())
        
        # Mock the monitor client
        mock_metrics = MagicMock()
        mock_timeseries = MagicMock()
        mock_timeseries.data = [
            MagicMock(average=10.0),
            MagicMock(average=20.0)
        ]
        mock_metric = MagicMock()
        mock_metric.name.value = metric_name
        mock_metric.timeseries = [mock_timeseries]
        mock_result = MagicMock()
        mock_result.value = [mock_metric]
        
        client._monitor_client = MagicMock()
        client._monitor_client.metrics.list.return_value = mock_result
        
        avg, max_val = await client._fetch_metric(
            resource_id, metric_name, time_range
        )
        
        assert avg == 15.0  # (10 + 20) / 2
        assert max_val == 20.0
    
    @pytest.mark.asyncio
    async def test_fetch_metric_error(self, client):
        """Test metric fetching with Azure error."""
        client._monitor_client = MagicMock()
        client._monitor_client.metrics.list.side_effect = AzureError("API Error")
        
        with pytest.raises(AzureError, match="Failed to fetch metric"):
            await client._fetch_metric(
                "test-resource",
                "cpu_percent",
                (datetime.utcnow(), datetime.utcnow())
            )