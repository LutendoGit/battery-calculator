# Integrated Admin Module Progress Dashboard - Testing Guide

## 🚀 Access the Dashboard

**URL:** http://localhost:5000/learn/admin/module-progress?token=sP1KYXbw3fS2ZYF5LmJF3Qr-TOdf0

**Admin Token:** `sP1KYXbw3fS2ZYF5LmJF3Qr-TOdf0` (from `.env` file)

---

## 📊 Dashboard Overview

### System Statistics (Top Cards)
- **Total Users** - Count of all registered users
- **Certificates Awarded** - Total certificates earned (75%+ quizzes)
- **Users with Certificates** - Count of unique users with at least 1 certificate
- **Avg Certs per User** - Average certificates per user

### Navigation Tabs

#### 1️⃣ **All Users Tab**
- Shows all registered users
- Displays:
  - Username
  - Email
  - Modules Completed (count)
  - Modules In Progress (count)
  - Certificates (count)
- **Features:**
  - Search/filter by username
  - Click any user to view detailed progress
  - View button to inspect user details

#### 2️⃣ **Certificates Tab**
- Lists all module certificates awarded (75%+)
- Displays:
  - User who earned it
  - Module ID (module_1, module_2, etc.)
  - Quiz ID taken
  - Score achieved
  - Percentage (with progress bar)
  - Award date/time

#### 3️⃣ **Module Stats Tab**
- System-wide module completion statistics
- Shows per-module breakdown:
  - Not Started (count)
  - In Progress (count)
  - Completed (count)

#### 4️⃣ **User Details Tab**
- Search for a specific user by ID
- Shows detailed progress including:
  - Modules completed/in-progress/not-started (counts)
  - Module completion status for each module
  - Visual module grid showing status
  - Earned certificates with percentages

---

## 🧪 Full Testing Workflow

### Step 1: Create a Test Account
1. Open: http://localhost:5000/learn/login
2. Click "Create Account"
3. Fill in:
   - **Username:** test_user_001
   - **Email:** test@example.com
   - **Password:** Test123!
4. Click "Register"

### Step 2: Start Learning Module 1
1. After login, click "Module 1 (Fundamentals)"
2. Read through the lesson content
3. At the end, click "Take Module 1 Quiz"

### Step 3: Complete Quiz with 75%+ Score
1. Answer the quiz questions
2. Try to get **75% or higher** to trigger certificate award
3. Submit the quiz
4. You should see message indicating pass/certificate award

### Step 4: Check Admin Dashboard (Instant Updates)
1. Go back to: http://localhost:5000/learn/admin/module-progress?token=sP1KYXbw3fS2ZYF5LmJF3Qr-TOdf0
2. Click **Refresh** button
3. Verify you see:
   - **Statistics updated** (certificates count increased)
   - **All Users tab** shows your test user with 1 certificate
   - **Certificates tab** shows your earned certificate
   - **Module Stats** shows module_1 with 1 completed
   - **User Details** (search by user ID) shows all your progress

---

## 🔄 Real-time Features

### Auto-Refresh
- Dashboard automatically refreshes every 30 seconds
- You'll see updates automatically without manually clicking Refresh

### Manual Refresh
- Click the **Refresh** button anytime to get latest data immediately

### Live Updates
- After each quiz completion, statistics update in real-time
- Certificates appear immediately in the certificates list
- Module progress shown across all views

---

## 📈 What Gets Tracked

### When User Starts a Module
- Module progress record created (status: 'in_progress')
- Timestamp recorded

### When User Completes Quiz with 75%+
- Certificate awarded to user
- Module status updated to 'completed'
- Event logged for audit trail
- Statistics updated
- Dashboard shows:
  - New certificate in "Certificates" tab
  - Module marked as completed in user details
  - Counts updated in statistics

### Dashboard Shows
✅ Real-time module completion tracking
✅ Quiz pass/fail status with percentages
✅ Certificate awards with timestamps
✅ Per-module and per-user statistics
✅ User filtering and search
✅ Progress visualization

---

## 🔐 Security Notes

- Admin token required: `sP1KYXbw3fS2ZYF5LmJF3Qr-TOdf0`
- Token from `.env` file (environment variable)
- All endpoints require valid token
- Data is SQLite (local storage)

---

## 🐛 Troubleshooting

### Dashboard not loading?
- Ensure Flask is running: `python app.py`
- Check admin token is correct in URL
- Verify `.env` file exists with ADMIN_STREAM_TOKEN set

### No users showing?
- Create test account first at: http://localhost:5000/learn/login
- Wait for page to load and data to fetch

### No certificates showing?
- Complete a quiz with 75%+ score
- Dashboard auto-refreshes every 30 seconds (or click Refresh)

### Data not updating?
- Click the Refresh button to force update
- Check that quiz was completed with 75%+ score
- Verify Flask logs for any errors

---

## 📝 Test Checklist

- [ ] Access dashboard at the admin URL
- [ ] Create test user account
- [ ] Complete Module 1 lesson
- [ ] Take Module 1 quiz with 75%+ score
- [ ] Check "All Users" tab shows updated progress
- [ ] Check "Certificates" tab shows new certificate
- [ ] Check "Module Stats" shows completion count
- [ ] Check "User Details" tab with user ID shows full progress
- [ ] Test search/filter functionality
- [ ] Test auto-refresh by waiting 30 seconds
- [ ] Test manual refresh button

---

## 💾 Database Schema

Data is stored in SQLite with tables:
- `users` - User accounts
- `module_progress` - Module status tracking
- `module_certificates` - Certificate records
- `quiz_attempts` - Quiz completion history
- `user_events` - Audit trail

All data is local in `modules/education.db`

---

## 🎯 Next Steps

1. **Test the complete flow** using the workflow above
2. **Create multiple users** to see data variation
3. **Try different quiz scores** to see threshold logic (75% = certificate)
4. **Monitor dashboard** updating in real-time
5. **Export data** via admin endpoints if needed

---

Enjoy testing your integrated module progress tracking system! 🚀
