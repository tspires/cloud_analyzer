#!/usr/bin/env python3
"""Test runner for the clean refactored analyze command."""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from commands.analyze_clean import analyze

if __name__ == "__main__":
    # Run with test arguments
    import sys
    
    # Simulate command line arguments
    sys.argv = [
        'analyze',
        '--provider', 'azure',
        '--severity', 'medium'
    ]
    
    # Call the analyze command
    analyze.main(standalone_mode=False)