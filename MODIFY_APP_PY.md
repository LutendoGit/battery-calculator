# HOW TO MODIFY YOUR app.py

## Current app.py Structure (Simplified)
```python
from flask import Flask, render_template, request, ...
import calculator
# ... other imports

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev'

# Your existing routes and code here...
```

## What To Add

### Step 1: Add Import at the Top
Add this line with your other imports:
```python
from routes.education_routes import education_bp
```

### Step 2: Register Blueprint
Add this line after `app = Flask(__name__)` and before your existing routes:
```python
app.register_blueprint(education_bp)
```

---

## Complete Modified app.py Example

Here's what the beginning of your app.py should look like:

```python
from flask import Flask, render_template, request, redirect, url_for, flash, send_file, jsonify
import calculator
import re
from io import BytesIO
import uuid
import tempfile
import os
from concurrent.futures import ProcessPoolExecutor
import threading
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors

# ===== ADD THIS IMPORT =====
from routes.education_routes import education_bp
# ===========================

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev'

# ===== ADD THESE LINES =====
# Register education blueprint
app.register_blueprint(education_bp)
# ===========================

# Store last result cache for PDF export
last_result = {'text': '', 'title': '', 'chemistry': 'LiFePO4', 'dod': '80'}

# ... rest of your existing code ...

@app.route('/')
def index():
    return render_template('index.html')

# ... your other routes ...

if __name__ == '__main__':
    app.run(debug=True)
```

---

## Verification Checklist

After making changes, verify:

### ✓ Check 1: File Structure
```
your_project/
├── app.py                          ← Modified (2 lines added)
├── modules/
│   ├── __init__.py                ← New (empty file)
│   ├── lithium_education.py       ← New
│   └── interactive_tools.py       ← New
├── routes/
│   ├── __init__.py                ← New (empty file)
│   └── education_routes.py        ← New
├── templates/
│   ├── education/                 ← New folder
│   │   ├── fundamentals.html      ← New
│   │   ├── chemistry.html         ← New
│   │   ├── capacity_dod.html      ← New
│   │   ├── crate.html             ← New
│   │   ├── cycles_aging.html      ← New
│   │   ├── cell_simulator.html    ← New
│   │   ├── pack_simulator.html    ← New
│   │   ├── glossary.html          ← New
│   │   └── (other templates)      ← New
│   └── (existing templates)
└── (other existing files)
```

### ✓ Check 2: Test Import
Run this in your Python terminal to verify imports work:
```python
from routes.education_routes import education_bp
print("Import successful!")
```

Expected output: `Import successful!`

### ✓ Check 3: Start Flask Server
```bash
python app.py
```

Expected output:
```
 * Serving Flask app 'app'
 * Running on http://127.0.0.1:5000
 * WARNING: This is a development server...
```

### ✓ Check 4: Test URLs
Open in browser:
- http://localhost:5000/learn/fundamentals
- http://localhost:5000/learn/glossary
- http://localhost:5000/learn/cell-simulator

---

## Troubleshooting

### Issue: "ModuleNotFoundError: No module named 'routes'"
**Solution:** 
1. Verify `routes/` folder exists
2. Create `routes/__init__.py` (empty file)
3. Restart Flask server

### Issue: "No module named 'education_routes'"
**Solution:**
1. Verify `routes/education_routes.py` exists
2. Check spelling and capitalization
3. Clear Python cache: `rm -rf routes/__pycache__`

### Issue: "TemplateNotFound: education/fundamentals.html"
**Solution:**
1. Create `templates/education/` folder
2. Copy all HTML files into it
3. Verify file names match exactly

### Issue: "404 Not Found" on /learn/ URLs
**Solution:**
1. Verify `app.register_blueprint(education_bp)` is in app.py
2. Check import line is correct
3. Restart Flask server

### Issue: Pages load but styles look wrong
**Solution:**
1. Clear browser cache (Ctrl+Shift+Del)
2. Do hard refresh (Ctrl+Shift+R on Windows)
3. Check browser console for CSS/JS errors (F12)

---

## Optional: Add Navigation Link

To add a link to the learning platform from your main page, add this to your `index.html`:

```html
<a href="/learn/fundamentals" class="btn btn-primary">
    📚 Lithium Battery Learning Hub
</a>
```

Or in your navigation menu:
```html
<nav>
    <a href="/">Home</a>
    <a href="/learn/fundamentals">Learning Hub</a>
    <a href="/calculator">Calculator</a>
</nav>
```

---

## Full Integration Checklist

- [ ] Created `modules/` directory
- [ ] Created `modules/__init__.py`
- [ ] Created `modules/lithium_education.py`
- [ ] Created `modules/interactive_tools.py`
- [ ] Created `routes/` directory
- [ ] Created `routes/__init__.py`
- [ ] Created `routes/education_routes.py`
- [ ] Created `templates/education/` directory
- [ ] Copied all 10 HTML template files
- [ ] Added import line to app.py
- [ ] Added register_blueprint line to app.py
- [ ] Verified file structure
- [ ] Tested import in Python console
- [ ] Started Flask server
- [ ] Tested /learn/fundamentals URL
- [ ] Checked browser console for errors
- [ ] Verified calculators work
- [ ] Tested simulator pages

---

## What You Get After Integration

✅ 10+ educational pages
✅ Interactive cell simulator
✅ Battery pack simulator
✅ 3+ quiz sets with explanations
✅ Educational calculators
✅ Chemistry comparison tool
✅ Searchable glossary
✅ Complete reference material
✅ Mobile-responsive design
✅ Zero new dependencies

---

## Final Verification

Run this Python script to verify everything is set up correctly:

```python
import sys
import os

def verify_setup():
    checks = {
        'modules/__init__.py': 'modules',
        'modules/lithium_education.py': 'lithium_education.py',
        'modules/interactive_tools.py': 'interactive_tools.py',
        'routes/__init__.py': 'routes',
        'routes/education_routes.py': 'education_routes.py',
        'templates/education/fundamentals.html': 'fundamentals.html',
        'templates/education/glossary.html': 'glossary.html',
    }
    
    all_good = True
    for path, name in checks.items():
        if os.path.exists(path):
            print(f"✓ {path}")
        else:
            print(f"✗ {path} - MISSING")
            all_good = False
    
    try:
        from routes.education_routes import education_bp
        print("✓ Import education_bp successful")
    except ImportError as e:
        print(f"✗ Import failed: {e}")
        all_good = False
    
    if all_good:
        print("\n✅ All files present! Ready to run app.py")
    else:
        print("\n❌ Some files missing. Check above.")
    
    return all_good

if __name__ == '__main__':
    verify_setup()
```

Save as `verify_setup.py` and run:
```bash
python verify_setup.py
```

---

**You're all set! 🎉**

Next: Start your Flask server and visit http://localhost:5000/learn/fundamentals
