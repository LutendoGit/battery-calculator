# 🚀 Render Deployment Checklist

**Project:** Battery Calculator with Login Tracking & Admin Dashboard  
**Target:** Render.com  
**Last Updated:** June 4, 2026

---

## 📋 Pre-Deployment (Complete These First)

### Code & Repository
- [ ] All changes committed to git
- [ ] No uncommitted changes (`git status` is clean)
- [ ] Pushed to GitHub (or other git provider)
- [ ] Branch is `main` or deployment branch
- [ ] No sensitive data in committed files
- [ ] `.gitignore` includes: `.env`, `*.db`, `*.db-shm`, `*.db-wal`

### Application Code
- [ ] `app.py` imports all modules correctly
- [ ] `requirements.txt` up to date with all dependencies
- [ ] `Procfile` includes both `release` and `web` commands
- [ ] All routes use `os.environ.get()` for config (no hardcoded paths)
- [ ] No `DEBUG=True` anywhere in production code
- [ ] No `SECRET_KEY` hardcoded (uses environment variable)

### Database & Tables
- [ ] Local database tested: `sqlite3 data/education.db ".tables"`
- [ ] All required tables exist:
  - `users` ✓
  - `progress` ✓
  - `quiz_attempts` ✓
  - `password_resets` ✓
  - `user_events` ✓
  - `login_tracking` ✓
- [ ] Sample users created and tested
- [ ] Login tracking tested (create user, login, check `login_tracking` table)
- [ ] Admin API endpoints tested locally

### Admin Dashboard
- [ ] Dashboard loads at `/learn/admin/users?token=YOUR_TOKEN`
- [ ] All Users tab shows users
- [ ] Active Sessions tab shows current logins
- [ ] User Details tab loads user stats
- [ ] Delete user functionality works
- [ ] Reset progress functionality works

### Documentation
- [ ] `.env.example` has all required variables
- [ ] `DEPLOYMENT_GUIDE.md` is present
- [ ] This checklist is complete
- [ ] `render.yaml` is created

---

## ⚙️ Render Dashboard Setup

### Service Creation
- [ ] Account created on [render.com](https://render.com)
- [ ] GitHub repository connected to Render
- [ ] New Web Service created
- [ ] Name set to: `battery-calculator` (or your preferred name)
- [ ] Runtime selected: `Python`
- [ ] Branch set to: `main` (or your deployment branch)

### Build Configuration
- [ ] Build Command: `pip install -r requirements.txt`
- [ ] Start Command: `gunicorn app:app --workers 3 --threads 2 --bind 0.0.0.0:$PORT --timeout 300`

### Environment Variables
Add in Render Dashboard **Environment** section:

- [ ] `FLASK_ENV` = `production`
- [ ] `FLASK_DEBUG` = `0`
- [ ] `DATABASE_URL` = `/data/education.db`
- [ ] `SECRET_KEY` = [Generate new: `python -c "import secrets; print(secrets.token_hex(32))"`]
- [ ] `ADMIN_STREAM_TOKEN` = [Generate new]
- [ ] `MAINTENANCE_MODE` = `false`
- [ ] `MAINTENANCE_RETRY_AFTER` = `300`

**Secure Token Generation:**
```bash
# Generate SECRET_KEY
python -c "import secrets; print(secrets.token_hex(32))"

# Generate ADMIN_STREAM_TOKEN
python -c "import secrets; print('admin_' + secrets.token_hex(32))"
```

### Persistent Storage
- [ ] Go to **Disks** section
- [ ] Create new persistent disk:
  - Name: `education-database`
  - Size: `1 GB` (sufficient for most use cases)
  - Mount Path: `/data`
- [ ] Disk attached to web service

### Advanced Settings (Optional)
- [ ] Health Check Path: `/` (default)
- [ ] Keep File Descriptors: Leave default
- [ ] Preemptible: Disable if availability is critical
- [ ] Auto-deploy: Enable for automatic deploys on push

---

## 🚀 Deployment

### Initial Deployment
1. [ ] All above items checked ✓
2. [ ] Click **Deploy** button
3. [ ] Watch deployment logs:
   - Build phase should succeed
   - `pip install -r requirements.txt` completes
   - Release phase runs: `python scripts/init_db_render.py` succeeds
   - Web service starts
4. [ ] Deployment completes (shows "Available")
5. [ ] No errors in logs tab

### Verify Deployment
- [ ] Live URL accessible (e.g., `https://battery-calculator.onrender.com`)
- [ ] Homepage loads without errors
- [ ] Admin dashboard accessible: `https://your-app.onrender.com/learn/admin/users?token=YOUR_ADMIN_TOKEN`
- [ ] Create test user: `/learn/signup`
- [ ] Test login: `/learn/login`
- [ ] Check admin dashboard for new user
- [ ] Test logout
- [ ] Check login history in admin dashboard

---

## 🔒 Post-Deployment Security

- [ ] Remove local `.env` file (don't commit it)
- [ ] Change `ADMIN_STREAM_TOKEN` from default
- [ ] Save admin token in password manager (not in code)
- [ ] Enable HTTPS (Render provides free SSL)
- [ ] Test HTTPS redirect is working
- [ ] Verify no sensitive data in logs
- [ ] Set up log monitoring for errors

---

## 📊 Monitoring & Maintenance

### Daily
- [ ] Check Render logs for errors
- [ ] Monitor response times
- [ ] Verify database is accessible

### Weekly
- [ ] Review user activity in admin dashboard
- [ ] Check for any failed login attempts
- [ ] Monitor persistent disk usage: `du -sh /data/`
- [ ] Test a sample user login/logout flow

### Monthly
- [ ] Rotate `ADMIN_STREAM_TOKEN` in environment variables
- [ ] Review and archive old login records (if > 10K entries)
- [ ] Update `requirements.txt` for security patches
- [ ] Check Render billing for any unexpected charges

### Quarterly
- [ ] Review all environment variables for correctness
- [ ] Test backup/restore procedure (if set up)
- [ ] Update deployment documentation as needed

---

## 🆘 Troubleshooting Quick Reference

| Issue | Cause | Fix |
|-------|-------|-----|
| **404 on /learn/admin/users** | Route not registered | Check `education_routes.py` has `@education_bp.get("/admin/users")` |
| **sqlite3.OperationalError: no such file** | DB path incorrect | Verify `DATABASE_URL=/data/education.db` in environment |
| **Admin token required** | Token not passed | Use `?token=YOUR_TOKEN` in URL or `X-Admin-Token` header |
| **Build fails** | Missing dependency | Check `requirements.txt` has all imports from code |
| **Timeout on /admin/api/** | Slow queries | Indexes should exist; check logs for query time |
| **Deployment won't start** | Pre-deploy command failed | Check logs for `init_db_render.py` errors |
| **Database locked** | SQLite concurrency | Render restarts fix it; consider PostgreSQL if persistent |
| **HTTPS redirect loop** | Proxy headers | Already configured in `app.py` ✓ |

---

## 📚 Documentation References

- **This checklist:** `DEPLOYMENT_CHECKLIST.md`
- **Full guide:** `DEPLOYMENT_GUIDE.md`
- **Render docs:** https://render.com/docs
- **SQLite persistence:** https://render.com/docs/persistent-disks
- **Flask on Render:** https://render.com/docs/deploy-flask

---

## ✅ Deployment Complete!

Once all items above are checked, your Battery Calculator with Login Tracking will be **live on Render** and ready for use!

**Key URLs:**
```
App: https://battery-calculator.onrender.com
Admin Dashboard: https://battery-calculator.onrender.com/learn/admin/users?token=YOUR_ADMIN_TOKEN
Logs: https://dashboard.render.com/web/battery-calculator/logs
```

**Next Steps:**
1. Share the app URL with users
2. Users create accounts at `/learn/signup`
3. Track all logins in admin dashboard
4. Monitor and maintain as needed

---

**Last Deployment:** [Update after each deploy]  
**Last Verified:** June 4, 2026  
**Status:** Ready for Deployment ✅
