"""Educational Flask Routes

Adds educational content to the battery calculator app.

Includes optional user accounts, progress tracking, and certificates.
"""

from __future__ import annotations


from dataclasses import dataclass
from datetime import datetime
from functools import wraps
from io import BytesIO
import csv
import os
import secrets
import sqlite3
import uuid


from flask import Blueprint, abort, flash, jsonify, redirect, render_template, request, send_file, session, url_for
from flask import current_app
from werkzeug.utils import secure_filename
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas

from modules import education_store

from modules.education_store import (
    authenticate_user,
    consume_password_reset,
    create_user,
    create_password_reset,
    get_completed_items,
    get_quiz_best,
    get_user,
    mark_progress,
    record_event,
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


def _project_root() -> str:
    """Return absolute project root (one level above `routes/`)."""
    return os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))


def _require_admin_token():
    """Require a shared admin token for potentially sensitive admin endpoints.

    The token is read from env var `ADMIN_STREAM_TOKEN`.
    Provide it either via `?token=...` or `X-Admin-Token` header.
    """
    expected = os.environ.get("ADMIN_STREAM_TOKEN", "")
    if not expected:
        abort(403, description="Set ADMIN_STREAM_TOKEN env var to enable admin endpoints")
    provided = request.headers.get("X-Admin-Token") or request.args.get("token", "")
    if provided != expected:
        abort(403)


def _connect_education_db() -> sqlite3.Connection:
    path = education_store.db_path()
    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA busy_timeout=5000;")
    return conn


def _int_param(name: str, default: int, *, min_value: int | None = None, max_value: int | None = None) -> int:
    try:
        val = int(request.args.get(name, str(default)))
    except Exception:
        val = default
    if min_value is not None:
        val = max(min_value, val)
    if max_value is not None:
        val = min(max_value, val)
    return val


def _demo_certificate_context() -> dict[str, object]:
    issued_date = datetime.now().strftime("%Y-%m-%d")
    certificate_id = f"DEMO-{datetime.now().strftime('%Y%m%d')}"
    completed_lessons = [{"key": item.key, "title": item.title} for item in _LESSON_ITEMS]
    return {
        "user": {"username": "Demo Reviewer"},
        "issued_date": issued_date,
        "certificate_id": certificate_id,
        "completed_lessons": completed_lessons,
        "quiz_count": 7,
        "overall_pct": 88.0,
    }


_ALLOWED_AVATAR_EXTS = {"png", "jpg", "jpeg", "webp"}


def _save_avatar_file(file_storage, *, user_id: int) -> str | None:
    if not file_storage:
        return None

    filename = secure_filename(str(getattr(file_storage, "filename", "") or ""))
    if not filename:
        return None

    if "." not in filename:
        return None
    ext = filename.rsplit(".", 1)[1].lower().strip()
    if ext not in _ALLOWED_AVATAR_EXTS:
        return None

    # Store avatars under static/avatars.
    static_folder = current_app.static_folder or "static"
    avatars_dir = os.path.join(static_folder, "avatars")
    os.makedirs(avatars_dir, exist_ok=True)

    safe_name = f"edu_{int(user_id)}_{uuid.uuid4().hex}.{ext}"
    out_path = os.path.join(avatars_dir, safe_name)
    file_storage.save(out_path)
    return safe_name


@dataclass(frozen=True)
class _NavItem:
    key: str
    title: str
    endpoint: str


_LESSON_ITEMS = [
    _NavItem("lesson:fundamentals", "Fundamentals (Module 1)", "education.fundamentals"),
    _NavItem("lesson:chemistry", "Battery Chemistry", "education.chemistry"),
    _NavItem("lesson:capacity-dod", "Capacity & DOD", "education.capacity_dod"),
    _NavItem("lesson:crate", "C-Rate Explained", "education.crate_learn"),
    _NavItem("lesson:cycles-aging", "Cycles & Aging", "education.cycles_aging"),
]

_QUIZZES = [
    {"id": "capacity-dod", "title": "Power vs Energy & Backup Sizing Quiz"},
    {"id": "crate", "title": "AC vs DC & Conversion Quiz"},
    {"id": "cell-health", "title": "Core System Components Quiz"},
    {"id": "chemistry", "title": "How Lithium-Ion Works Quiz"},
    {"id": "cycles-aging", "title": "Key Battery Concepts Quiz"},
    {"id": "pack-design", "title": "System Types & Energy Flow Quiz"},
    {"id": "bms-balancing", "title": "Efficiency, Losses & REVOV Fit Quiz"},
]


def _quiz_order_ids() -> list[str]:
    return [str(q["id"]) for q in _QUIZZES]


def _quiz_unlock_state(user_id: int) -> dict[str, object]:
    """Return sequential unlock state derived from persisted progress.

    Persistence is stored in SQLite via `mark_progress(user_id, f"quiz:{quiz_id}")`.
    Unlock is sequential: only the first uncompleted quiz and those before it
    are unlocked.
    """

    order = _quiz_order_ids()
    completed_items = get_completed_items(int(user_id))
    completed_quizzes = {k.split("quiz:", 1)[1] for k in completed_items if str(k).startswith("quiz:")}

    unlocked_index = 0
    for idx in range(len(order) - 1):
        if order[idx] in completed_quizzes:
            unlocked_index = idx + 1
        else:
            break

    # Ensure at least the first quiz is available.
    unlocked_index = max(0, min(unlocked_index, max(0, len(order) - 1)))
    return {
        "order": order,
        "unlocked_index": unlocked_index,
        "completed": sorted([qid for qid in completed_quizzes if qid in order]),
    }


def _randomize_quiz_questions(questions: list[dict]) -> list[dict]:
    """Return a randomized (shuffled) copy of quiz questions.

    Randomizes:
    - Question order
    - Option order per question (and updates the `correct` index accordingly)

    This is done per API request so even the same user retaking a quiz
    will typically see a different sequence.
    """

    rng = secrets.SystemRandom()
    randomized: list[dict] = []

    for q in list(questions or []):
        if not isinstance(q, dict):
            continue

        options = q.get("options")
        correct = q.get("correct")
        if not isinstance(options, list) or not options:
            randomized.append(dict(q))
            continue

        try:
            correct_index = int(correct)
        except Exception:
            correct_index = -1

        indexed = list(enumerate(options))
        rng.shuffle(indexed)
        new_options = [opt for _, opt in indexed]
        new_correct = next((i for i, (old_i, _) in enumerate(indexed) if old_i == correct_index), -1)

        q2 = dict(q)
        q2["options"] = new_options
        q2["correct"] = new_correct
        randomized.append(q2)

    rng.shuffle(randomized)
    return randomized


def _require_quiz_unlocked(user_id: int, quiz_id: str):
    quiz_id = str(quiz_id or "").strip()
    order = _quiz_order_ids()
    if quiz_id not in order:
        return jsonify({"error": "unknown_quiz"}), 404

    state = _quiz_unlock_state(int(user_id))
    unlocked_index = int(state["unlocked_index"])
    quiz_idx = order.index(quiz_id)
    if quiz_idx > unlocked_index:
        return jsonify({"error": "locked", "unlocked_index": unlocked_index, "quiz_index": quiz_idx}), 403
    return None


def _current_user():
    user_id = session.get("edu_user_id")
    if not user_id:
        return None
    return get_user(int(user_id))


def _user_has_progress(user_id: int) -> bool:
    """Return True if the user has any saved learning/quiz activity."""
    try:
        completed = get_completed_items(int(user_id))
        if completed:
            return True
        quiz_best = get_quiz_best(int(user_id))
        return bool(quiz_best)
    except Exception:
        # If the DB is unavailable or schema is missing, fail open
        # (treat as no progress) rather than breaking auth flows.
        return False


def _safe_next_url(next_url: str | None) -> str | None:
    """Return a safe relative next URL, or None.

    Prevents open redirects like "//evil.com" or "http://...".
    """
    if not next_url:
        return None
    next_url = str(next_url).strip()
    if not next_url.startswith("/"):
        return None
    if next_url.startswith("//"):
        return None
    return next_url


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
        session["edu_avatar"] = user.avatar_filename
        flash("Logged in.", "success")

        next_url = _safe_next_url(request.form.get("next") or request.args.get("next"))
        if next_url:
            return redirect(next_url)

        # Default post-login landing:
        # - Returning users with any progress: Dashboard
        # - First-time / no-progress users: Home (Training Hub)
        if _user_has_progress(user.id):
            return redirect(url_for("education.progress"))
        return redirect(url_for("education.learn_index"))

    return render_template("education/login.html")


@education_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        try:
            user = create_user(username=request.form.get("username", ""), password=request.form.get("password", ""))

            # Optional avatar upload.
            avatar_file = request.files.get("avatar")
            avatar_filename = _save_avatar_file(avatar_file, user_id=user.id)
            if avatar_filename:
                # Update db row and return updated user object.
                from modules.education_store import set_user_avatar

                user = set_user_avatar(user.id, avatar_filename)
        except ValueError as e:
            flash(str(e), "danger")
            return redirect(url_for("education.register"))

        session["edu_user_id"] = user.id
        session["edu_username"] = user.username
        session["edu_avatar"] = user.avatar_filename
        flash("Account created.", "success")

        # First login after registration should always land on the Training Hub.
        return redirect(url_for("education.learn_index"))

    return render_template("education/register.html")


@education_bp.route("/avatar", methods=["POST"])
@login_required(message="Please log in to update your profile picture.")
def update_avatar():
    user = _current_user()
    if not user:
        abort(401)

    avatar_file = request.files.get("avatar")
    avatar_filename = _save_avatar_file(avatar_file, user_id=user.id)
    if not avatar_filename:
        flash("Please choose a PNG/JPG/WEBP image to upload.", "warning")
        return redirect(url_for("education.learn_index", hub=1))

    # Best-effort cleanup of old avatar file.
    old = user.avatar_filename
    if old:
        try:
            static_folder = current_app.static_folder or "static"
            old_path = os.path.join(static_folder, "avatars", str(old))
            if os.path.isfile(old_path):
                os.remove(old_path)
        except OSError:
            pass

    from modules.education_store import set_user_avatar

    user = set_user_avatar(user.id, avatar_filename)
    session["edu_avatar"] = user.avatar_filename
    flash("Profile picture updated.", "success")
    return redirect(url_for("education.learn_index", hub=1))


@education_bp.route("/forgot-password", methods=["GET", "POST"])
def forgot_password():
    """Start password reset.

    For this demo app, we can optionally display the reset link directly after POST.
    In production, you would email the reset link instead.
    """
    reset_url = None
    if request.method == "POST":
        username = request.form.get("username", "")
        token = create_password_reset(username)

        # Avoid account enumeration: always show the same message.
        flash("If that account exists, a password reset link has been generated.", "info")

        show_link = bool(current_app.config.get("EDU_SHOW_RESET_LINK", current_app.debug))
        if token and show_link:
            reset_url = url_for("education.reset_password", token=token, _external=True)

    return render_template("education/forgot_password.html", reset_url=reset_url)


@education_bp.route("/reset-password/<token>", methods=["GET", "POST"])
def reset_password(token: str):
    if request.method == "POST":
        password = request.form.get("password", "")
        confirm = request.form.get("confirm_password", "")
        if not password or len(password) < 6:
            flash("Password must be at least 6 characters.", "danger")
            return redirect(url_for("education.reset_password", token=token))
        if password != confirm:
            flash("Passwords do not match.", "danger")
            return redirect(url_for("education.reset_password", token=token))

        user = consume_password_reset(token, password)
        if not user:
            flash("That reset link is invalid or expired. Please try again.", "warning")
            return redirect(url_for("education.forgot_password"))

        flash("Password updated. Please log in.", "success")
        return redirect(url_for("education.login"))

    return render_template("education/reset_password.html", token=token)


@education_bp.route("/logout")
def logout():
    # Capture before clearing session
    user_id = session.get("edu_user_id")
    username = session.get("edu_username")

    if user_id:
        record_event("logout", user_id=int(user_id), payload={"username": username})

    session.pop("edu_user_id", None)
    session.pop("edu_username", None)
    session.pop("edu_avatar", None)

    flash("Logged out.", "success")
    return redirect(url_for("education.login"))

# ============= PROGRESS & CERTIFICATES =============


@education_bp.route("/progress")
@login_required(message="Please log in to view your progress and certificates.")
def progress():
    user = _current_user()
    if not user:
        abort(401)

    # Used by the Home template to keep the Dashboard button hidden
    # until the user has actually navigated to the dashboard at least once.
    session["edu_seen_dashboard"] = True

    completed = get_completed_items(user.id)
    quiz_best = get_quiz_best(user.id)
    overall_pct = _overall_quiz_percentage(user.id)
    eligible = _is_certificate_eligible(user.id)
    unlock_state = _quiz_unlock_state(user.id)

    lesson_items = [
        {
            "key": item.key,
            "title": item.title,
            "url": url_for(item.endpoint),
        }
        for item in _LESSON_ITEMS
    ]

    lessons_completed_count = sum(1 for item in _LESSON_ITEMS if item.key in completed)
    quizzes_completed_count = len(unlock_state.get("completed") or [])

    # Always start/continue users at Module 1 (Fundamentals).
    continue_url = url_for("education.fundamentals")

    return render_template(
        "education/progress.html",
        user=user,
        lesson_items=lesson_items,
        completed=completed,
        quizzes=_QUIZZES,
        quiz_best=quiz_best,
        overall_pct=overall_pct,
        eligible=eligible,
        unlock_state=unlock_state,
        lessons_completed_count=lessons_completed_count,
        lessons_total=len(_LESSON_ITEMS),
        quizzes_completed_count=quizzes_completed_count,
        quizzes_total=len(_QUIZZES),
        continue_url=continue_url,
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


@education_bp.get("/certificate/demo")
def certificate_demo():
    """Public demo certificate page for styling/format review (no login required)."""
    return render_template("education/certificate_demo.html", **_demo_certificate_context())


@education_bp.get("/certificate/demo.pdf")
def certificate_demo_pdf():
    """Public demo PDF download for certificate styling review (no login required)."""
    ctx = _demo_certificate_context()
    username = str((ctx.get("user") or {}).get("username") or "Demo Reviewer")
    issued_date = str(ctx.get("issued_date") or "")
    certificate_id = str(ctx.get("certificate_id") or "")
    completed_lessons = ctx.get("completed_lessons") or []
    quiz_count = int(ctx.get("quiz_count") or 0)
    overall_pct = float(ctx.get("overall_pct") or 0.0)

    buf = BytesIO()
    c = canvas.Canvas(buf, pagesize=letter)
    width, height = letter

    margin = 0.75 * inch
    frame_color = (102 / 255, 126 / 255, 234 / 255)  # #667eea

    # Background
    c.setFillColorRGB(1, 1, 1)
    c.rect(0, 0, width, height, stroke=0, fill=1)

    # Frame
    c.setLineWidth(3)
    c.setStrokeColorRGB(*frame_color)
    c.roundRect(margin, margin, width - 2 * margin, height - 2 * margin, 12, stroke=1, fill=0)

    # Title
    c.setFillColorRGB(*frame_color)
    c.setFont("Helvetica-Bold", 26)
    c.drawCentredString(width / 2, height - 2.0 * inch, "Certificate of Completion")

    c.setFillColorRGB(0.25, 0.25, 0.25)
    c.setFont("Helvetica", 12)
    c.drawCentredString(width / 2, height - 2.45 * inch, "Lithium Battery Educational Platform")

    # Body
    c.setFont("Helvetica", 12)
    c.drawCentredString(width / 2, height - 3.30 * inch, "This certifies that")

    c.setFont("Helvetica-Bold", 22)
    c.setFillColorRGB(0.07, 0.09, 0.15)
    c.drawCentredString(width / 2, height - 3.85 * inch, username)

    c.setFont("Helvetica", 12)
    c.setFillColorRGB(0.25, 0.25, 0.25)
    c.drawCentredString(
        width / 2,
        height - 4.35 * inch,
        "has completed the required learning modules and assessments.",
    )

    # Left section: lessons
    c.setFillColorRGB(0.25, 0.25, 0.25)
    c.setFont("Helvetica", 10)
    y = height - 5.1 * inch
    c.drawString(margin + 12, y, "Completed lessons:")
    y -= 0.22 * inch
    c.setFont("Helvetica", 9)
    for item in list(completed_lessons)[:6]:
        title = str((item or {}).get("title") or "").strip()
        if not title:
            continue
        c.drawString(margin + 20, y, f"• {title}")
        y -= 0.18 * inch

    # Right section: stats
    stats_x = width - margin - 220
    stats_y = height - 5.1 * inch
    c.setFont("Helvetica", 10)
    c.drawString(stats_x, stats_y, "Quiz attempts recorded:")
    c.setFont("Helvetica-Bold", 12)
    c.drawString(stats_x, stats_y - 0.22 * inch, str(quiz_count))
    c.setFont("Helvetica", 10)
    c.drawString(stats_x, stats_y - 0.55 * inch, "Overall quiz score (avg):")
    c.setFont("Helvetica-Bold", 12)
    c.drawString(stats_x, stats_y - 0.77 * inch, f"{overall_pct:.0f}%")

    # Footer metadata
    c.setFillColorRGB(0.2, 0.2, 0.2)
    c.setFont("Helvetica", 10)
    c.drawString(margin + 12, margin + 26, f"Date: {issued_date}")
    c.drawRightString(width - margin - 12, margin + 26, f"Certificate ID: {certificate_id}")

    c.showPage()
    c.save()

    buf.seek(0)
    filename = "certificate_demo.pdf"
    return send_file(buf, mimetype="application/pdf", as_attachment=True, download_name=filename)


@education_bp.post("/certificate/demo/review")
def certificate_demo_review_submit():
    """Collect lightweight certificate styling/format feedback into a CSV."""
    def _to_rating(val: str) -> int | None:
        try:
            n = int(str(val).strip())
        except Exception:
            return None
        if 1 <= n <= 5:
            return n
        return None

    reviewer_name = (request.form.get("reviewer_name") or "").strip()
    rating_format = _to_rating(request.form.get("rating_format") or "")
    rating_typography = _to_rating(request.form.get("rating_typography") or "")
    rating_colors = _to_rating(request.form.get("rating_colors") or "")
    rating_overall = _to_rating(request.form.get("rating_overall") or "")
    comments = (request.form.get("comments") or "").strip()

    if not (rating_format and rating_typography and rating_colors and rating_overall):
        flash("Please rate all categories (1–5).", "warning")
        return redirect(url_for("education.certificate_demo") + "#review")

    out_dir = os.path.join(_project_root(), "data")
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "certificate_demo_reviews.csv")

    is_new = not os.path.exists(out_path)
    with open(out_path, "a", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        if is_new:
            w.writerow([
                "submitted_at",
                "reviewer_name",
                "rating_format",
                "rating_typography",
                "rating_colors",
                "rating_overall",
                "comments",
            ])
        w.writerow([
            datetime.now().isoformat(timespec="seconds"),
            reviewer_name,
            rating_format,
            rating_typography,
            rating_colors,
            rating_overall,
            comments,
        ])

    flash("Thanks — your feedback was recorded.", "success")
    return redirect(url_for("education.certificate_demo") + "#review")


@education_bp.get("/certificate/demo/reviews.csv")
def certificate_demo_reviews_csv():
    """Download collected demo poll results as CSV."""
    out_path = os.path.join(_project_root(), "data", "certificate_demo_reviews.csv")
    if not os.path.exists(out_path):
        flash("No reviews recorded yet.", "warning")
        return redirect(url_for("education.certificate_demo") + "#review")
    return send_file(out_path, mimetype="text/csv", as_attachment=True, download_name="certificate_demo_reviews.csv")


# ============= ADMIN: LIVE DB QUERIES =============


@education_bp.get("/admin/db")
def admin_db_live_page():
    _require_admin_token()
    token = request.args.get("token", "")
    return render_template("education/admin_db_live.html", token=token)


@education_bp.get("/admin/db/api/users")
def admin_db_users():
    _require_admin_token()
    limit = _int_param("limit", 50, min_value=1, max_value=500)
    with _connect_education_db() as conn:
        rows = conn.execute(
            "SELECT id, username, created_at, avatar_filename FROM users ORDER BY id DESC LIMIT ?",
            (limit,),
        ).fetchall()
    return jsonify({"rows": [dict(r) for r in rows]})


@education_bp.get("/admin/db/api/progress")
def admin_db_progress():
    _require_admin_token()
    user_id = _int_param("user_id", 0, min_value=0)
    limit = _int_param("limit", 200, min_value=1, max_value=2000)
    with _connect_education_db() as conn:
        if user_id:
            rows = conn.execute(
                """
                SELECT p.user_id, u.username, p.item_key, p.completed_at
                FROM progress p
                LEFT JOIN users u ON u.id = p.user_id
                WHERE p.user_id = ?
                ORDER BY p.completed_at DESC
                LIMIT ?
                """,
                (user_id, limit),
            ).fetchall()
        else:
            rows = conn.execute(
                """
                SELECT p.user_id, u.username, p.item_key, p.completed_at
                FROM progress p
                LEFT JOIN users u ON u.id = p.user_id
                ORDER BY p.completed_at DESC
                LIMIT ?
                """,
                (limit,),
            ).fetchall()
    return jsonify({"rows": [dict(r) for r in rows]})


@education_bp.get("/admin/db/api/quiz_attempts")
def admin_db_quiz_attempts():
    _require_admin_token()
    user_id = _int_param("user_id", 0, min_value=0)
    limit = _int_param("limit", 200, min_value=1, max_value=2000)
    with _connect_education_db() as conn:
        if user_id:
            rows = conn.execute(
                """
                SELECT q.user_id, u.username, q.quiz_id, q.best_score, q.total, q.completed_at
                FROM quiz_attempts q
                LEFT JOIN users u ON u.id = q.user_id
                WHERE q.user_id = ?
                ORDER BY q.completed_at DESC
                LIMIT ?
                """,
                (user_id, limit),
            ).fetchall()
        else:
            rows = conn.execute(
                """
                SELECT q.user_id, u.username, q.quiz_id, q.best_score, q.total, q.completed_at
                FROM quiz_attempts q
                LEFT JOIN users u ON u.id = q.user_id
                ORDER BY q.completed_at DESC
                LIMIT ?
                """,
                (limit,),
            ).fetchall()
    return jsonify({"rows": [dict(r) for r in rows]})


@education_bp.get("/admin/db/api/events")
def admin_db_events():
    _require_admin_token()
    since_id = _int_param("since", 0, min_value=0)
    limit = _int_param("limit", 200, min_value=1, max_value=2000)
    user_id = _int_param("user_id", 0, min_value=0)
    with _connect_education_db() as conn:
        if user_id:
            rows = conn.execute(
                """
                SELECT e.id, e.user_id, u.username, e.type, e.payload, e.created_at
                FROM user_events e
                LEFT JOIN users u ON u.id = e.user_id
                WHERE e.id > ? AND (e.user_id = ?)
                ORDER BY e.id ASC
                LIMIT ?
                """,
                (since_id, user_id, limit),
            ).fetchall()
        else:
            rows = conn.execute(
                """
                SELECT e.id, e.user_id, u.username, e.type, e.payload, e.created_at
                FROM user_events e
                LEFT JOIN users u ON u.id = e.user_id
                WHERE e.id > ?
                ORDER BY e.id ASC
                LIMIT ?
                """,
                (since_id, limit),
            ).fetchall()
    last_id = int(rows[-1]["id"]) if rows else since_id
    return jsonify({"rows": [dict(r) for r in rows], "last_id": last_id})


@education_bp.get("/admin/db/api/users_summary")
def admin_db_users_summary():
        """Per-user completion + score summary.

        Computes:
        - lessons_completed: count of `progress.item_key` like 'lesson:%'
        - quizzes_attempted: count of rows in `quiz_attempts`
        - overall_pct: avg(best_score/total)*100 across attempted quizzes
        """
        _require_admin_token()
        limit = _int_param("limit", 200, min_value=1, max_value=2000)

        with _connect_education_db() as conn:
                rows = conn.execute(
                        """
                        SELECT
                            u.id AS user_id,
                            u.username,
                            u.created_at,
                            COALESCE(p.lessons_completed, 0) AS lessons_completed,
                            COALESCE(q.quizzes_attempted, 0) AS quizzes_attempted,
                            ROUND(COALESCE(q.overall_pct, 0), 1) AS overall_pct,
                            COALESCE(a.last_activity, u.created_at) AS last_activity
                        FROM users u
                        LEFT JOIN (
                            SELECT user_id, COUNT(*) AS lessons_completed
                            FROM progress
                            WHERE item_key LIKE 'lesson:%'
                            GROUP BY user_id
                        ) p ON p.user_id = u.id
                        LEFT JOIN (
                            SELECT
                                user_id,
                                COUNT(*) AS quizzes_attempted,
                                AVG(CAST(best_score AS REAL) / NULLIF(total, 0)) * 100.0 AS overall_pct,
                                MAX(completed_at) AS last_quiz_at
                            FROM quiz_attempts
                            GROUP BY user_id
                        ) q ON q.user_id = u.id
                        LEFT JOIN (
                            SELECT
                                u2.id AS user_id,
                                MAX(
                                    COALESCE(q2.last_quiz_at, ''),
                                    COALESCE(p2.last_progress_at, ''),
                                    COALESCE(e2.last_event_at, ''),
                                    COALESCE(u2.created_at, '')
                                ) AS last_activity
                            FROM users u2
                            LEFT JOIN (
                                SELECT user_id, MAX(completed_at) AS last_progress_at
                                FROM progress
                                GROUP BY user_id
                            ) p2 ON p2.user_id = u2.id
                            LEFT JOIN (
                                SELECT user_id, MAX(completed_at) AS last_quiz_at
                                FROM quiz_attempts
                                GROUP BY user_id
                            ) q2 ON q2.user_id = u2.id
                            LEFT JOIN (
                                SELECT user_id, MAX(created_at) AS last_event_at
                                FROM user_events
                                GROUP BY user_id
                            ) e2 ON e2.user_id = u2.id
                            GROUP BY u2.id
                        ) a ON a.user_id = u.id
                        ORDER BY last_activity DESC
                        LIMIT ?
                        """,
                        (limit,),
                ).fetchall()

        return jsonify({"rows": [dict(r) for r in rows]})


@education_bp.get("/admin/db/api/latest_quiz")
def admin_db_latest_quiz():
        """Latest quiz attempt per user (based on quiz_attempts.completed_at).

        Note: `quiz_attempts` stores best attempt per quiz, not every attempt.
        """
        _require_admin_token()
        limit = _int_param("limit", 200, min_value=1, max_value=2000)

        with _connect_education_db() as conn:
                rows = conn.execute(
                        """
                        SELECT
                            u.id AS user_id,
                            u.username,
                            qa.quiz_id,
                            qa.best_score,
                            qa.total,
                            ROUND(CASE WHEN qa.total > 0 THEN (CAST(qa.best_score AS REAL) / qa.total) * 100.0 ELSE NULL END, 1) AS pct,
                            qa.completed_at
                        FROM users u
                        LEFT JOIN quiz_attempts qa
                            ON qa.user_id = u.id
                         AND qa.completed_at = (
                             SELECT MAX(completed_at) FROM quiz_attempts WHERE user_id = u.id
                         )
                        ORDER BY qa.completed_at DESC
                        LIMIT ?
                        """,
                        (limit,),
                ).fetchall()

        return jsonify({"rows": [dict(r) for r in rows]})


@education_bp.get("/admin/db/api/quiz_failures")
def admin_db_quiz_failures():
        """List quiz best-attempt records that are still below a pass threshold.

        Pass threshold default is 75%.
        """
        _require_admin_token()
        user_id = _int_param("user_id", 0, min_value=0)
        limit = _int_param("limit", 200, min_value=1, max_value=2000)
        pass_pct = _int_param("pass_pct", 75, min_value=1, max_value=100)

        with _connect_education_db() as conn:
                if user_id:
                        rows = conn.execute(
                                """
                                SELECT
                                    q.user_id,
                                    u.username,
                                    q.quiz_id,
                                    q.best_score,
                                    q.total,
                                    ROUND(CASE WHEN q.total > 0 THEN (CAST(q.best_score AS REAL) / q.total) * 100.0 ELSE NULL END, 1) AS pct,
                                    q.completed_at
                                FROM quiz_attempts q
                                LEFT JOIN users u ON u.id = q.user_id
                                WHERE q.user_id = ?
                                    AND (CASE WHEN q.total > 0 THEN (CAST(q.best_score AS REAL) / q.total) * 100.0 ELSE 0 END) < ?
                                ORDER BY q.completed_at DESC
                                LIMIT ?
                                """,
                                (user_id, pass_pct, limit),
                        ).fetchall()
                else:
                        rows = conn.execute(
                                """
                                SELECT
                                    q.user_id,
                                    u.username,
                                    q.quiz_id,
                                    q.best_score,
                                    q.total,
                                    ROUND(CASE WHEN q.total > 0 THEN (CAST(q.best_score AS REAL) / q.total) * 100.0 ELSE NULL END, 1) AS pct,
                                    q.completed_at
                                FROM quiz_attempts q
                                LEFT JOIN users u ON u.id = q.user_id
                                WHERE (CASE WHEN q.total > 0 THEN (CAST(q.best_score AS REAL) / q.total) * 100.0 ELSE 0 END) < ?
                                ORDER BY q.completed_at DESC
                                LIMIT ?
                                """,
                                (pass_pct, limit),
                        ).fetchall()

        return jsonify({"rows": [dict(r) for r in rows], "pass_pct": pass_pct})


# ============= FUNDAMENTAL CONCEPTS ROUTES =============

@education_bp.route('/fundamentals')
def fundamentals():
    """Main fundamentals page"""
    _track("lesson:fundamentals")
    content = LithiumBatteryFundamentals.MODULE_1_FUNDAMENTALS
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
    return render_template('education/calculators.html')


@education_bp.route('/learn', strict_slashes=False)
@education_bp.route('/learn/', strict_slashes=False)
def learn_index():
    """Training hub landing page.

    Home page for the education module.

    Shows welcome/intro content. Users can start with Fundamentals.
    """
    user_id = session.get("edu_user_id")
    force_hub = str(request.args.get("hub") or "").strip().lower() in {"1", "true", "yes", "y"}
    if user_id:
        if _user_has_progress(int(user_id)) and not force_hub:
            return redirect(url_for("education.progress"))
        _track("hub:learn-index")
    return render_template("education/learn_index.html")


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
    quizzes = [
        {'id': 'capacity-dod', 'title': 'Power vs Energy & Backup Sizing Quiz'},
        {'id': 'crate', 'title': 'AC vs DC & Conversion Quiz'},
        {'id': 'cell-health', 'title': 'Core System Components Quiz'},
        {'id': 'chemistry', 'title': 'How Lithium-Ion Works Quiz'},
        {'id': 'cycles-aging', 'title': 'Key Battery Concepts Quiz'},
        {'id': 'pack-design', 'title': 'System Types & Energy Flow Quiz'},
        {'id': 'bms-balancing', 'title': 'Efficiency, Losses & REVOV Fit Quiz'}
    ]
    return render_template('education/quiz_index.html', quizzes=quizzes)


@education_bp.route("/api/quiz/unlock-state")
@api_login_required
def api_quiz_unlock_state():
    user = _current_user()
    if not user:
        return jsonify({"error": "login_required"}), 401
    return jsonify(_quiz_unlock_state(user.id))


@education_bp.route('/api/quiz/capacity-dod')
@api_login_required
def api_quiz_capacity_dod():
    """API: Get capacity & DOD quiz"""
    user = _current_user()
    if not user:
        return jsonify({"error": "login_required"}), 401
    locked = _require_quiz_unlocked(user.id, "capacity-dod")
    if locked is not None:
        return locked
    questions = EducationalQuizzes.quiz_capacity_dod()
    resp = jsonify(_randomize_quiz_questions(questions))
    resp.headers["Cache-Control"] = "no-store"
    return resp


@education_bp.route('/api/quiz/crate')
@api_login_required
def api_quiz_crate():
    """API: Get C-rate quiz"""
    user = _current_user()
    if not user:
        return jsonify({"error": "login_required"}), 401
    locked = _require_quiz_unlocked(user.id, "crate")
    if locked is not None:
        return locked
    questions = EducationalQuizzes.quiz_crate()
    resp = jsonify(_randomize_quiz_questions(questions))
    resp.headers["Cache-Control"] = "no-store"
    return resp


@education_bp.route('/api/quiz/cell-health')
@api_login_required
def api_quiz_cell_health():
    """API: Get cell health quiz"""
    user = _current_user()
    if not user:
        return jsonify({"error": "login_required"}), 401
    locked = _require_quiz_unlocked(user.id, "cell-health")
    if locked is not None:
        return locked
    questions = EducationalQuizzes.quiz_cell_health()
    resp = jsonify(_randomize_quiz_questions(questions))
    resp.headers["Cache-Control"] = "no-store"
    return resp


@education_bp.route('/api/quiz/chemistry')
@api_login_required
def api_quiz_chemistry():
    """API: Get chemistry quiz"""
    user = _current_user()
    if not user:
        return jsonify({"error": "login_required"}), 401
    locked = _require_quiz_unlocked(user.id, "chemistry")
    if locked is not None:
        return locked
    questions = EducationalQuizzes.quiz_chemistry()
    resp = jsonify(_randomize_quiz_questions(questions))
    resp.headers["Cache-Control"] = "no-store"
    return resp


@education_bp.route('/api/quiz/cycles-aging')
@api_login_required
def api_quiz_cycles_aging():
    """API: Get cycles & aging quiz"""
    user = _current_user()
    if not user:
        return jsonify({"error": "login_required"}), 401
    locked = _require_quiz_unlocked(user.id, "cycles-aging")
    if locked is not None:
        return locked
    questions = EducationalQuizzes.quiz_cycles_aging()
    resp = jsonify(_randomize_quiz_questions(questions))
    resp.headers["Cache-Control"] = "no-store"
    return resp


@education_bp.route('/api/quiz/pack-design')
@api_login_required
def api_quiz_pack_design():
    """API: Get pack design quiz"""
    user = _current_user()
    if not user:
        return jsonify({"error": "login_required"}), 401
    locked = _require_quiz_unlocked(user.id, "pack-design")
    if locked is not None:
        return locked
    questions = EducationalQuizzes.quiz_pack_design()
    resp = jsonify(_randomize_quiz_questions(questions))
    resp.headers["Cache-Control"] = "no-store"
    return resp


@education_bp.route('/api/quiz/bms-balancing')
@api_login_required
def api_quiz_bms_balancing():
    """API: Get BMS & balancing quiz"""
    user = _current_user()
    if not user:
        return jsonify({"error": "login_required"}), 401
    locked = _require_quiz_unlocked(user.id, "bms-balancing")
    if locked is not None:
        return locked
    questions = EducationalQuizzes.quiz_bms_balancing()
    resp = jsonify(_randomize_quiz_questions(questions))
    resp.headers["Cache-Control"] = "no-store"
    return resp


# ============= REFERENCE PAGES =============

@education_bp.route('/reference/good-cell')
@login_required(message="Please log in to access reference materials.")
def reference_good_cell():
    """Reference: What makes a good cell"""
    return redirect(url_for("education.fundamentals"))


@education_bp.route('/reference/bad-cell')
@login_required(message="Please log in to access reference materials.")
def reference_bad_cell():
    """Reference: Signs of a bad cell"""
    return redirect(url_for("education.fundamentals"))


@education_bp.route('/reference/pack-issues')
@login_required(message="Please log in to access reference materials.")
def reference_pack_issues():
    """Reference: Cell imbalance in packs"""
    return redirect(url_for("education.fundamentals"))


@education_bp.route('/glossary')
@login_required(message="Please log in to access reference materials.")
def glossary():
    """Battery terminology glossary"""
    terms = {
        # Module 1 only — ordered to match the learning flow (1.2 → 1.12)

        # 1.2 Why Energy Storage Matters in South Africa
        "Loadshedding": "Planned power cuts used to balance demand on South Africa’s grid.",
        "Tariff": "The price structure for electricity; impacts when you charge from grid vs use PV/battery.",

        # 1.3 Power vs Energy
        "Power (kW)": "The rate at which electricity is used right now. Used to size the inverter.",
        "Energy (kWh)": "Total electricity stored/used over time. Used to size the battery bank.",
        "Voltage (V)": "Electrical pressure. Used to confirm system compatibility.",
        "Current (A)": "Flow of electrons. Used to size cables and protection.",

        # 1.4 How to Calculate Backup Requirements
        "Essential Loads": "Critical appliances kept running during outages; the basis for backup sizing.",
        "Surge Load": "Short-duration high power draw (e.g., motor start) that can affect inverter sizing.",
        "Backup Sizing": "Battery size (kWh) = essential load (kW) × outage duration (hours), then add margin (avoid 100% discharge).",

        # 1.5 AC vs DC
        "AC": "Alternating current (grid/house power; South Africa is typically 230 V, 50 Hz).",
        "DC": "Direct current (PV and battery power; flows in one direction).",
        "Inverter": "Converts DC→AC for loads and AC→DC for charging, and controls energy flow between PV, battery, and grid.",

        # 1.6 Core Components of a Modern Energy System
        "PV Array": "Solar panels that generate DC electricity from sunlight.",
        "Battery Bank": "Stores energy for backup and later use (REVOV uses LiFePO₄ lithium-ion chemistry).",
        "Load": "Devices/appliances that consume power.",
        "Grid": "Utility supply that can supplement loads and (in some systems) accept exported energy.",
        "Generator": "Supplemental/off-grid backup source used when PV/battery is insufficient.",
        "SANS 10142-1": "South African low-voltage wiring standard used for safe installation and compliance.",

        # 1.7 How Lithium-Ion Batteries Work
        "LiFePO₄": "Lithium Iron Phosphate; a lithium-ion chemistry known for safety, stability, high efficiency, and long cycle life.",
        "Anode": "The negative electrode in a lithium-ion cell (typically graphite). Stores lithium ions during charging.",
        "Cathode": "The positive electrode in a LiFePO₄ cell. Releases/receives lithium ions during charge/discharge.",
        "Electrolyte": "Conductive medium that allows lithium ions to move between anode and cathode.",
        "Separator": "Porous membrane that prevents short circuits while allowing ions to pass.",

        # 1.8 Key Battery Concepts Installers Must Know
        "Cycle": "One full process of charging and discharging. Cycle life is often quoted to ~80% remaining capacity.",
        "State of Charge (SOC)": "Battery “fuel gauge” (%). Example: 60% SOC on a 10 kWh battery ≈ 6 kWh remaining.",
        "Depth of Discharge (DoD)": "% of capacity used in a cycle. Example: using 8 kWh from 10 kWh = 80% DoD.",
        "Efficiency": "How much energy you get out versus put in; reduced by conversion and heat losses.",
        "Battery Management System (BMS)": "Electronics that monitor/protect cells (voltage/current/temp), balance the pack, and communicate with the inverter.",

        # 1.9 The Four Main System Types
        "Backup System": "Inverter + battery only (no solar). Charges from grid and powers essentials during outages.",
        "Grid-Tied Solar": "Solar + inverter only (no battery). Saves on bills but provides no backup during outages.",
        "Hybrid System": "Solar + battery + grid. Provides backup and savings by managing energy flow.",
        "Off-Grid System": "No grid connection; relies on PV + batteries (often generator) and must be sized correctly.",

        # 1.10 Energy Flow and System Operation
        "Self-Consumption": "Using your own PV energy on-site instead of exporting it.",
        "Export": "Sending excess solar energy back to the grid (requires correct settings and utility approval).",

        # 1.11 Efficiency and System Losses
        "System Losses": "The small % of energy lost as power moves through inverter, wiring/connectors, and battery processes.",
        "Voltage Drop": "Voltage lost along cables due to resistance; worsens with long runs or undersized conductors.",

        # 1.12 Where REVOV Fits
        "REVOV": "Lithium energy storage solutions using safe LiFePO₄ chemistry, strong BMS communication, high efficiency, and scalable configurations.",
    }
    return render_template('education/glossary.html', terms=terms)
