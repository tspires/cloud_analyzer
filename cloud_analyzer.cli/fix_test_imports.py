#!/usr/bin/env python3
"""Fix import paths in test files."""

import os
import re

def fix_imports_in_file(filepath):
    """Fix imports in a single test file."""
    with open(filepath, 'r') as f:
        content = f.read()
    
    original = content
    
    # Fix common import patterns
    replacements = [
        # Main imports
        (r'from cli\.main import', 'from main import'),
        (r'from cli\.src\.main import', 'from main import'),
        
        # Command imports
        (r'from cli\.src\.commands\.(\w+) import', r'from commands.\1 import'),
        (r'from cli\.commands\.(\w+) import', r'from commands.\1 import'),
        
        # Utils imports
        (r'from cli\.src\.utils\.(\w+) import', r'from utils.\1 import'),
        (r'from cli\.utils\.(\w+) import', r'from utils.\1 import'),
        
        # Formatter imports
        (r'from cli\.src\.formatters\.(\w+) import', r'from formatters.\1 import'),
        (r'from cli\.formatters\.(\w+) import', r'from formatters.\1 import'),
        
        # Constants imports
        (r'from cli\.src\.constants import', 'from cli_constants import'),
        (r'from cli\.constants import', 'from cli_constants import'),
        
        # Patch paths
        (r'"cli\.src\.utils\.config\.', '"utils.config.'),
        (r'"cli\.src\.commands\.', '"commands.'),
        (r'"cli\.src\.formatters\.', '"formatters.'),
        (r'"cli\.src\.main\.', '"main.'),
        (r'"cli\.main\.', '"main.'),
        (r'"cli\.utils\.', '"utils.'),
        (r'"cli\.commands\.', '"commands.'),
    ]
    
    for pattern, replacement in replacements:
        content = re.sub(pattern, replacement, content)
    
    if content != original:
        with open(filepath, 'w') as f:
            f.write(content)
        print(f"Fixed imports in {filepath}")

# Fix imports in all test files
test_dir = "tests"
for root, dirs, files in os.walk(test_dir):
    for file in files:
        if file.endswith('.py'):
            filepath = os.path.join(root, file)
            fix_imports_in_file(filepath)

print("Import fixes completed.")