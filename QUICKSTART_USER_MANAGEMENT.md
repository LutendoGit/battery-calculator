# Quick Start: User Management & Login Tracking

## What's Been Added

✅ **Login Tracking System**
- Automatically records every user login with timestamp, IP address, and session ID
- Tracks logout times to calculate session duration
- Stored in `login_tracking` table in your SQLite database

✅ **User Management Functions**
- `track_login()` - Record a user login
- `track_logout()` - Record a user logout
- `get_user_login_history()` - View login history for a user
- `get_current_sessions()` - See who's currently logged in
- `delete_user()` - Remove a user and all their data
- `bulk_delete_users()` - Delete multiple users at once
- `reset_user_progress()` - Clear user progress without deleting account
- `get_user_stats()` - Get comprehensive user statistics

✅ **Admin API Endpoints** (6 new endpoints)
- `/learn/admin/api/users/list` - List all users
- `/learn/admin/api/users/<id>/stats` - View user statistics
- `/learn/admin/api/users/<id>/logins` - View login history
- `/learn/admin/api/sessions/current` - See active sessions
- `/learn/admin/api/users/<id>` (DELETE) - Delete user
- `/learn/admin/api/logins/summary` - Login statistics

✅ **Admin Dashboard Web Interface**
- Visual dashboard at `/learn/admin/users?token=YOUR_TOKEN`
- Browse all users with search
- View active sessions
- Manage users (view details, delete, reset progress)
- View analytics and statistics

## Getting Started

### Step 1: Set Admin Token

Add this to your environment variables or `.env` file:

```bash
ADMIN_STREAM_TOKEN=super-secret-admin-token-here
```

Generate a secure token:
```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

### Step 2: Access Admin Dashboard

Navigate to:
```
http://localhost:5000/learn/admin/users?token=your-admin-token
```

Or use the header:
```bash
curl -H "X-Admin-Token: your-admin-token" http://localhost:5000/learn/admin/api/users/list
```

### Step 3: Start Using

**In Python code:**
```python
from modules.education_store import (
    get_all_users_list,
    delete_user,
    get_user_login_history,
    get_current_sessions
)

# List all users
users = get_all_users_list()

# Get active sessions
active = get_current_sessions()

# View login history for user 1
history = get_user_login_history(1)

# Delete user 5
delete_user(5)
```

## Key Files Modified

1. **modules/education_store.py**
   - Added `login_tracking` table schema
   - Added 8 new functions for user management
   - Functions are exported and ready to use

2. **routes/education_routes.py**
   - Login tracking integrated into `/login` route
   - Logout tracking integrated into `/logout` route
   - Added 7 new admin API endpoints
   - Added admin dashboard route

3. **templates/education/admin_user_management.html** (NEW)
   - Professional web dashboard
   - User browsing with search
   - Session monitoring
   - Bulk delete functionality
   - User statistics

## Files to Reference

- **[USER_MANAGEMENT_GUIDE.md](./USER_MANAGEMENT_GUIDE.md)** - Full documentation
- **modules/education_store.py** - Function implementations
- **routes/education_routes.py** - API endpoints and integration

## Example Use Cases

### Get User Login Count
```python
from modules.education_store import get_user_login_history

user_id = 1
logins = get_user_login_history(user_id, limit=1000)
print(f"User {user_id} has logged in {len(logins)} times")
```

### Find Inactive Users
```python
from modules.education_store import get_all_users_list, get_user_login_history
from datetime import datetime, timedelta

users = get_all_users_list()
inactive_days = 30

for user in users:
    history = get_user_login_history(user['id'], limit=1)
    if history:
        last_login = datetime.fromisoformat(history[0]['login_at'])
        age = (datetime.now() - last_login.replace(tzinfo=None)).days
        if age > inactive_days:
            print(f"User {user['username']} inactive for {age} days")
```

### Get Today's Login Stats
```python
from modules.education_store import get_current_sessions

# Current active sessions
active = get_current_sessions()
print(f"Currently online: {len(active)} users")
for session in active:
    print(f"  - {session['username']} from {session['ip_address']}")
```

### Export User Report
```python
from modules.education_store import get_all_users_list, get_user_stats
import json

users = get_all_users_list()
report = []

for user in users:
    stats = get_user_stats(user['id'])
    report.append({
        'username': user['username'],
        'email': user['email'],
        'created': user['created_at'],
        **stats
    })

with open('user_report.json', 'w') as f:
    json.dump(report, f, indent=2)
```

## Important Notes

⚠️ **Backups**: Always backup `data/education.db` before bulk operations
⚠️ **Cascade Delete**: Deleting a user removes all their related data (progress, quizzes, sessions, etc.)
⚠️ **Admin Token**: Keep your `ADMIN_STREAM_TOKEN` secret - anyone with it can manage users
⚠️ **Session Data**: Login tracking automatically cleans up on logout (logout_at field set)

## Database Structure

The new `login_tracking` table:
```
id (PRIMARY KEY)
user_id (FOREIGN KEY → users)
login_at (ISO-8601 UTC timestamp)
logout_at (NULL while logged in)
session_id (UUID)
ip_address (Client IP)
```

Automatic indexes:
- On `user_id` for fast user lookups
- On `login_at` for time-range queries

## What Happens Automatically

1. ✅ Every successful login records timestamp + IP + session
2. ✅ Every logout records the logout time
3. ✅ Session duration is calculated from login_at and logout_at
4. ✅ User deletion cascades to remove all login records
5. ✅ Events are logged for audit trail

## Admin Endpoints Summary

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/admin/users` | GET | View dashboard |
| `/admin/api/users/list` | GET | Get all users |
| `/admin/api/users/<id>/stats` | GET | User statistics |
| `/admin/api/users/<id>/logins` | GET | Login history |
| `/admin/api/sessions/current` | GET | Active sessions |
| `/admin/api/logins/summary` | GET | Login stats |
| `/admin/api/users/<id>` | DELETE | Delete user |
| `/admin/api/users/bulk-delete` | POST | Delete multiple |
| `/admin/api/users/<id>/reset-progress` | POST | Clear progress |

All endpoints require `ADMIN_STREAM_TOKEN` authentication.

## Next Steps

1. Set your `ADMIN_STREAM_TOKEN` environment variable
2. Restart Flask app
3. Visit the admin dashboard at `/learn/admin/users?token=...`
4. Start managing users and monitoring logins!

For detailed documentation, see [USER_MANAGEMENT_GUIDE.md](./USER_MANAGEMENT_GUIDE.md)
