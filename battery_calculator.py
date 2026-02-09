from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QLineEdit, QComboBox, QPushButton, QMessageBox, QFileDialog, QTabWidget, QTextEdit
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QPainter, QPen,QIcon
import sys
import re
import os 
import matplotlib.pyplot as plt
from dataclasses import dataclass
import math

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


# --- Solar design dataclasses and helper functions ---
@dataclass
class Load:
    name: str
    power_w: float
    hours_per_day: float


@dataclass
class PanelSpecs:
    p_stc_w: float
    area_m2: float
    voc_v: float
    vmp_v: float
    isc_a: float
    imp_a: float
    temp_coeff_pmp_pct_per_c: float
    nominal_operating_cell_temp_c: float
    weight_kg: float
    manufacturer: str = ""
    model: str = ""


@dataclass
class inverterSpecs:
    ac_power_w: float
    dc_power_w: float
    mppt_min_v: float
    mppt_max_v: float
    mppt_max_current_a: float


@dataclass
class BatterySpecs:
    capacity_ah: float
    nominal_voltage_v: float
    max_discharge_current_a: float
    round_trip_efficiency_pct: float
    depth_of_discharge_pct: float
    manufacturer: str = ""
    model: str = ""
    efficiency: float = None


@dataclass
class siteSpecs:
    latitude_deg: float
    longitude_deg: float
    timezone: str
    elevation_m: float
    avg_solar_irradiance_kw_per_m2: float
    psh_per_day: float
    shading_factor_pct: float
    t_hot_c: float
    t_cold_c: float = 0.0


def calculate_daily_energy_consumption(loads):
    total_energy_wh = 0.0
    for load in loads:
        energy_wh = load.power_w * load.hours_per_day
        total_energy_wh += energy_wh
    return total_energy_wh


def calculate_panel_output(panel: PanelSpecs, site: siteSpecs):
    irradiance_factor = site.avg_solar_irradiance_kw_per_m2 / 1.0  # kW/m2 (already kW/m2)
    temperature_factor = (site.t_hot_c - panel.nominal_operating_cell_temp_c) * panel.temp_coeff_pmp_pct_per_c / 100.0
    adjusted_power = panel.p_stc_w * irradiance_factor * (1 - temperature_factor)
    return adjusted_power


def calculate_battery_capacity(battery: BatterySpecs):
    usable_capacity_ah = battery.capacity_ah * (battery.depth_of_discharge_pct / 100.0)
    usable_capacity_wh = usable_capacity_ah * battery.nominal_voltage_v
    return usable_capacity_wh


def string_voltage_limits(inverter: inverterSpecs, panel: PanelSpecs):
    min_panels = math.ceil(inverter.mppt_min_v / panel.vmp_v)
    max_panels = math.floor(inverter.mppt_max_v / panel.vmp_v)
    return min_panels, max_panels


def array_layout(total_power_w, panel: PanelSpecs, inverter: inverterSpecs):
    num_panels = math.ceil(total_power_w / panel.p_stc_w)
    min_strings = math.ceil(num_panels / max(1, string_voltage_limits(inverter, panel)[1]))
    max_strings = math.floor(num_panels / max(1, string_voltage_limits(inverter, panel)[0]))
    return num_panels, min_strings, max_strings


def check_mppt_current(inverter: inverterSpecs, panel: PanelSpecs, num_panels_per_string: int, num_strings: int):
    total_current_a = panel.imp_a * num_strings
    return total_current_a <= inverter.mppt_max_current_a


def system_size(loads, panel: PanelSpecs, inverter: inverterSpecs, battery: BatterySpecs, site: siteSpecs):
    daily_energy_wh = calculate_daily_energy_consumption(loads)
    panel_output_w = calculate_panel_output(panel, site)
    # size array to meet average daily energy using peak sun hours
    if site.psh_per_day <= 0:
        num_panels = 0
        min_strings = 0
        max_strings = 0
    else:
        num_panels, min_strings, max_strings = array_layout(daily_energy_wh / site.psh_per_day, panel, inverter)
    battery_capacity_wh = calculate_battery_capacity(battery)
    return {
        "daily_energy_wh": daily_energy_wh,
        "panel_output_w": panel_output_w,
        "num_panels": num_panels,
        "min_strings": min_strings,
        "max_strings": max_strings,
        "battery_capacity_wh": battery_capacity_wh
    }


# --------- Main Application Class ----------
class BatteryCalculator(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Solar Energy System Design")
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

        # Tab 3: Solar system design
        self.tab3 = QWidget()
        tab_layout3 = QVBoxLayout(self.tab3)
        self.tabs.addTab(self.tab3, "Solar design")

        # --- Solar inputs ---
        loads_label = QLabel("Loads (one per line: name,power_w,hrs/day):")
        loads_label.setStyleSheet("background:Transparent;color:purple;font-weight:bold;")
        self.loads_edit = QTextEdit()
        self.loads_edit.setPlaceholderText("Light,50,4\nFridge,150,24")
        tab_layout3.addWidget(loads_label)
        tab_layout3.addWidget(self.loads_edit)

        # Panel specs
        h_panel = QHBoxLayout()
        self.panel_pstc_input = QLineEdit()
        self.panel_pstc_input.setPlaceholderText("Panel Pstc (W)")
        self.panel_vmp_input = QLineEdit()
        self.panel_vmp_input.setPlaceholderText("Vmp (V)")
        self.panel_imp_input = QLineEdit()
        self.panel_imp_input.setPlaceholderText("Imp (A)")
        h_panel.addWidget(QLabel("Panel Pstc(W):"))
        h_panel.addWidget(self.panel_pstc_input)
        h_panel.addWidget(QLabel("Vmp(V):"))
        h_panel.addWidget(self.panel_vmp_input)
        h_panel.addWidget(QLabel("Imp(A):"))
        h_panel.addWidget(self.panel_imp_input)
        tab_layout3.addLayout(h_panel)

        # Inverter specs
        h_inv = QHBoxLayout()
        self.inv_mppt_min = QLineEdit(); self.inv_mppt_min.setPlaceholderText("MPPT min V")
        self.inv_mppt_max = QLineEdit(); self.inv_mppt_max.setPlaceholderText("MPPT max V")
        self.inv_mppt_i = QLineEdit(); self.inv_mppt_i.setPlaceholderText("MPPT max I (A)")
        h_inv.addWidget(QLabel("MPPT Vmin:")); h_inv.addWidget(self.inv_mppt_min)
        h_inv.addWidget(QLabel("MPPT Vmax:")); h_inv.addWidget(self.inv_mppt_max)
        h_inv.addWidget(QLabel("MPPT I(A):")); h_inv.addWidget(self.inv_mppt_i)
        tab_layout3.addLayout(h_inv)

        # Battery specs
        h_batt = QHBoxLayout()
        self.batt_cap_ah = QLineEdit(); self.batt_cap_ah.setPlaceholderText("Battery Ah")
        self.batt_nom_v = QLineEdit(); self.batt_nom_v.setPlaceholderText("Battery V")
        self.batt_dod = QLineEdit(); self.batt_dod.setPlaceholderText("DOD %")
        h_batt.addWidget(QLabel("Batt Ah:")); h_batt.addWidget(self.batt_cap_ah)
        h_batt.addWidget(QLabel("Batt V:")); h_batt.addWidget(self.batt_nom_v)
        h_batt.addWidget(QLabel("DOD%:")); h_batt.addWidget(self.batt_dod)
        tab_layout3.addLayout(h_batt)

        # Site specs
        h_site = QHBoxLayout()
        self.site_psh = QLineEdit(); self.site_psh.setPlaceholderText("PSH/day")
        self.site_irr = QLineEdit(); self.site_irr.setPlaceholderText("Irr (kW/m2)")
        h_site.addWidget(QLabel("PSH/day:")); h_site.addWidget(self.site_psh)
        h_site.addWidget(QLabel("Irr (kW/m2):")); h_site.addWidget(self.site_irr)
        tab_layout3.addLayout(h_site)

        # Calculate and result
        self.solar_calc_btn = QPushButton("Calculate Solar System")
        self.solar_calc_btn.setStyleSheet("background-color:orange;color:white;")
        self.solar_calc_btn.clicked.connect(self.calculate_solar)
        tab_layout3.addWidget(self.solar_calc_btn, alignment=Qt.AlignLeft)

        self.result_label3 = QLabel("")
        self.result_label3.setWordWrap(True)
        tab_layout3.addWidget(self.result_label3)

        self.tabs.setStyleSheet("""
                                QTabWidget::pane {border:0px solid #ccc;}
                                QTabBar::tab{background:#eee;padding:8px;}
                                QTabBar::tab:selected{ background:#ddd;font-weight:bold;}

        """)
        self.tabs.currentChanged.connect(self.on_tab_switch)

        # --------- Battery design (Tab 1) inputs ----------
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
    # Solar calculation handler
    def calculate_solar(self):
        try:
            # parse loads from text area
            loads_text = self.loads_edit.toPlainText().strip()
            loads = []
            if loads_text:
                for line in loads_text.splitlines():
                    parts = [p.strip() for p in line.split(',') if p.strip()]
                    if len(parts) >= 3:
                        name = parts[0]
                        power = float(parts[1])
                        hrs = float(parts[2])
                        loads.append(Load(name, power, hrs))

            # Panel
            pstc = float(self.panel_pstc_input.text() or 0)
            vmp = float(self.panel_vmp_input.text() or 0)
            imp = float(self.panel_imp_input.text() or 0)
            panel = PanelSpecs(p_stc_w=pstc, area_m2=0.0, voc_v=0.0, vmp_v=vmp, isc_a=0.0, imp_a=imp,
                               temp_coeff_pmp_pct_per_c=0.0, nominal_operating_cell_temp_c=25.0, weight_kg=0.0)

            # Inverter
            mppt_min = float(self.inv_mppt_min.text() or 0)
            mppt_max = float(self.inv_mppt_max.text() or 0)
            mppt_i = float(self.inv_mppt_i.text() or 0)
            inverter = inverterSpecs(ac_power_w=0.0, dc_power_w=0.0, mppt_min_v=mppt_min, mppt_max_v=mppt_max, mppt_max_current_a=mppt_i)

            # Battery
            batt_ah = float(self.batt_cap_ah.text() or 0)
            batt_v = float(self.batt_nom_v.text() or 0)
            batt_dod = float(self.batt_dod.text() or 80)
            battery = BatterySpecs(capacity_ah=batt_ah, nominal_voltage_v=batt_v, max_discharge_current_a=0.0,
                                   round_trip_efficiency_pct=90.0, depth_of_discharge_pct=batt_dod)

            # Site
            psh = float(self.site_psh.text() or 4.0)
            irr = float(self.site_irr.text() or 1.0)
            site = siteSpecs(latitude_deg=0.0, longitude_deg=0.0, timezone="UTC", elevation_m=0.0,
                             avg_solar_irradiance_kw_per_m2=irr, psh_per_day=psh, shading_factor_pct=0.0, t_hot_c=25.0)

            results = system_size(loads, panel, inverter, battery, site)

            out = (
                f"Daily load: {results['daily_energy_wh']:.1f} Wh\n"
                f"Panel per-unit adjusted power: {results['panel_output_w']:.1f} W\n"
                f"Panels needed: {results['num_panels']} (strings min:{results['min_strings']}, max:{results['max_strings']})\n"
                f"Battery usable capacity: {results['battery_capacity_wh']:.1f} Wh\n"
            )
            self.result_label3.setText(out)
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Solar calculation failed: {e}")

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
            QApplication.processEvents()
            
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Invalid input: {e}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = BatteryCalculator()
    win.show()
    sys.exit(app.exec_())