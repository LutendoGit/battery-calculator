# Module Progress & Certificate Tracking System

## Overview
A comprehensive tracking system has been added to monitor user learning progress across modules, quiz completions, and certificate eligibility. This system tracks:

1. **Module Learning Status** - Which modules users have started, are actively learning, or completed
2. **Quiz Pass/Fail Tracking** - Records when users score 75%+ on module quizzes (qualifying for certificates)
3. **Admin Dashboard Support** - REST APIs to query user progress and award certificates

---

## Database Schema

### New Tables

#### `module_progress`
Tracks user progress through each learning module with status tracking.

```sql
CREATE TABLE module_progress (
    user_id INTEGER NOT NULL,
    module_id TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'not_started',  -- 'not_started', 'in_progress', 'completed'
    started_at TEXT,                             -- ISO-8601 timestamp when user started
    completed_at TEXT,                           -- ISO-8601 timestamp when user completed
    updated_at TEXT NOT NULL,                    -- Last update time
    PRIMARY KEY (user_id, module_id),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
)
```

#### `module_certificates`
Records successful quiz completions (75%+) for certificate eligibility.

```sql
CREATE TABLE module_certificates (
    user_id INTEGER NOT NULL,
    module_id TEXT NOT NULL,
    quiz_id TEXT NOT NULL,
    score INTEGER NOT NULL,
    total INTEGER NOT NULL,
    percentage REAL NOT NULL,
    passed BOOLEAN NOT NULL,                    -- TRUE when percentage >= 75%
    awarded_at TEXT NOT NULL,                   -- ISO-8601 timestamp
    PRIMARY KEY (user_id, module_id),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
)
```

---

## Core Functions (education_store.py)

### Module Progress Management

#### `update_module_status(user_id, module_id, status)`
Updates user's module learning status.

**Parameters:**
- `user_id` (int): User ID
- `module_id` (str): Module identifier (e.g., 'module_1', 'module_2')
- `status` (str): One of 'not_started', 'in_progress', 'completed'

**Example:**
```python
from modules.education_store import update_module_status

# Mark user 5's module_1 as in progress
update_module_status(5, 'module_1', 'in_progress')

# Mark user 5's module_1 as completed
update_module_status(5, 'module_1', 'completed')
```

#### `get_module_status(user_id) → dict`
Retrieves all module statuses for a user.

**Returns:**
```python
{
    'module_1': {
        'status': 'completed',
        'started_at': '2026-06-08T10:30:00',
        'completed_at': '2026-06-08T12:45:00',
        'updated_at': '2026-06-08T12:45:00'
    },
    'module_2': {
        'status': 'in_progress',
        'started_at': '2026-06-08T13:00:00',
        'completed_at': None,
        'updated_at': '2026-06-08T14:15:00'
    }
}
```

### Certificate Management

#### `record_module_certificate(user_id, module_id, quiz_id, score, total) → bool`
Awards a certificate if quiz score is 75%+.

**Parameters:**
- `user_id` (int): User ID
- `module_id` (str): Module identifier
- `quiz_id` (str): Quiz identifier
- `score` (int): Quiz score achieved
- `total` (int): Total possible points

**Returns:** `True` if certificate awarded, `False` otherwise

**Example:**
```python
from modules.education_store import record_module_certificate

# User scored 18/20 (90%) on module_1 quiz
awarded = record_module_certificate(
    user_id=5,
    module_id='module_1',
    quiz_id='capacity-dod',
    score=18,
    total=20
)
# Returns: True (90% >= 75%)
```

#### `get_module_certificates(user_id) → dict`
Gets all earned certificates for a user (75%+).

**Returns:**
```python
{
    'module_1': {
        'quiz_id': 'capacity-dod',
        'score': 18,
        'total': 20,
        'percentage': 90.0,
        'awarded_at': '2026-06-08T12:45:00'
    },
    'module_3': {
        'quiz_id': 'module-3-assessment',
        'score': 15,
        'total': 20,
        'percentage': 75.0,
        'awarded_at': '2026-06-08T14:30:00'
    }
}
```

### User Progress Summary

#### `get_user_module_progress_summary(user_id) → dict`
Complete module progress snapshot for a user.

**Returns:**
```python
{
    'user_id': 5,
    'modules_status': { ... },           # Dict from get_module_status()
    'certificates': { ... },             # Dict from get_module_certificates()
    'summary': {
        'completed': 3,                  # Number of completed modules
        'in_progress': 1,                # Number in progress
        'not_started': 4,                # Number not started
        'certificates_count': 3          # Number of certificates earned
    }
}
```

#### `get_all_users_module_progress() → list[dict]`
Admin view of all users' module progress.

**Returns:**
```python
[
    {
        'user_id': 1,
        'username': 'john_doe',
        'email': 'john@example.com',
        'modules_completed': 3,
        'modules_in_progress': 1,
        'certificates_earned': 3
    },
    {
        'user_id': 2,
        'username': 'jane_smith',
        'email': 'jane@example.com',
        'modules_completed': 5,
        'modules_in_progress': 0,
        'certificates_earned': 5
    }
]
```

---

## Automatic Tracking (routes/education_routes.py)

### Quiz Completion Flow
When a user completes a quiz and scores 75%+:

1. `api_quiz_complete()` is called
2. Quiz score is recorded in `quiz_attempts` table
3. **NEW:** Quiz completion automatically triggers:
   - `record_module_certificate()` - Awards certificate if 75%+
   - `update_module_status()` - Marks module as 'completed'
   - `record_event()` - Logs certificate award to audit trail

### Example Flow
```python
POST /learn/api/progress/quiz-complete
{
    "quiz_id": "module-3-assessment",
    "score": 18,
    "total": 20
}

# Automatic actions:
# 1. score stored in quiz_attempts table
# 2. percentage calculated: 90% >= 75% ✓
# 3. module_certificate created with 75% check
# 4. module_progress.module_3 set to 'completed'
# 5. event logged: "certificate_awarded"
```

---

## Admin API Endpoints

### 1. All Users Module Progress (Summary)
**GET** `/learn/admin/api/module-progress/all-users?token=ADMIN_TOKEN`

Returns quick summary of each user's module progress.

**Response:**
```json
{
  "users": [
    {
      "user_id": 1,
      "username": "trainer_user",
      "email": "trainer@example.com",
      "modules_completed": 3,
      "modules_in_progress": 1,
      "certificates_earned": 3
    }
  ]
}
```

### 2. Single User Module Progress (Detailed)
**GET** `/learn/admin/api/module-progress/user/<user_id>?token=ADMIN_TOKEN`

Complete breakdown of one user's progress.

**Response:**
```json
{
  "user_id": 5,
  "modules_status": {
    "module_1": {
      "status": "completed",
      "started_at": "2026-06-08T10:30:00",
      "completed_at": "2026-06-08T12:45:00",
      "updated_at": "2026-06-08T12:45:00"
    }
  },
  "certificates": {
    "module_1": {
      "quiz_id": "capacity-dod",
      "score": 18,
      "total": 20,
      "percentage": 90.0,
      "awarded_at": "2026-06-08T12:45:00"
    }
  },
  "summary": {
    "completed": 3,
    "in_progress": 1,
    "not_started": 4,
    "certificates_count": 3
  }
}
```

### 3. All Module Certificates (Awards List)
**GET** `/learn/admin/api/module-progress/certificates?token=ADMIN_TOKEN`

Who passed which module quizzes.

**Response:**
```json
{
  "certificates": [
    {
      "user_id": 1,
      "username": "john_doe",
      "module_id": "module_1",
      "quiz_id": "capacity-dod",
      "score": 18,
      "total": 20,
      "percentage": 90.0,
      "awarded_at": "2026-06-08T12:45:00"
    }
  ]
}
```

### 4. Module Progress Statistics
**GET** `/learn/admin/api/module-progress/statistics?token=ADMIN_TOKEN`

Overall system statistics.

**Response:**
```json
{
  "total_users": 42,
  "module_progress_by_status": {
    "module_1": {
      "not_started": 5,
      "in_progress": 8,
      "completed": 29
    },
    "module_2": {
      "not_started": 12,
      "in_progress": 5,
      "completed": 25
    }
  },
  "total_certificates_awarded": 78,
  "users_with_certificates": 25,
  "average_certificates_per_user": 3.12
}
```

---

## Integration Points

### Module IDs
Automatically mapped from quiz IDs:
- `capacity-dod` → `module_1`
- `module-2-assessment` → `module_2`
- `module-3-assessment` → `module_3`
- `module-4-assessment` → `module_4`
- `module-5-assessment` → `module_5`
- `module-6-assessment` → `module_6`
- `module-7-assessment` → `module_7`
- `module-8-assessment` → `module_8`

### User Sessions
Module progress is tied to user sessions. When users log in:
- `login_tracking` records the session (existing feature)
- When they complete a quiz, module progress is updated
- Certificate is awarded if score >= 75%

### Events/Audit Trail
All actions are logged to `user_events` table:
- `module_status_updated` - When module status changes
- `certificate_awarded` - When certificate is earned
- `module_certificate_error` - If any errors occur (but quiz completion succeeds)

---

## Usage Examples

### For Developers

#### Check if user has started module 3
```python
from modules.education_store import get_module_status

status_dict = get_module_status(user_id=5)
if 'module_3' in status_dict:
    status = status_dict['module_3']['status']
    if status == 'completed':
        print("User has completed module 3!")
    elif status == 'in_progress':
        print("User is learning module 3...")
```

#### Get all users ready for certification
```python
from modules.education_store import get_all_users_module_progress

users = get_all_users_module_progress()
ready_for_cert = [u for u in users if u['certificates_earned'] >= 3]
print(f"{len(ready_for_cert)} users are ready for certification")
```

### For Admins

#### View dashboard statistics
```
Navigate to: /learn/admin/api/module-progress/statistics?token=YOUR_ADMIN_TOKEN
```

#### Export user progress as JSON
```
Navigate to: /learn/admin/api/module-progress/all-users?token=YOUR_ADMIN_TOKEN
```

---

## Testing Checklist

- [ ] Create user account
- [ ] Navigate to Module 1 (auto-sets status to 'in_progress' on first visit)
- [ ] Complete Module 1 quiz with score >= 75%
  - [ ] Verify certificate is awarded
  - [ ] Verify module status shows 'completed'
  - [ ] Check admin endpoint shows certificate
- [ ] Take same quiz again with lower score
  - [ ] Verify best score is kept
  - [ ] Verify no duplicate certificate
- [ ] Check admin dashboard shows user progress correctly
- [ ] Verify events are logged to user_events table
- [ ] Test admin API endpoints with and without token

---

## Notes

- All timestamps are stored in ISO-8601 UTC format
- Certificates require exactly 75% or higher to be awarded
- Module status is automatically updated when quiz is completed at 75%+
- User progress is independent per user (no sharing or inheritance)
- Database changes are minimal and backward-compatible
- Existing quiz tracking (quiz_attempts) remains unchanged
