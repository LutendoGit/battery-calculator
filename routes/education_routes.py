"""
Educational Flask Routes
Adds educational content to the battery calculator app
"""

from flask import Blueprint, render_template, request, jsonify, redirect, url_for
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


# ============= FUNDAMENTAL CONCEPTS ROUTES =============

@education_bp.route('/fundamentals')
def fundamentals():
    """Main fundamentals page"""
    content = {
        "good_cell": LithiumBatteryFundamentals.CELL_BEHAVIORS["good_cell_operation"],
        "bad_cell": LithiumBatteryFundamentals.CELL_BEHAVIORS["bad_cell_detection"],
        "pack_imbalance": LithiumBatteryFundamentals.CELL_BEHAVIORS["pack_imbalance"]
    }
    return render_template('education/fundamentals.html', content=content)


@education_bp.route('/chemistry')
def chemistry():
    """Learn about battery chemistries"""
    chemistries = {}
    for chem in CellChemistry:
        chemistries[chem.value] = LithiumBatteryFundamentals.CHEMISTRY_PROPERTIES[chem]
    
    return render_template('education/chemistry.html', chemistries=chemistries)


@education_bp.route('/capacity-dod')
def capacity_dod():
    """Learn about capacity and DOD"""
    content = {
        "capacity": CapacityAndDOD.capacity_explanation(),
        "dod": CapacityAndDOD.dod_explanation()
    }
    return render_template('education/capacity_dod.html', content=content)


@education_bp.route('/crate')
def crate_learn():
    """Learn about C-rates"""
    content = CRate.crate_explanation()
    return render_template('education/crate.html', content=content)


@education_bp.route('/cycles-aging')
def cycles_aging():
    """Learn about battery cycles and aging"""
    content = {
        "cycles": BatteryLifeAndCycles.cycle_definition(),
        "degradation": BatteryLifeAndCycles.degradation_factors()
    }
    return render_template('education/cycles_aging.html', content=content)


# ============= INTERACTIVE TOOLS ROUTES =============

@education_bp.route('/cell-simulator')
def cell_simulator_page():
    """Cell discharge/charge simulator page"""
    return render_template('education/cell_simulator.html')


@education_bp.route('/api/cell-simulator/discharge', methods=['POST'])
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
def pack_simulator_page():
    """Pack simulator page"""
    return render_template('education/pack_simulator.html')


@education_bp.route('/api/pack-simulator/discharge', methods=['POST'])
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
def calculators():
    """Interactive calculators page"""
    return render_template('education/calculators.html')


@education_bp.route('/', strict_slashes=False)
@education_bp.route('')
def learn_index():
    """Redirect /learn to the interactive calculators landing page."""
    # Render a small landing page that links to calculators and quizzes
    return render_template('education/learn_index.html')


@education_bp.route('/api/calculate/energy', methods=['POST'])
def api_calculate_energy():
    """API: Calculate energy from capacity"""
    data = request.json
    result = InteractiveCalculators.capacity_energy_calculator(
        capacity_mah=float(data.get('capacity_mah', 2000)),
        voltage_v=float(data.get('voltage_v', 3.7))
    )
    return jsonify(result)


@education_bp.route('/api/calculate/crate', methods=['POST'])
def api_calculate_crate():
    """API: Calculate C-rate"""
    data = request.json
    result = InteractiveCalculators.crate_calculator(
        current_a=float(data.get('current_a', 1.0)),
        capacity_ah=float(data.get('capacity_ah', 2.0))
    )
    return jsonify(result)


@education_bp.route('/api/calculate/cycle-life', methods=['POST'])
def api_calculate_cycle_life():
    """API: Calculate expected cycle life"""
    data = request.json
    result = InteractiveCalculators.cycle_life_calculator(
        chemistry=CellChemistry[data.get('chemistry', 'LI_ION')],
        dod_percent=int(data.get('dod_percent', 80))
    )
    return jsonify(result)


@education_bp.route('/api/calculate/pack-voltage', methods=['POST'])
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
def quiz_index():
    """Quiz selection page"""
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
def api_quiz_capacity_dod():
    """API: Get capacity & DOD quiz"""
    questions = EducationalQuizzes.quiz_capacity_dod()
    return jsonify(questions)


@education_bp.route('/api/quiz/crate')
def api_quiz_crate():
    """API: Get C-rate quiz"""
    questions = EducationalQuizzes.quiz_crate()
    return jsonify(questions)


@education_bp.route('/api/quiz/cell-health')
def api_quiz_cell_health():
    """API: Get cell health quiz"""
    questions = EducationalQuizzes.quiz_cell_health()
    return jsonify(questions)


@education_bp.route('/api/quiz/chemistry')
def api_quiz_chemistry():
    """API: Get chemistry quiz"""
    questions = EducationalQuizzes.quiz_chemistry()
    return jsonify(questions)


@education_bp.route('/api/quiz/cycles-aging')
def api_quiz_cycles_aging():
    """API: Get cycles & aging quiz"""
    questions = EducationalQuizzes.quiz_cycles_aging()
    return jsonify(questions)


@education_bp.route('/api/quiz/pack-design')
def api_quiz_pack_design():
    """API: Get pack design quiz"""
    questions = EducationalQuizzes.quiz_pack_design()
    return jsonify(questions)


@education_bp.route('/api/quiz/bms-balancing')
def api_quiz_bms_balancing():
    """API: Get BMS & balancing quiz"""
    questions = EducationalQuizzes.quiz_bms_balancing()
    return jsonify(questions)


# ============= REFERENCE PAGES =============

@education_bp.route('/reference/good-cell')
def reference_good_cell():
    """Reference: What makes a good cell"""
    content = LithiumBatteryFundamentals.CELL_BEHAVIORS["good_cell_operation"]
    return render_template('education/reference_good_cell.html', content=content)


@education_bp.route('/reference/bad-cell')
def reference_bad_cell():
    """Reference: Signs of a bad cell"""
    content = LithiumBatteryFundamentals.CELL_BEHAVIORS["bad_cell_detection"]
    return render_template('education/reference_bad_cell.html', content=content)


@education_bp.route('/reference/pack-issues')
def reference_pack_issues():
    """Reference: Cell imbalance in packs"""
    content = LithiumBatteryFundamentals.CELL_BEHAVIORS["pack_imbalance"]
    return render_template('education/reference_pack_issues.html', content=content)


@education_bp.route('/glossary')
def glossary():
    """Battery terminology glossary"""
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
