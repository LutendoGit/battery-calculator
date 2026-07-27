# Battery Calculator - REST API Reference

**Last Updated:** June 2026  
**Status:** Production Ready  
**Base URL:** `http://localhost:5000` (dev), `https://api.yourdomain.com` (production)

---

## 🔐 Authentication

All endpoints use **Bearer Token** authentication (except `/` and `/health`).

**How to authenticate:**

```javascript
// JavaScript/Fetch
fetch('http://localhost:5000/api/v1/modules', {
  headers: {
    'Authorization': `Bearer YOUR_TOKEN_HERE`
  }
});
```

```python
# Python/Requests
import requests

headers = {
    'Authorization': f'Bearer YOUR_TOKEN_HERE'
}
response = requests.get(
    'http://localhost:5000/api/v1/modules',
    headers=headers
)
```

---

## 📚 Education Modules - Endpoints

### GET `/fundamentals/module-{id}`
Returns HTML content for a specific learning module.

**URL Parameters:**
- `id` (int): Module number (1-10)

**Query Parameters:**
- `format` (optional): `json` or `html` (default: `html`)

**Response (HTML format):**
```html
<div class="module-content">
  <h1>Lithium Battery Fundamentals</h1>
  <p>Content here...</p>
</div>
```

**Response (JSON format):**
```json
{
  "module_id": 1,
  "title": "Lithium Battery Fundamentals",
  "content": "<html content>",
  "quiz_url": "/fundamentals/module-1/quiz",
  "next_module": "/fundamentals/module-2",
  "prev_module": null
}
```

**Example:**
```javascript
fetch('/fundamentals/module-1?format=json', {
  headers: { 'Authorization': `Bearer ${token}` }
})
.then(r => r.json())
.then(data => {
  console.log(data.title);
  document.getElementById('content').innerHTML = data.content;
});
```

---

### GET `/fundamentals/module-{id}/quiz`
Returns quiz for a module.

**Response:**
```json
{
  "module_id": 1,
  "questions": [
    {
      "id": 1,
      "question": "What is a lithium battery?",
      "options": ["A", "B", "C", "D"],
      "type": "multiple_choice"
    }
  ],
  "total_questions": 10,
  "time_limit": 600
}
```

---

## 🧮 Calculator API

### POST `/api/v1/calculate`
Calculate battery parameters based on inputs.

**Request Body:**
```json
{
  "capacity_wh": 100,
  "voltage": 48,
  "current": 20,
  "efficiency": 0.95
}
```

**Response:**
```json
{
  "status": "success",
  "results": {
    "power_watts": 960,
    "energy_kwh": 0.1,
    "runtime_hours": 5.0,
    "efficiency_percent": 95,
    "estimated_cost": 150.25
  },
  "warnings": [],
  "metadata": {
    "calculated_at": "2026-06-03T14:30:00Z",
    "calculation_time_ms": 45
  }
}
```

**Error Response:**
```json
{
  "status": "error",
  "error": "Invalid voltage: must be 6-800V",
  "code": "INVALID_INPUT"
}
```

**JavaScript Example:**
```javascript
async function calculate() {
  const response = await fetch('/api/v1/calculate', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`
    },
    body: JSON.stringify({
      capacity_wh: 100,
      voltage: 48,
      current: 20
    })
  });
  
  const data = await response.json();
  if (data.status === 'success') {
    console.log(`Power: ${data.results.power_watts}W`);
  }
}
```

---

## 👤 User Management

### POST `/api/v1/auth/login`
Authenticate user and get token.

**Request:**
```json
{
  "username": "user@example.com",
  "password": "password123"
}
```

**Response:**
```json
{
  "status": "success",
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "user": {
    "id": 1,
    "username": "user@example.com",
    "name": "John Doe"
  },
  "expires_in": 86400
}
```

---

### POST `/api/v1/auth/logout`
End current session.

**Headers:**
```
Authorization: Bearer {token}
```

**Response:**
```json
{
  "status": "success",
  "message": "Logged out successfully"
}
```

---

### GET `/api/v1/users/profile`
Get current user profile.

**Headers:**
```
Authorization: Bearer {token}
```

**Response:**
```json
{
  "status": "success",
  "user": {
    "id": 1,
    "username": "user@example.com",
    "name": "John Doe",
    "email": "user@example.com",
    "created_at": "2026-01-01T00:00:00Z",
    "modules_completed": 3,
    "progress_percent": 30
  }
}
```

---

## 📊 Progress Tracking

### GET `/api/v1/progress`
Get user's learning progress.

**Response:**
```json
{
  "status": "success",
  "progress": {
    "total_modules": 10,
    "completed_modules": 3,
    "current_module": 4,
    "progress_percent": 30,
    "modules": [
      {
        "id": 1,
        "title": "Lithium Battery Fundamentals",
        "completed": true,
        "quiz_score": 85,
        "completed_at": "2026-05-15T10:30:00Z"
      },
      {
        "id": 2,
        "title": "Electrical Fundamentals",
        "completed": true,
        "quiz_score": 92,
        "completed_at": "2026-05-20T14:15:00Z"
      }
    ]
  }
}
```

---

### POST `/api/v1/progress/module-{id}/complete`
Mark module as complete.

**Request:**
```json
{
  "quiz_score": 85,
  "time_spent_seconds": 1800
}
```

**Response:**
```json
{
  "status": "success",
  "message": "Module 1 marked as complete",
  "next_module": "/fundamentals/module-2"
}
```

---

## 🏥 Health & Status

### GET `/health`
Check API status (no auth required).

**Response:**
```json
{
  "status": "healthy",
  "uptime_seconds": 12345,
  "version": "1.0.0",
  "timestamp": "2026-06-03T14:30:00Z"
}
```

---

## ⚙️ Admin Endpoints

**Note:** Admin endpoints require `ADMIN_TOKEN` in Authorization header.

### POST `/api/v1/admin/content/create`
Create new module content.

**Headers:**
```
Authorization: Bearer {ADMIN_TOKEN}
Content-Type: application/json
```

**Request:**
```json
{
  "module_id": 11,
  "title": "New Module",
  "content": "<html>...</html>",
  "quiz_data": [...]
}
```

**Response:**
```json
{
  "status": "success",
  "module_id": 11,
  "message": "Module created successfully"
}
```

---

### GET `/api/v1/admin/users`
List all users (admin only).

**Response:**
```json
{
  "status": "success",
  "users": [
    {
      "id": 1,
      "username": "user1@example.com",
      "name": "John Doe",
      "last_login": "2026-06-03T10:00:00Z",
      "modules_completed": 5
    }
  ],
  "total": 42
}
```

---

## 🚨 Error Codes

| Code | Status | Meaning |
|------|--------|---------|
| `UNAUTHORIZED` | 401 | Missing or invalid token |
| `FORBIDDEN` | 403 | Insufficient permissions (admin only) |
| `NOT_FOUND` | 404 | Resource not found |
| `INVALID_INPUT` | 400 | Bad request data |
| `SERVER_ERROR` | 500 | Internal server error |
| `RATE_LIMITED` | 429 | Too many requests |

**Error Response Format:**
```json
{
  "status": "error",
  "code": "INVALID_INPUT",
  "message": "Detailed error message",
  "details": {
    "field": "voltage",
    "reason": "Must be between 6 and 800"
  }
}
```

---

## 📝 Rate Limiting

- **Default:** 100 requests per minute per token
- **Admin:** 1000 requests per minute

**Response Headers:**
```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1687362600
```

---

## 🔗 Quick Links

- **Security Guide:** `FRONTEND_SHARING_SECURITY.md`
- **Implementation Setup:** `IMPLEMENTATION_SETUP.md`
- **Backend Python API:** See `modules/education_store.py`

---

## Examples by Framework

### React.js
```javascript
import { useState, useEffect } from 'react';

export function ModuleView({ moduleId }) {
  const [module, setModule] = useState(null);
  const token = localStorage.getItem('token');

  useEffect(() => {
    fetch(`/fundamentals/module-${moduleId}?format=json`, {
      headers: { 'Authorization': `Bearer ${token}` }
    })
    .then(r => r.json())
    .then(data => setModule(data));
  }, [moduleId]);

  return <div dangerouslySetInnerHTML={{ __html: module?.content }} />;
}
```

### Vue.js
```vue
<template>
  <div v-if="module">
    <h1>{{ module.title }}</h1>
    <div v-html="module.content"></div>
  </div>
</template>

<script>
export default {
  data() {
    return { module: null };
  },
  mounted() {
    const token = localStorage.getItem('token');
    fetch(`/fundamentals/module-${this.$route.params.id}?format=json`, {
      headers: { 'Authorization': `Bearer ${token}` }
    })
    .then(r => r.json())
    .then(data => this.module = data);
  }
};
</script>
```

### jQuery
```javascript
$.ajax({
  url: '/fundamentals/module-1?format=json',
  headers: {
    'Authorization': `Bearer ${token}`
  },
  success: function(data) {
    $('#content').html(data.content);
    $('#title').text(data.title);
  }
});
```

---

## Support

For issues or questions:
1. Check `FRONTEND_SHARING_SECURITY.md` for security details
2. Review examples above for your framework
3. Check error codes section for troubleshooting
