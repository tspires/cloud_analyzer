#!/usr/bin/env python3
"""Fix model imports in test files."""

import os
import re

def fix_imports_in_file(filepath):
    """Fix imports in a single test file."""
    with open(filepath, 'r') as f:
        content = f.read()
    
    original = content
    
    # Fix common.src imports to just use the module name
    replacements = [
        # Models imports
        (r'from common\.src\.models import', 'from models import'),
        (r'from common\.src\.models\.(\w+) import', r'from models.\1 import'),
        
        # Checks imports
        (r'from common\.src\.checks import', 'from checks import'),
        (r'from common\.src\.checks\.(\w+) import', r'from checks.\1 import'),
        
        # Constants imports
        (r'from common\.src\.constants import', 'from constants import'),
        
        # Patch paths
        (r'"common\.src\.checks\.registry', '"checks.registry'),
        (r'"common\.src\.models\.', '"models.'),
        
        # Fix specific enum issues
        (r'Severity\.', 'CheckSeverity.'),
    ]
    
    for pattern, replacement in replacements:
        content = re.sub(pattern, replacement, content)
    
    if content != original:
        with open(filepath, 'w') as f:
            f.write(content)
        print(f"Fixed model imports in {filepath}")

# Fix imports in all test files
test_dir = "tests"
for root, dirs, files in os.walk(test_dir):
    for file in files:
        if file.endswith('.py'):
            filepath = os.path.join(root, file)
            fix_imports_in_file(filepath)

print("Model import fixes completed.")