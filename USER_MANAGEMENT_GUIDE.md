# User Management & Login Tracking Documentation

## Overview

Your Battery Calculator application now has comprehensive user management and login tracking capabilities. This includes:

- **Login Tracking**: Automatically records when users log in and out, including IP address and session ID
- **User Management**: Add, remove, or manage user accounts
- **Progress Management**: Track user learning progress and quiz attempts
- **Admin Dashboard**: Web interface to manage all users and view analytics

## Features

### 1. Login Tracking
- Every successful login is recorded with:
  - User ID
  - Timestamp (ISO-8601 UTC)
  - Session ID (UUID)
  - IP Address
  - Login duration (calculated from logout time)
  
- Login data is stored in the `login_tracking` table in your SQLite database

### 2. User Management Functions

#### Track a Login
```python
from modules.education_store import track_login

# Returns login_id which can be used to record logout
login_id = track_login(user_id=1, session_id="uuid", ip_address="192.168.1.1")
```

#### Track a Logout
```python
from modules.education_store import track_logout

track_logout(login_id)
```

#### Get User Login History
```python
from modules.education_store import get_user_login_history

history = get_user_login_history(user_id=1, limit=50)
# Returns list of dicts with login_at, logout_at, session_id, ip_address
```

#### Get Current Active Sessions
```python
from modules.education_store import get_current_sessions

sessions = get_current_sessions()
# Returns all users currently logged in (logout_at IS NULL)
```

#### Get All Users
```python
from modules.education_store import get_all_users_list

users = get_all_users_list()
# Returns all users with id, username, email, created_at, avatar_filename
```

#### Delete a User
```python
from modules.education_store import delete_user

success = delete_user(user_id=1)
# Returns True if deleted, False if not found
# Cascades: deletes all related progress, quiz_attempts, login_tracking, etc.
```

#### Delete Multiple Users
```python
from modules.education_store import bulk_delete_users

result = bulk_delete_users(user_ids=[1, 2, 3])
# Returns {"deleted": 3, "failed": 0, "total": 3}
```

#### Reset User Progress
```python
from modules.education_store import reset_user_progress

reset_user_progress(user_id=1)
# Clears all progress and quiz_attempts for the user (keeps account active)
```

#### Get User Statistics
```python
from modules.education_store import get_user_stats

stats = get_user_stats(user_id=1)
# Returns comprehensive stats including logins, progress, quiz data, events
```

## Database Schema

### login_tracking Table
```sql
CREATE TABLE login_tracking (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    login_at TEXT NOT NULL,          -- ISO-8601 UTC timestamp
    logout_at TEXT,                  -- NULL while logged in
    session_id TEXT,                 -- UUID for session
    ip_address TEXT,                 -- Client IP address
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Indexes for efficient queries
CREATE INDEX idx_login_tracking_user ON login_tracking(user_id);
CREATE INDEX idx_login_tracking_time ON login_tracking(login_at);
```

## Admin API Endpoints

All endpoints require `ADMIN_STREAM_TOKEN` environment variable to be set. 
Provide token via `?token=...` query parameter or `X-Admin-Token` header.

### User List & Management
```
GET    /learn/admin/api/users/list
       Returns all users

GET    /learn/admin/api/users/<user_id>/stats
       Get comprehensive stats for a user

GET    /learn/admin/api/users/<user_id>/logins?limit=50
       Get login history for a user

DELETE /learn/admin/api/users/<user_id>
       Delete a user and all their data

POST   /learn/admin/api/users/bulk-delete
       Delete multiple users (JSON body: {"user_ids": [1,2,3]})

POST   /learn/admin/api/users/<user_id>/reset-progress
       Clear progress/quiz data (keep account)
```

### Session & Login Management
```
GET    /learn/admin/api/sessions/current
       Get all currently active sessions

GET    /learn/admin/api/logins/summary
       Get login statistics (today's logins, active sessions, avg duration)
```

## Admin Dashboard

### Accessing the Dashboard

1. **Set Admin Token** (in environment variables or `.env`):
   ```
   ADMIN_STREAM_TOKEN=your-secret-token-here
   ```

2. **Navigate to Admin Page**:
   ```
   http://localhost:5000/learn/admin/users?token=your-secret-token-here
   ```

### Dashboard Features

**Tabs:**
- **All Users**: Browse all registered users, search by username/email, delete users
- **Active Sessions**: View currently logged-in users with session details
- **User Details**: View detailed stats and login history for a specific user

**Statistics Displayed:**
- Total number of users
- Number of active sessions
- Logins today
- Average session duration

**Actions Available:**
- View user details and login history
- Delete individual users
- Bulk delete multiple users
- Reset user progress
- Search and filter users

## Implementation Details

### Automatic Login Tracking

Login tracking is automatically integrated into the login flow:

1. User submits login credentials
2. `authenticate_user()` validates credentials
3. User is logged in, session created
4. `track_login()` is called with user_id, session_id, and IP address
5. Login ID is stored in session for later logout tracking
6. User is redirected to dashboard

### Logout Tracking

When user logs out:

1. `track_logout()` is called with the login_id
2. Logout timestamp is recorded
3. Session variables are cleared
4. User is redirected to login page

## Example Usage Scenarios

### Scenario 1: Find All Users Logged In from a Specific IP

```python
from modules.education_store import get_current_sessions

sessions = get_current_sessions()
target_ip = "192.168.1.100"

matching = [s for s in sessions if s.get('ip_address') == target_ip]
for session in matching:
    print(f"{session['username']} logged in from {session['ip_address']}")
```

### Scenario 2: Delete an Inactive User & Clean Their Data

```python
from modules.education_store import get_user_login_history, delete_user
from datetime import datetime, timedelta

user_id = 5
history = get_user_login_history(user_id)

if history:
    last_login = datetime.fromisoformat(history[0]['login_at'])
    days_inactive = (datetime.now() - last_login.replace(tzinfo=None)).days
    
    if days_inactive > 90:
        success = delete_user(user_id)
        if success:
            print(f"Deleted inactive user {user_id}")
```

### Scenario 3: Export Login Report

```python
from modules.education_store import get_all_users_list, get_user_login_history
import csv

users = get_all_users_list()

with open('login_report.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['Username', 'Total Logins', 'Last Login', 'Avg Session Duration'])
    
    for user in users:
        history = get_user_login_history(user['id'], limit=1000)
        total_logins = len(history)
        last_login = history[0]['login_at'] if history else 'Never'
        
        writer.writerow([
            user['username'],
            total_logins,
            last_login,
            'N/A for now'
        ])
```

## Configuration

### Environment Variables

```bash
# Required for admin endpoints
ADMIN_STREAM_TOKEN=your-secure-random-token

# Example: Generate a secure token
# python -c "import secrets; print(secrets.token_urlsafe(32))"
```

### Database Location

Login tracking data is stored in:
```
data/education.db
```

The database file is created automatically when the app starts.

## Troubleshooting

### Issue: Login tracking not recording

**Check:**
1. Ensure `ADMIN_STREAM_TOKEN` environment variable is set
2. Verify `track_login()` is being called in the login route
3. Check database permissions for `data/education.db`

### Issue: Can't access admin dashboard

**Check:**
1. Token is correct and matches `ADMIN_STREAM_TOKEN`
2. URL includes token: `/learn/admin/users?token=...`
3. Flask app is running and education blueprint is registered

### Issue: Session data missing after logout

**Check:**
1. Verify `track_logout()` is called before session is cleared
2. Ensure `login_id` is stored in session during login
3. Check database for logout_at timestamp

## Best Practices

1. **Backup Database**: Regularly backup `data/education.db` before bulk operations
2. **Use Bulk Operations**: For deleting many users, use `bulk_delete_users()` instead of loops
3. **Secure Admin Token**: Use a strong, random token and rotate it periodically
4. **Monitor Sessions**: Regularly check for idle/orphaned sessions
5. **Archive Old Data**: Consider archiving login data older than 1 year for performance

## Performance Considerations

- Login tracking adds minimal overhead (single INSERT per login)
- Indexes on `user_id` and `login_at` ensure fast queries
- For large databases (10,000+ users), consider archiving old login data
- Session queries are optimized with indexes

## Future Enhancements

Possible additions to consider:

1. **Geolocation**: Track IP geolocation for security
2. **Device Fingerprinting**: Identify device types
3. **Login Alerts**: Alert admins of suspicious login patterns
4. **GDPR Compliance**: Auto-delete old login data
5. **Session Management**: Force logout, session timeout settings
6. **2FA Support**: Two-factor authentication integration

## Support

For issues or questions:

1. Check the troubleshooting section above
2. Review `modules/education_store.py` for function signatures
3. Check Flask logs for error messages
4. Verify database integrity with SQLite CLI

## Summary

Your application now has enterprise-grade user tracking and management capabilities. The system is designed to be:

- **Automatic**: Login tracking works without code changes
- **Scalable**: Handles thousands of users efficiently
- **Secure**: Admin-token protected, cascading deletes prevent orphaned data
- **User-Friendly**: Web dashboard for non-technical management
- **Developer-Friendly**: Simple Python API for custom integration
