# 🔐 Pre-Share Security Checklist

Run through this before giving frontend developer access to ANY files.

---

## ✅ Environment & Secrets

- [ ] **`.env` file exists** with all secrets:
  ```bash
  ls -la .env  # Should exist but not be tracked by git
  git status | grep .env  # Should NOT show .env
  ```

- [ ] **`.env.example` created** with dummy values for sharing:
  ```bash
  cat .env.example  # Has placeholder values, NOT real secrets
  ```

- [ ] **All sensitive values moved to `.env`:**
  - `SECRET_KEY` ✅
  - `ADMIN_TOKEN` ✅
  - Database credentials ✅
  - API keys ✅

- [ ] **Backend code uses environment variables:**
  ```python
  # ✅ GOOD
  ADMIN_TOKEN = os.environ.get('ADMIN_TOKEN')
  
  # ❌ BAD
  ADMIN_TOKEN = "hardcoded-secret"
  ```

---

## ✅ File Protection

- [ ] **`.gitignore` includes sensitive directories:**
  ```bash
  grep -E "^\.env$|^Admin tokens/|^credentials/" .gitignore
  ```

- [ ] **`.gitignore` includes sensitive files:**
  ```bash
  grep -E "\.pem|\.key|token.*\.txt|cookies\.txt" .gitignore
  ```

- [ ] **`Admin tokens/` folder exists locally but NOT in git:**
  ```bash
  ls -d "Admin tokens/"           # Should exist locally
  git ls-files | grep Admin       # Should return nothing
  ```

- [ ] **No production secrets in git history:**
  ```bash
  git log --all -S "SECRET_KEY" --oneline      # Should be empty
  git log --all -S "ADMIN_TOKEN" --oneline     # Should be empty
  git log --all -S ".env" --oneline            # Should be empty
  ```

---

## ✅ Backend Code Protection

- [ ] **Backend files are NOT in share folder:**
  - ❌ Don't include: `app.py`
  - ❌ Don't include: `calculator.py`
  - ❌ Don't include: `routes/`
  - ❌ Don't include: `modules/`
  - ✅ DO include: `templates/`
  - ✅ DO include: `static/`

- [ ] **Requirements.txt is private:**
  ```bash
  # ❌ Don't share requirements.txt - reveals backend dependencies
  # ✅ Share ONLY: static/ and templates/
  ```

---

## ✅ Documentation

- [ ] **`API_REFERENCE_REST.md` created** with:
  - Base URL
  - Authentication method
  - Available endpoints
  - Request/response examples
  - Error codes

- [ ] **`FRONTEND_SHARING_SECURITY.md` created** with:
  - What to share (templates, static, docs)
  - What NOT to share (backend, secrets)
  - Security best practices
  - Storage recommendations

- [ ] **`.env.example` is complete** with:
  - All configuration keys
  - Placeholder/dummy values
  - Comments explaining each setting

---

## ✅ Git Status

Before sharing, run:

```bash
git status
```

**Should NOT show:**
- `.env` file
- `Admin tokens/` folder
- Any `*.pem`, `*.key`, `*.txt` credential files
- Sensitive configuration

**Expected output:**
```
On branch main
nothing to commit, working tree clean
```

---

## ✅ Sharing Package Structure

If creating a share folder, verify it contains:

```
frontend-share/
├── static/              ✅ INCLUDE (CSS, JS, images, videos)
├── templates/           ✅ INCLUDE (HTML)
├── .env.example         ✅ INCLUDE (template only)
├── API_REFERENCE_REST.md  ✅ INCLUDE
├── FRONTEND_SHARING_SECURITY.md ✅ INCLUDE
└── README.md            ✅ INCLUDE

And does NOT contain:
├── app.py               ❌ NO
├── calculator.py        ❌ NO
├── routes/              ❌ NO
├── modules/             ❌ NO
├── .env                 ❌ NO
├── Admin tokens/        ❌ NO
└── requirements.txt     ❌ NO
```

---

## ✅ Frontend Developer Communication

Send them this checklist:

```
✅ You'll receive:
- HTML templates (templates/)
- Frontend assets (static/)
- API documentation
- Configuration template (.env.example)
- Security guidelines

❌ You should NOT have:
- Python files (app.py, routes/, modules/)
- Production secrets (.env)
- Admin tokens or credentials
- Backend configuration

🔗 To set up:
1. Copy .env.example to .env
2. Set API endpoint to: http://localhost:5000 (dev)
3. Review API_REFERENCE_REST.md for available endpoints
4. Start your frontend development server
5. Frontend will call backend APIs automatically
```

---

## ✅ One-Time Setup Commands

Run these before sharing:

```bash
# 1. Ensure .gitignore is set up correctly
echo ".env" >> .gitignore
echo "Admin tokens/" >> .gitignore
git add .gitignore

# 2. Remove sensitive files from git tracking (if they were added)
git rm --cached .env 2>/dev/null || true
git rm -r --cached "Admin tokens/" 2>/dev/null || true

# 3. Verify nothing sensitive is being tracked
git ls-files | grep -E "\.(env|pem|key)|token|Admin" && echo "⚠️  SENSITIVE FILES FOUND!" || echo "✅ Clean!"

# 4. Create .env from .env.example
cp .env.example .env

# 5. Add your real secrets to .env (LOCAL ONLY, don't commit)
# Edit .env manually with your actual values

# 6. Test that .env is ignored
git status | grep ".env" || echo "✅ .env properly ignored by git"

# 7. Commit the security setup
git add .gitignore .env.example
git commit -m "Add security configuration and sharing guidelines"

# 8. Create share package
mkdir frontend-share
cp -r static/ frontend-share/
cp -r templates/ frontend-share/
cp .env.example frontend-share/
cp API_REFERENCE_REST.md frontend-share/
cp FRONTEND_SHARING_SECURITY.md frontend-share/
```

---

## ✅ Verification Checklist

Run this script to verify security:

```bash
#!/bin/bash

echo "🔐 Security Verification"
echo "========================"

# Check 1: .env file exists
if [ -f .env ]; then
  echo "✅ .env file exists"
else
  echo "❌ .env file missing"
fi

# Check 2: .env not in git
if git ls-files | grep -q ".env"; then
  echo "❌ ERROR: .env is being tracked by git!"
else
  echo "✅ .env properly ignored by git"
fi

# Check 3: Admin tokens not in git
if git ls-files | grep -q "Admin"; then
  echo "❌ ERROR: Admin tokens in git!"
else
  echo "✅ Admin tokens not in git"
fi

# Check 4: .env.example exists
if [ -f .env.example ]; then
  echo "✅ .env.example exists for sharing"
else
  echo "❌ .env.example missing"
fi

# Check 5: No hardcoded secrets in code
if grep -r "SECRET_KEY.*=" app.py 2>/dev/null | grep -v "os.environ"; then
  echo "❌ Hardcoded secrets found in code!"
else
  echo "✅ No hardcoded secrets detected"
fi

echo ""
echo "Done! Ready to share with frontend dev ✅"
```

Save as `verify_security.sh` and run:
```bash
bash verify_security.sh
```

---

## 🚨 If You Find Issues

### **Issue: .env is in git history**
```bash
# Clean it from history
git filter-branch --tree-filter 'rm -f .env' HEAD
git push origin --force-with-lease
```

### **Issue: Secrets hardcoded in app.py**
```bash
# Update app.py to use environment variables
# OLD: SECRET_KEY = "hardcoded-value"
# NEW: SECRET_KEY = os.environ.get('SECRET_KEY', 'dev')
```

### **Issue: Admin tokens/ folder tracked by git**
```bash
git rm -r --cached "Admin tokens/"
git add .gitignore
git commit -m "Remove Admin tokens from git tracking"
```

---

## ✅ Final Sign-Off

- [ ] All sensitive files in `.gitignore`
- [ ] `.env` exists locally with real secrets
- [ ] `.env.example` shared with dummy values
- [ ] No secrets in git history
- [ ] Backend code protected (not shared)
- [ ] API documentation complete
- [ ] Frontend sharing package prepared
- [ ] Frontend dev has security guidelines
- [ ] Ready to share! ✅

---

**When you're done with this checklist, your backend is safe and your frontend developer can work without compromising security.** 🎉
