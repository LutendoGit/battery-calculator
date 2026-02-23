"""
Interactive Educational Tools and Calculators
Hands-on learning for lithium battery concepts
"""

from dataclasses import dataclass
from typing import Dict, List, Tuple
from modules.lithium_education import CellChemistry, CellSpecifications, CRate, CapacityAndDOD


class CellSimulator:
    """Simulate cell behavior during charge/discharge"""
    
    def __init__(self, cell_spec: CellSpecifications):
        self.spec = cell_spec
        self.current_voltage = cell_spec.nominal_voltage_v
        self.current_soc = 50.0  # Start at 50% SOC
        self.current_capacity = cell_spec.capacity_mah
    
    def discharge(self, current_a: float, duration_hours: float) -> Dict:
        """Simulate discharging the cell"""
        crate = CRate.calculate_crate(current_a, self.spec.capacity_mah / 1000)
        
        # Calculate energy discharged
        energy_discharged_wh = current_a * duration_hours
        nominal_energy_wh = self.spec.energy_wh()
        
        # Calculate new SOC
        soc_decrease = (energy_discharged_wh / nominal_energy_wh) * 100
        new_soc = max(0, self.current_soc - soc_decrease)
        
        # Voltage drops with discharge (simplified curve)
        voltage_range = self.spec.voltage_range()
        soc_ratio = new_soc / 100.0
        new_voltage = self.spec.min_voltage_v + (voltage_range * soc_ratio)
        
        # Add voltage sag (loss due to internal resistance)
        # Higher C-rate = more voltage sag
        voltage_sag = current_a * 0.05 * crate  # Simplified
        new_voltage = max(self.spec.min_voltage_v, new_voltage - voltage_sag)
        
        self.current_voltage = new_voltage
        self.current_soc = new_soc
        
        return {
            "crate": round(crate, 2),
            "energy_discharged_wh": round(energy_discharged_wh, 2),
            "new_soc": round(new_soc, 1),
            "new_voltage": round(new_voltage, 3),
            "voltage_sag_v": round(voltage_sag, 3),
            "time_remaining_hours": self._estimate_remaining_time(current_a),
            "status": "HEALTHY" if new_voltage > self.spec.min_voltage_v else "CUTOFF"
        }
    
    def charge(self, current_a: float, duration_hours: float) -> Dict:
        """Simulate charging the cell"""
        energy_charged_wh = current_a * duration_hours
        nominal_energy_wh = self.spec.energy_wh()
        
        soc_increase = (energy_charged_wh / nominal_energy_wh) * 100
        new_soc = min(100, self.current_soc + soc_increase)
        
        voltage_range = self.spec.voltage_range()
        soc_ratio = new_soc / 100.0
        new_voltage = self.spec.min_voltage_v + (voltage_range * soc_ratio)
        
        # Voltage rise faster near end of charge
        if new_soc > 80:
            new_voltage = self.spec.max_voltage_v * (1 - (100 - new_soc) / 100)
        
        self.current_voltage = min(self.spec.max_voltage_v, new_voltage)
        self.current_soc = new_soc
        
        return {
            "energy_charged_wh": round(energy_charged_wh, 2),
            "new_soc": round(new_soc, 1),
            "new_voltage": round(self.current_voltage, 3),
            "time_to_full_hours": self._estimate_charge_time(),
            "status": "CHARGING" if new_soc < 100 else "FULL"
        }
    
    def _estimate_remaining_time(self, current_a: float) -> float:
        """Estimate remaining discharge time"""
        if current_a <= 0:
            return 0
        energy_remaining_wh = self.current_soc / 100.0 * self.spec.energy_wh()
        return energy_remaining_wh / current_a
    
    def _estimate_charge_time(self) -> float:
        """Estimate remaining charge time"""
        energy_needed_wh = (100 - self.current_soc) / 100.0 * self.spec.energy_wh()
        # Assume 1A charging for estimation
        return energy_needed_wh / 1.0


class PackSimulator:
    """Simulate a battery pack with multiple cells"""
    
    def __init__(self, num_cells: int, cell_spec: CellSpecifications):
        self.num_cells = num_cells
        self.cell_spec = cell_spec
        self.cells = [CellSimulator(cell_spec) for _ in range(num_cells)]
        self.imbalance_factor = 0.0  # 0 = perfect balance, 1 = maximum imbalance
    
    def introduce_imbalance(self):
        """Introduce realistic cell imbalance"""
        # Simulate one cell being weaker (higher resistance, lower capacity)
        if self.num_cells > 1:
            weak_cell_idx = self.num_cells // 2
            self.cells[weak_cell_idx].current_capacity *= 0.85  # 85% capacity
            self.imbalance_factor = 0.15
    
    def discharge_pack(self, pack_current_a: float, duration_hours: float) -> Dict:
        """Discharge entire pack"""
        cell_current_a = pack_current_a / self.num_cells
        
        cell_results = []
        for i, cell in enumerate(self.cells):
            result = cell.discharge(cell_current_a, duration_hours)
            result["cell_id"] = i + 1
            cell_results.append(result)
        
        voltages = [cell.current_voltage for cell in self.cells]
        socs = [cell.current_soc for cell in self.cells]
        
        return {
            "pack_current_a": pack_current_a,
            "pack_voltage_v": round(sum(voltages), 2),
            "avg_soc": round(sum(socs) / len(socs), 1),
            "min_voltage_v": round(min(voltages), 3),
            "max_voltage_v": round(max(voltages), 3),
            "voltage_imbalance_v": round(max(voltages) - min(voltages), 3),
            "cell_results": cell_results,
            "imbalance_detected": max(voltages) - min(voltages) > 0.1,
            "lowest_cell": min(range(len(self.cells)), key=lambda i: self.cells[i].current_voltage) + 1,
            "highest_cell": max(range(len(self.cells)), key=lambda i: self.cells[i].current_voltage) + 1
        }
    
    def get_pack_health(self) -> Dict:
        """Assess overall pack health"""
        capacities = [cell.current_capacity for cell in self.cells]
        voltages = [cell.current_voltage for cell in self.cells]
        
        capacity_retention = sum(capacities) / (self.num_cells * self.cell_spec.capacity_mah) * 100
        voltage_imbalance = max(voltages) - min(voltages)
        
        health_status = "HEALTHY"
        if voltage_imbalance > 0.2:
            health_status = "IMBALANCED - NEEDS BALANCING"
        if capacity_retention < 80:
            health_status = "DEGRADED - REPLACE PACK"
        
        return {
            "num_cells": self.num_cells,
            "pack_voltage_v": round(sum(voltages), 2),
            "avg_cell_voltage": round(sum(voltages) / len(voltages), 3),
            "voltage_imbalance_v": round(voltage_imbalance, 3),
            "capacity_retention_percent": round(capacity_retention, 1),
            "health_status": health_status,
            "weak_cells": [i + 1 for i, cap in enumerate(capacities) if cap < self.cell_spec.capacity_mah * 0.90]
        }


class EducationalQuizzes:
    """Interactive quizzes to test understanding"""
    
    @staticmethod
    def quiz_capacity_dod() -> List[Dict]:
        """Module 1 quiz: Power vs Energy & Backup Sizing"""
        return [
            {
                "question": "Power (kW) is best described as…",
                "options": [
                    "The total electricity used over time (kWh)",
                    "The rate electricity is used right now",
                    "Electrical pressure",
                    "The AC frequency"
                ],
                "correct": 1,
                "explanation": "Power is the instantaneous rate of use and is a key input for inverter sizing."
            },
            {
                "question": "Energy (kWh) is best described as…",
                "options": [
                    "The rate electricity is used right now",
                    "The total electricity stored/used over time",
                    "The current through a cable",
                    "The voltage of the grid"
                ],
                "correct": 1,
                "explanation": "Energy is what determines runtime and battery bank sizing."
            },
            {
                "question": "Which most directly determines inverter size?",
                "options": [
                    "Peak/continuous load power (kW)",
                    "Battery energy (kWh)",
                    "System frequency (Hz)",
                    "Cable color"
                ],
                "correct": 0,
                "explanation": "Inverter sizing is driven by the power demand it must supply."
            },
            {
                "question": "Which most directly determines battery size for backup runtime?",
                "options": [
                    "Energy needed (kWh)",
                    "Load frequency (Hz)",
                    "Inverter brand",
                    "Battery chemistry color"
                ],
                "correct": 0,
                "explanation": "Battery bank size is about kWh required over the outage duration."
            },
            {
                "question": "If essential loads average 1 kW and the outage lasts 4 hours, the energy needed is…",
                "options": ["1 kWh", "4 kWh", "10 kWh", "40 kWh"],
                "correct": 1,
                "explanation": "Energy (kWh) = Load (kW) × Hours. 1 × 4 = 4 kWh."
            },
            {
                "question": "A 10 kWh battery can ideally supply 2 kW for about…",
                "options": ["2 hours", "5 hours", "10 hours", "20 hours"],
                "correct": 1,
                "explanation": "Time ≈ Energy ÷ Power = 10 ÷ 2 = 5 hours (idealized)."
            },
            {
                "question": "If a kettle (2 kW) and microwave (1.2 kW) run at the same time, total power is…",
                "options": ["1.2 kW", "2.0 kW", "3.2 kW", "4.2 kW"],
                "correct": 2,
                "explanation": "Power adds when loads run together: 2.0 + 1.2 = 3.2 kW."
            },
            {
                "question": "Why is it not ideal to size a battery to discharge 100% on every outage?",
                "options": [
                    "Deep discharge generally reduces lifespan and leaves no safety margin",
                    "It increases PV output",
                    "It increases grid frequency",
                    "It changes AC into DC"
                ],
                "correct": 0,
                "explanation": "Practical designs include usable DoD limits and margin for longevity and real-world variation."
            },
            {
                "question": "Which statement is MOST accurate for sizing?",
                "options": [
                    "kW sets inverter size; kWh sets runtime",
                    "kWh sets inverter size; kW sets runtime",
                    "Hz sets runtime; V sets inverter size",
                    "A sets battery size; V sets runtime"
                ],
                "correct": 0,
                "explanation": "Power (kW) is about how much at once; energy (kWh) is about how long."
            },
            {
                "question": "Why do installers often add sizing margin beyond the simple kW×hours calculation?",
                "options": [
                    "DoD limits, efficiency losses, surge loads, and future expansion",
                    "Because AC has no losses",
                    "Because kW and kWh are identical",
                    "Because voltage is the same as current"
                ],
                "correct": 0,
                "explanation": "Real systems have losses and constraints; margin improves reliability and durability."
            }
        ]
    
    @staticmethod
    def quiz_crate() -> List[Dict]:
        """Module 1 quiz: AC vs DC — How Electricity Moves Through the System"""
        return [
            {
                "question": "In South Africa, household wall plugs are supplied with…",
                "options": ["DC at 48 V", "AC at about 230 V, 50 Hz", "AC at 110 V, 60 Hz", "DC at 12 V"],
                "correct": 1,
                "explanation": "Standard residential supply is AC around 230 V at 50 Hz in South Africa."
            },
            {
                "question": "Solar PV panels produce…",
                "options": ["AC power directly", "DC power", "Only reactive power", "Only frequency"],
                "correct": 1,
                "explanation": "PV panels generate DC electricity."
            },
            {
                "question": "Lithium batteries store and deliver…",
                "options": ["AC energy directly", "DC energy", "Only frequency", "Only voltage"],
                "correct": 1,
                "explanation": "Batteries are DC devices; conversion to AC happens in the inverter."
            },
            {
                "question": "The main job of an inverter is to…",
                "options": [
                    "Convert DC (PV/battery) into AC for household loads",
                    "Convert AC into DC only for plugs",
                    "Increase battery capacity",
                    "Change system voltage without losses"
                ],
                "correct": 0,
                "explanation": "Inverters provide AC output for normal household appliances from DC sources."
            },
            {
                "question": "A charger/rectifier function typically converts…",
                "options": ["DC to AC", "AC to DC", "kW to kWh", "Hz to V"],
                "correct": 1,
                "explanation": "Charging a battery requires DC; grid power is AC."
            },
            {
                "question": "What does “50 Hz” mean?",
                "options": ["50 volts", "50 amps", "50 cycles per second", "50% state of charge"],
                "correct": 2,
                "explanation": "Hz is cycles per second; 50 Hz means the AC waveform cycles 50 times each second."
            },
            {
                "question": "Which part of a system is MOST likely DC-only?",
                "options": ["Household plug circuits", "Battery bank", "AC geyser element", "AC DB breakers"],
                "correct": 1,
                "explanation": "Batteries are DC devices; household circuits are typically AC."
            },
            {
                "question": "Why can conversion reduce usable energy compared to battery nameplate kWh?",
                "options": [
                    "Conversion is not 100% efficient and creates losses",
                    "kW and kWh are the same",
                    "AC has no losses",
                    "DC cannot flow in cables"
                ],
                "correct": 0,
                "explanation": "Inverters/chargers and wiring have losses (heat), so delivered energy is usually less than stored energy."
            },
            {
                "question": "Which statement is MOST accurate?",
                "options": [
                    "Grid and household loads are mostly AC; PV and batteries are DC",
                    "Everything in the system is DC",
                    "Everything in the system is AC",
                    "PV panels output AC"
                ],
                "correct": 0,
                "explanation": "Homes primarily use AC, while PV/batteries are DC internally."
            }
        ]
    
    @staticmethod
    def quiz_cell_health() -> List[Dict]:
        """Module 1 quiz: Core Components of a Modern Energy System"""
        return [
            {
                "question": "Which component primarily supplies AC power to household loads?",
                "options": ["Battery bank", "Inverter", "PV panel", "Circuit breaker"],
                "correct": 1,
                "explanation": "The inverter converts DC (battery/PV) into AC for household appliances."
            },
            {
                "question": "The battery bank is mainly sized in…",
                "options": ["kW", "kWh", "Hz", "°C"],
                "correct": 1,
                "explanation": "Battery storage sizing is about energy over time (kWh)."
            },
            {
                "question": "Solar PV panels supply which type of power directly?",
                "options": ["AC", "DC", "Only frequency", "Only voltage"],
                "correct": 1,
                "explanation": "PV panels generate DC power."
            },
            {
                "question": "An MPPT/charge controller is primarily used to…",
                "options": [
                    "Create 50 Hz AC",
                    "Optimize PV power and regulate charging into the battery/DC bus",
                    "Increase battery kWh by software",
                    "Replace breakers"
                ],
                "correct": 1,
                "explanation": "MPPT improves PV harvest and controls charging safely."
            },
            {
                "question": "Why are breakers/fuses and isolators important?",
                "options": [
                    "They increase battery energy",
                    "They provide protection and safe isolation for faults/maintenance",
                    "They convert DC to AC",
                    "They increase inverter kW"
                ],
                "correct": 1,
                "explanation": "Protection devices help prevent damage and allow safe servicing."
            },
            {
                "question": "If essential loads exceed the inverter’s rating, the system will most likely…",
                "options": [
                    "Run normally with no effect",
                    "Overload/trip and shut down the output",
                    "Increase battery capacity",
                    "Increase PV power"
                ],
                "correct": 1,
                "explanation": "Inverters have protection limits; overload typically causes a trip/shutdown."
            },
            {
                "question": "Monitoring (app/display) is mainly used to…",
                "options": [
                    "Make panels generate more sunlight",
                    "See SOC, power flow, alarms, and performance for troubleshooting",
                    "Increase inverter kW",
                    "Replace the battery"
                ],
                "correct": 1,
                "explanation": "Visibility into SOC and power flows makes commissioning and troubleshooting easier."
            },
            {
                "question": "Which statement about cables is MOST accurate?",
                "options": [
                    "Current (A) is used to size cable thickness",
                    "Hz is used to size cable thickness",
                    "kWh is used to size cable thickness",
                    "Cable thickness is unrelated to current"
                ],
                "correct": 0,
                "explanation": "Higher current needs thicker conductors to reduce heating and voltage drop."
            },
            {
                "question": "The distribution board (DB) is mainly where you find…",
                "options": ["Lithium ions", "Protection devices and circuit distribution", "Solar irradiance", "Battery chemistry"],
                "correct": 1,
                "explanation": "The DB handles distribution and protection (breakers, isolators, etc.)."
            }
        ]

    @staticmethod
    def quiz_chemistry() -> List[Dict]:
        """Module 1 quiz: How Lithium-Ion Batteries Work"""
        return [
            {
                "question": "In a lithium-ion battery, energy is stored and released mainly by…",
                "options": [
                    "Water evaporation",
                    "Movement of lithium ions between electrodes",
                    "Changing AC frequency",
                    "Increasing grid voltage"
                ],
                "correct": 1,
                "explanation": "Lithium ions move between anode and cathode during charge/discharge."
            },
            {
                "question": "During charging, lithium ions generally move…",
                "options": ["From anode to cathode", "From cathode to anode", "Out to the grid", "Only through AC cables"],
                "correct": 1,
                "explanation": "Charging drives ions toward the anode; discharge reverses the direction."
            },
            {
                "question": "During discharge, the battery…",
                "options": [
                    "Absorbs energy and SOC increases",
                    "Delivers energy to loads and SOC decreases",
                    "Creates AC frequency",
                    "Increases grid voltage"
                ],
                "correct": 1,
                "explanation": "Discharge means delivering energy to the system; SOC goes down."
            },
            {
                "question": "The separator is important because it…",
                "options": [
                    "Carries electrons freely",
                    "Prevents electrode contact while allowing ions to pass",
                    "Creates AC output",
                    "Increases kWh by itself"
                ],
                "correct": 1,
                "explanation": "The separator reduces short-circuit risk while allowing ionic movement."
            },
            {
                "question": "Why is a BMS important in lithium systems?",
                "options": [
                    "It converts DC to AC",
                    "It monitors and protects the battery within safe limits",
                    "It creates sunlight",
                    "It increases kW rating"
                ],
                "correct": 1,
                "explanation": "A BMS enforces protections (voltage/current/temperature) and supports safe operation."
            },
            {
                "question": "Which statement is a good installer takeaway?",
                "options": [
                    "Voltage alone always tells the full story",
                    "Protections and correct design are essential for safety and lifespan",
                    "BMS is optional in all systems",
                    "Conversion has no losses"
                ],
                "correct": 1,
                "explanation": "Correct design and operating limits matter; real systems have losses and constraints."
            }
        ]

    @staticmethod
    def quiz_cycles_aging() -> List[Dict]:
        """Module 1 quiz: Key Battery Concepts Installers Must Know"""
        return [
            {
                "question": "SOC stands for…",
                "options": ["System Output Capacity", "State of Charge", "Series of Cells", "Standard Operating Condition"],
                "correct": 1,
                "explanation": "SOC is the battery’s remaining charge percentage."
            },
            {
                "question": "DoD (Depth of Discharge) is…",
                "options": ["The percentage of capacity used", "The battery’s nominal voltage", "The AC frequency", "The cable thickness"],
                "correct": 0,
                "explanation": "DoD is how much of the battery capacity has been discharged."
            },
            {
                "question": "Which relationship is correct?",
                "options": ["SOC + DoD = 100%", "SOC × DoD = 100%", "SOC − DoD = 100%", "SOC + DoD = 50%"],
                "correct": 0,
                "explanation": "If 30% SOC remains, 70% DoD has been used: 30 + 70 = 100."
            },
            {
                "question": "A “cycle” generally means…",
                "options": [
                    "One charge/discharge equivalent over time",
                    "One inverter restart",
                    "One hour of loadshedding",
                    "One AC sinewave"
                ],
                "correct": 0,
                "explanation": "Cycles track throughput; several partial cycles can add up to one equivalent full cycle."
            },
            {
                "question": "Round-trip efficiency refers to…",
                "options": [
                    "Energy out divided by energy in (charge + discharge)",
                    "Battery voltage multiplied by current",
                    "The number of AC cycles per second",
                    "Cable thickness"
                ],
                "correct": 0,
                "explanation": "Efficiency describes how much energy you can get back after losses."
            },
            {
                "question": "A BMS primarily helps by…",
                "options": [
                    "Monitoring and protecting the battery within safe limits",
                    "Increasing solar irradiance",
                    "Making the inverter bigger",
                    "Removing the need for breakers"
                ],
                "correct": 0,
                "explanation": "BMS protections include over/under-voltage, over-current, and temperature safeguards."
            },
            {
                "question": "Which statement about kW vs kWh is correct?",
                "options": ["kW is energy; kWh is power", "kW is power; kWh is energy", "Both mean the same thing", "kWh is frequency"],
                "correct": 1,
                "explanation": "kW is how much at once; kWh is how long."
            },
            {
                "question": "Why might delivered usable energy be lower than the battery nameplate kWh?",
                "options": [
                    "Because of conversion and system losses",
                    "Because energy cannot be measured",
                    "Because AC has no losses",
                    "Because kW and kWh are identical"
                ],
                "correct": 0,
                "explanation": "Inverters, wiring, and internal behavior create losses; practical design includes margin."
            }
        ]

    @staticmethod
    def quiz_pack_design() -> List[Dict]:
        """Module 1 quiz: System Types & Energy Flow"""
        return [
            {
                "question": "Which system type can keep loads running during loadshedding using a battery?",
                "options": [
                    "Grid-tied solar with no battery",
                    "Backup/UPS or hybrid system with battery",
                    "PV panels with no inverter",
                    "Grid-only supply"
                ],
                "correct": 1,
                "explanation": "Backup/hybrid systems with batteries can supply loads when the grid is down."
            },
            {
                "question": "Which description best fits an off-grid system?",
                "options": [
                    "Relies on PV + battery (and possibly generator) without needing the grid",
                    "Always exports energy to the grid",
                    "Uses only AC power and no DC",
                    "Cannot use batteries"
                ],
                "correct": 0,
                "explanation": "Off-grid systems are designed to run without a utility connection."
            },
            {
                "question": "A hybrid system typically allows…",
                "options": [
                    "Only grid power",
                    "PV + battery + grid to work together under inverter control",
                    "Only battery with no inverter",
                    "Only DC loads"
                ],
                "correct": 1,
                "explanation": "Hybrid systems coordinate PV, battery, and grid to power loads and optimize usage."
            },
            {
                "question": "When PV production is higher than current household load, excess energy is MOST commonly used to…",
                "options": [
                    "Increase grid frequency",
                    "Charge the battery (if configured) and/or export to grid",
                    "Reduce battery SOC",
                    "Turn AC into DC in the DB"
                ],
                "correct": 1,
                "explanation": "Excess PV can charge batteries and sometimes export to the grid depending on configuration."
            },
            {
                "question": "When PV is low and the grid is available, a hybrid system will typically…",
                "options": [
                    "Stop powering loads",
                    "Use the grid to supply loads (and possibly charge the battery)",
                    "Only power DC loads",
                    "Disable protections"
                ],
                "correct": 1,
                "explanation": "Grid often supplements PV when needed and can charge the battery if configured."
            },
            {
                "question": "Which statement about “grid-tied solar with no battery” is MOST accurate during loadshedding?",
                "options": [
                    "It usually cannot power the home when the grid is down (anti-islanding)",
                    "It always provides full backup",
                    "It charges batteries automatically",
                    "It works without an inverter"
                ],
                "correct": 0,
                "explanation": "Most grid-tied systems shut down when the grid fails to protect line workers."
            },
            {
                "question": "Which flow describes a common backup scenario during an outage?",
                "options": [
                    "Grid → Loads",
                    "Battery (DC) → Inverter → Loads (AC)",
                    "PV → Grid only",
                    "DB → Battery"
                ],
                "correct": 1,
                "explanation": "During outages, the battery supplies DC which the inverter converts to AC for loads."
            },
            {
                "question": "Which is an example of a “backup/UPS” style system?",
                "options": [
                    "Battery + inverter to keep essential loads on when grid fails",
                    "PV panels with no inverter",
                    "Grid-only supply",
                    "A system that exports but has no loads"
                ],
                "correct": 0,
                "explanation": "Backup systems focus on keeping essential loads running during outages."
            }
        ]

    @staticmethod
    def quiz_bms_balancing() -> List[Dict]:
        """Module 1 quiz: Efficiency, System Losses & Where REVOV Fits"""
        return [
            {
                "question": "Round-trip efficiency is best defined as…",
                "options": [
                    "Energy out divided by energy in (including charge + discharge)",
                    "Battery voltage multiplied by current",
                    "The number of AC cycles per second",
                    "The battery’s nameplate capacity"
                ],
                "correct": 0,
                "explanation": "Round-trip efficiency describes how much energy you get back after losses."
            },
            {
                "question": "Which is a common source of system loss?",
                "options": ["Inverter conversion losses", "Making the cable shorter", "Increasing SOC", "Using correct fusing"],
                "correct": 0,
                "explanation": "Conversion electronics and wiring losses reduce delivered usable energy."
            },
            {
                "question": "Why do installers add margin to battery sizing beyond the basic kW×hours calculation?",
                "options": [
                    "To account for DoD limits and losses",
                    "Because voltage becomes power",
                    "Because AC has no losses",
                    "Because kW always equals kWh"
                ],
                "correct": 0,
                "explanation": "Usable energy is reduced by DoD limits and conversion/system losses."
            },
            {
                "question": "Which statement about real systems is MOST accurate?",
                "options": [
                    "All systems are 100% efficient",
                    "Losses mean delivered energy is usually less than stored energy",
                    "Efficiency only matters for DC loads",
                    "Efficiency is the same as frequency"
                ],
                "correct": 1,
                "explanation": "Conversion and wiring losses appear as heat and reduce usable delivered energy."
            },
            {
                "question": "Where does REVOV typically fit in a modern energy system?",
                "options": ["As the battery energy storage component", "As the AC distribution board", "As the PV panels", "As the household plug circuits"],
                "correct": 0,
                "explanation": "REVOV batteries provide storage that the inverter can charge/discharge as part of the system."
            },
            {
                "question": "If your loads need 5 kWh delivered to AC appliances, a safe sizing assumption is…",
                "options": [
                    "Exactly 5 kWh battery is always enough",
                    "You may need more than 5 kWh due to DoD limits and losses",
                    "Battery size depends only on Hz",
                    "Battery size depends only on inverter color"
                ],
                "correct": 1,
                "explanation": "Delivered usable energy must account for conversion losses and usable DoD."
            },
            {
                "question": "Why do efficiency and losses matter in troubleshooting?",
                "options": [
                    "They explain why input and output may not match perfectly",
                    "They guarantee no heat is generated",
                    "They eliminate the need for protection devices",
                    "They make AC become DC"
                ],
                "correct": 0,
                "explanation": "Losses show up as heat/voltage drop and differences between stored vs delivered energy."
            },
            {
                "question": "Which statement best captures the Module 1 “REVOV fit” message?",
                "options": [
                    "Energy storage is core infrastructure; the battery enables backup and solar self-consumption",
                    "Batteries are optional and only cosmetic",
                    "Only PV matters; batteries never help",
                    "Efficiency and losses do not matter"
                ],
                "correct": 0,
                "explanation": "Module 1 positions storage as essential for reliability and savings in modern systems."
            }
        ]


class InteractiveCalculators:
    """Interactive tools for learning calculations"""
    
    @staticmethod
    def capacity_energy_calculator(capacity_mah: float, voltage_v: float) -> Dict:
        """Calculate energy from capacity and voltage"""
        capacity_ah = capacity_mah / 1000
        energy_wh = capacity_ah * voltage_v
        
        return {
            "capacity_mah": capacity_mah,
            "capacity_ah": round(capacity_ah, 3),
            "voltage_v": voltage_v,
            "energy_wh": round(energy_wh, 2),
            "explanation": f"A {capacity_mah}mAh cell at {voltage_v}V contains {round(energy_wh, 2)} Wh of energy"
        }
    
    @staticmethod
    def crate_calculator(current_a: float, capacity_ah: float) -> Dict:
        """Calculate C-rate"""
        crate = CRate.calculate_crate(current_a, capacity_ah)
        discharge_time = current_a / capacity_ah  # Hours (inverse of C-rate)
        
        return {
            "current_a": current_a,
            "capacity_ah": capacity_ah,
            "crate": round(crate, 2),
            "discharge_time_hours": round(1 / crate, 2) if crate > 0 else 0,
            "explanation": f"A {current_a}A discharge from a {capacity_ah}Ah cell = {round(crate, 2)}C rate"
        }
    
    @staticmethod
    def cycle_life_calculator(chemistry: CellChemistry, dod_percent: int) -> Dict:
        """Calculate expected cycle life"""
        base_cycles = {
            CellChemistry.LI_ION: 800,
            CellChemistry.LIFEPO4: 2500,
            CellChemistry.LI_POLYMER: 500,
            CellChemistry.NCA: 800,
            CellChemistry.NCM: 1000
        }
        
        cycles = CapacityAndDOD.calculate_cycle_life(chemistry, dod_percent, base_cycles[chemistry])
        
        return {
            "chemistry": chemistry.value,
            "dod_percent": dod_percent,
            "estimated_cycles": cycles,
            "years_at_1_cycle_daily": cycles,
            "explanation": f"{chemistry.value} at {dod_percent}% DOD: ~{cycles:,} cycles"
        }
    
    @staticmethod
    def pack_voltage_calculator(num_cells: int, cell_voltage_v: float, configuration: str = "series") -> Dict:
        """Calculate pack voltage for different configurations"""
        if configuration.lower() == "series":
            pack_voltage = num_cells * cell_voltage_v
        elif configuration.lower() == "parallel":
            pack_voltage = cell_voltage_v
        else:
            pack_voltage = cell_voltage_v
        
        return {
            "num_cells": num_cells,
            "cell_voltage_v": cell_voltage_v,
            "configuration": configuration,
            "pack_voltage_v": round(pack_voltage, 1),
            "explanation": f"{num_cells}S (series) = {round(pack_voltage, 1)}V pack"
        }
