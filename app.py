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

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev'

# Store last result for PDF export
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


@app.route('/', methods=['GET', 'POST'])
def index():
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
            return redirect(url_for('index'))

    # GET
    return render_template('index.html')


@app.route('/export-pdf',methods = ['POST'])
def export_pdf():
     result_text = last_result['text']
     title = last_result['title']
     chemistry = last_result['chemistry']
     dod = last_result['dod']

     if not result_text.strip():
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
        return redirect(url_for('index'))
    future = job['future']
    if not future.done():
        flash('File still being generated. Try again in a moment.', 'warning')
        return redirect(url_for('pdf_status_page', job_id=job_id))
    path = job['path']
    if not os.path.exists(path):
        flash('Generated file missing', 'danger')
        return redirect(url_for('index'))
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
    app.run(debug=True)
