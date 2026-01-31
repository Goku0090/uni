#!/usr/bin/env python
"""
Quick script to run social app setup
"""
import subprocess
import sys
import os

def run_social_setup():
    """Run the Django management command to setup social apps"""
    try:
        # Change to the project directory
        os.chdir('auth_project')

        # Run the management command
        result = subprocess.run([
            sys.executable, 'manage.py', 'setup_social_apps'
        ], capture_output=True, text=True, cwd='.')

        print("STDOUT:")
        print(result.stdout)
        if result.stderr:
            print("STDERR:")
            print(result.stderr)

        print(f"Return code: {result.returncode}")

        if result.returncode == 0:
            print("\n✅ Social login setup completed successfully!")
            print("🔗 The Google and GitHub login buttons should now be visible on the login page.")
        else:
            print("\n❌ Setup failed. Please check the output above for errors.")

    except Exception as e:
        print(f"❌ Error running setup: {e}")

if __name__ == '__main__':
