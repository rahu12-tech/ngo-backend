#!/usr/bin/env python
"""
Quick PostgreSQL Setup Script
"""
import os
import subprocess
import sys

def run_command(command, description):
    """Run command with description"""
    print(f"\n🔄 {description}...")
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    if result.returncode == 0:
        print(f"✅ {description} - Success!")
        if result.stdout:
            print(result.stdout)
    else:
        print(f"❌ {description} - Failed!")
        print(result.stderr)
        return False
    return True

def main():
    print("🚀 NGO Backend Quick Setup")
    print("=" * 40)
    
    # Check if PostgreSQL is running
    print("\n📋 Setup Checklist:")
    print("1. PostgreSQL installed? (https://www.postgresql.org/download/)")
    print("2. PostgreSQL service running?")
    print("3. Database 'ngo_db' created?")
    print("4. Password set in .env file?")
    
    input("\nPress Enter when ready to continue...")
    
    # Run migrations
    if not run_command("python manage.py makemigrations", "Creating migrations"):
        return
    
    if not run_command("python manage.py migrate", "Applying migrations"):
        return
    
    # Create superuser prompt
    print("\n👤 Create superuser for admin access:")
    run_command("python manage.py createsuperuser", "Creating superuser")
    
    print("\n🎉 Setup completed!")
    print("\nNext steps:")
    print("1. python manage.py runserver")
    print("2. Visit http://127.0.0.1:8000/admin/")
    print("3. Test API: python test_api.py")

if __name__ == "__main__":
    main()