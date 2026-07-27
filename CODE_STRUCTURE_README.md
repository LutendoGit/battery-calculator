# BATTERY CALCULATOR - Code Structure & Rendering Architecture

## 📋 Overview

This document outlines the current production code structure, focusing on the active application architecture and the data flow from backend (Flask) to frontend (Jinja2 templates + JavaScript).

---

## 🏗️ Project Architecture

```
Battery Calculator Web App
├── Backend (Flask)
│   ├── app.py (Main application entry point)
│   ├── calculator.py (Core calculation logic)
│   ├── routes/ (Route blueprints)
│   │   └── education_routes.py (Educational module routing)
│   └── modules/ (Business logic & data)
│       ├── education_store.py (User progress tracking)
│       ├── lithium_education.py (Educational content)
│       ├── fundamentals.py (Battery fundamentals)
│       ├── interactive_tools.py (Interactive components)
│       └── __init__.py
├── Frontend (Templates & Static Assets)
│   ├── templates/
│   │   ├── base layouts
│   │   ├── education/ (Educational module templates)
│   │   └── static components
│   └── static/
│       ├── lesson_pager.js (Pagination logic)
│       ├── images/ (Educational content)
│       └── videos/ (Video resources)
└── Configuration
    ├── requirements.txt (Python dependencies)
    ├── runtime.txt (Python version)
    └── Procfile (Deployment configuration)
```

---

## 📁 Core File Structure

### **Backend Files**

#### **1. `app.py` - Main Application**
- **Purpose**: Flask application factory and global route handlers
- **Key Responsibilities**:
  - Initialize Flask app with configuration
  - Register blueprints (education routes)
  - Handle maintenance mode gating
  - Cache management for PDF exports
  - Static file caching optimization for development

**Key Imports**:
```python
from flask import Flask, render_template, url_for, redirect
from routes.education_routes import education_bp
from modules import education_store
```

**Configuration**:
```python
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "dev")
app.config['TEMPLATES_AUTO_RELOAD'] = True  # Hot reload in development
```

#### **2. `routes/education_routes.py` - Education Module Routing**
- **Purpose**: Defines all educational module endpoints (Module 1-10)
- **Route Pattern**: `@education_bp.route('/fundamentals/module-X')`
- **Modules Covered**: 10 learning modules
  1. Module 1: Lithium Battery Fundamentals
  2. Module 2: Electrical Fundamentals
  3. Module 3: Battery Fundamentals
  4. Module 4: Battery Management System (BMS)
  5. Module 5: Energy System Design & Sizing
  6. Module 6: Installation, Wiring & Integration
  7. Module 7: System Configuration
  8. Module 8: Monitoring & Troubleshooting
  9. Module 9: REVOV Ecosystem
  10. Module 10: Installer Guides & Resources

**Authentication**: Modules 6-10 require `@login_required` decorator

**Data Flow Structure**:
```python
@education_bp.route('/fundamentals/module-X')
def fundamentals_moduleX():
    # 1. Load content from lithium_education.py
    content = MODULE_X_DATA
    
    # 2. Create continue card (navigation context)
    continue_card = {
        "step_title": "Continue Learning",
        "title": "📚 Next Steps",
        "paragraphs": [...],
        "links": [
            {"url": url_for("education.quiz_index"), "label": "Take Quiz"},
            {"url": url_for("education.fundamentals_moduleY"), "label": "Start Module Y"}
        ]
    }
    
    # 3. Render template with context
    return render_template(
        'education/fundamentals.html',
        content=content,
        continue_card=continue_card,
        lesson_key="lesson:fundamentals-X"
    )
```

#### **3. `calculator.py` - Core Calculation Engine**
- **Purpose**: Pure calculation logic for battery designs
- **Functions**: Performs mathematical computations for battery parameters
- **Usage**: Called by app.py for battery calculator endpoints

#### **4. `modules/lithium_education.py` - Educational Content**
- **Purpose**: Stores all educational module content as Python dictionaries
- **Structure**: Each module defined as `MODULE_X_CONSTANTNAME`
- **Content Type**: 
  - Text blocks with markdown support
  - Image references with classes
  - Code examples
  - Interactive components

**Content Dictionary Structure**:
```python
MODULE_1_FUNDAMENTALS = {
    "title": "Module Title",
    "description": "Module description",
    "blocks": [
        {
            "type": "heading",
            "content": "Section heading"
        },
        {
            "type": "paragraph",
            "content": "Paragraph text"
        },
        {
            "type": "image",
            "src": "/static/images/module1/battery-diagram.png",
            "alt": "Image description",
            "classes": ["content-image", "example-image"]
        },
        {
            "type": "code",
            "language": "python",
            "content": "code snippet"
        }
    ]
}
```

#### **5. `modules/education_store.py` - User Progress**
- **Purpose**: SQLite database for tracking user learning progress
- **Tracks**: 
  - Quiz scores
  - Module completion status
  - User engagement metrics

#### **6. `modules/interactive_tools.py` - Interactive Components**
- **Purpose**: Business logic for interactive educational tools
- **Features**: Cell simulators, calculators within lessons

#### **7. `modules/fundamentals.py` - Supporting Logic**
- **Purpose**: Utility functions and data processing
- **Usage**: Supports content rendering and data transformation

### **Frontend Files**

#### **1. `templates/education/fundamentals.html` - Main Module Template**
- **Purpose**: Renders educational module content with interactive features
- **Key Components**:

**Macro for Content Rendering**:
```jinja2
{% macro render_block(block, level=3) %}
    {% if block.type == 'image' %}
        <img src="{{ block.src }}" 
             alt="{{ block.alt }}"
             class="{{ block.classes | join(' ') }} clickable-image"
             data-clickable="true">
    {% elif block.type == 'code' %}
        <pre><code class="language-{{ block.language }}">{{ block.content }}</code></pre>
    {% elif block.type == 'heading' %}
        <h{{ level }}>{{ block.content }}</h{{ level }}>
    {% else %}
        <p>{{ block.content | safe }}</p>
    {% endif %}
{% endmacro %}
```

**Interactive Image Viewer Modal**:
```html
<div id="image-viewer-modal" class="image-viewer-modal">
    <div class="image-viewer-controls">
        <span id="zoom-level">100%</span>
        <button id="zoom-in">+</button>
        <button id="zoom-out">−</button>
        <button id="reset-zoom">Reset</button>
        <button id="close-modal">Close</button>
    </div>
    <img id="modal-image" src="" alt="">
</div>
```

**ImageViewer JavaScript Object**:
```javascript
const ImageViewer = {
    init: function() {
        // Initialize zoom levels (50-300%)
        // Handle mouse wheel, keyboard shortcuts (+, -, 0, Esc)
        // Manage pan/drag functionality
        // Toggle zoom-in cursor on clickable images
    },
    zoom: function(direction) { ... },
    pan: function(x, y) { ... },
    reset: function() { ... }
}
```

#### **2. `templates/base.html` - Base Layout**
- **Purpose**: Main page structure and navigation
- **Includes**: Header, navigation, footer
- **Child Template Blocks**: `{% block content %}`, `{% block styles %}`, `{% block scripts %}`

#### **3. `static/lesson_pager.js` - Pagination Logic**
- **Purpose**: Handles module navigation and pagination
- **Features**: Next/Previous module buttons, progress tracking

#### **4. `static/images/` - Educational Assets**
```
static/images/
├── module 5/
│   └── [battery design diagrams]
├── module 6/
│   └── [installation guides]
├── module 7/
│   └── [system configuration]
├── module 8/
│   └── [monitoring dashboards]
├── module 9/
│   └── [REVOV ecosystem]
└── module 10/
    └── [installer resources]
```

#### **5. `static/videos/` - Video Resources**
- Embedded video content for supplementary learning

#### **6. `templates/_site_footer.html` - Footer Component**
- Reusable footer for all pages

#### **7. `templates/_site_footer_styles.html` - Footer Styles**
- Dedicated footer styling

---

## 🔄 Backend-to-Frontend Data Flow

### **1. Request Phase**

```
User navigates to /fundamentals/module-3
         ↓
Flask routes to fundamentals_module3()
         ↓
Route function executes (in education_routes.py)
```

### **2. Data Retrieval Phase**

```python
# Step 1: Load content
content = MODULE_3_BATTERY_FUNDAMENTALS  # From lithium_education.py

# Step 2: Build navigation context
continue_card = {
    "step_title": "Continue Learning",
    "links": [
        {"url": url_for("education.quiz_index", start="module-3-assessment"), 
         "label": "Take Module 3 Quiz"},
        {"url": url_for("education.fundamentals_module4"), 
         "label": "Start Module 4 (Battery Management System)"}
    ]
}

# Step 3: Track user progress (optional)
# education_store.track_module_view(user_id, "module-3")
```

### **3. Template Rendering Phase**

```
render_template('education/fundamentals.html', 
                content=content,
                continue_card=continue_card,
                lesson_key="lesson:fundamentals-3")
         ↓
Jinja2 engine processes template
         ↓
```

### **4. Template Processing**

```jinja2
{# Template receives context variables #}
{% for block in content.blocks %}
    {% if block.type == 'image' %}
        {# Render block macro #}
        {{ render_block(block) }}
    {% endif %}
{% endfor %}

{# Render continue card with module links #}
{% for link in continue_card.links %}
    <a href="{{ link.url }}">{{ link.label }}</a>
{% endfor %}
```

### **5. HTML Generation Phase**

```html
<!-- Final HTML sent to browser -->
<div class="module-content">
    <h2>Module 3: Battery Fundamentals</h2>
    
    <!-- Images with interactive classes -->
    <img src="/static/images/module3/battery-diagram.png" 
         class="content-image clickable-image" 
         data-clickable="true">
    
    <!-- Navigation links from continue_card -->
    <a href="/fundamentals/module-4" class="continue-link">
        Start Module 4 (Battery Management System)
    </a>
</div>

<!-- Inline JavaScript for interactivity -->
<script src="/static/lesson_pager.js"></script>
```

### **6. Client-Side Interaction Phase**

```javascript
// Browser loads static assets
// lesson_pager.js and ImageViewer object execute
// Event listeners attached to images
// User clicks image → ImageViewer zooms/pans
// User clicks "Start Module 4" → Navigate to next module
```

---

## 📊 Data Structure Example: Complete Module Flow

### **Backend (Python)**
```python
# routes/education_routes.py
@education_bp.route('/fundamentals/module-3')
def fundamentals_module3():
    """Fundamentals Module 3: Battery Fundamentals"""
    content = MODULE_3_BATTERY_FUNDAMENTALS
    
    continue_card = {
        "step_title": "Continue Learning",
        "title": "📚 Continue to Module 3 Assessment",
        "paragraphs": ["You've reached the end of Module 3."],
        "links": [
            {
                "url": url_for("education.quiz_index", start="module-3-assessment"),
                "label": "Take Module 3 Quiz"
            },
            {
                "url": url_for("education.fundamentals_module4"),
                "label": "Start Module 4 (BMS)"
            }
        ]
    }
    
    return render_template(
        'education/fundamentals.html',
        content=content,
        continue_card=continue_card,
        lesson_key="lesson:fundamentals-3"
    )
```

### **Content Module (Python)**
```python
# modules/lithium_education.py
MODULE_3_BATTERY_FUNDAMENTALS = {
    "title": "Module 3: Battery Fundamentals",
    "blocks": [
        {
            "type": "heading",
            "content": "Understanding Lithium Batteries"
        },
        {
            "type": "image",
            "src": "/static/images/module3/battery-cell-diagram.png",
            "alt": "Battery cell internal structure",
            "classes": ["content-image", "example-image"]
        },
        {
            "type": "paragraph",
            "content": "Lithium batteries consist of..."
        }
    ]
}
```

### **Template Rendering (Jinja2)**
```html
<!-- templates/education/fundamentals.html -->
{% for block in content.blocks %}
    {% if block.type == 'heading' %}
        <h3>{{ block.content }}</h3>
    {% elif block.type == 'image' %}
        <img src="{{ block.src }}" 
             alt="{{ block.alt }}"
             class="{{ block.classes | join(' ') }} clickable-image">
    {% elif block.type == 'paragraph' %}
        <p>{{ block.content | safe }}</p>
    {% endif %}
{% endfor %}

<!-- Continue Card Navigation -->
<div class="continue-card">
    <h4>{{ continue_card.step_title }}</h4>
    {% for link in continue_card.links %}
        <a href="{{ link.url }}" class="btn">{{ link.label }}</a>
    {% endfor %}
</div>
```

### **Browser Output (HTML)**
```html
<div class="module-content">
    <h3>Understanding Lithium Batteries</h3>
    
    <img src="/static/images/module3/battery-cell-diagram.png" 
         alt="Battery cell internal structure"
         class="content-image example-image clickable-image">
    
    <p>Lithium batteries consist of...</p>
    
    <div class="continue-card">
        <h4>Continue Learning</h4>
        <a href="/education/quiz?start=module-3-assessment" class="btn">
            Take Module 3 Quiz
        </a>
        <a href="/fundamentals/module-4" class="btn">
            Start Module 4 (BMS)
        </a>
    </div>
</div>
```

---

## 🎨 Image Rendering Enhancement

### **Quality Features**

**1. Native Resolution Preservation**
```css
/* Display images at original size */
width: auto;
max-width: auto;
```

**2. Crisp Rendering**
```css
/* Prioritize sharp edges over smooth scaling */
image-rendering: -webkit-optimize-contrast;  /* WebKit */
image-rendering: crisp-edges;                 /* Standard */
object-fit: auto;
```

**3. Interactive Zoom System**
- Detects all image types (`.content-image`, `.content-image-native`, `.example-image`)
- Mouse wheel: Scroll to zoom 50%-300%
- Keyboard: `+`/`−` to zoom, `0` to reset, `Esc` to close
- Drag/Pan: Move zoomed images to view different sections
- Visual Feedback: Cursor changes (`zoom-in`, `grab`, `grabbing`)

---

## 🔗 Module Navigation Architecture

### **Sequential Navigation Chain**
```
Module 1 → Quiz 1 + Start Module 2
     ↓
Module 2 → Quiz 2 + Start Module 3
     ↓
Module 3 → Quiz 3 + Start Module 4
     ↓
... (continues)
     ↓
Module 9 → Start Module 10
     ↓
Module 10 → Training Hub (final)
```

### **URL Pattern**
```
/fundamentals/module-1 → fundamentals_module1()
/fundamentals/module-2 → fundamentals_module2()
...
/fundamentals/module-10 → fundamentals_module10()
```

### **Navigation Link Generation**
```python
# Backend generates links using Flask's url_for()
"url": url_for("education.fundamentals_module4")

# Renders to:
href="/fundamentals/module-4"
```

---

## 🚀 Deployment & Configuration

### **Environment Variables**
```bash
SECRET_KEY          # Flask session encryption
MAINTENANCE_MODE    # Enable maintenance page (1/true/yes/on)
MAINTENANCE_RETRY_AFTER  # HTTP Retry-After header value
```

### **Key Files**
- `Procfile` - Deployment configuration for Render
- `requirements.txt` - Python dependencies
- `runtime.txt` - Python version specification

---

## 📝 Template Hierarchy

```
base.html (Base layout)
├── Header
├── Navigation
├── {% block content %}
│   └── education/fundamentals.html (Module content)
│       ├── Module header
│       ├── render_block macro (repeats for each content block)
│       ├── Image viewer modal
│       └── Continue card (navigation)
├── Footer (_site_footer.html)
└── Scripts
    └── lesson_pager.js (Pagination & interactivity)
```

---

## 📱 Responsive Design Considerations

### **Current CSS Approach**
- Flexbox layouts for responsive grids
- Auto sizing for images (prevents quality loss)
- Modal overlay for full-screen image viewer
- Mobile-friendly touch events for zoom/pan

### **Future CSS Optimization Areas**
- Breakpoints for small screens
- Touch gesture improvements
- Accessibility enhancements (ARIA labels, keyboard navigation)

---

## 🔐 Authentication & Authorization

**Protected Routes**: Modules 6-10 require login
```python
@login_required(message="Please log in to access this lesson.")
def fundamentals_module6():
    ...
```

**Free Modules**: Modules 1-5 are public
```python
@education_bp.route('/fundamentals/module-1')
def fundamentals_module1():
    # No @login_required decorator
```

---

## 📚 Summary: Rendering Pipeline

1. **Request** → User navigates to `/fundamentals/module-X`
2. **Route Match** → Flask matches URL to `fundamentals_moduleX()`
3. **Load Content** → Route retrieves `MODULE_X_DATA` from `lithium_education.py`
4. **Build Context** → Creates `continue_card` dict with navigation links
5. **Render Template** → Jinja2 processes `fundamentals.html` with context
6. **Process Blocks** → Template macro renders each content block (text, images, code)
7. **Generate HTML** → Final HTML with clickable images and navigation links
8. **Serve to Browser** → Flask sends HTML response
9. **Client-Side Init** → JavaScript (lesson_pager.js, ImageViewer) attaches event listeners
10. **User Interaction** → Click image to zoom, click "Next Module" to navigate

This architecture separates concerns (content storage, routing, rendering, styling) while maintaining a clean data flow from backend to frontend.
