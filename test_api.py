#!/usr/bin/env python
"""
API Testing Script for NGO Backend
Run this after starting the server to test all endpoints
"""

import requests
import json

BASE_URL = "http://127.0.0.1:8000/api"

def test_registration():
    """Test user registration"""
    data = {
        "username": "testuser",
        "email": "test@example.com",
        "password": "testpass123",
        "first_name": "Test",
        "phone": "1234567890"
    }
    response = requests.post(f"{BASE_URL}/auth/register/", json=data)
    print(f"Registration: {response.status_code}")
    if response.status_code == 201:
        return response.json()['token']
    return None

def test_login():
    """Test user login"""
    data = {
        "email": "test@example.com",
        "password": "testpass123"
    }
    response = requests.post(f"{BASE_URL}/auth/login/", json=data)
    print(f"Login: {response.status_code}")
    if response.status_code == 200:
        return response.json()['token']
    return None

def test_campaigns():
    """Test campaigns endpoint"""
    response = requests.get(f"{BASE_URL}/campaigns/")
    print(f"Campaigns List: {response.status_code}")

def test_events():
    """Test events endpoint"""
    response = requests.get(f"{BASE_URL}/events/")
    print(f"Events List: {response.status_code}")

def test_news():
    """Test news endpoint"""
    response = requests.get(f"{BASE_URL}/news/")
    print(f"News List: {response.status_code}")

if __name__ == "__main__":
    print("Testing NGO Backend API...")
    print("=" * 30)
    
    # Test registration
    token = test_registration()
    
    # Test login
    if not token:
        token = test_login()
    
    # Test other endpoints
    test_campaigns()
    test_events()
    test_news()
    
    print("=" * 30)
    print("API testing completed!")