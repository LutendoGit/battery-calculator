from flask import Flask, render_template, request, redirect, url_for, flash, send_file
import calculator
import re
from io import BytesIO
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


@app.route('/export-pdf')
def export_pdf():
    """Generate and download PDF report"""
    try:
        result_text = last_result['text']
        title = last_result['title']
        chemistry = last_result['chemistry']
        dod = last_result['dod']
        
        if not result_text.strip():
            flash('No result to export. Please calculate first.', 'danger')
            return redirect(url_for('index'))
        
        # Strip HTML tags and convert <br> to newlines
        plain_text = result_text.replace('<br>', '\n')
        plain_text = re.sub('<[^<]+?>', '', plain_text)
        
        # Create PDF in memory
        pdf_buffer = BytesIO()
        
        doc = SimpleDocTemplate(
            pdf_buffer,
            pagesize=letter,
            rightMargin=0.75*inch,
            leftMargin=0.75*inch,
            topMargin=1*inch,
            bottomMargin=0.75*inch
        )
        
        story = []
        
        # Define styles
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
        
        # Add title
        story.append(Paragraph("Battery Design Report", title_style))
        story.append(Spacer(1, 0.3*inch))
        
        # Add metadata
        metadata = f"<b>Generated:</b> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}<br/>"
        metadata += f"<b>Report Type:</b> {title}<br/>"
        metadata += f"<b>Chemistry:</b> {chemistry}<br/>"
        metadata += f"<b>DOD:</b> {dod}%"
        story.append(Paragraph(metadata, normal_style))
        story.append(Spacer(1, 0.2*inch))
        
        story.append(Paragraph("_" * 80, normal_style))
        story.append(Spacer(1, 0.1*inch))
        
        story.append(Paragraph("Configuration Details", heading_style))
        
        # Extract key-value pairs
        lines = [line.strip() for line in plain_text.split('\n') if line.strip() and ':' in line]
        
        # Create table data
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
        
        # Build PDF
        doc.build(story)
        
        # Prepare response
        pdf_buffer.seek(0)
        return send_file(
            pdf_buffer,
            mimetype='application/pdf',
            as_attachment=True,
            download_name=f'battery-design-{datetime.now().strftime("%Y%m%d_%H%M%S")}.pdf'
        )
    
    except Exception as e:
        flash(f'Error generating PDF: {e}', 'danger')
        return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
