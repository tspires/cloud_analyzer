#!/usr/bin/env python3
"""Test output file functionality."""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from commands.analyze_clean import analyze

if __name__ == "__main__":
    # Test JSON output to file
    print("=== Testing JSON Output to File ===")
    sys.argv = [
        'analyze',
        '--provider', 'azure',
        '--output', 'json',
        '--output-file', '/tmp/clean_results.json',
        '--severity', 'medium'
    ]
    
    try:
        analyze.main(standalone_mode=False)
    except SystemExit:
        pass
    
    # Check if file was created
    if os.path.exists('/tmp/clean_results.json'):
        print("\n✓ JSON file created successfully")
        with open('/tmp/clean_results.json', 'r') as f:
            import json
            data = json.load(f)
            print(f"  Found {len(data)} findings in the file")
    
    # Test CSV output to file
    print("\n=== Testing CSV Output to File ===")
    sys.argv = [
        'analyze',
        '--provider', 'azure',
        '--output', 'csv',
        '--output-file', '/tmp/clean_results.csv',
        '--severity', 'low'
    ]
    
    try:
        analyze.main(standalone_mode=False)
    except SystemExit:
        pass
    
    # Check if file was created
    if os.path.exists('/tmp/clean_results.csv'):
        print("\n✓ CSV file created successfully")
        with open('/tmp/clean_results.csv', 'r') as f:
            lines = f.readlines()
            print(f"  Found {len(lines) - 1} findings in the file (plus header)")