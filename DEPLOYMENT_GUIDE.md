# Deployment Guide: Battery Calculator + Admin Dashboard to Render

This guide walks you through deploying your Flask app with **Login Tracking & User Management** to Render.com.

---

## 📋 Pre-Deployment Checklist

- [ ] Code pushed to GitHub
- [ ] `.env.example` updated with all required variables
- [ ] `requirements.txt` includes all dependencies
- [ ] `Procfile` configured for Render
- [ ] Database schema tested locally
- [ ] All secrets stored as environment variables (not in code)
- [ ] Admin token generated and secure
- [ ] SSL/HTTPS enabled in Render
- [ ] Domain configured (optional)

---

## 🚀 Part 1: Prepare Your Repository

### 1.1 Update `.env.example`

Create/update `.env.example` with **all** production variables:

```bash
# Flask Configuration
SECRET_KEY=your-secret-key-here-min-32-chars
FLASK_ENV=production
FLASK_DEBUG=0

# Admin Settings (CRITICAL)
ADMIN_STREAM_TOKEN=your-secure-admin-token-here

# Database
DATABASE_URL=sqlite:////tmp/education.db

# Maintenance Mode
MAINTENANCE_MODE=false
MAINTENANCE_RETRY_AFTER=300
```

### 1.2 Update `requirements.txt`

Your current `requirements.txt` should include:

```
Flask>=2.0
matplotlib>=3.0
reportlab>=3.5
openpyxl>=3.0
gunicorn>=20.0.4
python-dotenv>=0.19.0
Werkzeug>=2.0
```

Add these if missing:
```bash
pip install python-dotenv Werkzeug
pip freeze > requirements.txt
```

### 1.3 Verify `Procfile`

Your Procfile should be:

```
web: gunicorn app:app --workers 3 --threads 2 --bind 0.0.0.0:$PORT --timeout 300
```

This is already correct ✅

---

## 📦 Part 2: Database Strategy for Render

### Option A: SQLite with Persistent Storage (Recommended for Small Apps)

**Pros:**
- Works out of the box
- No external database to manage
- Free tier available

**Cons:**
- Limited concurrency
- Not ideal for high-traffic apps
- Render restarts can discard data if not on persistent volume

**Setup:**
1. Create a persistent volume in Render dashboard
2. Mount at `/data` 
3. Update environment variable: `DATABASE_URL=/data/education.db`

### Option B: PostgreSQL (Recommended for Production)

**Pros:**
- Scales with your app
- High availability
- Better for concurrent users
- Render provides free managed PostgreSQL

**Cons:**
- Requires schema changes to your code (not recommended if you like SQLite)
- Additional setup

### Implementation for This App

**We'll use Option A (SQLite + Persistent Volume)** since your app is already SQLite-based and this requires minimal changes.

---

## 🔧 Part 3: Render Dashboard Setup

### Step 1: Create a Web Service

1. Go to [render.com](https://render.com) and sign in
2. Click **New** → **Web Service**
3. Connect your GitHub repository
4. Configure:
   - **Name:** `battery-calculator` (or your app name)
   - **Environment:** `Python 3`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn app:app --workers 3 --threads 2 --bind 0.0.0.0:$PORT --timeout 300`

### Step 2: Add Environment Variables

In the Render dashboard, go to **Environment** and add:

```
SECRET_KEY=<generate-a-random-string-minimum-32-chars>
FLASK_ENV=production
FLASK_DEBUG=0
ADMIN_STREAM_TOKEN=<your-secure-admin-token>
DATABASE_URL=/data/education.db
MAINTENANCE_MODE=false
```

**Generate a secure SECRET_KEY:**
```python
import secrets
print(secrets.token_hex(32))
```

### Step 3: Create a Persistent Volume

1. In Render dashboard, go to your service
2. Click **Environment** → **Persistent Disk**
3. Create with:
   - **Size:** 1 GB (sufficient for databases)
   - **Mount Path:** `/data`

This ensures your database persists across app restarts.

### Step 4: Deploy

1. Click **Deploy** button
2. Wait for build to complete (5-10 minutes)
3. View logs in the dashboard to check for errors

---

## 🗄️ Part 4: Database Initialization on Render

### Auto-Initialization via Python

Your `education_store.py` already calls `ensure_db()` which creates tables automatically. However, for safety, we'll create an explicit initialization script:

**Create: `scripts/init_db_render.py`**

```python
#!/usr/bin/env python3
"""Initialize database for Render deployment."""

import os
import sys

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from modules.education_store import ensure_db

def main():
    """Initialize database."""
    try:
        ensure_db()
        print("✅ Database initialized successfully")
    except Exception as e:
        print(f"❌ Database initialization failed: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()
```

### Add Post-Build Hook to `Procfile`

Update your Procfile to run initialization before starting:

```
release: python scripts/init_db_render.py
web: gunicorn app:app --workers 3 --threads 2 --bind 0.0.0.0:$PORT --timeout 300
```

The `release` command runs once after deployment but before the web service starts.

---

## 🔐 Part 5: Security Checklist

- [ ] **SECRET_KEY:** 32+ character random string (use `secrets.token_hex(32)`)
- [ ] **ADMIN_STREAM_TOKEN:** Generate new token for production
  ```python
  import secrets
  print(f"sP1KYXbw3fS2ZYF5LmJF3Qr-TOdf0{secrets.token_hex(32)}")
  ```
- [ ] **HTTPS:** Render auto-enables this ✅
- [ ] **Database Backups:** Render doesn't auto-backup SQLite on volumes
  - Set up a cron job or use Render's backup service
  - Consider weekly exports to external storage
- [ ] **Admin Dashboard Access:** Change token in production!
  - Token should only be known by admins
  - Store in Render environment, NOT in code
  - Rotate token periodically
- [ ] **FLASK_DEBUG=0:** Never set to 1 in production

---

## 📝 Part 6: Configuration Files

### `render.yaml` (Optional but Recommended)

Create `render.yaml` at project root for Infrastructure as Code:

```yaml
services:
  - type: web
    name: battery-calculator
    env: python
    plan: starter
    buildCommand: pip install -r requirements.txt
    startCommand: gunicorn app:app --workers 3 --threads 2 --bind 0.0.0.0:$PORT --timeout 300
    diskSize: 1
    disk:
      name: education-db
      mountPath: /data
      sizeGB: 1
    envVars:
      - key: FLASK_ENV
        value: production
      - key: FLASK_DEBUG
        value: "0"
      - key: DATABASE_URL
        value: /data/education.db
      - key: SECRET_KEY
        sync: false  # Set this in dashboard
      - key: ADMIN_STREAM_TOKEN
        sync: false  # Set this in dashboard
```

---

## 🧪 Part 7: Testing on Render

### Test Login Tracking
1. Go to `https://your-app.onrender.com/learn/login`
2. Create test account
3. Log in and log out
4. Access admin dashboard: `https://your-app.onrender.com/learn/admin/users?token=YOUR_ADMIN_TOKEN`
5. Verify login appears in "Active Sessions" and "User Details"

### Test Database Persistence
1. Create a user
2. Note their ID
3. Trigger an app restart (deploy new version or restart from Render dashboard)
4. Check admin dashboard - user should still exist

### Check Logs
In Render dashboard:
- Go to **Logs** tab
- Look for `ensure_db()` output
- Check for any `sqlite3` errors
- Monitor performance

---

## 🔄 Part 8: Ongoing Maintenance

### Regular Backups
```bash
# Backup SQLite database (run locally or via cron)
curl -o backup_$(date +%Y%m%d).db \
  "https://your-app.onrender.com/api/admin/backup" \
  -H "X-Admin-Token: $ADMIN_TOKEN"
```

### Monitor Database Size
```bash
# Check database usage on Render
ls -lh /data/education.db
sqlite3 /data/education.db "PRAGMA page_count; PRAGMA page_size;"
```

### Rotate Admin Token
1. Generate new token
2. Update in Render environment variables
3. Test with new token
4. Update local `.env`

### Database Cleanup
```python
# In Python shell on Render:
from modules.education_store import db
conn = sqlite3.connect('/data/education.db')
# Archive old login_tracking records older than 90 days
conn.execute("""
  DELETE FROM login_tracking 
  WHERE login_at < datetime('now', '-90 days')
""")
conn.commit()
```

---

## 🚨 Troubleshooting

### "No such file or directory: /data/education.db"
- ✅ Solution: Check persistent volume is mounted in Render dashboard
- ✅ Verify `DATABASE_URL=/data/education.db` in environment variables
- ✅ Check `Procfile` has `release:` command to initialize DB

### "Admin token required but not found"
- ✅ Solution: Add `ADMIN_STREAM_TOKEN` to Render environment variables
- ✅ Verify token is at least 32 characters
- ✅ Use token in URL: `?token=YOUR_TOKEN`

### "Timeout errors on /admin/users"
- ✅ Solution: Database query taking too long
- ✅ Check: Are you viewing stats for users with huge login histories?
- ✅ Add database indexes: See `education_store.py` line 300+
- ✅ Increase worker count in `Procfile`

### Database locked (sqlite3.OperationalError)
- ✅ Solution: SQLite concurrent write issue
- ✅ Render restarts: Auto-recovers
- ✅ Permanent fix: Migrate to PostgreSQL
- ✅ Temporary: Add `busy_timeout=10000` to connection

---

## 📊 Part 9: Performance Optimization

### For Login Tracking at Scale

If you exceed 10,000+ logins:

1. **Archive old data:**
   ```sql
   -- Archive logins older than 1 year
   INSERT INTO login_tracking_archive
   SELECT * FROM login_tracking 
   WHERE login_at < datetime('now', '-365 days');
   
   DELETE FROM login_tracking 
   WHERE login_at < datetime('now', '-365 days');
   ```

2. **Add indexes (already done in code):**
   ```sql
   CREATE INDEX idx_login_tracking_user ON login_tracking(user_id);
   CREATE INDEX idx_login_tracking_login_at ON login_tracking(login_at);
   ```

3. **Enable WAL mode (already done in code):**
   ```sql
   PRAGMA journal_mode=WAL;
   ```

4. **Consider PostgreSQL migration** if hitting limits

---

## ✅ Final Deployment Checklist

Before hitting "Deploy":

- [ ] Git repository up to date
- [ ] All secrets in Render environment (not in code)
- [ ] `requirements.txt` has all dependencies
- [ ] `Procfile` correct
- [ ] `.env.example` updated
- [ ] Persistent volume created and mounted at `/data`
- [ ] Database will initialize via `ensure_db()` or release command
- [ ] Admin token generated and stored securely
- [ ] Testing on local environment successful
- [ ] Domain configured (optional)
- [ ] Monitoring/logging enabled

---

## 🎯 Quick Reference: Commands

**Generate secure tokens:**
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

**Test locally before deploying:**
```bash
python app.py
# Visit http://localhost:5000/learn/admin/users?token=YOUR_TOKEN
```

**Check database:**
```bash
sqlite3 data/education.db ".tables"
sqlite3 data/education.db "SELECT COUNT(*) FROM users;"
```

**Deploy to Render:**
1. Push to GitHub
2. Render auto-detects and builds
3. Check logs for errors
4. Test live dashboard

---

## 📞 Support & Resources

- **Render Docs:** https://render.com/docs
- **SQLite Persistence:** https://render.com/docs/persistent-disks
- **Flask on Render:** https://render.com/docs/deploy-flask
- **Environment Variables:** https://render.com/docs/environment-variables

---

**Last Updated:** June 4, 2026  
**Status:** Ready for Deployment ✅
