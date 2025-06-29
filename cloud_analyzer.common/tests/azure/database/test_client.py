"""Unit tests for Azure database metrics wrapper client."""
import asyncio
from datetime import datetime, timedelta
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from azure.core.exceptions import AzureError, ClientAuthenticationError, ResourceNotFoundError

from src.azure.database import (
    AzureDatabaseMetricsWrapper,
    DatabaseMetrics,
)


@pytest.fixture
def mock_credential():
    """Create mock Azure credential."""
    return MagicMock()


@pytest.fixture
def metrics_wrapper(mock_credential):
    """Create metrics wrapper instance for testing."""
    return AzureDatabaseMetricsWrapper(
        credential=mock_credential,
        subscription_id="test-subscription-id",
        retry_count=2,
        retry_delay=0.1,
        timeout=5.0
    )


@pytest.fixture
def sample_metrics():
    """Create sample database metrics."""
    return DatabaseMetrics(
        resource_id="/subscriptions/test/resourceGroups/test-rg/providers/Microsoft.Sql/servers/test-server/databases/test-db",
        database_name="test-db",
        server_name="test-server",
        resource_group="test-rg",
        database_type="Azure SQL Database",
        time_range=(datetime.utcnow() - timedelta(days=7), datetime.utcnow()),
        cpu_percent_avg=35.5,
        cpu_percent_max=78.2,
        memory_percent_avg=42.1,
        memory_percent_max=65.3,
        storage_percent_avg=55.0,
        storage_percent_max=55.5
    )


class TestAzureDatabaseMetricsWrapper:
    """Test cases for AzureDatabaseMetricsWrapper."""
    
    def test_initialization(self, mock_credential):
        """Test wrapper initialization."""
        wrapper = AzureDatabaseMetricsWrapper(
            credential=mock_credential,
            subscription_id="test-sub"
        )
        
        assert wrapper.subscription_id == "test-sub"
        assert wrapper.credential == mock_credential
        assert wrapper.retry_count == 3
        assert wrapper.retry_delay == 1.0
        assert wrapper.timeout == 30.0
    
    def test_initialization_defaults(self):
        """Test wrapper initialization with defaults."""
        wrapper = AzureDatabaseMetricsWrapper()
        
        assert wrapper.subscription_id is None
        assert wrapper.credential is not None
        assert wrapper.retry_count == 3
    
    def test_set_subscription(self, metrics_wrapper):
        """Test setting subscription ID."""
        new_sub_id = "new-subscription-id"
        metrics_wrapper.set_subscription(new_sub_id)
        
        assert metrics_wrapper.subscription_id == new_sub_id
        assert metrics_wrapper._sql_client is None
        assert metrics_wrapper._postgresql_client is None
        assert metrics_wrapper._mysql_client is None
    
    def test_validate_subscription_error(self, mock_credential):
        """Test validation error when subscription not set."""
        wrapper = AzureDatabaseMetricsWrapper(credential=mock_credential)
        
        with pytest.raises(ValueError, match="Subscription ID not set"):
            wrapper._validate_subscription()
    
    def test_get_database_type(self, metrics_wrapper):
        """Test database type detection from resource ID."""
        # SQL Database
        sql_id = "/subscriptions/test/resourceGroups/rg/providers/Microsoft.Sql/servers/server/databases/db"
        assert metrics_wrapper._get_database_type(sql_id) == 'sql'
        
        # PostgreSQL
        pg_id = "/subscriptions/test/resourceGroups/rg/providers/Microsoft.DBforPostgreSQL/servers/server"
        assert metrics_wrapper._get_database_type(pg_id) == 'postgresql'
        
        # MySQL
        mysql_id = "/subscriptions/test/resourceGroups/rg/providers/Microsoft.DBforMySQL/servers/server"
        assert metrics_wrapper._get_database_type(mysql_id) == 'mysql'
        
        # Unknown
        unknown_id = "/subscriptions/test/resourceGroups/rg/providers/Microsoft.Unknown/servers/server"
        with pytest.raises(ValueError, match="Unknown database type"):
            metrics_wrapper._get_database_type(unknown_id)
    
    @pytest.mark.asyncio
    async def test_get_database_metrics_sql(self, metrics_wrapper, sample_metrics):
        """Test getting SQL database metrics."""
        with patch.object(metrics_wrapper, 'sql_metrics_client') as mock_client:
            mock_client.get_database_metrics = AsyncMock(return_value=sample_metrics)
            
            result = await metrics_wrapper.get_database_metrics(
                sample_metrics.resource_id
            )
            
            assert result == sample_metrics
            mock_client.get_database_metrics.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_get_database_metrics_postgresql(self, metrics_wrapper):
        """Test getting PostgreSQL metrics."""
        resource_id = "/subscriptions/test/resourceGroups/rg/providers/Microsoft.DBforPostgreSQL/servers/server"
        mock_metrics = DatabaseMetrics(
            resource_id=resource_id,
            database_name="server",
            server_name="server",
            resource_group="rg",
            database_type="Azure PostgreSQL",
            time_range=(datetime.utcnow() - timedelta(days=7), datetime.utcnow()),
            cpu_percent_avg=25.0,
            cpu_percent_max=45.0
        )
        
        with patch.object(metrics_wrapper, 'postgresql_metrics_client') as mock_client:
            mock_client.get_database_metrics = AsyncMock(return_value=mock_metrics)
            
            result = await metrics_wrapper.get_database_metrics(resource_id)
            
            assert result == mock_metrics
            mock_client.get_database_metrics.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_get_database_metrics_mysql(self, metrics_wrapper):
        """Test getting MySQL metrics."""
        resource_id = "/subscriptions/test/resourceGroups/rg/providers/Microsoft.DBforMySQL/servers/server"
        mock_metrics = DatabaseMetrics(
            resource_id=resource_id,
            database_name="server",
            server_name="server",
            resource_group="rg",
            database_type="Azure MySQL",
            time_range=(datetime.utcnow() - timedelta(days=7), datetime.utcnow()),
            cpu_percent_avg=30.0,
            cpu_percent_max=50.0
        )
        
        with patch.object(metrics_wrapper, 'mysql_metrics_client') as mock_client:
            mock_client.get_database_metrics = AsyncMock(return_value=mock_metrics)
            
            result = await metrics_wrapper.get_database_metrics(resource_id)
            
            assert result == mock_metrics
            mock_client.get_database_metrics.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_retry_operation_success(self, metrics_wrapper):
        """Test retry operation succeeds on first attempt."""
        async def mock_operation():
            return "success"
        
        result = await metrics_wrapper._retry_operation(mock_operation)
        assert result == "success"
    
    @pytest.mark.asyncio
    async def test_retry_operation_eventual_success(self, metrics_wrapper):
        """Test retry operation succeeds after failures."""
        attempt_count = 0
        
        async def mock_operation():
            nonlocal attempt_count
            attempt_count += 1
            if attempt_count < 2:
                raise AzureError("Temporary failure")
            return "success"
        
        result = await metrics_wrapper._retry_operation(mock_operation)
        assert result == "success"
        assert attempt_count == 2
    
    @pytest.mark.asyncio
    async def test_retry_operation_all_failures(self, metrics_wrapper):
        """Test retry operation fails after all attempts."""
        async def mock_operation():
            raise AzureError("Persistent failure")
        
        with pytest.raises(AzureError, match="Persistent failure"):
            await metrics_wrapper._retry_operation(mock_operation)
    
    @pytest.mark.asyncio
    async def test_retry_operation_timeout(self, metrics_wrapper):
        """Test retry operation with timeout."""
        async def mock_operation():
            await asyncio.sleep(10)  # Longer than timeout
            return "success"
        
        with pytest.raises(TimeoutError):
            await metrics_wrapper._retry_operation(mock_operation)
    
    @pytest.mark.asyncio
    async def test_error_handler_authentication_error(self, metrics_wrapper):
        """Test error handler with authentication error."""
        async with metrics_wrapper._error_handler("test_operation", "test_resource"):
            with pytest.raises(AzureError, match="Authentication failed"):
                raise ClientAuthenticationError("Invalid credentials")
    
    @pytest.mark.asyncio
    async def test_error_handler_resource_not_found(self, metrics_wrapper):
        """Test error handler with resource not found error."""
        async with metrics_wrapper._error_handler("test_operation", "test_resource"):
            with pytest.raises(AzureError, match="Resource not found"):
                raise ResourceNotFoundError("Resource does not exist")
    
    @pytest.mark.asyncio
    async def test_list_all_databases(self, metrics_wrapper):
        """Test listing all databases."""
        mock_sql_dbs = [{"id": "sql1", "name": "sqldb1"}]
        mock_pg_dbs = [{"id": "pg1", "name": "pgdb1"}]
        mock_mysql_dbs = [{"id": "mysql1", "name": "mysqldb1"}]
        
        with patch.object(metrics_wrapper, 'sql_metrics_client') as mock_sql:
            with patch.object(metrics_wrapper, 'postgresql_metrics_client') as mock_pg:
                with patch.object(metrics_wrapper, 'mysql_metrics_client') as mock_mysql:
                    mock_sql.list_databases = AsyncMock(return_value=mock_sql_dbs)
                    mock_pg.list_databases = AsyncMock(return_value=mock_pg_dbs)
                    mock_mysql.list_databases = AsyncMock(return_value=mock_mysql_dbs)
                    
                    result = await metrics_wrapper.list_all_databases()
                    
                    assert result['sql'] == mock_sql_dbs
                    assert result['postgresql'] == mock_pg_dbs
                    assert result['mysql'] == mock_mysql_dbs
    
    @pytest.mark.asyncio
    async def test_get_all_database_metrics(self, metrics_wrapper, sample_metrics):
        """Test getting metrics for all databases."""
        mock_databases = {
            'sql': [{"id": sample_metrics.resource_id}],
            'postgresql': [],
            'mysql': []
        }
        
        with patch.object(metrics_wrapper, 'list_all_databases', AsyncMock(return_value=mock_databases)):
            with patch.object(metrics_wrapper, 'get_database_metrics', AsyncMock(return_value=sample_metrics)):
                result = await metrics_wrapper.get_all_database_metrics()
                
                assert len(result) == 1
                assert result[0] == sample_metrics
    
    @pytest.mark.asyncio
    async def test_get_optimization_recommendations_single(self, metrics_wrapper, sample_metrics):
        """Test getting recommendations for single database."""
        mock_recommendations = [
            {
                'type': 'downsize',
                'severity': 'medium',
                'description': 'Low CPU utilization'
            }
        ]
        
        with patch.object(metrics_wrapper, 'sql_metrics_client') as mock_client:
            mock_client.get_database_recommendations = AsyncMock(return_value=mock_recommendations)
            
            result = await metrics_wrapper.get_optimization_recommendations(
                resource_id=sample_metrics.resource_id,
                metrics=sample_metrics
            )
            
            assert result == mock_recommendations
    
    @pytest.mark.asyncio
    async def test_get_optimization_recommendations_all(self, metrics_wrapper, sample_metrics):
        """Test getting recommendations for all databases."""
        with patch.object(metrics_wrapper, 'get_all_database_metrics', AsyncMock(return_value=[sample_metrics])):
            with patch.object(metrics_wrapper, 'sql_metrics_client') as mock_client:
                mock_recommendations = [{'type': 'test'}]
                mock_client.get_database_recommendations = AsyncMock(return_value=mock_recommendations)
                
                result = await metrics_wrapper.get_optimization_recommendations(include_all=True)
                
                assert isinstance(result, dict)
                assert sample_metrics.database_name in result
                assert result[sample_metrics.database_name] == mock_recommendations
    
    @pytest.mark.asyncio
    async def test_close(self, metrics_wrapper):
        """Test closing the wrapper."""
        await metrics_wrapper.close()  # Should not raise any errors