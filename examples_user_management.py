#!/usr/bin/env python3
"""
Example script demonstrating user management and login tracking functions.

Run this script from the project root:
    python examples_user_management.py

Note: This assumes the Flask app is NOT running (or use within Flask context)
"""

import os
import sys
from datetime import datetime, timedelta

# Add project to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from modules.education_store import (
    get_all_users_list,
    get_user,
    get_user_login_history,
    get_current_sessions,
    get_user_stats,
    delete_user,
    reset_user_progress,
    track_login,
)

def print_section(title):
    """Print a formatted section header."""
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}\n")

def example_1_list_all_users():
    """Example 1: List all registered users."""
    print_section("Example 1: List All Users")
    
    users = get_all_users_list()
    
    if not users:
        print("No users found in database.")
        return
    
    print(f"Total users: {len(users)}\n")
    
    for user in users[:10]:  # Show first 10
        print(f"  ID: {user['id']:<5} Username: {user['username']:<20} Email: {user['email']}")
    
    if len(users) > 10:
        print(f"\n  ... and {len(users) - 10} more users")

def example_2_user_login_history():
    """Example 2: View login history for a specific user."""
    print_section("Example 2: User Login History")
    
    users = get_all_users_list()
    if not users:
        print("No users found.")
        return
    
    user_id = users[0]['id']
    user = get_user(user_id)
    
    print(f"Viewing login history for: {user.username} (ID: {user.id})\n")
    
    history = get_user_login_history(user_id, limit=10)
    
    if not history:
        print("No login history found.")
        return
    
    print(f"Recent logins (showing up to 10):\n")
    
    for i, login in enumerate(history, 1):
        login_time = datetime.fromisoformat(login['login_at'])
        logout_time = datetime.fromisoformat(login['logout_at']) if login['logout_at'] else None
        
        duration = "Still logged in"
        if logout_time:
            duration = f"{(logout_time - login_time).total_seconds() / 60:.1f} minutes"
        
        ip = login['ip_address'] or "Unknown"
        
        print(f"  {i}. {login_time.strftime('%Y-%m-%d %H:%M:%S')} - {duration} - IP: {ip}")

def example_3_active_sessions():
    """Example 3: View currently active sessions."""
    print_section("Example 3: Currently Active Sessions")
    
    sessions = get_current_sessions()
    
    if not sessions:
        print("No active sessions.")
        return
    
    print(f"Active sessions: {len(sessions)}\n")
    
    for session in sessions:
        login_time = datetime.fromisoformat(session['login_at'])
        duration = (datetime.now() - login_time).total_seconds() / 60
        
        print(f"  User: {session['username']:<15} IP: {session['ip_address']:<15} Duration: {duration:.1f} min")

def example_4_user_statistics():
    """Example 4: Get comprehensive user statistics."""
    print_section("Example 4: User Statistics")
    
    users = get_all_users_list()
    if not users:
        print("No users found.")
        return
    
    user_id = users[0]['id']
    stats = get_user_stats(user_id)
    
    if not stats:
        print(f"User {user_id} not found.")
        return
    
    print(f"Statistics for: {stats['user']['username']}\n")
    print(f"  Email: {stats['user']['email']}")
    print(f"  Total Logins: {stats['logins']}")
    print(f"  Progress Items Completed: {stats['progress_items_completed']}")
    print(f"  Quizzes Taken: {stats['quizzes_taken']}")
    print(f"  Total Events: {stats['total_events']}")

def example_5_find_inactive_users():
    """Example 5: Find users inactive for more than N days."""
    print_section("Example 5: Find Inactive Users")
    
    users = get_all_users_list()
    if not users:
        print("No users found.")
        return
    
    inactive_days = 30
    inactive_users = []
    
    for user in users:
        history = get_user_login_history(user['id'], limit=1)
        
        if not history:
            # User never logged in
            created = datetime.fromisoformat(user['created_at'])
            age = (datetime.now() - created).days
            if age > inactive_days:
                inactive_users.append({
                    'username': user['username'],
                    'status': f'Never logged in ({age} days since creation)'
                })
        else:
            last_login = datetime.fromisoformat(history[0]['login_at'])
            days_inactive = (datetime.now() - last_login).days
            
            if days_inactive > inactive_days:
                inactive_users.append({
                    'username': user['username'],
                    'status': f'Inactive for {days_inactive} days'
                })
    
    if not inactive_users:
        print(f"No users inactive for more than {inactive_days} days.")
        return
    
    print(f"Found {len(inactive_users)} inactive users:\n")
    
    for user in inactive_users[:10]:
        print(f"  - {user['username']:<20} {user['status']}")
    
    if len(inactive_users) > 10:
        print(f"\n  ... and {len(inactive_users) - 10} more")

def example_6_login_statistics():
    """Example 6: Calculate login statistics."""
    print_section("Example 6: Login Statistics")
    
    users = get_all_users_list()
    if not users:
        print("No users found.")
        return
    
    total_logins = 0
    users_with_logins = 0
    avg_logins = 0
    
    today = datetime.now().date()
    logins_today = 0
    
    for user in users:
        history = get_user_login_history(user['id'], limit=1000)
        
        if history:
            users_with_logins += 1
            total_logins += len(history)
            
            # Count today's logins
            for login in history:
                login_date = datetime.fromisoformat(login['login_at']).date()
                if login_date == today:
                    logins_today += 1
    
    if users_with_logins > 0:
        avg_logins = total_logins / users_with_logins
    
    print(f"Total users: {len(users)}")
    print(f"Users with login history: {users_with_logins}")
    print(f"Total logins recorded: {total_logins}")
    print(f"Average logins per user: {avg_logins:.1f}")
    print(f"Logins today: {logins_today}")

def example_7_demo_login_tracking():
    """Example 7: Demonstrate login tracking (creates test data)."""
    print_section("Example 7: Demo Login Tracking")
    
    print("Note: This creates test login records in the database.\n")
    
    users = get_all_users_list()
    if not users:
        print("No users found to track login for. Create a user first.")
        return
    
    user_id = users[0]['id']
    user = get_user(user_id)
    
    print(f"Recording test login for user: {user.username}")
    
    login_id = track_login(
        user_id=user_id,
        session_id="demo-session-12345",
        ip_address="192.168.1.100"
    )
    
    print(f"✓ Login recorded with ID: {login_id}")
    print(f"  User ID: {user_id}")
    print(f"  Session ID: demo-session-12345")
    print(f"  IP Address: 192.168.1.100")
    print(f"\nCheck login_tracking table to see the record.")

def main():
    """Run all examples."""
    print("\n" + "="*60)
    print("  USER MANAGEMENT & LOGIN TRACKING EXAMPLES")
    print("="*60)
    
    try:
        # Run examples
        example_1_list_all_users()
        example_2_user_login_history()
        example_3_active_sessions()
        example_4_user_statistics()
        example_5_find_inactive_users()
        example_6_login_statistics()
        example_7_demo_login_tracking()
        
        print("\n" + "="*60)
        print("  ALL EXAMPLES COMPLETED")
        print("="*60)
        print("\nFor more information, see USER_MANAGEMENT_GUIDE.md")
        print("For quick start, see QUICKSTART_USER_MANAGEMENT.md\n")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
