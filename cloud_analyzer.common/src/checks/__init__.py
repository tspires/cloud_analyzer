"""Optimization check implementations."""

from checks.base import Check, CheckRunner
from checks.registry import CheckRegistry, check_registry

# Auto-register all checks
import checks.register_checks

__all__ = ["Check", "CheckRunner", "CheckRegistry", "check_registry"]