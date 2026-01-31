#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Fix User Password Issues
"""

import os
import sys
import django

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'auth_project.settings')
sys.path.insert(0, os.path.dirname(__file__))
django.setup()

from django.contrib.auth.models import User
from django.contrib.auth import authenticate

print("\n" + "="*70)
print("USER PASSWORD FIX")
print("="*70)

# List all users
users = User.objects.all()
print(f"\nUsers in database: {users.count()}")
for user in users:
    print(f"\nUser: {user.username}")
    print(f"  Email: {user.email}")
    print(f"  Password hash: {user.password[:20]}...")
    print(f"  Is active: {user.is_active}")
    print(f"  Is staff: {user.is_staff}")

# Reset password for the user
print("\n" + "="*70)
print("RESETTING USER PASSWORDS")
print("="*70)

for user in users:
    # Set a simple test password
    new_password = 'password123'
    user.set_password(new_password)
    user.save()
    print(f"\nReset password for {user.username}")
    print(f"  New password: {new_password}")
    
    # Test authentication
    test_user = authenticate(username=user.username, password=new_password)
    if test_user:
        print(f"  Authentication: OK")
    else:
        print(f"  Authentication: FAILED")

print("\n" + "="*70)
print("DONE")
print("="*70)
print("\nYou can now login with:")
for user in User.objects.all():
    print(f"  Username: {user.username}")
    print(f"  Password: password123")
