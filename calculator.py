"""Calculator logic extracted from the original PyQt app.
Provides functions to compute pack design and bank/module requirements.
"""
from typing import Dict


def estimate_cycle_life(chemistry: str, dod: int) -> int:
    base_cycle_life = {
        "Li-ion": 500,
        "LiFePO4": 2000,
        "Lead Acid": 300,
        "NiMH": 500
    }
    dod_multiplier = {100: 1.0, 80: 1.2, 60: 1.5, 40: 2.0, 20: 3.0}
    base = base_cycle_life.get(chemistry, 500)
    multiplier = dod_multiplier.get(dod, 1.0)
    return int(base * multiplier)


def compute_pack_design(cell_voltage: float,
                        cell_capacity: float,
                        num_cells: int,
                        connection_type: str,
                        series_cells: int = None,
                        parallel_cells: int = None,
                        c_rate: float = 5.0,
                        cell_ir_milli: float = 0.0,
                        chemistry: str = 'LiFePO4',
                        dod: int = 80) -> Dict:
    """Compute battery pack parameters and return a result dict.

    Returns keys: series_cells, parallel_cells, total_voltage, rated_voltage,
    total_capacity, total_energy_Wh, cycle_life_estimate, warnings, summary_html
    """
    conn = connection_type.lower()
    if conn == 'series':
        series = num_cells
        parallel = 1
    elif conn == 'parallel':
        series = 1
        parallel = num_cells
    elif conn in ('series-parallel', 'series_parallel'):
        if not series_cells or not parallel_cells:
            raise ValueError('series and parallel values required for series-parallel')
        series = int(series_cells)
        parallel = int(parallel_cells)
        if series * parallel != num_cells:
            # continue but warn
            mismatch = True
        else:
            mismatch = False
    else:
        raise ValueError('Invalid connection type')

    total_voltage = cell_voltage * series
    nominal_voltage = (cell_voltage - 0.2)
    rated_voltage = nominal_voltage * series
    total_capacity = cell_capacity * parallel
    total_energy_Wh = total_voltage * total_capacity

    cycle_life_estimate = estimate_cycle_life(chemistry, dod)

    # Internal resistance calculations
    cell_ir = cell_ir_milli / 1000.0
    ir_lines = ""
    runtime = 0
    max_power = None
    voltage_sag = None
    if cell_ir > 0:
        pack_ir = cell_ir * series / parallel
        max_current = total_capacity * c_rate
        voltage_sag = pack_ir * max_current
        max_power = (total_voltage - voltage_sag) * max_current
        runtime = int(total_capacity // max_current) if max_current > 0 else 0
        ir_lines = {
            'pack_ir_milliohm': pack_ir * 1000.0,
            'voltage_sag_V': voltage_sag,
            'max_power_kW': (max_power / 1000.0) if max_power is not None else None,
        }

    safety_voltages = {"Li-ion": 4.2, "LiFePO4": 3.65, "Lead Acid": 2.45, "NiMH": 1.5}
    max_cell_v = safety_voltages.get(chemistry, 4.2)
    warning = None
    if cell_voltage > max_cell_v:
        warning = f"Cell voltage {cell_voltage}V exceeds safe max {max_cell_v}V for {chemistry}"

    bms_recommendation = None
    if series > 1:
        bms_recommendation = 'Use a BMS with cell balancing and over/under-voltage protection.'

    summary = (
        f"Configuration: {series}S{parallel}P\n"
        f"Chemistry: {chemistry}\n"
        f"Rated Voltage: {rated_voltage:.2f} V\n"
        f"Nominal Voltage: {total_voltage:.2f} V\n"
        f"Rated Capacity: {total_capacity:.2f} Ah\n"
        f"Total Energy: {total_energy_Wh/1000.0:.2f} kWh ({total_energy_Wh:.2f} Wh)\n"
        f"Estimated Cycle Life: {cycle_life_estimate} cycles @ {dod}% DOD\n"
    )

    if isinstance(ir_lines, dict) and ir_lines:
        summary += (f"Pack IR: {ir_lines['pack_ir_milliohm']:.2f} mΩ\n"
                    f"Voltage Sag @ {c_rate:.1f}C: {ir_lines['voltage_sag_V']:.2f} V\n"
                    f"Max Power @ {c_rate:.1f}C: {ir_lines['max_power_kW']:.2f} kW\n")

    if bms_recommendation:
        summary += f"Recommendation: {bms_recommendation}\n"
    if warning:
        summary += f"Warning: {warning}\n"
    if runtime:
        summary += f"Runtime (hrs): {runtime}\n"

    return {
        'series_cells': series,
        'parallel_cells': parallel,
        'total_voltage': total_voltage,
        'rated_voltage': rated_voltage,
        'total_capacity_Ah': total_capacity,
        'total_energy_Wh': total_energy_Wh,
        'cycle_life_estimate': cycle_life_estimate,
        'ir_info': ir_lines,
        'warning': warning,
        'bms_recommendation': bms_recommendation,
        'summary_text': summary,
    }


def compute_bank_design(target_energy_kwh: float, module_capacity_kwh: float, chemistry: str = 'LiFePO4', dod: int = 100) -> Dict:
    modules_needed = int((target_energy_kwh + module_capacity_kwh - 1) // module_capacity_kwh)
    cycle_life = estimate_cycle_life(chemistry, dod)
    summary = f"modules_needed: {modules_needed}, cycle_life: {cycle_life} cycles @ {dod}% DOD"
    return {
        'modules_needed': modules_needed,
        'cycle_life': cycle_life,
        'summary_text': summary
    }
