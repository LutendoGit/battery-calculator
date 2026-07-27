# Frontend Developer Sharing - Security Best Practices

## 🔒 Core Security Strategy

Protect your backend by **separating concerns** and only exposing what the frontend developer needs via a clean API.

---

## 1. Repository Structure - Two-Repo Approach

### **Option A: Recommended - Separate Repositories**

```
your-backend-repo/ (PRIVATE)
├── app.py
├── calculator.py
├── routes/
├── modules/
├── requirements.txt
├── .env (NEVER commit)
├── .gitignore
└── Admin tokens/ (NEVER SHARE)

frontend-repo/ (PUBLIC/SHARED)
├── static/
│   ├── css/
│   ├── js/
│   ├── images/
│   └── videos/
├── templates/
├── package.json (for Node.js frontend tools)
├── API_DOCUMENTATION.md
├── .env.example (NO actual values)
└── .gitignore
```

### **Option B: Monorepo with Strict Separation**

```
project-root/
├── backend/ (PRIVATE - don't share source)
│   ├── app.py
│   ├── routes/
│   ├── modules/
│   └── .env (NEVER commit)
├── frontend/ (SHARED with frontend developer)
│   ├── static/
│   ├── templates/
│   └── API_DOCUMENTATION.md
└── .gitignore
```

---

## 2. What to Share with Frontend Developer

### ✅ **SAFE TO SHARE**
- Frontend code (HTML, CSS, JavaScript)
- API documentation
- Template files (.html files in `templates/`)
- Static assets (images, videos, CSS)
- `.env.example` (with dummy values - NO secrets)
- API endpoint specifications
- Design system & component library

### ❌ **NEVER SHARE**
- `app.py` (backend logic)
- `routes/` directory (business logic)
- `modules/` directory (database & calculations)
- `calculator.py` (core algorithms)
- `.env` files (contains API keys, SECRET_KEY)
- `Admin tokens/` directory
- `requirements.txt` (reveals backend dependencies)
- Database credentials
- Private keys/tokens

---

## 3. Protect Sensitive Files

### **Step 1: Create `.gitignore` (Root)**

```gitignore
# Environment variables
.env
.env.local
.env.*.local

# Python
__pycache__/
*.pyc
*.pyo
*.egg-info/
.venv/
venv/

# Sensitive directories
Admin tokens/
secrets/
private/

# Credentials
credentials.json
api_keys.txt
cookies.txt

# OS files
.DS_Store
Thumbs.db

# IDE
.vscode/
.idea/
*.swp

# Temporary files
temp.json
temp.txt
*.tmp
```

### **Step 2: Create `.gitignore` (Frontend folder, if monorepo)**

```gitignore
# DO NOT include backend source
../app.py
../calculator.py
../routes/
../modules/
../Admin tokens/
../.env

# Frontend-specific
node_modules/
dist/
.next/
```

---

## 4. Environment Variables - Secrets Management

### **Create `.env` (Backend - Local Only)**
```env
SECRET_KEY=your-super-secret-key-here
DATABASE_URL=your-db-url
API_KEY=your-api-key
MAINTENANCE_MODE=false
```

### **Create `.env.example` (Share with Frontend Dev)**
```env
# Backend Configuration (Shared for reference)
# Frontend developers should NOT set these
SECRET_KEY=your-secret-key-here
DATABASE_URL=your-database-url
API_KEY=your-api-key-placeholder
MAINTENANCE_MODE=false

# Frontend Configuration (Frontend Dev can set)
VITE_API_BASE_URL=http://localhost:5000
VITE_APP_NAME=Battery Calculator
```

---

## 5. API-Only Backend Exposure

### **Frontend Developer Only Needs:**

**API Endpoints Documentation** - Create `API_REFERENCE.md`:

```markdown
# Battery Calculator API Reference

## Authentication
- Token-based: `Authorization: Bearer {token}`
- Session-based: Cookies automatically sent

## Endpoints

### GET /api/v1/modules
Returns list of available modules

**Response:**
```json
{
  "modules": [
    {
      "id": 1,
      "title": "Lithium Battery Fundamentals",
      "content": "...",
      "quiz_url": "/api/v1/quiz/1"
    }
  ]
}
```

### POST /api/v1/calculate
Calculate battery parameters

**Request:**
```json
{
  "capacity": 100,
  "voltage": 48
}
```

**Response:**
```json
{
  "result": {...},
  "status": "success"
}
```
```

---

## 6. Deployment - Two Separate Servers

### **Option 1: Same Server, Different Port**
```
Backend API:    http://localhost:5000 (Private network)
Frontend Build: http://localhost:3000 (Public) → Calls API
```

### **Option 2: Different Servers**
```
Backend API:    api.yourdomain.com (Private/Authenticated)
Frontend:       yourdomain.com (Public)
```

**Frontend makes AJAX calls to backend API:**
```javascript
// frontend/static/app.js
const API_BASE = process.env.VITE_API_BASE_URL || 'http://localhost:5000';

async function getModules() {
  const response = await fetch(`${API_BASE}/api/v1/modules`, {
    headers: {
      'Authorization': `Bearer ${token}`
    }
  });
  return response.json();
}
```

---

## 7. File Sharing Workflow

### **For GitHub/Sharing Platform:**

1. **Backend Developer Keeps:**
   - Private repo with all backend code
   - `.env` (NEVER commit)
   - `Admin tokens/` directory

2. **Frontend Developer Gets:**
   - Separate repo/folder with:
     - `static/` folder (CSS, JS, images, videos)
     - `templates/` folder (HTML templates)
     - `API_DOCUMENTATION.md`
     - `.env.example`
     - `package.json` (if using Node.js tools)

3. **Shared Via:**
   - GitHub private repo (if collaborating)
   - Dropbox/Google Drive for static files only
   - Shared folder for frontend assets only
   - Never share:
     - `.env`
     - Backend Python files
     - Admin tokens
     - Database scripts

---

## 8. Token & Admin Protection

### **Current Issue: `Admin tokens/` Folder**

**DO NOT SHARE THIS FOLDER!**

### **Solution: Move to Environment Variable**

**Current (Insecure):**
```
Admin tokens/
  └── token=sP1KYXbw3fS2ZYF5LmJF3Qr-TOdf0.txt
```

**Better (Secure):**

`.env` (Backend only):
```env
ADMIN_TOKEN=sP1KYXbw3fS2ZYF5LmJF3Qr-TOdf0
```

**Python Code:**
```python
import os
ADMIN_TOKEN = os.environ.get('ADMIN_TOKEN')

@app.route('/admin')
def admin_panel():
    token = request.headers.get('Authorization', '').replace('Bearer ', '')
    if token != ADMIN_TOKEN:
        return jsonify({"error": "Unauthorized"}), 401
    # ... admin logic
```

---

## 9. Hands-On Checklist

- [ ] Create separate backend & frontend folders/repos
- [ ] Set up `.gitignore` in root to exclude sensitive files
- [ ] Move all secrets to `.env` file
- [ ] Create `.env.example` with dummy values
- [ ] Create `API_DOCUMENTATION.md`
- [ ] Delete `Admin tokens/` folder from git history
  ```bash
  git filter-branch --tree-filter 'rm -rf Admin\ tokens' HEAD
  ```
- [ ] Add to `.gitignore`:
  ```
  Admin tokens/
  .env
  ```
- [ ] Share ONLY `static/`, `templates/`, and `API_DOCUMENTATION.md` with frontend dev
- [ ] Use environment variables for all secrets
- [ ] Set up CORS if APIs are on different domains
- [ ] Implement rate limiting on public endpoints
- [ ] Add authentication to sensitive routes

---

## 10. Quick Reference - What to Exclude

| File/Folder | Reason | Action |
|---|---|---|
| `.env` | Contains secrets | Add to `.gitignore` |
| `Admin tokens/` | Credentials | Delete, use env vars |
| `app.py` | Backend logic | Keep private |
| `routes/` | Business logic | Keep private |
| `modules/` | Database logic | Keep private |
| `calculator.py` | Algorithms | Keep private |
| `requirements.txt` | Backend deps | Keep private |
| `templates/` | HTML files | OK to share (no secrets) |
| `static/` | CSS, JS, images | OK to share |
| `.env.example` | Template only | OK to share |

---

## 11. Advanced Security - CORS & API Calls

If frontend and backend are on different domains:

**Backend (`app.py`):**
```python
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={
    r"/api/*": {
        "origins": ["https://yourdomain.com"],
        "methods": ["GET", "POST", "PUT", "DELETE"],
        "allow_headers": ["Content-Type", "Authorization"]
    }
})
```

**Frontend API Call:**
```javascript
fetch('https://api.yourdomain.com/api/v1/modules', {
  method: 'GET',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${token}`
  }
});
```

---

## Summary

✅ **Keep Safe**: Backend code, `.env`, admin tokens, database credentials  
✅ **Share Only**: Frontend files, API docs, templates, static assets  
✅ **Use**: Environment variables for all secrets  
✅ **Separate**: Backend logic from frontend presentation  
✅ **Document**: Clear API reference for frontend dev  

Your backend stays protected while frontend dev can work efficiently! 🚀
