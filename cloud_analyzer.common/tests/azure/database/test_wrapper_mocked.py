"""Unit tests for Azure database wrapper with mocked Azure imports."""
import pytest
from unittest.mock import AsyncMock, MagicMock, patch
import sys
import os
from datetime import datetime, timedelta, timezone

# Add the src directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..', 'src'))

# Mock Azure modules before importing our code
sys.modules['azure.core'] = MagicMock()
sys.modules['azure.core.exceptions'] = MagicMock()
sys.modules['azure.core.credentials'] = MagicMock()
sys.modules['azure.identity'] = MagicMock()
sys.modules['azure.mgmt.monitor'] = MagicMock()
sys.modules['azure.mgmt.monitor.models'] = MagicMock()
sys.modules['azure.mgmt.sql'] = MagicMock()
sys.modules['azure.mgmt.rdbms'] = MagicMock()
sys.modules['azure.mgmt.rdbms.postgresql'] = MagicMock()
sys.modules['azure.mgmt.rdbms.postgresql_flexibleservers'] = MagicMock()
sys.modules['azure.mgmt.rdbms.mysql'] = MagicMock()
sys.modules['azure.mgmt.rdbms.mysql_flexibleservers'] = MagicMock()

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
from src.azure.database import AzureDatabaseMetricsWrapper, DatabaseMetrics


class TestAzureDatabaseMetricsWrapper:
    """Test cases for the unified database metrics wrapper."""
    
    @pytest.fixture
    def wrapper(self):
        """Create wrapper instance for testing."""
        wrapper = AzureDatabaseMetricsWrapper(
            subscription_id="test-subscription",
            retry_count=2,
            retry_delay=0.1,
            timeout=5.0
        )
        return wrapper
    
    @pytest.fixture
    def sample_metrics(self):
        """Create sample metrics data."""
        return DatabaseMetrics(
            resource_id="/subscriptions/test/resourceGroups/rg/providers/Microsoft.Sql/servers/server/databases/db",
            database_name="test-db",
            server_name="test-server",
            resource_group="test-rg",
            database_type="Azure SQL Database",
            time_range=(datetime.now(timezone.utc) - timedelta(days=7), datetime.now(timezone.utc)),
            cpu_percent_avg=45.5,
            cpu_percent_max=78.9,
            memory_percent_avg=32.1,
            memory_percent_max=45.6
        )
    
    def test_initialization(self):
        """Test wrapper initialization."""
        wrapper = AzureDatabaseMetricsWrapper(
            subscription_id="test-sub",
            retry_count=5,
            retry_delay=2.0,
            timeout=60.0
        )
        
        assert wrapper.subscription_id == "test-sub"
        assert wrapper.retry_count == 5
        assert wrapper.retry_delay == 2.0
        assert wrapper.timeout == 60.0
    
    def test_set_subscription(self, wrapper):
        """Test setting subscription ID."""
        new_sub = "new-subscription-id"
        wrapper.set_subscription(new_sub)
        
        assert wrapper.subscription_id == new_sub
        assert wrapper._sql_client is None
        assert wrapper._postgresql_client is None
        assert wrapper._mysql_client is None
    
    def test_get_database_type(self, wrapper):
        """Test database type detection."""
        # SQL Database
        sql_id = "/subscriptions/test/resourceGroups/rg/providers/Microsoft.Sql/servers/server/databases/db"
        assert wrapper._get_database_type(sql_id) == 'sql'
        
        # PostgreSQL
        pg_id = "/subscriptions/test/resourceGroups/rg/providers/Microsoft.DBforPostgreSQL/servers/server"
        assert wrapper._get_database_type(pg_id) == 'postgresql'
        
        # MySQL
        mysql_id = "/subscriptions/test/resourceGroups/rg/providers/Microsoft.DBforMySQL/servers/server"
        assert wrapper._get_database_type(mysql_id) == 'mysql'
        
        # Unknown type should raise error
        unknown_id = "/subscriptions/test/resourceGroups/rg/providers/Microsoft.Unknown/servers/server"
        with pytest.raises(ValueError):
            wrapper._get_database_type(unknown_id)
    
    def test_validate_subscription_error(self):
        """Test validation when subscription not set."""
        wrapper = AzureDatabaseMetricsWrapper()
        
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
    async def test_retry_operation_all_failures(self, wrapper):
        """Test retry operation that always fails."""
        async def mock_operation():
            raise Exception("Persistent failure")
        
        with pytest.raises(Exception, match="Persistent failure"):
            await wrapper._retry_operation(mock_operation)
    
    @pytest.mark.asyncio
    async def test_error_handler_authentication_error(self, wrapper):
        """Test error handler with authentication error."""
        with pytest.raises(MockAzureError, match="Authentication failed"):
            async with wrapper._error_handler("test_op", "test_resource"):
                raise MockClientAuthenticationError("Invalid credentials")
    
    @pytest.mark.asyncio
    async def test_error_handler_resource_not_found(self, wrapper):
        """Test error handler with resource not found."""
        with pytest.raises(MockAzureError, match="Resource not found"):
            async with wrapper._error_handler("test_op", "test_resource"):
                raise MockResourceNotFoundError("Resource does not exist")
    
    @pytest.mark.asyncio
    async def test_get_database_metrics_sql(self, wrapper, sample_metrics):
        """Test getting SQL database metrics."""
        # Mock the SQL client property getter
        mock_client = MagicMock()
        mock_client.get_database_metrics = AsyncMock(return_value=sample_metrics)
        
        with patch.object(type(wrapper), 'sql_metrics_client', new_callable=lambda: property(lambda self: mock_client)):
            result = await wrapper.get_database_metrics(sample_metrics.resource_id)
            
            assert result == sample_metrics
            mock_client.get_database_metrics.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_list_all_databases(self, wrapper):
        """Test listing all databases."""
        mock_sql_dbs = [{"id": "sql1", "name": "sqldb1"}]
        mock_pg_dbs = [{"id": "pg1", "name": "pgdb1"}]
        mock_mysql_dbs = [{"id": "mysql1", "name": "mysqldb1"}]
        
        # Create mock clients
        mock_sql_client = MagicMock()
        mock_sql_client.list_databases = AsyncMock(return_value=mock_sql_dbs)
        mock_pg_client = MagicMock()
        mock_pg_client.list_databases = AsyncMock(return_value=mock_pg_dbs)
        mock_mysql_client = MagicMock()
        mock_mysql_client.list_databases = AsyncMock(return_value=mock_mysql_dbs)
        
        # Patch all three property getters
        with patch.object(type(wrapper), 'sql_metrics_client', new_callable=lambda: property(lambda self: mock_sql_client)):
            with patch.object(type(wrapper), 'postgresql_metrics_client', new_callable=lambda: property(lambda self: mock_pg_client)):
                with patch.object(type(wrapper), 'mysql_metrics_client', new_callable=lambda: property(lambda self: mock_mysql_client)):
                    result = await wrapper.list_all_databases()
                    
                    assert result['sql'] == mock_sql_dbs
                    assert result['postgresql'] == mock_pg_dbs
                    assert result['mysql'] == mock_mysql_dbs
    
    @pytest.mark.asyncio
    async def test_get_all_database_metrics(self, wrapper, sample_metrics):
        """Test getting metrics for all databases."""
        mock_databases = {
            'sql': [{"id": sample_metrics.resource_id}],
            'postgresql': [],
            'mysql': []
        }
        
        with patch.object(wrapper, 'list_all_databases', AsyncMock(return_value=mock_databases)):
            with patch.object(wrapper, 'get_database_metrics', AsyncMock(return_value=sample_metrics)):
                result = await wrapper.get_all_database_metrics()
                
                assert len(result) == 1
                assert result[0] == sample_metrics
    
    @pytest.mark.asyncio
    async def test_get_optimization_recommendations_single(self, wrapper, sample_metrics):
        """Test getting recommendations for single database."""
        mock_recommendations = [
            {
                'type': 'downsize',
                'severity': 'medium',
                'description': 'Low CPU utilization'
            }
        ]
        
        # Create mock client
        mock_client = MagicMock()
        mock_client.get_database_recommendations = AsyncMock(return_value=mock_recommendations)
        
        with patch.object(type(wrapper), 'sql_metrics_client', new_callable=lambda: property(lambda self: mock_client)):
            result = await wrapper.get_optimization_recommendations(
                resource_id=sample_metrics.resource_id,
                metrics=sample_metrics
            )
            
            assert result == mock_recommendations
    
    @pytest.mark.asyncio
    async def test_close(self, wrapper):
        """Test closing the wrapper."""
        await wrapper.close()  # Should not raise any errors


class TestDatabaseMetrics:
    """Test cases for DatabaseMetrics dataclass."""
    
    def test_database_metrics_creation(self):
        """Test creating DatabaseMetrics with all fields."""
        now = datetime.now(timezone.utc)
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
            memory_percent_max=45.6,
            dtu_percent_avg=55.0,
            dtu_percent_max=75.0,
            storage_percent_avg=60.0,
            storage_percent_max=65.0,
            io_percent_avg=30.0,
            io_percent_max=40.0,
            sessions_percent_avg=20.0,
            sessions_percent_max=25.0,
            workers_percent_avg=15.0,
            workers_percent_max=18.0,
            additional_metrics={"custom": "value"}
        )
        
        assert metrics.database_name == "test-db"
        assert metrics.server_name == "test-server"
        assert metrics.cpu_percent_avg == 45.5
        assert metrics.memory_percent_avg == 32.1
        assert metrics.dtu_percent_avg == 55.0
        assert metrics.storage_percent_avg == 60.0
        assert metrics.additional_metrics == {"custom": "value"}
    
    def test_database_metrics_minimal(self):
        """Test creating DatabaseMetrics with minimal required fields."""
        now = datetime.now(timezone.utc)
        
        metrics = DatabaseMetrics(
            resource_id="test-id",
            database_name="test-db",
            server_name="test-server",
            resource_group="test-rg",
            database_type="Test",
            time_range=(now, now),
            cpu_percent_avg=50.0,
            cpu_percent_max=60.0
        )
        
        assert metrics.cpu_percent_avg == 50.0
        assert metrics.cpu_percent_max == 60.0
        assert metrics.memory_percent_avg is None
        assert metrics.dtu_percent_avg is None
        assert metrics.additional_metrics is None