"""End-to-end tests that simulate real cloud provider interactions."""

import os
from datetime import datetime, timedelta
from decimal import Decimal
from unittest.mock import patch, MagicMock

import pytest
import boto3
from moto import mock_ec2, mock_rds, mock_cloudwatch
from click.testing import CliRunner

from src.main import cli


@pytest.mark.e2e
class TestRealProviderE2E:
    """End-to-end tests with mocked AWS services."""
    
    @pytest.fixture
    def cli_runner(self):
        """Create a CLI runner."""
        return CliRunner()
    
    @pytest.fixture
    def mock_aws_credentials(self):
        """Mock AWS credentials."""
        os.environ["AWS_ACCESS_KEY_ID"] = "testing"
        os.environ["AWS_SECRET_ACCESS_KEY"] = "testing"
        os.environ["AWS_SECURITY_TOKEN"] = "testing"
        os.environ["AWS_SESSION_TOKEN"] = "testing"
        os.environ["AWS_DEFAULT_REGION"] = "us-east-1"
        yield
        # Cleanup
        for key in ["AWS_ACCESS_KEY_ID", "AWS_SECRET_ACCESS_KEY", 
                    "AWS_SECURITY_TOKEN", "AWS_SESSION_TOKEN", "AWS_DEFAULT_REGION"]:
            os.environ.pop(key, None)
    
    @mock_ec2
    @mock_cloudwatch
    def test_e2e_unattached_volumes_with_moto(self, cli_runner, mock_aws_credentials):
        """Test unattached volumes check with moto mocked AWS."""
        # Create EC2 client
        ec2 = boto3.client("ec2", region_name="us-east-1")
        
        # Create a volume (unattached)
        volume = ec2.create_volume(
            AvailabilityZone="us-east-1a",
            Size=100,
            VolumeType="gp3",
            TagSpecifications=[
                {
                    "ResourceType": "volume",
                    "Tags": [
                        {"Key": "Name", "Value": "TestUnattachedVolume"},
                    ]
                }
            ]
        )
        volume_id = volume["VolumeId"]
        
        # Mock the configuration
        with patch("src.utils.config.AuthManager") as mock_auth:
            auth_manager = MagicMock()
            auth_manager.is_provider_configured.return_value = True
            auth_manager.get_provider_config.return_value = {
                "access_key_id": "testing",
                "secret_access_key": "testing",
                "region": "us-east-1"
            }
            auth_manager.get_configured_providers.return_value = ["aws"]
            mock_auth.return_value = auth_manager
            
            # Run the analyze command
            result = cli_runner.invoke(
                cli,
                ["analyze", "--provider", "aws", "--checks", "unattached_volume"]
            )
            
            # Note: This would require implementing the actual AWS provider
            # For now, this shows the structure of how real e2e tests would work
            assert result.exit_code == 0
    
    @mock_ec2
    def test_e2e_old_snapshots_with_moto(self, cli_runner, mock_aws_credentials):
        """Test old snapshots check with moto mocked AWS."""
        # Create EC2 client
        ec2 = boto3.client("ec2", region_name="us-east-1")
        
        # Create a volume first
        volume = ec2.create_volume(
            AvailabilityZone="us-east-1a",
            Size=50
        )
        
        # Create a snapshot
        snapshot = ec2.create_snapshot(
            VolumeId=volume["VolumeId"],
            Description="Old test snapshot",
            TagSpecifications=[
                {
                    "ResourceType": "snapshot",
                    "Tags": [
                        {"Key": "Name", "Value": "OldSnapshot"},
                        {"Key": "CreatedDate", "Value": "2023-01-01"},
                    ]
                }
            ]
        )
        
        with patch("src.utils.config.AuthManager") as mock_auth:
            auth_manager = MagicMock()
            auth_manager.is_provider_configured.return_value = True
            auth_manager.get_provider_config.return_value = {
                "access_key_id": "testing",
                "secret_access_key": "testing",
                "region": "us-east-1"
            }
            mock_auth.return_value = auth_manager
            
            # Run the analyze command
            result = cli_runner.invoke(
                cli,
                ["analyze", "--provider", "aws", "--checks", "old_snapshot"]
            )
            
            assert result.exit_code == 0
    
    @mock_rds
    @mock_cloudwatch
    def test_e2e_database_sizing_with_moto(self, cli_runner, mock_aws_credentials):
        """Test database sizing check with moto mocked AWS."""
        # Create RDS client
        rds = boto3.client("rds", region_name="us-east-1")
        cloudwatch = boto3.client("cloudwatch", region_name="us-east-1")
        
        # Create a database instance
        rds.create_db_instance(
            DBInstanceIdentifier="test-db-oversized",
            DBInstanceClass="db.r5.2xlarge",
            Engine="postgres",
            MasterUsername="admin",
            MasterUserPassword="password123",
            AllocatedStorage=100,
            Tags=[
                {"Key": "Name", "Value": "OversizedDatabase"},
            ]
        )
        
        # Add CloudWatch metrics for low utilization
        namespace = "AWS/RDS"
        
        # Add CPU utilization metrics
        for i in range(7):
            cloudwatch.put_metric_data(
                Namespace=namespace,
                MetricData=[
                    {
                        "MetricName": "CPUUtilization",
                        "Dimensions": [
                            {
                                "Name": "DBInstanceIdentifier",
                                "Value": "test-db-oversized"
                            }
                        ],
                        "Timestamp": datetime.utcnow() - timedelta(days=i),
                        "Value": 15.0,  # Low CPU usage
                        "Unit": "Percent"
                    }
                ]
            )
        
        with patch("src.utils.config.AuthManager") as mock_auth:
            auth_manager = MagicMock()
            auth_manager.is_provider_configured.return_value = True
            auth_manager.get_provider_config.return_value = {
                "access_key_id": "testing",
                "secret_access_key": "testing",
                "region": "us-east-1"
            }
            mock_auth.return_value = auth_manager
            
            # Run the analyze command
            result = cli_runner.invoke(
                cli,
                ["analyze", "--provider", "aws", "--checks", "right_sizing"]
            )
            
            assert result.exit_code == 0
    
    def test_e2e_cost_explorer_checks(self, cli_runner, mock_aws_credentials):
        """Test cost optimization checks that use Cost Explorer API."""
        # Note: moto doesn't support Cost Explorer API, so we need to mock differently
        
        with patch("src.utils.config.AuthManager") as mock_auth, \
             patch("boto3.client") as mock_boto_client:
            
            # Mock auth
            auth_manager = MagicMock()
            auth_manager.is_provider_configured.return_value = True
            auth_manager.get_provider_config.return_value = {
                "access_key_id": "testing",
                "secret_access_key": "testing",
                "region": "us-east-1"
            }
            mock_auth.return_value = auth_manager
            
            # Mock Cost Explorer client
            mock_ce_client = MagicMock()
            
            # Mock RI utilization response
            mock_ce_client.get_reservation_utilization.return_value = {
                "UtilizationsByTime": [
                    {
                        "TimePeriod": {
                            "Start": "2024-01-01",
                            "End": "2024-01-31"
                        },
                        "Total": {
                            "UtilizationPercentage": "60",
                            "PurchasedHours": "744",
                            "TotalActualHours": "446.4",
                            "UnusedHours": "297.6",
                            "OnDemandCostOfRIHoursUsed": "1000.00",
                            "NetRISavings": "400.00",
                            "TotalPotentialRISavings": "666.67",
                            "AmortizedUpfrontFee": "0",
                            "AmortizedRecurringFee": "600.00",
                            "TotalAmortizedFee": "600.00"
                        },
                        "Groups": []
                    }
                ]
            }
            
            # Mock savings plans coverage response
            mock_ce_client.get_savings_plans_coverage.return_value = {
                "SavingsPlansCoverages": [
                    {
                        "TimePeriod": {
                            "Start": "2024-01-01",
                            "End": "2024-01-31"
                        },
                        "Coverage": {
                            "CoveragePercentage": "40",
                            "OnDemandCost": "6000.00",
                            "SpendCoveredBySavingsPlans": "4000.00",
                            "TotalCost": "10000.00"
                        }
                    }
                ]
            }
            
            def get_mock_client(service_name, **kwargs):
                if service_name == "ce":
                    return mock_ce_client
                else:
                    # Return real boto3 client for other services
                    return boto3.client(service_name, **kwargs)
            
            mock_boto_client.side_effect = get_mock_client
            
            # Run the analyze command for cost optimization checks
            result = cli_runner.invoke(
                cli,
                [
                    "analyze",
                    "--provider", "aws",
                    "--checks", "reserved_instance_optimization,savings_plan_optimization"
                ]
            )
            
            assert result.exit_code == 0
    
    def test_e2e_multi_region_analysis(self, cli_runner, mock_aws_credentials):
        """Test analyzing resources across multiple regions."""
        with patch("src.utils.config.AuthManager") as mock_auth, \
             patch("boto3.client") as mock_boto_client:
            
            # Mock auth
            auth_manager = MagicMock()
            auth_manager.is_provider_configured.return_value = True
            auth_manager.get_provider_config.return_value = {
                "access_key_id": "testing",
                "secret_access_key": "testing",
                "region": "us-east-1"
            }
            mock_auth.return_value = auth_manager
            
            # Mock EC2 client for multiple regions
            mock_ec2_clients = {}
            
            for region in ["us-east-1", "us-west-2", "eu-west-1"]:
                mock_client = MagicMock()
                mock_client.describe_volumes.return_value = {
                    "Volumes": [
                        {
                            "VolumeId": f"vol-{region}-1234",
                            "Size": 100,
                            "State": "available",
                            "VolumeType": "gp3",
                            "CreateTime": datetime.utcnow() - timedelta(days=30),
                            "Tags": [{"Key": "Name", "Value": f"Volume-{region}"}]
                        }
                    ]
                }
                mock_ec2_clients[region] = mock_client
            
            def get_mock_client(service_name, region_name=None, **kwargs):
                if service_name == "ec2" and region_name:
                    return mock_ec2_clients.get(region_name, MagicMock())
                return MagicMock()
            
            mock_boto_client.side_effect = get_mock_client
            
            # Run analyze across all regions
            result = cli_runner.invoke(
                cli,
                ["analyze", "--provider", "aws", "--checks", "unattached_volume"]
            )
            
            assert result.exit_code == 0