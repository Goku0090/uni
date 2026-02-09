#!/usr/bin/env python
"""
Verify that branding has been updated from UniSync to UniSinq
"""
import os
import re

def search_for_term(root_dir, term, file_extensions):
    """Search for a term in files"""
    found = []
    for root, dirs, files in os.walk(root_dir):
        # Skip certain directories
        dirs[:] = [d for d in dirs if d not in ['.git', '__pycache__', 'venv', '.venv', 'node_modules']]
        
        for file in files:
            if any(file.endswith(ext) for ext in file_extensions):
                filepath = os.path.join(root, file)
                try:
                    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()
                        if term.lower() in content.lower():
                            count = len(re.findall(re.escape(term), content, re.IGNORECASE))
                            found.append((filepath, count))
                except:
                    pass
    return found

def main():
    print("=" * 70)
    print("BRANDING VERIFICATION: UniSinq Update Check")
    print("=" * 70)
    
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    # Extensions to check
    extensions = ['.html', '.py', '.js', '.css', '.txt', '.md']
    
    # Check for remaining UniSync references (should be minimal)
    print("\n[1] Checking for remaining 'UniSync' references...")
    print("-" * 70)
    
    unisync_files = search_for_term('.', 'unisync', extensions)
    
    # Filter out files that might legitimately have 'unisync' (like old test files)
    legitimate = [
        'update_branding_unisync_to_unisinq.py',
        'fix_duplicate_social_apps_final.py',
        'cleanup_social_apps.py',
        'unisync-/',
    ]
    
    unisync_files = [(f, c) for f, c in unisync_files if not any(l in f for l in legitimate)]
    
    if unisync_files:
        print(f"Found {len(unisync_files)} file(s) with 'unisync' references:")
        for filepath, count in sorted(unisync_files):
            print(f"  {filepath}: {count} occurrence(s)")
    else:
        print("[OK] No remaining 'unisync' references found!")
    
    # Check for UniSinq references (should have many)
    print("\n[2] Checking for 'UniSinq' branding...")
    print("-" * 70)
    
    unisinq_files = search_for_term('.', 'unisinq', extensions)
    
    if unisinq_files:
        print(f"Found {len(unisinq_files)} file(s) with 'unisinq' references:")
        total_count = sum(c for _, c in unisinq_files)
        print(f"Total occurrences: {total_count}")
        
        # Show sample files
        for filepath, count in sorted(unisinq_files)[:10]:
            print(f"  {filepath}: {count} occurrence(s)")
        
        if len(unisinq_files) > 10:
            print(f"  ... and {len(unisinq_files) - 10} more files")
    else:
        print("[WARNING] No 'unisinq' references found!")
    
    # Check key files
    print("\n[3] Checking key branding locations...")
    print("-" * 70)
    
    key_checks = [
        ('accounts/views.py', 'UniSinq', 'Registration message'),
        ('accounts/views_contact.py', 'support@unisinq.com', 'Support email'),
        ('auth_project/settings.py', 'unisinq.app', 'Email domain'),
        ('accounts/templates/messages.html', 'UniSinq', 'Messages page'),
        ('accounts/templates/notifications.html', 'UniSinq', 'Notifications page'),
        ('accounts/templates/my_connections.html', 'UniSinq', 'Connections page'),
        ('accounts/templates/post_project.html', 'UniSinq', 'Post project page'),
    ]
    
    all_good = True
    for filepath, term, description in key_checks:
        if os.path.exists(filepath):
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                if term in content:
                    print(f"[OK] {description:30} - Found in {filepath}")
                else:
                    print(f"[MISSING] {description:30} - NOT found in {filepath}")
                    all_good = False
        else:
            print(f"[FILE NOT FOUND] {filepath}")
            all_good = False
    
    # Summary
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    
    if all_good and not unisync_files:
        print("[SUCCESS] Branding update verified!")
        print("  - All key files have 'UniSinq' branding")
        print("  - No remaining 'UniSync' references in code")
        print("\nNext steps:")
        print("  1. Clear browser cache (Ctrl+Shift+Delete)")
        print("  2. Restart Django server")
        print("  3. Test pages: /messages/, /notifications/, /my-connections/")
        print("  4. Verify email sending with correct domain")
    else:
        if unisync_files:
            print("[WARNING] Some 'unisync' references remain:")
            for filepath, _ in unisync_files[:5]:
                print(f"  - {filepath}")
        
        if not all_good:
            print("[WARNING] Some key files missing expected branding")
        
        print("\nTo fix:")
        print("  1. Review remaining references")
        print("  2. Run: python update_branding_unisync_to_unisinq.py")
        print("  3. Re-run this verification")
    
    print("\n" + "=" * 70)

if __name__ == '__main__':
    main()
