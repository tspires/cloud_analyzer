"""Register all available checks with the registry."""

import logging

from checks.registry import check_registry

logger = logging.getLogger(__name__)


def register_all_checks():
    """Register all available checks."""
    # Try to import and register compute checks
    try:
        from checks.compute.idle_instances import IdleInstanceCheck
        from checks.compute.right_sizing import RightSizingCheck
        check_registry.register(IdleInstanceCheck())
        check_registry.register(RightSizingCheck())
    except ImportError as e:
        logger.warning(f"Failed to import compute checks: {e}")
    
    # Register storage checks
    try:
        from checks.storage.unattached_volumes import UnattachedVolumesCheck
        from checks.storage.old_snapshots import OldSnapshotsCheck
        check_registry.register(UnattachedVolumesCheck())
        check_registry.register(OldSnapshotsCheck())
    except ImportError as e:
        logger.warning(f"Failed to import storage checks: {e}")
    
    # Register cost optimization checks
    # AWS-specific checks are disabled since we're Azure-only
    # try:
    #     from checks.cost_optimization.reserved_instances import ReservedInstancesUtilizationCheck
    #     from checks.cost_optimization.savings_plans import SavingsPlansCoverageCheck
    #     check_registry.register(ReservedInstancesUtilizationCheck())
    #     check_registry.register(SavingsPlansCoverageCheck())
    # except ImportError as e:
    #     logger.warning(f"Failed to import cost optimization checks: {e}")
    
    # Register database checks
    try:
        from checks.database.database_sizing import DatabaseSizingCheck
        check_registry.register(DatabaseSizingCheck())
    except ImportError as e:
        logger.warning(f"Failed to import database checks: {e}")
    
    # Register Azure-specific checks
    try:
        # Azure VM checks
        from checks.azure.vm_deallocated import AzureVMDeallocatedCheck
        from checks.azure.vm_hybrid_benefit import AzureVMHybridBenefitCheck
        from checks.azure.vm_reserved_instances import AzureVMReservedInstancesCheck
        from checks.azure.vm_spot_instances import AzureSpotVMCheck
        from checks.azure.vm_right_sizing import AzureVMRightSizingCheck
        
        check_registry.register(AzureVMDeallocatedCheck())
        check_registry.register(AzureVMHybridBenefitCheck())
        check_registry.register(AzureVMReservedInstancesCheck())
        check_registry.register(AzureSpotVMCheck())
        check_registry.register(AzureVMRightSizingCheck())
        
        # Azure Storage checks
        from checks.azure.storage_lifecycle import AzureStorageLifecycleCheck
        from checks.azure.storage_redundancy import AzureStorageRedundancyCheck
        from checks.azure.storage_unused import AzureUnusedStorageCheck
        from checks.azure.storage_logging import AzureStorageLoggingCheck
        from checks.azure.storage_premium import AzurePremiumStorageCheck
        
        check_registry.register(AzureStorageLifecycleCheck())
        check_registry.register(AzureStorageRedundancyCheck())
        check_registry.register(AzureUnusedStorageCheck())
        check_registry.register(AzureStorageLoggingCheck())
        check_registry.register(AzurePremiumStorageCheck())
        
        # Azure SQL Database checks
        from checks.azure.sql_idle_databases import AzureSQLIdleDatabaseCheck
        from checks.azure.sql_elastic_pools import AzureSQLElasticPoolCheck
        from checks.azure.sql_backup_retention import AzureSQLBackupRetentionCheck
        from checks.azure.sql_serverless_tier import AzureSQLServerlessTierCheck
        from checks.azure.sql_geo_replication import AzureSQLGeoReplicationCheck
        
        check_registry.register(AzureSQLIdleDatabaseCheck())
        check_registry.register(AzureSQLElasticPoolCheck())
        check_registry.register(AzureSQLBackupRetentionCheck())
        check_registry.register(AzureSQLServerlessTierCheck())
        check_registry.register(AzureSQLGeoReplicationCheck())
    except ImportError as e:
        logger.warning(f"Failed to import Azure checks: {e}")


# Auto-register when imported
# register_all_checks()  # Commented out to prevent duplicate registration