"""Compute-related optimization checks."""

from checks.compute.idle_instances import IdleInstanceCheck
from checks.compute.right_sizing import RightSizingCheck

__all__ = ["IdleInstanceCheck", "RightSizingCheck"]