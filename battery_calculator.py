from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QLineEdit, QComboBox, QPushButton, QMessageBox, QFileDialog,QComboBox,QTabWidget
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QPainter, QPen,QIcon
import sys
import re
import os 
import matplotlib.pyplot as plt

icon_path = os.path.join(os.path.dirname(__file__), "Unleashing-Solar-Power-Illuminate-Your-Life-with-Solar-Panels-in-Poquoson-700x441.png")


# -------chemistry cycle and DOD for Energy bank design tab__
class cycleLifeEstimator():
    def __init__(self):
        self.base_cycle_life = {
            "Li-ion": 500,
            "LiFePO4": 2000,
            "Lead Acid": 300,
            "NiMH": 500
        }
        self.dod_multiplier = {
            100: 1.0,
            80: 1.2,
            60: 1.5,
            40: 2.0,
            20: 3.0
        }
    def estimate(self, chemistry: str, dod: int) -> int:
        base = self.base_cycle_life.get(chemistry, 500)
        multiplier = self.dod_multiplier.get(dod, 1.0)
        return int(base * multiplier)    


# --------- Main Application Class ----------
class BatteryCalculator(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Battery Design Calculator")
        self.setWindowIcon(QIcon(icon_path))
        self.setGeometry(200, 200, 520, 700)
        self.background_image = icon_path

       

        central = QWidget()
        self.setCentralWidget(central)
        
         # creating tabs
        self.tabs = QTabWidget()
        layout = QVBoxLayout(central)
        layout.addWidget(self.tabs)

        # Tab 1: Battery Design
        self.tab1 = QWidget()
        tab_layout1 = QVBoxLayout(self.tab1)
        self.tabs.addTab(self.tab1,"Battery design")

        # bank design calculator
        self.tab2 = QWidget()
        self.tabs.addTab(self.tab2,"Bank design")

        self.tabs.setStyleSheet("""
                                QTabWidget::pane {border:0px solid #ccc;}
                                QTabBar::tab{background:#eee;padding:8px;}
                                QTabBar::tab:selected{ background:#ddd;font-weight:bold;}

        """)
        self.tabs.currentChanged.connect(self.on_tab_switch)

        # Cell voltage
        hlayout1 = QHBoxLayout()
        self.cell_label = QLabel("Cell Voltage (V):")
        self.cell_label.setToolTip("Nominal voltage of a single cell")
        self.cell_label.setStyleSheet("background:Transparent;color:purple;font-weight:bold;font-size:12px;")
        self.cell_voltage_input = QLineEdit()
        self.cell_voltage_input.setPlaceholderText("e.g. 3.2V for LiFePO4")
        self.cell_voltage_input.setToolTip("Nominal voltage of a single cell")
        self.cell_voltage_input.setStyleSheet("background:Transparent;")
        hlayout1.addWidget(self.cell_label)
        hlayout1.addWidget(self.cell_voltage_input)
        tab_layout1.addLayout(hlayout1)
        # Cell capacity
        hlayout2 = QHBoxLayout()
        self.cell_capacity_label = QLabel("Cell Capacity (Ah):")
        self.cell_capacity_label.setToolTip("Nominal capacity of a single cell")
        self.cell_capacity_label.setStyleSheet("background:Transparent;color:purple;font-weight:bold;font-size:12px;")
        hlayout2.addWidget(self.cell_capacity_label)
        self.cell_capacity_input = QLineEdit()
        self.cell_capacity_input.setPlaceholderText("e.g. 100Ah")
        self.cell_capacity_input.setToolTip("Nominal capacity of a single cell")
        self.cell_capacity_input.setStyleSheet("background:Transparent;")
        hlayout2.addWidget(self.cell_capacity_input)
        tab_layout1.addLayout(hlayout2)

        # Number of cells
        hlayout3 = QHBoxLayout()
        self.num_cells_label = QLabel("Total Number of Cells:")
        self.num_cells_label.setToolTip("Total number of cells in the pack")
        self.num_cells_label.setStyleSheet("background:Transparent;color:purple;font-weight:bold;font-size:12px;")
        hlayout3.addWidget(self.num_cells_label)
        self.num_cells_input = QLineEdit()
        self.num_cells_input.setPlaceholderText("e.g. 4cells for 12.8V pack")
        self.num_cells_input.setToolTip("Total number of cells in the pack")
        self.num_cells_input.setStyleSheet("background:Transparent;")   
        hlayout3.addWidget(self.num_cells_input)
        tab_layout1.addLayout(hlayout3)

        # Connection type
        hlayout4 = QHBoxLayout()
        self.connection_type_label = QLabel("Connection Type:")
        self.connection_type_label.setToolTip("Select how cells are connected")
        self.connection_type_label.setStyleSheet("background:Transparent;color:purple;font-weight:bold;font-size:12px;")
        self.connection_type = QComboBox()
        self.connection_type.addItems(["Series", "Parallel", "Series-Parallel"])
        self.connection_type.setToolTip("Select how cells are connected")
        self.connection_type.setStyleSheet("background:Transparent;")
        self.connection_type.currentTextChanged.connect(self.toggle_series_parallel_inputs)
        self.connection_type.setFixedWidth(130)
        hlayout4.addWidget(self.connection_type_label)
        hlayout4.addWidget(self.connection_type)
        tab_layout1.addLayout(hlayout4)

        # Series/Parallel inputs for series-parallel
        self.series_cells_input = QLineEdit()
        self.parallel_cells_input = QLineEdit()
        self.series_cells_input.setPlaceholderText("Cells in Series")
        self.parallel_cells_input.setPlaceholderText("Cells in Parallel")
        self.series_cells_input.hide()
        self.parallel_cells_input.hide()
        tab_layout1.addWidget(self.series_cells_input)
        tab_layout1.addWidget(self.parallel_cells_input)

        # Chemistry selection
        hlayout5 = QHBoxLayout()
        self.chemistry_label = QLabel("Chemistry:")
        self.chemistry_label.setToolTip("Select battery chemistry for cycle life estimation")
        self.chemistry_label.setStyleSheet("background:Transparent;color:purple;font-weight:bold;font-size:12px;")
        self.chemistry_box = QComboBox()
        self.chemistry_box.setToolTip("Select battery chemistry for cycle life estimation")
        self.chemistry_box.addItems(["Li-ion", "LiFePO4", "Lead Acid", "NiMH"])
        self.chemistry_box.setCurrentText("LiFePO4")  # Default to LiFePO4
        self.chemistry_box.setStyleSheet("background:Transparent;")
        self.chemistry_box.setFixedWidth(130)
        hlayout5.addWidget(self.chemistry_label)
        hlayout5.addWidget(self.chemistry_box)
        tab_layout1.addLayout(hlayout5)

        # C-rate
        hlayout_crate = QHBoxLayout()
        self.crate_label = QLabel("C-rate for Max Power:")
        self.crate_label.setToolTip("C-rate to estimate max power and voltage sag (default 5C if empty)")
        self.crate_label.setStyleSheet("background:Transparent;color:purple;font-weight:bold;font-size:12px;")
        self.c_rate_input = QLineEdit()
        self.c_rate_input.setToolTip("C-rate to estimate max power and voltage sag (default 5C if empty)")
        self.c_rate_input.setStyleSheet("background:Transparent;")
        self.c_rate_input.setPlaceholderText("e.g. 5 for 5C")
        hlayout_crate.addWidget(self.crate_label)
        hlayout_crate.addWidget(self.c_rate_input)
        tab_layout1.addLayout(hlayout_crate)

        

        # Internal resistance (mΩ)
        hlayout7 = QHBoxLayout()
        self.cell_ir_label = QLabel("Cell Internal Resistance (mΩ):")
        self.cell_ir_label.setToolTip("Internal resistance of a single cell in milliohms")
        self.cell_ir_label.setStyleSheet("background:Transparent;color:purple;font-weight:bold;font-size:12px;")
        self.cell_ir_input = QLineEdit()
        self.cell_ir_input.setPlaceholderText("e.g. 50mΩ")
        self.cell_ir_input.setToolTip("Internal resistance of a single cell in milliohms")
        self.cell_ir_input.setStyleSheet("background:Transparent;")
        hlayout7.addWidget(self.cell_ir_label)
        hlayout7.addWidget(self.cell_ir_input)
        tab_layout1.addLayout(hlayout7)

        

        # DOD Dropdown
        hlayout_dod = QHBoxLayout()
        self.dod_label = QLabel("Depth of Discharge (DOD):")
        self.dod_label.setToolTip("Select Depth of Discharge for cycle life estimation")
        self.dod_label.setStyleSheet("background:Transparent;color:purple;font-weight:bold;font-size:12px;")
        self.dod_combo = QComboBox()
        self.dod_combo.setToolTip("Select Depth of Discharge for cycle life estimation")
        self.dod_combo.setStyleSheet("background:Transparent;")
        self.dod_combo.setFixedWidth(130)
        self.dod_combo.addItems(["100%", "80%", "60%", "40%", "20%"])
        self.dod_combo.setCurrentText("80%")  # Default to 80%
        hlayout_dod.addWidget(self.dod_label)
        hlayout_dod.addWidget(self.dod_combo)
        tab_layout1.addLayout(hlayout_dod)


        # Calculate button
        self.calc_btn = QPushButton("Calculate")
        self.calc_btn.setFixedWidth(120)
        self.calc_btn.setStyleSheet("background-color:orange;color:white;")
        self.calc_btn.clicked.connect(self.calculate_battery)
        tab_layout1.addWidget(self.calc_btn, alignment=Qt.AlignLeft)

        # Result label
        self.result_label = QLabel("")
        self.result_label.setStyleSheet("background:Transparent;color:black;font-weight:bold;font-size:12px;border:1px solid purple;padding:5px;")
        #self.result_label.setWordWrap(True)
        self.result_label.setTextFormat(Qt.RichText)
        tab_layout1.addWidget(self.result_label)
        self.result_label.hide() # ensure the label is hidden initially
        """# --------- Diagram Section ----------
        self.diagram_widget = PackDiagramWidget()
        self.diagram_widget.setMinimumHeight(120)
        layout.addWidget(self.diagram_widget)

        # Save diagram button
        self.save_diagram_btn = QPushButton("Save Pack Diagram")
        self.save_diagram_btn.clicked.connect(self.save_diagram)
        layout.addWidget(self.save_diagram_btn)"""

        # --------- Export Section ----------
        self.export_button = QPushButton("Export data")
        self.export_button.clicked.connect(self.export_results)
        tab_layout1.addWidget(self.export_button, alignment=Qt.AlignRight)

        self.pdf_export_button = QPushButton("Export PDF file")
        self.pdf_export_button.clicked.connect(self.export_pdf)
        self.pdf_export_button.setStyleSheet("background-color:blue;color:white;")
        tab_layout1.addWidget(self.pdf_export_button, alignment=Qt.AlignRight)

        self.csv_export_button = QPushButton("Export CSV file")
        self.csv_export_button.clicked.connect(self.export_csv)
        self.csv_export_button.setStyleSheet("background-color:purple;color:white;")
        tab_layout1.addWidget(self.csv_export_button, alignment=Qt.AlignRight)

        self.xlsx_export_button = QPushButton("Export Excel file")
        self.xlsx_export_button.clicked.connect(self.export_xlsx)
        tab_layout1.addWidget(self.xlsx_export_button, alignment=Qt.AlignRight)


        # Lookup cell button (demo)
        self.cell_lookup_button = QPushButton("Lookup Cell Example")
        self.cell_lookup_button.setToolTip("Demo: Fill fields for a common 18650 Li-ion cell")
        self.cell_lookup_button.setStyleSheet("background-color:green;color:purple;font-weight:bold;font-size:14px;")
        self.cell_lookup_button.clicked.connect(self.lookup_cell)
        tab_layout1.addWidget(self.cell_lookup_button, alignment=Qt.AlignLeft)

    #-----energy bank design tab layouts-----#
        tab_layout2 = QVBoxLayout(self.tab2)

    #----Energy bank design inputs------#

    # Energy input
        h_layout_b1 = QHBoxLayout()
        self.energy_label= QLabel("Target Energy in (kWh):")
        self.energy_label.setToolTip("Total energy capacity of the battery bank")
        self.energy_label.setStyleSheet("background:Transparent;color:purple;font-weight:bold;font-size:12px;")
        self.energy_input = QLineEdit()
        self.energy_input.setPlaceholderText("e.g. 20kWh")
        self.energy_input.setToolTip("Total energy capacity of the battery bank")
        self.energy_input.setStyleSheet("background:Transparent;")
        h_layout_b1.addWidget(self.energy_label)
        h_layout_b1.addWidget(self.energy_input)
        tab_layout2.addLayout(h_layout_b1)

    # Capacity input
        h_layout_b2 = QHBoxLayout()
        self.capacity_label= QLabel("Module Capacity in (KWH):")
        self.capacity_label.setToolTip("Capacity of a single battery module")
        self.capacity_label.setStyleSheet("background:Transparent;color:purple;font-weight:bold;font-size:12px;")
        self.capacity_input = QLineEdit()
        self.capacity_input.setPlaceholderText("e.g. 5kWh")
        self.capacity_input.setToolTip("Capacity of a single battery module")
        self.capacity_input.setStyleSheet("background:Transparent;")
        h_layout_b2.addWidget(self.capacity_label)
        h_layout_b2.addWidget(self.capacity_input)
        tab_layout2.addLayout(h_layout_b2)

        # Chemistry selection dropbox
        h_layout_chem = QHBoxLayout()
        self.chemistry_label = QLabel("Battery Chemistry")
        self.chemistry_label.setToolTip("select the chemistry type for your modules")
        self.chemistry_label.setStyleSheet("background:Transparent;color:purple;font-weight:bold;font-size:12px;")
        self.chemistry_box = QComboBox()
        self.chemistry_box.addItems(["LiFePO4", "Li-ion", "Lead Acid", "NiMH"])
        self.chemistry_box.setCurrentText("LiFePO4")  # default Chemistry
        self.chemistry_box.setToolTip("select the chemistry type for life cycle estimations")
        h_layout_chem.addWidget(self.chemistry_label)
        h_layout_chem.addWidget(self.chemistry_box)
        tab_layout2.addLayout(h_layout_chem)

        # DOD dropbox
        hlayout_dod = QHBoxLayout()
        self.dod_label = QLabel("Depth of Discharge (DOD %):")
        self.dod_box = QComboBox()
        self.dod_box.addItems(["100", "80", "60", "40", "20"])
        self.dod_box.setCurrentText("100")
        hlayout_dod.addWidget(self.dod_label)
        hlayout_dod.addWidget(self.dod_box)
        tab_layout2.addLayout(hlayout_dod)

        # Calculate button
        self.calculate_button = QPushButton("Calculate")
        self.calculate_button.setFixedWidth(120)
        self.calculate_button.setStyleSheet("background-color:orange;color:white;")
        self.calculate_button.clicked.connect(self.calculate)
        self.result_label2 = QLabel("")
        tab_layout2.addWidget(self.calculate_button, alignment=Qt.AlignLeft)
        tab_layout2.addWidget(self.result_label2)

        # cycle Life label
        self.cycle_life_label = QLabel("")
        self.cycle_life_label.setStyleSheet("color: navy; font-weight: bold;")
        self.cycle_life_label.setToolTip("Estimated cycle life based on chemistry and depth of discharge")
        tab_layout2.addWidget(self.cycle_life_label)

        # export button
        self.export_button = QPushButton("Export Result")
        self.export_button.setToolTip("Save the module calculation result to a text file")
        self.export_button.clicked.connect(self.export_result)
        self.export_button.setStyleSheet("background-color:green;color:white;")
        self.export_button.setFixedWidth(100)
        tab_layout2.addWidget(self.export_button)

        # chart button
        self.chart_button = QPushButton("Show Chart")
        self.chart_button.setToolTip("Visualize how module count scales with energy")
        self.chart_button.setStyleSheet("background-color:purple;color:white;")
        self.chart_button.clicked.connect(self.show_chart)
        self.chart_button.setFixedWidth(100)
        tab_layout2.addWidget(self.chart_button)

    # export section
    def export_result(self):
        try:
            result_text = self.result_label2.text()
            chem = self.chemistry_box.currentText()
            with open("bank_design_result.txt", "w") as f:
                f.write(f"Chemistry: {chem}\n")
                f.write(f"{result_text}\n")
            QMessageBox.information(self, "Success", "Result exported to bank_design_result.txt")
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Export failed: {str(e)}")

    # ----calculates function----
    def calculate(self):
        try:
            energy = float(self.energy_input.text())
            module_capacity = float(self.capacity_input.text())
            modules_needed = int((energy + module_capacity -1)//module_capacity)

            # Estimate cycle life
            chem = self.chemistry_box.currentText()
            dod = int(self.dod_box.currentText())
            estimator = cycleLifeEstimator()
            cycle_life = estimator.estimate(chem,dod)

            self.result_label2.setText(f"you need {modules_needed} modules in parallel ")
            self.cycle_life_label.setText(f"Estimated Cycle Life: {cycle_life} cycles")
        except ValueError:
            self.result_label2.setText("Please enter valid numeric values.")
            self.cycle_life_label.setText("")

    # chart function
    def show_chart(self):
        try:
            module_capacity = float(self.capacity_input.text())
            energies = list(range(5, 105, 5))  # 5 to 100 kWh
            modules = [int((e + module_capacity - 1) // module_capacity) for e in energies]

            plt.figure(figsize=(6, 4))
            plt.plot(energies, modules, marker='o', color='blue')
            plt.title("Modules Needed vs Energy Requirement")
            plt.xlabel("Energy Requirement (kWh)")
            plt.ylabel("Modules Needed")
            plt.grid(True)
            plt.tight_layout()
            plt.show()
        except ValueError:
            QMessageBox.warning(self, "Error", "Please enter a valid module capacity.")

#-----end of bank design layout(tab2)----------#
    # printing the index of the selected tab
    def on_tab_switch(self,index):
        print(f"Switched to tab{index}")

    # painting background image
    def paintEvent(self, event):
        painter = QPainter(self)
        pixmap = QPixmap(self.background_image)
        if not pixmap.isNull():
            painter.drawPixmap(self.rect(), pixmap)
        super().paintEvent(event)

    # Series-Parallel fields show/hide
    def toggle_series_parallel_inputs(self, text):
        if text == "Series-Parallel":
            self.series_cells_input.show()
            self.parallel_cells_input.show()
        else:
            self.series_cells_input.hide()
            self.parallel_cells_input.hide()

    # Demo lookup cell method
    def lookup_cell(self):
        # Example: set values for an 18650 Li-ion cell
        self.cell_voltage_input.setText("3.7")
        self.cell_capacity_input.setText("2.5")
        self.cell_weight_input.setText("45")
        self.cell_ir_input.setText("0.045")
        self.cell_length_input.setText("65")
        self.cell_width_input.setText("18")
        self.cell_height_input.setText("18")
        self.chemistry_box.setCurrentText("Li-ion")

    # Export as plain text
    def export_results(self):
        results = self.result_label.text()
        if not results.strip():
            QMessageBox.warning(self, "Error", "No design to export. Please fill all fields and calculate first")
            return
        plain_text = re.sub('<[^<]+?>', '', results)
        file_path, _ = QFileDialog.getSaveFileName(self, "Export data", "", "Text Files(*.txt)")
        if file_path:
            try:
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(plain_text)
                QMessageBox.information(self, "Success", "Design exported Successfully!")
            except Exception as e:
                QMessageBox.warning(self, "Error", f"Could not save file: {e}")

    # Export as PDF
    def export_pdf(self):
        from reportlab.lib.pagesizes import letter
        from reportlab.lib.units import inch
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
        from reportlab.lib import colors
        from datetime import datetime
        
        result_text = self.result_label.text()
        if not result_text.strip():
            QMessageBox.warning(self, "Error", "No result to export. Please calculate first.")
            return
        
        # Strip HTML tags and convert <br> to newlines for proper parsing
        plain_text = result_text.replace('<br>', '\n')
        plain_text = re.sub('<[^<]+?>', '', plain_text)
        
        file_path, _ = QFileDialog.getSaveFileName(self, "Save as PDF", "", "PDF Files (*.pdf)")
        if not file_path:
            return
        
        try:
            doc = SimpleDocTemplate(
                file_path,
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
                textColor=colors.HexColor('#1a1a1a'),
                spaceAfter=6,
                alignment=1
            )
            heading_style = ParagraphStyle(
                'CustomHeading',
                parent=styles['Heading2'],
                fontSize=14,
                textColor=colors.HexColor('#0066cc'),
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
            # Cell text style for table content (smaller font, wrappable)
            cell_style = ParagraphStyle(
                'CellText',
                parent=styles['Normal'],
                fontSize=10,
                textColor=colors.HexColor('#333333')
            )
            
            story.append(Paragraph("Battery Design Report", title_style))
            story.append(Spacer(1, 0.3*inch))
            
            metadata = f"<b>Generated:</b> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}<br/>"
            metadata += f"<b>Chemistry:</b> {self.chemistry_box.currentText()}<br/>"
            metadata += f"<b>DOD:</b> {self.dod_combo.currentText()}"
            story.append(Paragraph(metadata, normal_style))
            story.append(Spacer(1, 0.2*inch))
            
            story.append(Paragraph("_" * 80, normal_style))
            story.append(Spacer(1, 0.1*inch))
            
            story.append(Paragraph("Configuration Details", heading_style))
            
            # Extract key-value pairs
            lines = [line.strip() for line in plain_text.split('\n') if line.strip() and ':' in line]
            
            # Create table data with Paragraph wrappers for text wrapping
            table_data = [["Parameter", "Value"]]
            for line in lines:
                if ':' in line:
                    parts = line.split(':', 1)
                    param = parts[0].strip()
                    value = parts[1].strip()
                    # Wrap cell content in Paragraph for automatic text wrapping
                    table_data.append([
                        Paragraph(param, cell_style),
                        Paragraph(value, cell_style)
                    ])
            
            if len(table_data) > 1:
                # Use flexible column widths — Parameter 40%, Value 60%
                table = Table(table_data, colWidths=[2.2*inch, 4.3*inch])
                table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#0066cc')),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                    ('VALIGN', (0, 0), (-1, -1), 'TOP'),  # align to top for multi-line cells
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, 0), 12),
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                    ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                    ('GRID', (0, 0), (-1, -1), 1, colors.black),
                    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f0f0f0')]),
                    ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                    ('FONTSIZE', (0, 1), (-1, -1), 10),
                    ('TOPPADDING', (0, 1), (-1, -1), 8),
                    ('BOTTOMPADDING', (0, 1), (-1, -1), 8),
                    ('LEFTPADDING', (0, 1), (-1, -1), 6),
                    ('RIGHTPADDING', (0, 1), (-1, -1), 6),
                ]))
                story.append(table)
            
            story.append(Spacer(1, 0.3*inch))
            
            if "Warning" in plain_text:
                story.append(Paragraph("Warnings & Recommendations", heading_style))
                warnings = [line for line in plain_text.split('\n') if 'Warning' in line or 'Recommendation' in line]
                for warning in warnings:
                    story.append(Paragraph(f"• {warning.strip()}", normal_style))
                story.append(Spacer(1, 0.2*inch))
            
            story.append(Spacer(1, 0.2*inch))
            story.append(Paragraph("_" * 80, normal_style))
            footer_text = "<i>This report was generated by Battery Design Calculator. Please verify calculations before use.</i>"
            story.append(Paragraph(footer_text, normal_style))
            
            doc.build(story)
            QMessageBox.information(self, "Success", f"PDF exported successfully to:\n{file_path}")
            
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Could not save PDF: {e}")
    # Export as CSV
    def export_csv(self):
        import csv
        result_text = self.result_label.text()
        if not result_text.strip():
            QMessageBox.warning(self, "Error", "No result to export. Please calculate first.")
            return
        plain_text = re.sub('<[^<]+?>', '', result_text)
        lines = [line for line in plain_text.split('\n') if ':' in line]
        data = [line.split(':', 1) for line in lines]
        file_path, _ = QFileDialog.getSaveFileName(self, "Save as CSV", "", "CSV Files (*.csv)")
        if file_path:
            try:
                with open(file_path, "w", newline='', encoding="utf-8") as f:
                    writer = csv.writer(f)
                    writer.writerow(["Parameter", "Value"])
                    for row in data:
                        writer.writerow([row[0].strip(), row[1].strip()])
                QMessageBox.information(self, "Success", "CSV exported successfully!")
            except Exception as e:
                QMessageBox.warning(self, "Error", f"Could not save CSV: {e}")

    # Export as Excel (XLSX)
    def export_xlsx(self):
        try:
            import openpyxl
        except ImportError:
            QMessageBox.warning(self, "Error", "openpyxl is not installed. Run 'pip install openpyxl'.")
            return
        result_text = self.result_label.text()
        if not result_text.strip():
            QMessageBox.warning(self, "Error", "No result to export. Please calculate first.")
            return
        plain_text = re.sub('<[^<]+?>', '', result_text)
        lines = [line for line in plain_text.split('\n') if ':' in line]
        data = [line.split(':', 1) for line in lines]
        file_path, _ = QFileDialog.getSaveFileName(self, "Save as Excel", "", "Excel Files (*.xlsx)")
        if file_path:
            try:
                wb = openpyxl.Workbook()
                ws = wb.active
                ws.append(["Parameter", "Value"])
                for row in data:
                    ws.append([row[0].strip(), row[1].strip()])
                wb.save(file_path)
                QMessageBox.information(self, "Success", "Excel exported successfully!")
            except Exception as e:
                QMessageBox.warning(self, "Error", f"Could not save Excel: {e}")

   
    # --------- Main Calculation ---------
                
    def calculate_battery(self):
        try:
            cell_voltage = float(self.cell_voltage_input.text())
            cell_capacity = float(self.cell_capacity_input.text())
            num_cells = int(self.num_cells_input.text())
            conn_type = self.connection_type.currentText().lower()
            chem = self.chemistry_box.currentText() if hasattr(self, "chemistry_box") else "Li-ion"
            dod = int(self.dod_combo.currentText().replace("%", ""))  # get correct DOD value
            cycle_life_dict = {
                "Li-ion": 500,
                "LiFePO4": 2000,
                "Lead Acid": 300,
                "NiMH": 500
            }
            dod_multiplier_dict = {100: 1.0, 80: 1.2, 60: 1.5, 40: 2.0, 20: 3.0}
            cycle_life = cycle_life_dict.get(chem, 500)
            dod_multiplier = dod_multiplier_dict.get(dod, 1.2)
            cycle_life_estimate = int(cycle_life * dod_multiplier)

            # Get user C-rate or default to 5
            c_rate = float(self.c_rate_input.text() or 5)

            # Series/Parallel computation
            if conn_type == "series":
                series_cells = num_cells
                parallel_cells = 1
                print(num_cells)

            elif conn_type == "parallel":
                series_cells = 1
                parallel_cells = num_cells
                print(num_cells)
            elif conn_type == "series-parallel":
                series_cells = int(self.series_cells_input.text())
                parallel_cells = int(self.parallel_cells_input.text())
                if series_cells * parallel_cells != num_cells:
                    QMessageBox.warning(self, "Warning", "series_cells * parallel_cells != total number of cells!")
            else:
                QMessageBox.warning(self, "Error", "Invalid connection type.")
                return

            total_voltage = cell_voltage * series_cells
            nominal_voltage = (cell_voltage - 0.2)
            rated_voltage = nominal_voltage * series_cells
            total_capacity = cell_capacity * parallel_cells
            total_energy = total_voltage * total_capacity  # in Wh
            num_of_years = cycle_life_estimate / 365  # assuming 1 cycle per day


           
            # Internal resistance and power calculations
            cell_ir = float(self.cell_ir_input.text() or 0) / 1000  # ohms
            ir_lines = ""
            runtime = 0
            if cell_ir > 0:
                pack_ir = cell_ir * series_cells / parallel_cells
                max_current = total_capacity * c_rate
                voltage_sag = pack_ir * max_current
                max_power = (total_voltage - voltage_sag) * max_current
                runtime = int(total_capacity//max_current)
               
                ir_lines = (
                    f"<br><b>Estimated Pack IR:</b> {pack_ir*1000:.2f} mΩ"
                    f"<br><b>Voltage Sag @ {max_current:.1f}A ({c_rate:.1f}C):</b> {voltage_sag:.2f} V"
                    f"<br><b>Max Power @ {c_rate:.1f}C:</b> {max_power/1000:.2f} kW"

                )
            if runtime >1:
                    runtime = f"<br><b> Runtime(hrs) will be {runtime} hours" 
            else:
                    runtime=f"<br><b> Runtime(hrs) will be {runtime} hour"
                    
            
           

            # Safety: Check if cell voltage exceeds safe value for chemistry
            safety_voltages = {"Li-ion": 4.2, "LiFePO4": 3.65, "Lead Acid": 2.45, "NiMH": 1.5}
            max_cell_v = safety_voltages.get(chem, 4.2)
            warning_line = ""
            if cell_voltage > max_cell_v:
                warning_line = f"<br><span style='color:red'><b>Warning:</b> Cell voltage exceeds safe max ({max_cell_v}V) for {chem}!</span>"

            # Recommend BMS if needed
            bms_config = (series_cells -1) + (parallel_cells -1)
            bms_line = ""
            if series_cells > 1:
                bms_line = "<br><b>Recommendation:</b> Use a BMS with cell balancing and over/under-voltage protection."
            


            summary = (
                f"<b>Configuration:</b> {series_cells}S{parallel_cells}P<br>"
                f"<b>Chemistry:</b> {chem}<br>"
                f"<b>Rated Voltage:</b> {rated_voltage:.2f} V<br>"
                f"<b>Nominal Voltage:</b> {total_voltage:.2f} V<br>"
                f"<b>Rated Capacity:</b> {total_capacity:.2f} Ah<br>"
                f"<b>Example:</b> {series_cells * parallel_cells} x {cell_capacity}Ah cells ({cell_voltage}V each)<br>"
                f"<b>Total Energy:</b> {total_energy/1000:.2f} kWh ({total_energy:.2f} Wh)<br>"
                f"<b>Estimated Cycle Life:</b> {cycle_life_estimate} cycles @{dod}% DOD ({num_of_years:.2f} years NB:cycling frequency will affect the number of years of service) <br>"
                f"<b>Example:</b> if cycled once in two days, the estimated years will be doubled to {num_of_years*2:.2f} years<br>"
                #f"<br><b>Total Weight:</b> {total_weight:.2f} Kg"
                #f"<br><b>Estimated Total Cell Cost:</b> ${total_price:.2f}"
                f"{ir_lines}"
                f"{bms_line}"
                f"{warning_line}"
                f"{runtime}"
            )

            self.result_label.setText(summary)
            # Update diagram
            #self.diagram_widget.set_config(series_cells, parallel_cells)
            self.result_label.show()
            self.result_label.resize(500, self.result_label.sizeHint().height())
            self.result_label.setText(summary)
            QApplication.processEvents( )
            self.resize(self.size().width(), self.size().height()+1)
            
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Invalid input: {e}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = BatteryCalculator()
    win.show()
    sys.exit(app.exec_())