"""Optimization checks registry and base classes."""

from .base import CheckBase
from .registry import check_registry

__all__ = ['CheckBase', 'check_registry']