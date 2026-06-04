# ⚡ Render Deployment: Quick Start (5 Minutes)

## Step 1: Prepare Your Code (5 minutes)

```bash
# Make sure you're in project root
cd /path/to/Battery_calculator

# Generate secure tokens
python -c "import secrets; print('SECRET_KEY:', secrets.token_hex(32))"
python -c "import secrets; print('ADMIN_TOKEN:', 'admin_' + secrets.token_hex(32))"

# Push to GitHub
git add -A
git commit -m "Prepare for Render deployment"
git push origin main
```

## Step 2: Create Service on Render (2 minutes)

1. Go to [render.com](https://render.com)
2. Click **New** → **Web Service**
3. Select your GitHub repository
4. Fill in:
   - **Name:** `battery-calculator`
   - **Runtime:** `Python`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn app:app --workers 3 --threads 2 --bind 0.0.0.0:$PORT --timeout 300`

## Step 3: Add Environment Variables (1 minute)

Click **Environment** and add:

| Key | Value |
|-----|-------|
| `FLASK_ENV` | `production` |
| `FLASK_DEBUG` | `0` |
| `DATABASE_URL` | `/data/education.db` |
| `SECRET_KEY` | [Paste from Step 1] |
| `ADMIN_STREAM_TOKEN` | [Paste from Step 1] |
| `MAINTENANCE_MODE` | `false` |

## Step 4: Create Persistent Disk (1 minute)

Click **Disks** → **Create Persistent Disk**:
- **Name:** `education-database`
- **Size:** `1 GB`
- **Mount Path:** `/data`

## Step 5: Deploy! (2 minutes)

Click **Create Web Service** and wait 5-10 minutes for deployment to complete.

---

## Verify It Works

```bash
# Get your Render URL from the dashboard
# Example: https://battery-calculator.onrender.com

# Test the app
curl https://battery-calculator.onrender.com

# Test admin dashboard (replace YOUR_ADMIN_TOKEN with your actual token)
curl "https://battery-calculator.onrender.com/learn/admin/users?token=YOUR_ADMIN_TOKEN"
```

Or visit in browser:
- App: `https://battery-calculator.onrender.com`
- Admin: `https://battery-calculator.onrender.com/learn/admin/users?token=YOUR_ADMIN_TOKEN`

---

## Troubleshooting

**Build fails?**
- Check logs in Render dashboard → Logs tab
- Verify all imports in `app.py` are in `requirements.txt`

**Database error?**
- Verify persistent disk is mounted at `/data`
- Check `DATABASE_URL=/data/education.db` in environment variables

**Can't access admin?**
- Verify token in environment variable matches URL
- Try: `?token=YOUR_ADMIN_TOKEN`

---

**Need more details?** See [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)  
**Need a checklist?** See [DEPLOYMENT_CHECKLIST.md](DEPLOYMENT_CHECKLIST.md)

---

**Status:** ✅ Ready to deploy!
