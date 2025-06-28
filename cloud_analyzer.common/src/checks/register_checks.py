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
    try:
        from checks.cost_optimization.reserved_instances import ReservedInstancesUtilizationCheck
        from checks.cost_optimization.savings_plans import SavingsPlansCoverageCheck
        check_registry.register(ReservedInstancesUtilizationCheck())
        check_registry.register(SavingsPlansCoverageCheck())
    except ImportError as e:
        logger.warning(f"Failed to import cost optimization checks: {e}")
    
    # Register database checks
    try:
        from checks.database.database_sizing import DatabaseSizingCheck
        check_registry.register(DatabaseSizingCheck())
    except ImportError as e:
        logger.warning(f"Failed to import database checks: {e}")


# Auto-register when imported
register_all_checks()