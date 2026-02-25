from flask import Flask, Response, render_template,abort, request,stream_with_context, redirect, url_for, flash, send_file, jsonify
import calculator
#import re
import json
import time
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
from routes.education_routes import education_bp
from modules import education_store


app = Flask(__name__)
# Never hard-code production secrets. On Render (and other hosts), set SECRET_KEY
# as an environment variable. Local dev can fall back to "dev".
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "dev")
# Ensure template changes reflect immediately during development, even when
# running via `flask run` (where the __main__ debug flag below is not used).
app.config.setdefault('TEMPLATES_AUTO_RELOAD', True)
app.jinja_env.auto_reload = True
# Reduce caching of static assets in dev so UI tweaks are visible.
app.config.setdefault('SEND_FILE_MAX_AGE_DEFAULT', 0)


@app.after_request
def _disable_client_caching_in_debug(response):
    if app.debug:
        response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
        response.headers["Pragma"] = "no-cache"
        response.headers["Expires"] = "0"
    return response
# Register the education blueprint only if explicitly enabled via env var.
# Keeps the app focused on the Battery Design calculator by default.
app.register_blueprint(education_bp)

# Store last result cache for PDF export
last_result = {'text': '', 'title': '', 'chemistry': 'LiFePO4', 'dod': '80'}

# Background PDF executor and job store
executor = ProcessPoolExecutor(max_workers=2)
pdf_jobs = {}  # job_id -> {'future': Future, 'path': str}


# Cleanup thread: remove temp PDF files older than X seconds
def cleanup_temp_files(interval_seconds=1800, max_age_seconds=3600):
    def _cleanup():
        while True:
            try:
                now = datetime.now().timestamp()
                for job_id, info in list(pdf_jobs.items()):
                    path = info.get('path')
                    # remove files older than max_age
                    if path and os.path.exists(path):
                        mtime = os.path.getmtime(path)
                        if now - mtime > max_age_seconds:
                            try:
                                os.remove(path)
                            except Exception:
                                pass
                            # also remove job entry
                            try:
                                del pdf_jobs[job_id]
                            except Exception:
                                pass
                # sleep
            except Exception:
                pass
            try:
                threading.Event().wait(interval_seconds)
            except Exception:
                break


# start cleanup thread as daemon
cleanup_thread = threading.Thread(target=cleanup_temp_files, args=(1800, 3600), daemon=True)
cleanup_thread.start()


def _require_admin_stream_token() -> None:
    expected = os.environ.get("ADMIN_STREAM_TOKEN", "")
    if not expected:
        abort(403, description="Set ADMIN_STREAM_TOKEN env var to enable admin event streaming")
    provided = request.headers.get("X-Admin-Token") or request.args.get("token", "")
    if provided != expected:
        abort(403)

@app.get("/admin/events")
def admin_events_page():
    _require_admin_stream_token()
    # Minimal inline page. (Keep token in query string or set header in your client.)
    token = request.args.get("token", "")
    html = f"""
    <!doctype html>
    <html>
      <head><meta charset="utf-8"><title>Live User Events</title></head>
      <body>
        <h3>Live User Events</h3>
        <pre id="log" style="white-space: pre-wrap;"></pre>
        <script>
          const log = document.getElementById("log");
          const es = new EventSource("/admin/events/stream?token={token}");
          es.addEventListener("user_event", (e) => {{
            log.textContent += e.data + "\\n";
          }});
          es.onerror = () => {{
            log.textContent += "[SSE disconnected]\\n";
          }};
        </script>
      </body>
    </html>
    """
    return Response(html, mimetype="text/html")

@app.get("/admin/events/recent")
def admin_events_recent():
    _require_admin_stream_token()
    since = int(request.args.get("since", "0"))
    limit = int(request.args.get("limit", "200"))
    events = education_store.get_events_since(since, limit=limit)
    return {"events": events, "last_id": (events[-1]["id"] if events else since)}

@app.get("/admin/events/stream")
def admin_events_stream():
    _require_admin_stream_token()

    @stream_with_context
    def gen():
        last_id = int(request.args.get("since", "0"))
        while True:
            events = education_store.get_events_since(last_id, limit=200)
            for ev in events:
                last_id = int(ev["id"])
                yield f"id: {last_id}\n"
                yield "event: user_event\n"
                yield f"data: {json.dumps(ev, ensure_ascii=False)}\n\n"
            time.sleep(0.5)

    resp = Response(gen(), mimetype="text/event-stream")
    resp.headers["Cache-Control"] = "no-cache"
    resp.headers["X-Accel-Buffering"] = "no"
    return resp


def build_pdf_to_file(result_text, title, chemistry, dod, out_path):
    """Builds the PDF using ReportLab and writes it to out_path (path string).
    This function is executed in a separate process so it must be self-contained.
    """
    try:
        # Strip HTML tags and convert <br> to newlines
        plain_text = result_text.replace('<br>', '\n')
        import re
        plain_text = re.sub('<[^<]+?>', '', plain_text)

        from reportlab.lib.pagesizes import letter
        from reportlab.lib.units import inch
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
        from reportlab.lib import colors
        from datetime import datetime

        doc = SimpleDocTemplate(
            out_path,
            pagesize=letter,
            rightMargin=0.75*inch,
            leftMargin=0.75*inch,
            topMargin=1*inch,
            bottomMargin=0.75*inch
        )

        story = []
        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#667eea'),
            spaceAfter=6,
            alignment=1
        )
        heading_style = ParagraphStyle(
            'CustomHeading',
            parent=styles['Heading2'],
            fontSize=14,
            textColor=colors.HexColor('#667eea'),
            spaceAfter=12,
            spaceBefore=6
        )
        normal_style = ParagraphStyle(
            'CustomNormal',
            parent=styles['Normal'],
            fontSize=11,
            textColor=colors.HexColor('#333333'),
            spaceAfter=6
        )
        cell_style = ParagraphStyle(
            'CellText',
            parent=styles['Normal'],
            fontSize=10,
            textColor=colors.HexColor('#333333')
        )

        story.append(Paragraph("Battery Design Report", title_style))
        story.append(Spacer(1, 0.3*inch))

        metadata = f"<b>Generated:</b> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}<br/>"
        metadata += f"<b>Report Type:</b> {title}<br/>"
        metadata += f"<b>Chemistry:</b> {chemistry}<br/>"
        metadata += f"<b>DOD:</b> {dod}%"
        story.append(Paragraph(metadata, normal_style))
        story.append(Spacer(1, 0.2*inch))

        story.append(Paragraph("_" * 80, normal_style))
        story.append(Spacer(1, 0.1*inch))

        story.append(Paragraph("Configuration Details", heading_style))

        lines = [line.strip() for line in plain_text.split('\n') if line.strip() and ':' in line]
        table_data = [["Parameter", "Value"]]
        for line in lines:
            if ':' in line:
                parts = line.split(':', 1)
                param = parts[0].strip()
                value = parts[1].strip()
                table_data.append([
                    Paragraph(param, cell_style),
                    Paragraph(value, cell_style)
                ])

        if len(table_data) > 1:
            table = Table(table_data, colWidths=[2.2*inch, 4.3*inch])
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#667eea')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 12),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#f9f9f9')),
                ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#ddd')),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f5f5f5')]),
                ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 1), (-1, -1), 10),
                ('TOPPADDING', (0, 1), (-1, -1), 8),
                ('BOTTOMPADDING', (0, 1), (-1, -1), 8),
                ('LEFTPADDING', (0, 1), (-1, -1), 6),
                ('RIGHTPADDING', (0, 1), (-1, -1), 6),
            ]))
            story.append(table)

        doc.build(story)
        return out_path
    except Exception:
        # ensure any partial file is removed on error
        try:
            if os.path.exists(out_path):
                os.remove(out_path)
        except Exception:
            pass
        raise


@app.route('/', methods=['GET'])
def index():
    """App landing page.

    Redirect away from the calculator UI so it is not the default homepage.
    """
    return redirect(url_for('education.login'))


@app.route('/calculator', methods=['GET', 'POST'])
def calculator_page():
    """Battery design calculator UI."""
    if request.method == 'POST':
        form_type = request.form.get('form_type')
        try:
            if form_type == 'pack':
                cell_voltage = float(request.form.get('cell_voltage') or 0)
                cell_capacity = float(request.form.get('cell_capacity') or 0)
                num_cells = int(request.form.get('num_cells') or 0)
                connection_type = request.form.get('connection_type')
                series_cells = request.form.get('series_cells') or None
                parallel_cells = request.form.get('parallel_cells') or None
                c_rate = float(request.form.get('c_rate') or 5)
                cell_ir = float(request.form.get('cell_ir') or 0)
                chemistry = request.form.get('chemistry') or 'LiFePO4'
                dod = int(request.form.get('dod') or 80)

                res = calculator.compute_pack_design(
                    cell_voltage=cell_voltage,
                    cell_capacity=cell_capacity,
                    num_cells=num_cells,
                    connection_type=connection_type,
                    series_cells=series_cells,
                    parallel_cells=parallel_cells,
                    c_rate=c_rate,
                    cell_ir_milli=cell_ir,
                    chemistry=chemistry,
                    dod=dod
                )

                # Store for PDF export
                last_result['text'] = res['summary_text']
                last_result['title'] = 'Pack Design Result'
                last_result['chemistry'] = chemistry
                last_result['dod'] = str(dod)

                return render_template('result.html', title='Pack Design Result', result=res)

            elif form_type == 'bank':
                energy = float(request.form.get('energy') or 0)
                module_capacity = float(request.form.get('module_capacity') or 1)
                chemistry = request.form.get('bank_chemistry') or 'LiFePO4'
                dod = int(request.form.get('bank_dod') or 100)

                res = calculator.compute_bank_design(energy, module_capacity, chemistry, dod)

                # Store for PDF export
                last_result['text'] = res['summary_text']
                last_result['title'] = 'Bank Design Result'
                last_result['chemistry'] = chemistry
                last_result['dod'] = str(dod)

                return render_template('result.html', title='Bank Design Result', result=res)

        except Exception as e:
            flash(f'Error: {e}', 'danger')
            return redirect(url_for('calculator_page'))

    # GET
    return render_template('index.html')


@app.route('/export-pdf',methods = ['POST'])
def export_pdf():
    # Allow the client to POST the result text (works across multiple workers)
    # Accept form fields or JSON: 'result_text', 'title', 'chemistry', 'dod'
    req_json = request.get_json(silent=True)
    result_text = request.form.get('result_text') or (req_json and req_json.get('result_text')) or last_result.get('text', '')
    title = request.form.get('title') or (req_json and req_json.get('title')) or last_result.get('title', 'Report')
    chemistry = request.form.get('chemistry') or (req_json and req_json.get('chemistry')) or last_result.get('chemistry', 'LiFePO4')
    dod = request.form.get('dod') or (req_json and req_json.get('dod')) or last_result.get('dod', '80')

    if not str(result_text).strip():
        return jsonify({"error": "No result to export"}), 400

    tmp = tempfile.NamedTemporaryFile(prefix='battery_pdf_', suffix='.pdf', delete=False)
    tmp_path = tmp.name
    tmp.close()

    job_id = str(uuid.uuid4())
    future = executor.submit(build_pdf_to_file, result_text, title, chemistry, dod, tmp_path)
    pdf_jobs[job_id] = {'future': future, 'path': tmp_path}

    return jsonify({"job_id": job_id})


@app.route('/pdf-status/<job_id>')
def pdf_status_page(job_id):
    job = pdf_jobs.get(job_id)
    if not job:
        return render_template('pdf_status.html', job_id=job_id, status='not_found')
    future = job['future']
    if future.done():
        if future.exception():                
           return render_template('pdf_status.html', job_id=job_id, status='error', message=str(future.exception()))
        return render_template('pdf_status.html', job_id=job_id, status='ready', url=url_for('download_pdf', job_id=job_id))
    else:
        return render_template('pdf_status.html', job_id=job_id, status='working')


@app.route('/pdf-status-api/<job_id>')
def pdf_status_api(job_id):
    """Return JSON status for a PDF job. Used by client-side polling."""
    job = pdf_jobs.get(job_id)
    if not job:
        return jsonify({'status': 'not_found'}), 404
    future = job['future']
    if future.done():
        if future.exception():
            return jsonify({'status': 'error', 'message': str(future.exception())})
        return jsonify({'status': 'ready', 'download_url': url_for('download_pdf', job_id=job_id, _external=True)})
    else:
        return jsonify({'status': 'working'})


@app.route('/download/<job_id>')
def download_pdf(job_id):
    job = pdf_jobs.get(job_id)
    if not job:
        flash('File not found', 'danger')
        return redirect(url_for('calculator_page'))
    future = job['future']
    if not future.done():
        flash('File still being generated. Try again in a moment.', 'warning')
        return redirect(url_for('pdf_status_page', job_id=job_id))
    path = job['path']
    if not os.path.exists(path):
        flash('Generated file missing', 'danger')
        return redirect(url_for('calculator_page'))
    # send file and optionally remove after sending
    return send_file(path, mimetype='application/pdf', as_attachment=True, download_name=os.path.basename(path))


@app.route('/pdf-status-json/<job_id>')
def pdf_status_json(job_id):
    """Return JSON status for a PDF job so clients can poll asynchronously."""
    job = pdf_jobs.get(job_id)
    if not job:
        return jsonify({'status': 'not_found'}), 404
    future = job['future']
    if future.done():
        # return external download URL
        download_url = url_for('download_pdf', job_id=job_id, _external=True)
        return jsonify({'status': 'ready', 'download_url': download_url})
    else:
        return jsonify({'status': 'working'})
if __name__ == '__main__':
    # Tidy startup: allow controlling debug with env var, avoid double browser
    # opens from the reloader, and reduce werkzeug log noise.
    import webbrowser
    import logging

    host = os.environ.get('FLASK_RUN_HOST', '127.0.0.1')
    port = int(os.environ.get('FLASK_RUN_PORT', 5000))
    debug = os.environ.get('FLASK_DEBUG', '1') == '1'

    # Reduce noisy request logs during development if desired
    logging.getLogger('werkzeug').setLevel(logging.WARNING)
    app.logger.setLevel(logging.INFO)

    def _mask_email(addr: str) -> str:
        addr = (addr or "").strip()
        if not addr or "@" not in addr:
            return ""
        local, domain = addr.split("@", 1)
        if len(local) <= 2:
            return f"{local[0:1]}***@{domain}"
        return f"{local[0:2]}***@{domain}"

    def _log_smtp_status() -> None:
        smtp_user = (os.environ.get("SMTP_USERNAME") or "").strip()
        smtp_pass = "".join((os.environ.get("SMTP_PASSWORD") or "").split())
        smtp_from = (os.environ.get("SMTP_FROM") or "").strip() or smtp_user
        smtp_host = (os.environ.get("SMTP_HOST") or "smtp.gmail.com").strip() or "smtp.gmail.com"
        smtp_port = (os.environ.get("SMTP_PORT") or "587").strip() or "587"
        enabled = bool(smtp_user and smtp_pass)
        app.logger.info(
            "SMTP enabled=%s host=%s port=%s user=%s from=%s",
            enabled,
            smtp_host,
            smtp_port,
            _mask_email(smtp_user),
            _mask_email(smtp_from),
        )

    url = f'http://{host}:{port}/'

    # Only open a browser once: when not running under the reloader parent.
    # When debug=True Flask uses the reloader which runs the script twice; the
    # reloader child sets WERKZEUG_RUN_MAIN='true'. Open browser in the child
    # (or when debug is False).
    if (not debug) or (os.environ.get('WERKZEUG_RUN_MAIN') == 'true'):
        _log_smtp_status()
        try:
            webbrowser.open(url)
        except Exception:
            pass

    # Use the debug flag from env and let Flask control the reloader.
    app.run(debug=debug, host=host, port=port)
