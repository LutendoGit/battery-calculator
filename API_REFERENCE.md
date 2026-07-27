# User Management API Reference

## Python Functions

All functions are available from `modules.education_store`:

```python
from modules.education_store import (
    track_login,
    track_logout,
    get_user_login_history,
    get_current_sessions,
    get_all_users_list,
    delete_user,
    bulk_delete_users,
    reset_user_progress,
    get_user_stats,
)
```

---

## Login Tracking Functions

### `track_login(user_id, session_id=None, ip_address=None) → int`

Records a user login in the `login_tracking` table.

**Parameters:**
- `user_id` (int): The user ID to track login for
- `session_id` (str, optional): UUID or session identifier
- `ip_address` (str, optional): Client IP address

**Returns:** `int` - The login record ID (use for `track_logout`)

**Raises:** None (handles errors gracefully)

**Example:**
```python
login_id = track_login(
    user_id=1,
    session_id="abc123def456",
    ip_address="192.168.1.100"
)
session['login_id'] = login_id  # Save for later logout
```

**Automatically Called:** Yes, in the login route after successful authentication

---

### `track_logout(login_id) → None`

Records the logout time for a login session.

**Parameters:**
- `login_id` (int): The login record ID from `track_login()`

**Returns:** `None`

**Raises:** None (handles invalid IDs gracefully)

**Example:**
```python
track_logout(session['login_id'])
session.pop('login_id', None)
```

**Automatically Called:** Yes, in the logout route

---

### `get_user_login_history(user_id, limit=50) → list[dict]`

Retrieves login history for a user (most recent first).

**Parameters:**
- `user_id` (int): The user ID to retrieve history for
- `limit` (int): Maximum records to return (default: 50, max: 500)

**Returns:** List of dictionaries with keys:
- `id` (int): Login record ID
- `user_id` (int): User ID
- `login_at` (str): ISO-8601 timestamp
- `logout_at` (str): ISO-8601 timestamp (NULL if still logged in)
- `session_id` (str): Session identifier
- `ip_address` (str): Client IP address

**Example:**
```python
history = get_user_login_history(user_id=1, limit=100)

for login in history:
    print(f"Logged in: {login['login_at']}")
    print(f"Logged out: {login['logout_at'] or 'Still logged in'}")
    print(f"From IP: {login['ip_address']}")
```

---

### `get_current_sessions() → list[dict]`

Get all currently active sessions (users still logged in).

**Parameters:** None

**Returns:** List of dictionaries with keys:
- `id` (int): Login record ID
- `user_id` (int): User ID
- `username` (str): Username
- `login_at` (str): ISO-8601 timestamp
- `session_id` (str): Session identifier
- `ip_address` (str): Client IP address

**Example:**
```python
active = get_current_sessions()
print(f"{len(active)} users currently online")

for session in active:
    duration_minutes = (datetime.now() - datetime.fromisoformat(session['login_at'])).total_seconds() / 60
    print(f"{session['username']} ({session['ip_address']}) - {duration_minutes:.0f} minutes")
```

---

## User Management Functions

### `get_all_users_list() → list[dict]`

Retrieve all users in the system.

**Parameters:** None

**Returns:** List of dictionaries with keys:
- `id` (int): User ID
- `username` (str): Username
- `email` (str): Email address
- `created_at` (str): ISO-8601 timestamp
- `avatar_filename` (str): Avatar filename (if set)

**Example:**
```python
users = get_all_users_list()
print(f"Total users: {len(users)}")

for user in users:
    print(f"{user['username']} ({user['email']}) - {user['created_at']}")
```

---

### `delete_user(user_id) → bool`

Delete a user account and all related data (cascading delete).

**Parameters:**
- `user_id` (int): The user ID to delete

**Returns:** `bool` - True if deleted, False if user not found

**Cascading Deletes:**
- `progress` records
- `quiz_attempts` records
- `login_tracking` records
- `user_events` records
- All user account data

**⚠️ WARNING:** This is permanent and cannot be undone!

**Example:**
```python
if delete_user(user_id=5):
    print("User deleted successfully")
else:
    print("User not found")
```

---

### `bulk_delete_users(user_ids) → dict`

Delete multiple users in one operation.

**Parameters:**
- `user_ids` (list[int]): List of user IDs to delete

**Returns:** Dictionary with keys:
- `deleted` (int): Number successfully deleted
- `failed` (int): Number that failed
- `total` (int): Total attempted

**Example:**
```python
result = bulk_delete_users(user_ids=[1, 2, 3, 4, 5])
print(f"Deleted {result['deleted']} users, {result['failed']} failed")
```

---

### `reset_user_progress(user_id) → None`

Clear all learning progress and quiz attempts for a user (keeps account active).

**Parameters:**
- `user_id` (int): The user ID to reset

**Returns:** `None`

**Clears:**
- All `progress` records
- All `quiz_attempts` records
- User account remains active

**Use Cases:**
- Reset user after course update
- Allow user to retake course
- Correct bad data

**Example:**
```python
# Reset user's progress
reset_user_progress(user_id=1)
print("User progress reset - they can start the course over")
```

---

### `get_user_stats(user_id) → dict`

Get comprehensive statistics for a user.

**Parameters:**
- `user_id` (int): The user ID to get stats for

**Returns:** Dictionary with structure:
```python
{
    "user": {
        "id": 1,
        "username": "john_doe",
        "email": "john@example.com",
        "created_at": "2026-01-15T10:30:00+00:00"
    },
    "logins": 42,
    "progress_items_completed": 15,
    "quizzes_taken": 8,
    "total_events": 156
}
```

Returns empty dict `{}` if user not found.

**Example:**
```python
stats = get_user_stats(user_id=1)

if stats:
    print(f"User: {stats['user']['username']}")
    print(f"Total Logins: {stats['logins']}")
    print(f"Progress Items: {stats['progress_items_completed']}")
    print(f"Quizzes: {stats['quizzes_taken']}")
else:
    print("User not found")
```

---

## REST API Endpoints

All endpoints require authentication via `ADMIN_STREAM_TOKEN`.

### Authentication

Provide token via:
- **Query parameter:** `?token=YOUR_TOKEN`
- **Header:** `X-Admin-Token: YOUR_TOKEN`

### User List Endpoint

```
GET /learn/admin/api/users/list
```

**Query Parameters:** None

**Response:**
```json
{
    "users": [
        {
            "id": 1,
            "username": "john_doe",
            "email": "john@example.com",
            "created_at": "2026-01-15T10:30:00",
            "avatar_filename": "avatar_1.png"
        },
        ...
    ]
}
```

---

### User Stats Endpoint

```
GET /learn/admin/api/users/<user_id>/stats
```

**URL Parameters:**
- `user_id` (int): User ID

**Response:**
```json
{
    "user": {
        "id": 1,
        "username": "john_doe",
        "email": "john@example.com",
        "created_at": "2026-01-15T10:30:00"
    },
    "logins": 42,
    "progress_items_completed": 15,
    "quizzes_taken": 8,
    "total_events": 156
}
```

**Error (404):**
```json
{"error": "User not found"}
```

---

### Login History Endpoint

```
GET /learn/admin/api/users/<user_id>/logins
```

**URL Parameters:**
- `user_id` (int): User ID

**Query Parameters:**
- `limit` (int, optional): Max results (default: 50, max: 500)

**Response:**
```json
{
    "login_history": [
        {
            "id": 1,
            "user_id": 1,
            "login_at": "2026-05-30T10:15:00",
            "logout_at": "2026-05-30T11:30:00",
            "session_id": "abc123",
            "ip_address": "192.168.1.100"
        },
        ...
    ]
}
```

---

### Active Sessions Endpoint

```
GET /learn/admin/api/sessions/current
```

**Query Parameters:** None

**Response:**
```json
{
    "active_sessions": [
        {
            "id": 5,
            "user_id": 1,
            "username": "john_doe",
            "login_at": "2026-05-30T14:20:00",
            "session_id": "xyz789",
            "ip_address": "192.168.1.101"
        },
        ...
    ]
}
```

---

### Login Summary Endpoint

```
GET /learn/admin/api/logins/summary
```

**Query Parameters:** None

**Response:**
```json
{
    "active_sessions": 3,
    "logins_today": 12,
    "unique_users_today": 8,
    "avg_session_duration_minutes": 23.5
}
```

---

### Delete User Endpoint

```
DELETE /learn/admin/api/users/<user_id>
```

**URL Parameters:**
- `user_id` (int): User ID to delete

**Response (200 Success):**
```json
{
    "success": true,
    "message": "User 5 deleted"
}
```

**Response (404 Not Found):**
```json
{
    "error": "User not found"
}
```

---

### Bulk Delete Endpoint

```
POST /learn/admin/api/users/bulk-delete
```

**Request Body:**
```json
{
    "user_ids": [1, 2, 3, 4, 5]
}
```

**Response (200 Success):**
```json
{
    "deleted": 5,
    "failed": 0,
    "total": 5
}
```

**Response (400 Bad Request):**
```json
{
    "error": "No user IDs provided"
}
```

---

### Reset Progress Endpoint

```
POST /learn/admin/api/users/<user_id>/reset-progress
```

**URL Parameters:**
- `user_id` (int): User ID

**Request Body:** `{}` (empty)

**Response (200 Success):**
```json
{
    "success": true,
    "message": "Progress reset for user 1"
}
```

**Response (400 Error):**
```json
{
    "error": "Error message"
}
```

---

## Database Schema

### login_tracking Table

```sql
CREATE TABLE login_tracking (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    login_at TEXT NOT NULL,          -- ISO-8601 UTC timestamp
    logout_at TEXT,                  -- NULL while logged in
    session_id TEXT,                 -- UUID or session identifier
    ip_address TEXT,                 -- Client IP address
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Indexes for performance
CREATE INDEX idx_login_tracking_user ON login_tracking(user_id);
CREATE INDEX idx_login_tracking_time ON login_tracking(login_at);
```

**Timestamps:** All timestamps are ISO-8601 format with UTC timezone
**Cascade:** When a user is deleted, all their login records are deleted

---

## Error Handling

### Python Functions

Functions gracefully handle errors:

```python
try:
    delete_user(user_id)
except Exception as e:
    print(f"Error: {e}")
```

Most functions return `None` or empty results on error rather than raising exceptions.

### REST API

All endpoints return appropriate HTTP status codes:

- `200 OK` - Success
- `400 Bad Request` - Invalid input
- `401 Unauthorized` - Missing/invalid token
- `403 Forbidden` - Token validation failed
- `404 Not Found` - Resource not found
- `500 Internal Server Error` - Server error

---

## Best Practices

1. **Always backup database before bulk operations**
   ```bash
   cp data/education.db data/education.db.backup
   ```

2. **Use bulk operations for multiple deletions**
   ```python
   # ✓ Good
   bulk_delete_users([1, 2, 3, 4, 5])
   
   # ✗ Inefficient
   for uid in [1, 2, 3, 4, 5]:
       delete_user(uid)
   ```

3. **Check if user exists before operations**
   ```python
   from modules.education_store import get_user
   
   if get_user(user_id):
       delete_user(user_id)
   ```

4. **Use timestamp filtering for reports**
   ```python
   from datetime import datetime, timedelta
   
   cutoff = datetime.now() - timedelta(days=90)
   # Find logins before cutoff
   ```

5. **Cache results when possible**
   ```python
   users = get_all_users_list()  # Cache this
   for user in users:
       # Process multiple times
   ```

---

## Performance Notes

- Queries are optimized with indexes
- `get_current_sessions()` is fast (uses NULL check on logout_at)
- `bulk_delete_users()` is more efficient than loops
- Consider archiving old login data (>1 year) for large databases

---

## Troubleshooting

### "ADMIN_STREAM_TOKEN not set"
```
Ensure ADMIN_STREAM_TOKEN is set in environment variables
export ADMIN_STREAM_TOKEN="your-token"
```

### "User not found"
```
Verify user_id exists before querying
users = get_all_users_list()  # Check available user IDs
```

### "Permission denied" on database
```
Check file permissions on data/education.db
chmod 644 data/education.db  # on Unix/Linux
```

---

For questions or issues, refer to the main USER_MANAGEMENT_GUIDE.md file.
