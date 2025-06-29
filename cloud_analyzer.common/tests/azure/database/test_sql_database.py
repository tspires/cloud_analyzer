"""Unit tests for SQL Database metrics collection."""
from datetime import datetime, timedelta
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from azure.core.exceptions import AzureError

from src.azure.database.sql_database import SqlDatabaseMetricsClient


@pytest.fixture
def mock_credential():
    """Create mock Azure credential."""
    return MagicMock()


@pytest.fixture
def sql_client(mock_credential):
    """Create SQL Database metrics client for testing."""
    return SqlDatabaseMetricsClient(
        credential=mock_credential,
        subscription_id="test-subscription-id"
    )


@pytest.fixture
def sql_resource_id():
    """Sample SQL Database resource ID."""
    return "/subscriptions/test-sub/resourceGroups/test-rg/providers/Microsoft.Sql/servers/test-server/databases/test-db"


class TestSqlDatabaseMetricsClient:
    """Test cases for SqlDatabaseMetricsClient."""
    
    def test_initialization(self, mock_credential):
        """Test client initialization."""
        client = SqlDatabaseMetricsClient(
            credential=mock_credential,
            subscription_id="test-sub",
            monitor_client=MagicMock(),
            sql_client=MagicMock()
        )
        
        assert client.credential == mock_credential
        assert client.subscription_id == "test-sub"
        assert client._sql_client is not None
        assert client._monitor_client is not None
    
    def test_sql_client_lazy_initialization(self, sql_client):
        """Test lazy initialization of SQL client."""
        with patch('src.azure.database.sql_database.SqlManagementClient') as mock_sql:
            mock_instance = MagicMock()
            mock_sql.return_value = mock_instance
            
            client = sql_client.sql_client
            assert client == mock_instance
            mock_sql.assert_called_once_with(
                credential=sql_client.credential,
                subscription_id=sql_client.subscription_id
            )
    
    @pytest.mark.asyncio
    async def test_is_dtu_based_database_true(self, sql_client, sql_resource_id):
        """Test DTU-based database detection."""
        mock_database = MagicMock()
        mock_database.current_sku = MagicMock(tier='Standard')
        
        sql_client._sql_client = MagicMock()
        sql_client._sql_client.databases.get.return_value = mock_database
        
        result = await sql_client._is_dtu_based_database(sql_resource_id)
        
        assert result is True
    
    @pytest.mark.asyncio
    async def test_is_dtu_based_database_false(self, sql_client, sql_resource_id):
        """Test vCore-based database detection."""
        mock_database = MagicMock()
        mock_database.current_sku = MagicMock(tier='GeneralPurpose')
        
        sql_client._sql_client = MagicMock()
        sql_client._sql_client.databases.get.return_value = mock_database
        
        result = await sql_client._is_dtu_based_database(sql_resource_id)
        
        assert result is False
    
    @pytest.mark.asyncio
    async def test_get_database_metrics_dtu(self, sql_client, sql_resource_id):
        """Test getting metrics for DTU-based database."""
        # Mock DTU detection
        sql_client._is_dtu_based_database = AsyncMock(return_value=True)
        
        # Mock metric fetching
        sql_client._fetch_metric = AsyncMock()
        sql_client._fetch_metric.side_effect = [
            (45.5, 78.9),  # CPU
            (60.0, 65.0),  # Storage
            (55.0, 85.0),  # DTU
        ]
        
        metrics = await sql_client.get_database_metrics(sql_resource_id)
        
        assert metrics.resource_id == sql_resource_id
        assert metrics.database_name == "test-db"
        assert metrics.server_name == "test-server"
        assert metrics.database_type == "Azure SQL Database"
        assert metrics.cpu_percent_avg == 45.5
        assert metrics.cpu_percent_max == 78.9
        assert metrics.storage_percent_avg == 60.0
        assert metrics.storage_percent_max == 65.0
        assert metrics.dtu_percent_avg == 55.0
        assert metrics.dtu_percent_max == 85.0
    
    @pytest.mark.asyncio
    async def test_get_database_metrics_vcore(self, sql_client, sql_resource_id):
        """Test getting metrics for vCore-based database."""
        # Mock vCore detection
        sql_client._is_dtu_based_database = AsyncMock(return_value=False)
        
        # Mock metric fetching
        sql_client._fetch_metric = AsyncMock()
        sql_client._fetch_metric.side_effect = [
            (35.0, 65.0),   # CPU
            (70.0, 75.0),   # Storage
            (45.0, 55.0),   # Memory
            (30.0, 40.0),   # Data IO
            (20.0, 25.0),   # Log IO
            (60.0, 80.0),   # Sessions
            (40.0, 50.0),   # Workers
        ]
        
        metrics = await sql_client.get_database_metrics(sql_resource_id)
        
        assert metrics.cpu_percent_avg == 35.0
        assert metrics.cpu_percent_max == 65.0
        assert metrics.memory_percent_avg == 45.0
        assert metrics.memory_percent_max == 55.0
        assert metrics.io_percent_avg == 30.0
        assert metrics.io_percent_max == 40.0
        assert metrics.sessions_percent_avg == 60.0
        assert metrics.sessions_percent_max == 80.0
        assert metrics.workers_percent_avg == 40.0
        assert metrics.workers_percent_max == 50.0
        assert metrics.dtu_percent_avg is None
    
    @pytest.mark.asyncio
    async def test_list_databases(self, sql_client):
        """Test listing SQL databases."""
        # Mock server
        mock_server = MagicMock()
        mock_server.id = "/subscriptions/test/resourceGroups/rg1/providers/Microsoft.Sql/servers/server1"
        mock_server.name = "server1"
        
        # Mock databases
        mock_db1 = MagicMock()
        mock_db1.id = f"{mock_server.id}/databases/db1"
        mock_db1.name = "db1"
        mock_db1.location = "eastus"
        mock_db1.status = "Online"
        mock_db1.current_service_objective_name = "S0"
        mock_db1.current_sku = MagicMock(name="Standard", tier="Standard", capacity=10)
        mock_db1.max_size_bytes = 1073741824
        mock_db1.collation = "SQL_Latin1_General_CP1_CI_AS"
        mock_db1.creation_date = datetime.utcnow()
        mock_db1.earliest_restore_date = datetime.utcnow() - timedelta(days=7)
        
        mock_system_db = MagicMock()
        mock_system_db.name = "master"
        
        sql_client._sql_client = MagicMock()
        sql_client._sql_client.servers.list.return_value = [mock_server]
        sql_client._sql_client.databases.list_by_server.return_value = [mock_db1, mock_system_db]
        
        databases = await sql_client.list_databases()
        
        assert len(databases) == 1  # System database filtered out
        assert databases[0]['name'] == 'db1'
        assert databases[0]['server_name'] == 'server1'
        assert databases[0]['location'] == 'eastus'
        assert databases[0]['status'] == 'Online'
        assert databases[0]['sku']['name'] == 'Standard'
    
    @pytest.mark.asyncio
    async def test_get_database_recommendations_downsize(self, sql_client, sql_resource_id):
        """Test recommendations for underutilized database."""
        from src.azure.database import DatabaseMetrics
        
        metrics = DatabaseMetrics(
            resource_id=sql_resource_id,
            database_name="test-db",
            server_name="test-server",
            resource_group="test-rg",
            database_type="Azure SQL Database",
            time_range=(datetime.utcnow() - timedelta(days=7), datetime.utcnow()),
            cpu_percent_avg=25.0,
            cpu_percent_max=35.0,
            dtu_percent_avg=30.0,
            dtu_percent_max=40.0,
            storage_percent_avg=50.0,
            storage_percent_max=55.0
        )
        
        recommendations = await sql_client.get_database_recommendations(
            sql_resource_id,
            metrics=metrics
        )
        
        assert len(recommendations) >= 1
        assert any(r['type'] == 'downsize' for r in recommendations)
        assert any('low DTU utilization' in r['description'] for r in recommendations)
    
    @pytest.mark.asyncio
    async def test_get_database_recommendations_upsize(self, sql_client, sql_resource_id):
        """Test recommendations for overutilized database."""
        from src.azure.database import DatabaseMetrics
        
        metrics = DatabaseMetrics(
            resource_id=sql_resource_id,
            database_name="test-db",
            server_name="test-server",
            resource_group="test-rg",
            database_type="Azure SQL Database",
            time_range=(datetime.utcnow() - timedelta(days=7), datetime.utcnow()),
            cpu_percent_avg=85.0,
            cpu_percent_max=95.0,
            storage_percent_avg=85.0,
            storage_percent_max=90.0
        )
        
        recommendations = await sql_client.get_database_recommendations(
            sql_resource_id,
            metrics=metrics
        )
        
        assert len(recommendations) >= 2
        assert any(r['type'] == 'upsize' for r in recommendations)
        assert any(r['type'] == 'storage' for r in recommendations)
        assert any('high CPU utilization' in r['description'] for r in recommendations)
    
    @pytest.mark.asyncio
    async def test_get_database_metrics_error_handling(self, sql_client, sql_resource_id):
        """Test error handling in get_database_metrics."""
        sql_client._is_dtu_based_database = AsyncMock(return_value=True)
        sql_client._fetch_metric = AsyncMock(side_effect=AzureError("API Error"))
        
        with pytest.raises(AzureError):
            await sql_client.get_database_metrics(sql_resource_id)