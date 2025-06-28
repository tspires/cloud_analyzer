#!/usr/bin/env python3
"""Fix all src. imports in the codebase."""

import os
import re

def fix_imports_in_file(filepath):
    """Fix imports in a single file."""
    with open(filepath, 'r') as f:
        content = f.read()
    
    # Replace all from src. imports
    original_content = content
    content = re.sub(r'from src\.', 'from ', content)
    
    if content != original_content:
        with open(filepath, 'w') as f:
            f.write(content)
        print(f"Fixed imports in {filepath}")
        return True
    return False

def main():
    """Fix all imports in the project."""
    base_dir = "/Users/tspires/Development/cloud_analyzer/cloud_analyzer.common/src"
    
    fixed_count = 0
    for root, dirs, files in os.walk(base_dir):
        for file in files:
            if file.endswith('.py'):
                filepath = os.path.join(root, file)
                if fix_imports_in_file(filepath):
                    fixed_count += 1
    
    print(f"\nFixed imports in {fixed_count} files")

if __name__ == "__main__":
    main()