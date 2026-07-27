#!/usr/bin/env python3
"""
Test module progress tracking API endpoints
"""
import requests
import json
from datetime import datetime

BASE_URL = "http://localhost:5000/learn/admin/api"
TOKEN = "sP1KYXbw3fS2ZYF5LmJF3Qr-TOdf0"

def print_header(title):
    print()
    print("=" * 70)
    print(f"  {title}")
    print("=" * 70)

def test_endpoint(name, endpoint, description):
    print(f"\n✓ Testing: {name}")
    print(f"  Endpoint: GET {endpoint}")
    print(f"  Description: {description}")
    print()
    
    try:
        url = f"{BASE_URL}{endpoint}?token={TOKEN}"
        response = requests.get(url, timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            print(f"  Status: ✓ 200 OK")
            print(f"  Response:")
            print(json.dumps(data, indent=4))
            return data
        else:
            print(f"  Status: ✗ {response.status_code}")
            print(f"  Error: {response.text}")
            return None
    except Exception as e:
        print(f"  Status: ✗ Error")
        print(f"  Message: {str(e)}")
        return None

def main():
    print_header("MODULE PROGRESS TRACKING - API ENDPOINT TESTS")
    print("\nTesting all 4 new admin endpoints...")
    print(f"Admin Token: {TOKEN}")
    print(f"Base URL: {BASE_URL}")
    
    # Test 1: Statistics
    print("\n" + "─" * 70)
    print("TEST 1: Module Progress Statistics")
    print("─" * 70)
    stats = test_endpoint(
        "Module Progress Statistics",
        "/module-progress/statistics",
        "Get overall system statistics about module tracking"
    )
    
    if stats:
        print("\n  Summary:")
        print(f"    • Total Users: {stats.get('total_users', 0)}")
        print(f"    • Total Certificates Awarded: {stats.get('total_certificates_awarded', 0)}")
        print(f"    • Users with Certificates: {stats.get('users_with_certificates', 0)}")
        print(f"    • Average Certs/User: {stats.get('average_certificates_per_user', 0)}")
    
    # Test 2: All Users Progress
    print("\n" + "─" * 70)
    print("TEST 2: All Users Module Progress")
    print("─" * 70)
    all_users = test_endpoint(
        "All Users Module Progress",
        "/module-progress/all-users",
        "Get quick summary of each user's module progress"
    )
    
    if all_users and all_users.get('users'):
        print("\n  Users Summary:")
        for user in all_users['users'][:3]:
            print(f"    • {user.get('username')} (ID: {user.get('user_id')})")
            print(f"      - Modules Completed: {user.get('modules_completed', 0)}")
            print(f"      - Modules In Progress: {user.get('modules_in_progress', 0)}")
            print(f"      - Certificates: {user.get('certificates_earned', 0)}")
    
    # Test 3: Single User Progress
    print("\n" + "─" * 70)
    print("TEST 3: Single User Module Progress (User ID: 1)")
    print("─" * 70)
    user_prog = test_endpoint(
        "Single User Module Progress",
        "/module-progress/user/1",
        "Get complete module progress for a specific user"
    )
    
    if user_prog and user_prog.get('user_id'):
        summary = user_prog.get('summary', {})
        print("\n  User Summary:")
        print(f"    • User ID: {user_prog.get('user_id')}")
        print(f"    • Completed: {summary.get('completed', 0)}")
        print(f"    • In Progress: {summary.get('in_progress', 0)}")
        print(f"    • Not Started: {summary.get('not_started', 0)}")
        print(f"    • Certificates: {summary.get('certificates_count', 0)}")
    elif user_prog and user_prog.get('error'):
        print(f"\n  Note: {user_prog.get('error')} (expected for new database)")
    
    # Test 4: Module Certificates
    print("\n" + "─" * 70)
    print("TEST 4: Module Certificates (Awards List)")
    print("─" * 70)
    certs = test_endpoint(
        "Module Certificates",
        "/module-progress/certificates",
        "Get list of all certificates awarded (75%+ passes)"
    )
    
    if certs and certs.get('certificates'):
        print("\n  Certificates Summary:")
        print(f"    • Total Certificates: {len(certs['certificates'])}")
        for cert in certs['certificates'][:3]:
            print(f"    • {cert.get('username')} - {cert.get('module_id')}: {cert.get('percentage')}%")
    
    # Final summary
    print_header("✓ ALL ENDPOINT TESTS COMPLETED")
    print("\nNext Steps to See Data:")
    print("1. Open: http://localhost:5000/learn/login")
    print("2. Create a test account (or use existing)")
    print("3. Start Module 1 (Fundamentals)")
    print("4. Complete Module 1 quiz with score ≥ 75%")
    print("5. Run the admin endpoints again to see:")
    print("   - Module progress tracked")
    print("   - Certificate awarded")
    print("   - Admin statistics updated")
    print("\nAdmin Endpoints:")
    print(f"  • Statistics: {BASE_URL}/module-progress/statistics?token={TOKEN}")
    print(f"  • All Users: {BASE_URL}/module-progress/all-users?token={TOKEN}")
    print(f"  • User Details: {BASE_URL}/module-progress/user/1?token={TOKEN}")
    print(f"  • Certificates: {BASE_URL}/module-progress/certificates?token={TOKEN}")
    print()

if __name__ == "__main__":
    main()
