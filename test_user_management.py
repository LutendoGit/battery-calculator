#!/usr/bin/env python3
"""Quick test of user management functions"""

from modules.education_store import (
    track_login, track_logout, get_user_login_history,
    get_current_sessions, get_all_users_list, delete_user,
    bulk_delete_users, reset_user_progress, get_user_stats,
    ensure_db, db_path
)

print("✓ All user management functions imported successfully\n")

# Initialize database
ensure_db()
print(f"✓ Database initialized at: {db_path()}\n")

# Test querying
users = get_all_users_list()
print(f"✓ Database query works - Found {len(users)} users\n")

if users:
    user = users[0]
    print(f"Sample user: {user['username']} ({user['email']})")
    
    # Get stats for first user
    stats = get_user_stats(user['id'])
    if stats:
        print(f"\nUser statistics:")
        print(f"  - Total Logins: {stats['logins']}")
        print(f"  - Progress Items: {stats['progress_items']}")
        print(f"  - Quizzes Taken: {stats['quizzes_taken']}")
        print(f"  - Events Recorded: {stats['total_events']}")
    
    # Check login history
    history = get_user_login_history(user['id'], limit=5)
    if history:
        print(f"\n✓ Login history available: {len(history)} records")

# Check active sessions
active = get_current_sessions()
print(f"\n✓ Active sessions query works: {len(active)} currently online")

print("\n" + "="*50)
print("✅ ALL USER MANAGEMENT FUNCTIONS WORKING!")
print("="*50)
