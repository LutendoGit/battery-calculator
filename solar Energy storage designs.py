from dataclasses import dataclass 
import math

@dataclass 
class Load: 
    name: str 
    power_w: float # watts 
    hours_per_day: float # hours

@dataclass
class PanelSpecs:
    p_stc_w:float # Standard Test Condition power in watts
    area_m2:float # Area in square meters
    voc_v:float # Open-circuit voltage in volts
    vmp_v:float # Voltage at maximum power in volts
    isc_a:float # Short-circuit current in amps
    imp_a:float # Current at maximum power in amps
    temp_coeff_pmp_pct_per_c:float # Temperature coefficient of power in %/°C
    nominal_operating_cell_temp_c:float # Nominal operating cell temperature in °C
    weight_kg:float # Weight in kilograms
    manufacturer: str
    model: str

@dataclass
class inverterSpecs:
    ac_power_w: float # AC power in watts
    dc_power_w: float # DC power in watts
    mppt_min_v: float # Minimum MPPT voltage in volts
    mppt_max_v: float # Maximum MPPT voltage in volts
    mppt_max_current_a: float # Maximum MPPT current in amps


@dataclass
class BatterySpecs:
    capacity_ah: float # Capacity in ampere-hours
    nominal_voltage_v: float # Nominal voltage in volts
    max_discharge_current_a: float # Maximum discharge current in amps
    round_trip_efficiency_pct: float # Round-trip efficiency in percentage
    depth_of_discharge_pct: float # Depth of discharge in percentage
    manufacturer: str
    model: str
    efficiency: float = None


@dataclass
class siteSpecs:
    latitude_deg: float # Latitude in degrees
    longitude_deg: float # Longitude in degrees
    timezone: str # Timezone string
    elevation_m: float # Elevation in meters
    avg_solar_irradiance_kw_per_m2: float # Average solar irradiance in kW/m^2
    psh_per_day: float # Peak sun hours per day
    shading_factor_pct: float # Shading factor in percentage
    t_hot_c: float # Average high temperature in Celsius
    t_cold_c: float # Average low temperature in Celsius

def calculate_daily_energy_consumption(loads):
    total_energy_wh = 0.0
    for load in loads:
        energy_wh = load.power_w * load.hours_per_day
        total_energy_wh += energy_wh
    return total_energy_wh

def calculate_panel_output(panel: PanelSpecs, site: siteSpecs):
    # Calculate panel output based on irradiance and temperature
    # Simplified model for demonstration purposes
    irradiance_factor = site.avg_solar_irradiance_kw_per_m2 / 1000.0  # Convert to kW/m^2
    temperature_factor = (site.t_hot_c - panel.nominal_operating_cell_temp_c) * panel.temp_coeff_pmp_pct_per_c / 100.0
    adjusted_power = panel.p_stc_w * irradiance_factor * (1 - temperature_factor)
    return adjusted_power

def calculate_battery_capacity(battery: BatterySpecs):
    usable_capacity_ah = battery.capacity_ah * (battery.depth_of_discharge_pct / 100.0)
    usable_capacity_wh = usable_capacity_ah * battery.nominal_voltage_v
    return usable_capacity_wh

def string_voltage_limits(inverter: inverterSpecs, panel: PanelSpecs):
    # Calculate the minimum and maximum number of panels in series for the inverter
    min_panels = math.ceil(inverter.mppt_min_v / panel.vmp_v)
    max_panels = math.floor(inverter.mppt_max_v / panel.vmp_v)
    return min_panels, max_panels

def array_layout(total_power_w, panel: PanelSpecs, inverter: inverterSpecs):
    # Calculate number of panels needed and string configuration
    num_panels = math.ceil(total_power_w / panel.p_stc_w)
    min_strings = math.ceil(num_panels / string_voltage_limits(inverter, panel)[1])
    max_strings = math.floor(num_panels / string_voltage_limits(inverter, panel)[0])
    return num_panels, min_strings, max_strings

def check_mppt_current(inverter: inverterSpecs, panel: PanelSpecs, num_panels_per_string: int, num_strings: int):
    total_current_a = panel.imp_a * num_strings
    return total_current_a <= inverter.mppt_max_current_a

def system_size(loads, panel: PanelSpecs, inverter: inverterSpecs, battery: BatterySpecs, site: siteSpecs):
    daily_energy_wh = calculate_daily_energy_consumption(loads)
    panel_output_w = calculate_panel_output(panel, site)
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
