#!/usr/bin/env python3
"""Test the clean refactored commands with various options."""

import sys
import os
import asyncio

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from commands.analyze_clean import analyze
from commands.configure_clean import configure

def test_analyze_dry_run():
    """Test analyze with dry-run."""
    print("\n=== Testing Analyze Dry Run ===")
    sys.argv = ['analyze', '--provider', 'all', '--dry-run']
    try:
        analyze.main(standalone_mode=False)
    except SystemExit:
        pass

def test_analyze_json():
    """Test analyze with JSON output."""
    print("\n=== Testing Analyze JSON Output ===")
    sys.argv = ['analyze', '--provider', 'azure', '--output', 'json', '--severity', 'high']
    try:
        analyze.main(standalone_mode=False)
    except SystemExit:
        pass

def test_configure_show():
    """Test configure show."""
    print("\n=== Testing Configure Show ===")
    sys.argv = ['configure', '--show']
    try:
        configure.main(standalone_mode=False)
    except SystemExit:
        pass

if __name__ == "__main__":
    # Run all tests
    test_analyze_dry_run()
    test_analyze_json()
    test_configure_show()