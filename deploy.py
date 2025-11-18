#!/usr/bin/env python
"""
Production Deployment Script
"""
import os
import subprocess

def run_command(command):
    """Run shell command"""
    print(f"Running: {command}")
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error: {result.stderr}")
    else:
        print(f"Success: {result.stdout}")

def deploy():
    """Deploy application"""
    print("Starting deployment...")
    
    # Install dependencies
    run_command("pip install -r requirements.txt")
    
    # Run migrations
    run_command("python manage.py makemigrations")
    run_command("python manage.py migrate")
    
    # Collect static files
    run_command("python manage.py collectstatic --noinput")
    
    print("Deployment completed!")

if __name__ == "__main__":
    deploy()