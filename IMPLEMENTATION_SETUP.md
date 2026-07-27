# Frontend Developer Sharing - Implementation Guide

## 🚀 Quick Start - 5 Steps to Safe Sharing

### **Step 1: Move Secrets to Environment Variables**

Your current setup has admin tokens in a file. Move them to `.env`:

**Before (Unsafe):**
```
Admin tokens/
  └── token=sP1KYXbw3fS2ZYF5LmJF3Qr-TOdf0.txt
```

**After (Safe):**

1. Open/create `.env` file in project root:
   ```env
   ADMIN_TOKEN=sP1KYXbw3fS2ZYF5LmJF3Qr-TOdf0
   SECRET_KEY=your-secret-key
   ```

2. Update `app.py` to use env var:
   ```python
   import os
   ADMIN_TOKEN = os.environ.get('ADMIN_TOKEN')
   
   @app.route('/admin')
   def admin_panel():
       token = request.headers.get('Authorization', '').replace('Bearer ', '')
       if token != ADMIN_TOKEN:
           return jsonify({"error": "Unauthorized"}), 401
       return render_template('admin.html')
   ```

3. Delete the `Admin tokens/` folder:
   ```bash
   rm -r "Admin tokens/"
   ```

4. Commit changes (`.env` is already in `.gitignore`):
   ```bash
   git add .gitignore app.py
   git commit -m "Move admin tokens to environment variables for security"
   ```

---

### **Step 2: Verify .gitignore Protects Sensitive Files**

Run this command to see what Git is tracking:

```bash
git status
```

**Expected Output:**
- `.env` should NOT appear (it's in `.gitignore`)
- `Admin tokens/` folder should NOT appear after deletion
- Only see: `modified: .gitignore`, `modified: .env.example`, etc.

**If `.env` shows up in git status:**
```bash
# Remove it from git tracking (keep local copy)
git rm --cached .env
git commit -m "Stop tracking .env file"
```

---

### **Step 3: Create Folder Structure for Frontend Dev**

**Option A: Monorepo (Backend & Frontend in same folder)**

Keep your current structure but clearly separate:

```
project-root/
├── app.py                          # BACKEND - DON'T SHARE
├── calculator.py                   # BACKEND - DON'T SHARE
├── routes/                         # BACKEND - DON'T SHARE
├── modules/                        # BACKEND - DON'T SHARE
├── .env                            # BACKEND - DON'T COMMIT
├── .env.example                    # SHARE ✅
├── FRONTEND_SHARING_SECURITY.md    # SHARE ✅
├── API_REFERENCE.md                # SHARE ✅
├── templates/                      # SHARE ✅ (frontend HTML)
└── static/                         # SHARE ✅ (CSS, JS, images)
```

**Option B: Separate Folders (Cleanest)**

Create a frontend subfolder for sharing:

```bash
# Create frontend folder
mkdir frontend-dev-share

# Copy ONLY frontend files
cp -r static/ frontend-dev-share/
cp -r templates/ frontend-dev-share/
cp .env.example frontend-dev-share/
cp API_REFERENCE.md frontend-dev-share/
cp FRONTEND_SHARING_SECURITY.md frontend-dev-share/

# Create README for frontend dev
cat > frontend-dev-share/README.md << 'EOF'
# Frontend Developer Setup

This folder contains everything a frontend developer needs.

## What's Included
- `templates/` - HTML templates
- `static/` - CSS, JavaScript, images, videos
- `.env.example` - Configuration template
- `API_REFERENCE.md` - Backend API documentation
- `FRONTEND_SHARING_SECURITY.md` - Security guidelines

## What's NOT Included (and why)
- Backend Python files (`app.py`, `routes/`, `modules/`)
  → Kept private for security
- `.env` file
  → Contains production secrets
- `Admin tokens/` directory
  → Sensitive credentials

## Setup

1. Copy `.env.example` to `.env`
2. Set your local API endpoint
3. Start development server
4. Template files will call backend APIs

## API Documentation
See `API_REFERENCE.md` for available endpoints.
EOF
```

---

### **Step 4: Update API_REFERENCE.md**

You already have this file. Make sure it documents all public endpoints:

**Add to your `API_REFERENCE.md`:**

```markdown
# Battery Calculator - API Reference

## Base URL
- **Development**: `http://localhost:5000`
- **Production**: `https://api.yourdomain.com`

## Authentication
Most endpoints require authentication via Bearer token:

```bash
curl -H "Authorization: Bearer {YOUR_TOKEN}" \
  http://localhost:5000/api/v1/modules
```

## Public Endpoints

### GET /api/v1/modules
Returns list of available learning modules

**Response:**
```json
{
  "modules": [
    {
      "id": 1,
      "title": "Lithium Battery Fundamentals",
      "content": "HTML content here",
      "quiz_url": "/fundamentals/module-1/quiz"
    }
  ]
}
```

### GET /api/v1/modules/{id}
Get specific module content

**Response:**
```json
{
  "id": 1,
  "title": "...",
  "content": "...",
  "videos": ["video1.mp4", "video2.mp4"],
  "quizzes": [...]
}
```

### POST /api/v1/calculate
Calculate battery parameters

**Request Body:**
```json
{
  "capacity_wh": 100,
  "voltage": 48,
  "current": 20
}
```

**Response:**
```json
{
  "power_w": 960,
  "energy_kwh": 0.1,
  "runtime_hours": 5,
  "status": "success"
}
```

## Protected Endpoints (Admin only)

### POST /api/v1/admin/content
Create new module content

**Headers Required:**
```
Authorization: Bearer {ADMIN_TOKEN}
Content-Type: application/json
```

**Request:**
```json
{
  "title": "New Module",
  "content": "HTML content"
}
```
```

---

### **Step 5: Share with Frontend Developer**

**Create a "Safe Share" Package:**

```bash
# Create shareable package
mkdir battery-calculator-frontend
cd battery-calculator-frontend

# Copy safe files
cp -r ../static .
cp -r ../templates .
cp ../.env.example .
cp ../API_REFERENCE.md .
cp ../FRONTEND_SHARING_SECURITY.md .

# Create share-specific README
cat > README.md << 'EOF'
# Battery Calculator - Frontend Development Package

This package contains everything needed for frontend development.

## ✅ What You Get
- HTML templates (Jinja2)
- Static assets (CSS, JavaScript, images, videos)
- API documentation
- Security best practices guide

## ❌ What You DON'T Get (and why)
- Backend Python code (kept private)
- Production secrets (in .env, never shared)
- Admin tokens and credentials

## Getting Started

1. Set up your environment:
   ```bash
   cp .env.example .env
   ```

2. Update `.env` with API endpoint:
   ```env
   VITE_API_BASE_URL=http://localhost:5000
   ```

3. Start development server
4. Frontend will communicate with backend via API

## API Calls Example

```javascript
// static/app.js
fetch(`${process.env.VITE_API_BASE_URL}/api/v1/modules`)
  .then(r => r.json())
  .then(data => console.log(data));
```

For full API reference, see: `API_REFERENCE.md`
EOF

# Create .gitignore for frontend dev
cat > .gitignore << 'EOF'
# Only copy backend API files you're allowed to see:
# DO NOT include:
../app.py
../calculator.py
../routes/
../modules/
../.env
../Admin tokens/

# Frontend-specific ignores
node_modules/
.env
dist/
build/
EOF

cd ..

# Zip for sharing
zip -r battery-calculator-frontend.zip battery-calculator-frontend/
```

Share the zip file or the folder with frontend developer.

---

## 📋 Security Checklist

- [ ] `.env` file created with secrets (NOT committed)
- [ ] `.env.example` created with dummy values (CAN be committed)
- [ ] `.gitignore` includes: `.env`, `Admin tokens/`, sensitive files
- [ ] `Admin tokens/` folder deleted from working directory
- [ ] Backend secrets moved to `.env` (environment variables)
- [ ] `app.py` updated to use `os.environ.get()` for secrets
- [ ] Git cache cleaned (no `.env` in git history)
- [ ] `API_REFERENCE.md` documented with all endpoints
- [ ] Frontend sharing folder created with safe files only
- [ ] Frontend dev has `.gitignore` preventing backend code access
- [ ] GitHub/sharing repo has no sensitive data

---

## 🔐 Ongoing Security

### **Before Each Share:**
```bash
# Verify no secrets in git
git log --all -S "ADMIN_TOKEN" --oneline
git log --all -S ".env" --oneline

# If found, clean history:
git filter-branch --tree-filter 'rm -f .env' HEAD
```

### **For Frontend Dev Collaboration:**
```bash
# Check what's being shared
git ls-files | grep -E "(\.env|Admin|secret|token)"

# Should return: nothing
```

### **Production Deployment:**
On Render, GitHub Actions, or your hosting:

```bash
# Set secrets as environment variables in hosting dashboard
# NEVER commit them to code
```

---

## Questions for Frontend Dev?

Send them this checklist:

```
✅ You can work with:
- Templates (HTML files)
- Static assets (CSS, JS, images)
- API documentation

❌ You should NOT have:
- Python files (app.py, routes/, modules/)
- .env file (has secrets)
- Admin credentials
- Database files

🔗 API endpoints: See API_REFERENCE.md
📚 Security details: See FRONTEND_SHARING_SECURITY.md
```

---

## Still Have Questions?

Read these files:
1. **FRONTEND_SHARING_SECURITY.md** - Detailed security strategy
2. **API_REFERENCE.md** - Endpoint documentation
3. **.gitignore** - Files being protected
4. **.env.example** - Configuration template
