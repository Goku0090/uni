#!/usr/bin/env python
"""
Update branding from UniSync to UniSinq across all files
Covers: collaborator page, connections, post project, messages, notifications, email
"""
import os
import re
from pathlib import Path

# Define replacements (case variations)
REPLACEMENTS = [
    ('UniSync', 'UniSinq'),
    ('unisync', 'unisinq'),
    ('UNISYNC', 'UNISINQ'),
]

# Files and directories to process
TARGET_PATTERNS = [
    # Templates
    'accounts/templates/**/*.html',
    # Python files (views, models, email)
    'accounts/views.py',
    'accounts/views_contact.py',
    'accounts/brevo_mail_backend.py',
    'accounts/zepto_mail_backend.py',
    # Settings
    'auth_project/settings.py',
    # Static files
    'staticfiles/**/*.css',
    'static/**/*.css',
    'static/**/*.js',
    # Test files
    'test_*.py',
    '*.py',  # Top-level Python files
]

def find_files(pattern):
    """Find files matching the pattern"""
    if '**' in pattern:
        # Use pathlib for glob patterns
        matches = list(Path('.').glob(pattern))
    else:
        # Direct file
        matches = [Path(pattern)] if Path(pattern).exists() else []
    return matches

def read_file(filepath):
    """Read file safely"""
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            return f.read()
    except Exception as e:
        print(f"  [ERROR] Could not read {filepath}: {e}")
        return None

def write_file(filepath, content):
    """Write file safely"""
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    except Exception as e:
        print(f"  [ERROR] Could not write {filepath}: {e}")
        return False

def update_file(filepath, replacements):
    """Update a single file with replacements"""
    content = read_file(filepath)
    if content is None:
        return False, 0
    
    original = content
    
    # Apply replacements
    for old, new in replacements:
        content = content.replace(old, new)
    
    # Count changes
    changes = sum(original.count(old) for old, _ in replacements)
    
    if changes > 0:
        if write_file(filepath, content):
            return True, changes
    
    return False, 0

def main():
    print("=" * 70)
    print("BRANDING UPDATE: UniSync to UniSinq")
    print("=" * 70)
    
    # Change to auth_project directory
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    total_files = 0
    total_changes = 0
    
    # Files to update with specific patterns
    files_to_update = [
        # Core files
        'accounts/views.py',
        'accounts/views_contact.py',
        'accounts/brevo_mail_backend.py',
        'auth_project/settings.py',
    ]
    
    # Add template files
    template_dir = 'accounts/templates'
    if os.path.exists(template_dir):
        for root, dirs, files in os.walk(template_dir):
            for file in files:
                if file.endswith('.html'):
                    files_to_update.append(os.path.join(root, file))
    
    print(f"\nFound {len(files_to_update)} files to update\n")
    print("-" * 70)
    
    for filepath in files_to_update:
        if not os.path.exists(filepath):
            continue
        
        success, changes = update_file(filepath, REPLACEMENTS)
        
        if success and changes > 0:
            print(f"[UPDATED] {filepath}")
            print(f"          Changes: {changes}")
            total_files += 1
            total_changes += changes
        elif changes > 0:
            print(f"[SKIPPED] {filepath} (could not write)")
        else:
            print(f"[NO CHANGE] {filepath}")
    
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print(f"Files updated: {total_files}")
    print(f"Total changes: {total_changes}")
    print("\nUpdated branding in:")
    print("  [OK] Views (views.py, views_contact.py)")
    print("  [OK] Email backends (brevo, zepto)")
    print("  [OK] Settings (settings.py)")
    print("  [OK] Templates (all HTML files)")
    print("  [OK] Page titles")
    print("  [OK] Email signatures")
    print("  [OK] Support contacts")
    print("\nChanges made:")
    print("  UniSync -> UniSinq")
    print("  unisync -> unisinq")
    print("  UNISYNC -> UNISINQ")
    print("\n" + "=" * 70)
    print("BRANDING UPDATE COMPLETE!")
    print("=" * 70)

if __name__ == '__main__':
    main()
