"""Educational Flask Routes

Adds educational content to the battery calculator app.

Includes optional user accounts, progress tracking, and certificates.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from functools import wraps
from io import BytesIO

from flask import Blueprint, abort, flash, jsonify, redirect, render_template, request, send_file, session, url_for
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas

from modules.education_store import (
    authenticate_user,
    create_user,
    get_completed_items,
    get_quiz_best,
    get_user,
    mark_progress,
    record_quiz_attempt,
)
from modules.lithium_education import (
    LithiumBatteryFundamentals, 
    CellChemistry,
    CapacityAndDOD,
    CRate,
    BatteryLifeAndCycles,
    CellSpecifications
)
from modules.interactive_tools import (
    CellSimulator,
    PackSimulator,
    EducationalQuizzes,
    InteractiveCalculators
)

education_bp = Blueprint('education', __name__, url_prefix='/learn')


@dataclass(frozen=True)
class _NavItem:
    key: str
    title: str
    endpoint: str


_LESSON_ITEMS = [
    _NavItem("lesson:fundamentals", "Cell Fundamentals", "education.fundamentals"),
    _NavItem("lesson:chemistry", "Battery Chemistry", "education.chemistry"),
    _NavItem("lesson:capacity-dod", "Capacity & DOD", "education.capacity_dod"),
    _NavItem("lesson:crate", "C-Rate Explained", "education.crate_learn"),
    _NavItem("lesson:cycles-aging", "Cycles & Aging", "education.cycles_aging"),
]

_QUIZZES = [
    {"id": "capacity-dod", "title": "Capacity & DOD Quiz"},
    {"id": "crate", "title": "C-Rate Quiz"},
    {"id": "cell-health", "title": "Cell Health Detection Quiz"},
    {"id": "chemistry", "title": "Chemistry Quiz"},
    {"id": "cycles-aging", "title": "Cycles & Aging Quiz"},
    {"id": "pack-design", "title": "Pack Design Quiz"},
    {"id": "bms-balancing", "title": "BMS & Balancing Quiz"},
]


def _current_user():
    user_id = session.get("edu_user_id")
    if not user_id:
        return None
    return get_user(int(user_id))


def _track(item_key: str) -> None:
    user = _current_user()
    if not user:
        return
    mark_progress(user.id, item_key)


def login_required(fn=None, *, message: str = "Please log in to access this content."):
    """Require an authenticated education user.

    Supports use as either:
        @login_required
        def view(): ...

    or:
        @login_required(message="...")
        def view(): ...
    """

    def _decorator(view_fn):
        @wraps(view_fn)
        def _wrapped(*args, **kwargs):
            if not session.get("edu_user_id"):
                flash(message, "warning")
                return redirect(url_for("education.login", next=request.path))
            return view_fn(*args, **kwargs)

        return _wrapped

    if fn is None:
        return _decorator
    return _decorator(fn)


def api_login_required(fn=None, *, message: str = "login_required"):
    """Require an authenticated education user for JSON API endpoints."""

    def _decorator(view_fn):
        @wraps(view_fn)
        def _wrapped(*args, **kwargs):
            if not session.get("edu_user_id"):
                return jsonify({"error": str(message)}), 401
            return view_fn(*args, **kwargs)

        return _wrapped

    if fn is None:
        return _decorator
    return _decorator(fn)


def _is_certificate_eligible(user_id: int) -> bool:
    completed = get_completed_items(user_id)
    has_required_lessons = all(item.key in completed for item in _LESSON_ITEMS)

    # Overall quiz score is defined as:
    #   overall_pct = (avg of each attempted quiz pct) * 100
    # Unattempted quizzes are excluded from the average.
    overall_pct = _overall_quiz_percentage(user_id)
    quiz_best = get_quiz_best(user_id)
    attempted_count = len(quiz_best)
    all_quizzes_attempted = attempted_count >= len(_QUIZZES)

    return bool(has_required_lessons and all_quizzes_attempted and overall_pct >= 75.0)


def _overall_quiz_percentage(user_id: int) -> float:
    quiz_best = get_quiz_best(user_id)
    if not quiz_best:
        return 0.0

    pct_sum = 0.0
    attempted = 0
    for q in _QUIZZES:
        qid = q["id"]
        if qid not in quiz_best:
            continue
        best_score = int(quiz_best[qid].get("best_score", 0))
        total = int(quiz_best[qid].get("total", 0))
        pct_sum += (best_score / total) if total else 0.0
        attempted += 1

    if attempted <= 0:
        return 0.0
    return (pct_sum / float(attempted)) * 100.0


# ============= AUTH ROUTES =============


@education_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "")
        password = request.form.get("password", "")
        user = authenticate_user(username, password)
        if not user:
            flash("Invalid username or password.", "danger")
            return redirect(url_for("education.login"))

        session["edu_user_id"] = user.id
        session["edu_username"] = user.username
        flash("Logged in.", "success")

        next_url = request.form.get("next") or request.args.get("next")
        return redirect(next_url or url_for("education.progress"))

    return render_template("education/login.html")


@education_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        try:
            user = create_user(
                username=request.form.get("username", ""),
                password=request.form.get("password", ""),
            )
        except ValueError as e:
            flash(str(e), "danger")
            return redirect(url_for("education.register"))

        session["edu_user_id"] = user.id
        session["edu_username"] = user.username
        flash("Account created.", "success")

        next_url = request.form.get("next") or request.args.get("next")
        return redirect(next_url or url_for("education.progress"))

    return render_template("education/register.html")


@education_bp.route("/logout")
def logout():
    session.pop("edu_user_id", None)
    session.pop("edu_username", None)
    flash("Logged out.", "success")
    return redirect(url_for("education.learn_index"))


# ============= PROGRESS & CERTIFICATES =============


@education_bp.route("/progress")
@login_required(message="Please log in to view your progress and certificates.")
def progress():
    user = _current_user()
    if not user:
        abort(401)

    completed = get_completed_items(user.id)
    quiz_best = get_quiz_best(user.id)
    overall_pct = _overall_quiz_percentage(user.id)
    eligible = _is_certificate_eligible(user.id)

    lesson_items = [
        {
            "key": item.key,
            "title": item.title,
            "url": url_for(item.endpoint),
        }
        for item in _LESSON_ITEMS
    ]

    return render_template(
        "education/progress.html",
        user=user,
        lesson_items=lesson_items,
        completed=completed,
        quizzes=_QUIZZES,
        quiz_best=quiz_best,
        overall_pct=overall_pct,
        eligible=eligible,
    )


@education_bp.route("/api/progress/quiz-complete", methods=["POST"])
def api_quiz_complete():
    user = _current_user()
    if not user:
        return jsonify({"error": "login_required"}), 401

    data = request.get_json(silent=True) or {}
    quiz_id = str(data.get("quiz_id") or "").strip()
    score = int(data.get("score") or 0)
    total = int(data.get("total") or 0)

    if not quiz_id:
        return jsonify({"error": "quiz_id_required"}), 400

    record_quiz_attempt(user.id, quiz_id, score, total)
    mark_progress(user.id, f"quiz:{quiz_id}")
    return jsonify({"ok": True})


@education_bp.route("/certificate")
@login_required(message="Please log in to view your certificate.")
def certificate():
    user = _current_user()
    if not user:
        abort(401)

    if not _is_certificate_eligible(user.id):
        flash("Complete the required lessons and at least one quiz to unlock your certificate.", "warning")
        return redirect(url_for("education.progress"))

    completed = get_completed_items(user.id)
    quiz_best = get_quiz_best(user.id)
    overall_pct = _overall_quiz_percentage(user.id)
    issued_date = datetime.now().strftime("%Y-%m-%d")
    certificate_id = f"EDU-{user.id}-{datetime.now().strftime('%Y%m%d')}"

    completed_lessons = [
        {"key": item.key, "title": item.title}
        for item in _LESSON_ITEMS
        if item.key in completed
    ]

    return render_template(
        "education/certificate.html",
        user=user,
        issued_date=issued_date,
        certificate_id=certificate_id,
        completed_lessons=completed_lessons,
        quiz_count=len(quiz_best),
        overall_pct=overall_pct,
    )


@education_bp.route("/certificate.pdf")
@login_required(message="Please log in to download your certificate.")
def certificate_pdf():
    user = _current_user()
    if not user:
        abort(401)

    if not _is_certificate_eligible(user.id):
        flash("Complete the required lessons and at least one quiz to unlock your certificate.", "warning")
        return redirect(url_for("education.progress"))

    issued_date = datetime.now().strftime("%Y-%m-%d")
    certificate_id = f"EDU-{user.id}-{datetime.now().strftime('%Y%m%d')}"

    buf = BytesIO()
    c = canvas.Canvas(buf, pagesize=letter)
    width, height = letter

    # Frame
    margin = 0.75 * inch
    c.setLineWidth(3)
    c.setStrokeColorRGB(102 / 255, 126 / 255, 234 / 255)
    c.rect(margin, margin, width - 2 * margin, height - 2 * margin)

    # Title
    c.setFillColorRGB(102 / 255, 126 / 255, 234 / 255)
    c.setFont("Helvetica-Bold", 26)
    c.drawCentredString(width / 2, height - 2.0 * inch, "Certificate of Completion")

    c.setFillColorRGB(0.2, 0.2, 0.2)
    c.setFont("Helvetica", 12)
    c.drawCentredString(width / 2, height - 2.45 * inch, "Lithium Battery Educational Platform")

    # Body
    c.setFont("Helvetica", 12)
    c.drawCentredString(width / 2, height - 3.3 * inch, "This certifies that")

    c.setFont("Helvetica-Bold", 22)
    c.drawCentredString(width / 2, height - 3.85 * inch, user.username)

    c.setFont("Helvetica", 12)
    c.drawCentredString(
        width / 2,
        height - 4.35 * inch,
        "has completed the required learning modules and assessments.",
    )

    # Footer metadata
    c.setFont("Helvetica", 10)
    c.drawString(margin + 10, margin + 30, f"Date: {issued_date}")
    c.drawRightString(width - margin - 10, margin + 30, f"Certificate ID: {certificate_id}")

    c.showPage()
    c.save()

    buf.seek(0)
    filename = f"certificate_{user.username}.pdf"
    return send_file(buf, mimetype="application/pdf", as_attachment=True, download_name=filename)


# ============= FUNDAMENTAL CONCEPTS ROUTES =============

@education_bp.route('/fundamentals')
def fundamentals():
    """Main fundamentals page"""
    _track("lesson:fundamentals")
    content = {
        "good_cell": LithiumBatteryFundamentals.CELL_BEHAVIORS["good_cell_operation"],
        "bad_cell": LithiumBatteryFundamentals.CELL_BEHAVIORS["bad_cell_detection"],
        "pack_imbalance": LithiumBatteryFundamentals.CELL_BEHAVIORS["pack_imbalance"]
    }
    return render_template('education/fundamentals.html', content=content)


@education_bp.route('/chemistry')
@login_required(message="Please log in to access this lesson.")
def chemistry():
    """Learn about battery chemistries"""
    _track("lesson:chemistry")
    chemistries = {}
    for chem in CellChemistry:
        chemistries[chem.value] = LithiumBatteryFundamentals.CHEMISTRY_PROPERTIES[chem]
    
    return render_template('education/chemistry.html', chemistries=chemistries)


@education_bp.route('/capacity-dod')
@login_required(message="Please log in to access this lesson.")
def capacity_dod():
    """Learn about capacity and DOD"""
    _track("lesson:capacity-dod")
    content = {
        "capacity": CapacityAndDOD.capacity_explanation(),
        "dod": CapacityAndDOD.dod_explanation()
    }
    return render_template('education/capacity_dod.html', content=content)


@education_bp.route('/crate')
@login_required(message="Please log in to access this lesson.")
def crate_learn():
    """Learn about C-rates"""
    _track("lesson:crate")
    content = CRate.crate_explanation()
    return render_template('education/crate.html', content=content)


@education_bp.route('/cycles-aging')
@login_required(message="Please log in to access this lesson.")
def cycles_aging():
    """Learn about battery cycles and aging"""
    _track("lesson:cycles-aging")
    content = {
        "cycles": BatteryLifeAndCycles.cycle_definition(),
        "degradation": BatteryLifeAndCycles.degradation_factors()
    }
    return render_template('education/cycles_aging.html', content=content)


# ============= INTERACTIVE TOOLS ROUTES =============

@education_bp.route('/cell-simulator')
@login_required(message="Please log in to use interactive tools.")
def cell_simulator_page():
    """Cell discharge/charge simulator page"""
    _track("tool:cell-simulator")
    return render_template('education/cell_simulator.html')


@education_bp.route('/api/cell-simulator/discharge', methods=['POST'])
@api_login_required
def api_cell_discharge():
    """API: Simulate cell discharge"""
    data = request.json
    
    # Create cell
    cell = CellSpecifications(
        nominal_voltage_v=float(data.get('nominal_voltage', 3.7)),
        capacity_mah=float(data.get('capacity_mah', 2000)),
        chemistry=CellChemistry.LI_ION,
        min_voltage_v=float(data.get('min_voltage', 2.5)),
        max_voltage_v=float(data.get('max_voltage', 4.2))
    )
    
    simulator = CellSimulator(cell)
    result = simulator.discharge(
        current_a=float(data.get('current_a', 1.0)),
        duration_hours=float(data.get('duration_hours', 1.0))
    )
    
    return jsonify(result)


@education_bp.route('/pack-simulator')
@login_required(message="Please log in to use interactive tools.")
def pack_simulator_page():
    """Pack simulator page"""
    _track("tool:pack-simulator")
    return render_template('education/pack_simulator.html')


@education_bp.route('/api/pack-simulator/discharge', methods=['POST'])
@api_login_required
def api_pack_discharge():
    """API: Simulate pack discharge"""
    data = request.json
    
    cell = CellSpecifications(
        nominal_voltage_v=float(data.get('nominal_voltage', 3.7)),
        capacity_mah=float(data.get('capacity_mah', 2000)),
        chemistry=CellChemistry.LI_ION,
        min_voltage_v=float(data.get('min_voltage', 2.5)),
        max_voltage_v=float(data.get('max_voltage', 4.2))
    )
    
    pack = PackSimulator(
        num_cells=int(data.get('num_cells', 4)),
        cell_spec=cell
    )
    
    if data.get('introduce_imbalance', False):
        pack.introduce_imbalance()
    
    result = pack.discharge_pack(
        pack_current_a=float(data.get('pack_current_a', 4.0)),
        duration_hours=float(data.get('duration_hours', 1.0))
    )
    
    return jsonify(result)


@education_bp.route('/api/pack-simulator/health', methods=['POST'])
@api_login_required
def api_pack_health():
    """API: Get pack health assessment"""
    data = request.json
    
    cell = CellSpecifications(
        nominal_voltage_v=float(data.get('nominal_voltage', 3.7)),
        capacity_mah=float(data.get('capacity_mah', 2000)),
        chemistry=CellChemistry.LI_ION,
        min_voltage_v=float(data.get('min_voltage', 2.5)),
        max_voltage_v=float(data.get('max_voltage', 4.2))
    )
    
    pack = PackSimulator(
        num_cells=int(data.get('num_cells', 4)),
        cell_spec=cell
    )
    
    health = pack.get_pack_health()
    return jsonify(health)


# ============= CALCULATORS ROUTES =============

@education_bp.route('/calculators')
@login_required(message="Please log in to use interactive tools.")
def calculators():
    """Interactive calculators page"""
    _track("tool:calculators")
    return render_template('education/calculators.html')


@education_bp.route('/', strict_slashes=False)
@education_bp.route('')
def learn_index():
    """Redirect /learn to the interactive calculators landing page."""
    # Render a small landing page that links to calculators and quizzes
    _track("hub:learn-index")
    return render_template('education/learn_index.html')


@education_bp.route('/api/calculate/energy', methods=['POST'])
@api_login_required
def api_calculate_energy():
    """API: Calculate energy from capacity"""
    data = request.json
    result = InteractiveCalculators.capacity_energy_calculator(
        capacity_mah=float(data.get('capacity_mah', 2000)),
        voltage_v=float(data.get('voltage_v', 3.7))
    )
    return jsonify(result)


@education_bp.route('/api/calculate/crate', methods=['POST'])
@api_login_required
def api_calculate_crate():
    """API: Calculate C-rate"""
    data = request.json
    result = InteractiveCalculators.crate_calculator(
        current_a=float(data.get('current_a', 1.0)),
        capacity_ah=float(data.get('capacity_ah', 2.0))
    )
    return jsonify(result)


@education_bp.route('/api/calculate/cycle-life', methods=['POST'])
@api_login_required
def api_calculate_cycle_life():
    """API: Calculate expected cycle life"""
    data = request.json
    result = InteractiveCalculators.cycle_life_calculator(
        chemistry=CellChemistry[data.get('chemistry', 'LI_ION')],
        dod_percent=int(data.get('dod_percent', 80))
    )
    return jsonify(result)


@education_bp.route('/api/calculate/pack-voltage', methods=['POST'])
@api_login_required
def api_calculate_pack_voltage():
    """API: Calculate pack voltage"""
    data = request.json
    result = InteractiveCalculators.pack_voltage_calculator(
        num_cells=int(data.get('num_cells', 4)),
        cell_voltage_v=float(data.get('cell_voltage_v', 3.7)),
        configuration=data.get('configuration', 'series')
    )
    return jsonify(result)


# ============= QUIZ ROUTES =============

@education_bp.route('/quiz')
@login_required(message="Please log in to take quizzes.")
def quiz_index():
    """Quiz selection page"""
    _track("tool:quiz")
    quizzes = [
        {'id': 'capacity-dod', 'title': 'Capacity & DOD Quiz'},
        {'id': 'crate', 'title': 'C-Rate Quiz'},
        {'id': 'cell-health', 'title': 'Cell Health Detection Quiz'},
        {'id': 'chemistry', 'title': 'Chemistry Quiz'},
        {'id': 'cycles-aging', 'title': 'Cycles & Aging Quiz'},
        {'id': 'pack-design', 'title': 'Pack Design Quiz'},
        {'id': 'bms-balancing', 'title': 'BMS & Balancing Quiz'}
    ]
    return render_template('education/quiz_index.html', quizzes=quizzes)


@education_bp.route('/api/quiz/capacity-dod')
@api_login_required
def api_quiz_capacity_dod():
    """API: Get capacity & DOD quiz"""
    questions = EducationalQuizzes.quiz_capacity_dod()
    return jsonify(questions)


@education_bp.route('/api/quiz/crate')
@api_login_required
def api_quiz_crate():
    """API: Get C-rate quiz"""
    questions = EducationalQuizzes.quiz_crate()
    return jsonify(questions)


@education_bp.route('/api/quiz/cell-health')
@api_login_required
def api_quiz_cell_health():
    """API: Get cell health quiz"""
    questions = EducationalQuizzes.quiz_cell_health()
    return jsonify(questions)


@education_bp.route('/api/quiz/chemistry')
@api_login_required
def api_quiz_chemistry():
    """API: Get chemistry quiz"""
    questions = EducationalQuizzes.quiz_chemistry()
    return jsonify(questions)


@education_bp.route('/api/quiz/cycles-aging')
@api_login_required
def api_quiz_cycles_aging():
    """API: Get cycles & aging quiz"""
    questions = EducationalQuizzes.quiz_cycles_aging()
    return jsonify(questions)


@education_bp.route('/api/quiz/pack-design')
@api_login_required
def api_quiz_pack_design():
    """API: Get pack design quiz"""
    questions = EducationalQuizzes.quiz_pack_design()
    return jsonify(questions)


@education_bp.route('/api/quiz/bms-balancing')
@api_login_required
def api_quiz_bms_balancing():
    """API: Get BMS & balancing quiz"""
    questions = EducationalQuizzes.quiz_bms_balancing()
    return jsonify(questions)


# ============= REFERENCE PAGES =============

@education_bp.route('/reference/good-cell')
@login_required(message="Please log in to access reference materials.")
def reference_good_cell():
    """Reference: What makes a good cell"""
    content = LithiumBatteryFundamentals.CELL_BEHAVIORS["good_cell_operation"]
    return render_template('education/reference_good_cell.html', content=content)


@education_bp.route('/reference/bad-cell')
@login_required(message="Please log in to access reference materials.")
def reference_bad_cell():
    """Reference: Signs of a bad cell"""
    content = LithiumBatteryFundamentals.CELL_BEHAVIORS["bad_cell_detection"]
    return render_template('education/reference_bad_cell.html', content=content)


@education_bp.route('/reference/pack-issues')
@login_required(message="Please log in to access reference materials.")
def reference_pack_issues():
    """Reference: Cell imbalance in packs"""
    content = LithiumBatteryFundamentals.CELL_BEHAVIORS["pack_imbalance"]
    return render_template('education/reference_pack_issues.html', content=content)


@education_bp.route('/glossary')
@login_required(message="Please log in to access reference materials.")
def glossary():
    """Battery terminology glossary"""
    _track("tool:glossary")
    terms = {
        "SOC": "State of Charge - Percentage of battery capacity currently available (0-100%)",
        "DOD": "Depth of Discharge - Percentage of capacity that has been used (100% - SOC)",
        "C-rate": "Discharge/charge current relative to capacity. 1C = discharge in 1 hour",
        "Cycle": "One complete charge-discharge cycle from 0% to 100% and back",
        "Capacity": "Total charge a battery can store, measured in mAh or Ah",
        "Internal Resistance": "Opposition to current flow inside the cell, increases with age",
        "Voltage Sag": "Temporary voltage drop under load due to internal resistance",
        "BMS": "Battery Management System - electronic device that monitors and controls battery",
        "Balancing": "Equalizing charge levels across cells in a pack",
        "Calendar Aging": "Battery degradation over time even without use",
        "Cycle Aging": "Battery degradation caused by charge-discharge cycles"
    }
    return render_template('education/glossary.html', terms=terms)
