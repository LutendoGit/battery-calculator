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
        """Module 1 assessment: Introduction to Energy Storage & Modern Energy Systems."""
        return [
            {
                "question": "Power (kW) determines:",
                "options": [
                    "A) Battery capacity",
                    "B) Inverter size",
                    "C) Solar panel colour",
                    "D) Grid frequency",
                ],
                "correct": 1,
                "explanation": "Power (kW) is the instantaneous demand; it drives inverter sizing so the inverter can supply the peak/continuous load.",
            },
            {
                "question": "Energy (kWh) determines:",
                "options": [
                    "A) Inverter voltage",
                    "B) Cable thickness",
                    "C) Battery bank size",
                    "D) AC frequency",
                ],
                "correct": 2,
                "explanation": "Energy (kWh) is power over time; it determines how much storage is needed in the battery bank to meet the required runtime.",
            },
            {
                "question": "A kettle rated at 2 kW uses:",
                "options": [
                    "A) 2 kWh per minute",
                    "B) 2 kW at that moment",
                    "C) 2 kWh per second",
                    "D) 2 volts",
                ],
                "correct": 1,
                "explanation": "A kW rating tells you the power draw at that moment. Energy (kWh) depends on how long the kettle runs.",
            },
            {
                "question": "If multiple appliances run at the same time, what happens?",
                "options": [
                    "A) Voltage drops automatically",
                    "B) Their kWh adds up",
                    "C) Their kW adds up",
                    "D) Nothing changes",
                ],
                "correct": 2,
                "explanation": "When loads run simultaneously, their power adds (kW). The inverter must be sized to handle the combined power.",
            },
            {
                "question": "In South Africa, standard household AC supply is:",
                "options": [
                    "A) 110 V / 60 Hz",
                    "B) 230 V / 50 Hz",
                    "C) 48 V DC",
                    "D) 400 Hz",
                ],
                "correct": 1,
                "explanation": "South Africa residential mains supply is typically AC around 230 V at 50 Hz.",
            },
            {
                "question": "Solar panels produce:",
                "options": [
                    "A) AC",
                    "B) DC",
                    "C) 3-phase only",
                    "D) Pulsed AC",
                ],
                "correct": 1,
                "explanation": "PV modules generate DC electricity; conversion to AC is done by an inverter.",
            },
            {
                "question": "The inverter converts:",
                "options": [
                    "A) AC to AC",
                    "B) DC to DC",
                    "C) DC to AC (and AC to DC when charging)",
                    "D) Voltage to current",
                ],
                "correct": 2,
                "explanation": "Inverters supply AC loads from DC sources (PV/battery) and typically rectify AC to DC when charging the battery.",
            },
            {
                "question": "Why is understanding AC and DC critical?",
                "options": [
                    "A) It reduces battery cost",
                    "B) It improves sales",
                    "C) It improves installation and fault finding",
                    "D) It changes grid frequency",
                ],
                "correct": 2,
                "explanation": "Knowing which side is AC or DC helps with correct wiring, protection, commissioning, and troubleshooting across conversion stages.",
            },
            {
                "question": "A home runs 1 kW of essential loads for 5 hours. Energy required is:",
                "options": [
                    "A) 1 kWh",
                    "B) 5 kWh",
                    "C) 6 kWh",
                    "D) 10 kWh",
                ],
                "correct": 1,
                "explanation": "Energy (kWh) = Load (kW) × Time (h). 1 kW × 5 h = 5 kWh.",
            },
            {
                "question": "Why should batteries not be sized at 100% discharge?",
                "options": [
                    "A) It increases voltage",
                    "B) It shortens lifespan",
                    "C) It improves efficiency",
                    "D) It increases SOC",
                ],
                "correct": 1,
                "explanation": "Regularly discharging to 100% DoD increases stress and typically reduces lifespan; practical designs keep a reserve and account for losses.",
            },
            {
                "question": "A safe design for 4 kWh required backup would typically recommend:",
                "options": [
                    "A) 4 kWh battery",
                    "B) 5 kWh battery",
                    "C) 8–10 kWh battery",
                    "D) 2 kWh battery",
                ],
                "correct": 2,
                "explanation": "A larger battery (e.g., 8–10 kWh) reduces depth of discharge, provides margin for inefficiencies/surges, and supports longer battery life.",
            },
            {
                "question": "If essential loads total 3 kW, the inverter must be sized based on:",
                "options": [
                    "A) 3 kWh",
                    "B) 3 kW",
                    "C) 48 V",
                    "D) Battery SOC",
                ],
                "correct": 1,
                "explanation": "Inverter sizing is driven by power (kW) because it must supply that load rate at the same time.",
            },
            {
                "question": "REVOV uses which chemistry?",
                "options": [
                    "A) Lead-acid",
                    "B) NMC",
                    "C) LiFePO₄",
                    "D) Gel",
                ],
                "correct": 2,
                "explanation": "REVOV systems use LiFePO₄ (Lithium Iron Phosphate), chosen for safety, stability, and long cycle life.",
            },
            {
                "question": "One full charge and discharge is called:",
                "options": [
                    "A) SOC",
                    "B) DoD",
                    "C) Cycle",
                    "D) Efficiency",
                ],
                "correct": 2,
                "explanation": "A cycle is one full equivalent charge and discharge (not necessarily in one continuous event).",
            },
            {
                "question": "State of Charge (SOC) represents:",
                "options": [
                    "A) Battery temperature",
                    "B) Remaining energy percentage",
                    "C) Maximum voltage",
                    "D) Discharge speed",
                ],
                "correct": 1,
                "explanation": "SOC is the remaining charge/energy in the battery expressed as a percentage.",
            },
            {
                "question": "Depth of Discharge (DoD) measures:",
                "options": [
                    "A) Charging time",
                    "B) Energy used per cycle",
                    "C) Voltage fluctuation",
                    "D) Cable resistance",
                ],
                "correct": 1,
                "explanation": "DoD indicates how much of the battery capacity has been used (discharged) relative to full capacity.",
            },
            {
                "question": "Typical lithium battery round-trip efficiency is:",
                "options": [
                    "A) 70%",
                    "B) 80%",
                    "C) 85%",
                    "D) 93–97%",
                ],
                "correct": 3,
                "explanation": "Lithium systems are high efficiency; typical round-trip (charge-to-discharge) efficiency is roughly in the mid-to-high 90% range.",
            },
            {
                "question": "The BMS is responsible for:",
                "options": [
                    "A) Generating AC",
                    "B) Cooling the inverter",
                    "C) Monitoring and protecting battery cells",
                    "D) Increasing voltage output",
                ],
                "correct": 2,
                "explanation": "A BMS monitors cell voltages/temperature/current and protects the pack by enforcing safe operating limits.",
            },
            {
                "question": "A system with inverter + battery only (no solar) is:",
                "options": [
                    "A) Hybrid",
                    "B) Grid-tied",
                    "C) Backup system",
                    "D) Off-grid",
                ],
                "correct": 2,
                "explanation": "With no PV generation, the system primarily provides backup power from the battery via the inverter.",
            },
            {
                "question": "A grid-tied system without batteries:",
                "options": [
                    "A) Provides backup",
                    "B) Reduces electricity bills only",
                    "C) Works during loadshedding",
                    "D) Is off-grid",
                ],
                "correct": 1,
                "explanation": "Without storage, grid-tied PV mainly offsets consumption to reduce bills; it generally cannot provide backup during outages.",
            },
            {
                "question": "A hybrid system:",
                "options": [
                    "A) Uses generator only",
                    "B) Uses battery only",
                    "C) Combines solar, battery, and grid",
                    "D) Cannot export energy",
                ],
                "correct": 2,
                "explanation": "Hybrid systems integrate PV, battery storage, and the grid so power can flow from multiple sources depending on conditions.",
            },
            {
                "question": "An off-grid system:",
                "options": [
                    "A) Requires Eskom connection",
                    "B) Runs independently of the grid",
                    "C) Cannot use batteries",
                    "D) Is cheaper than hybrid",
                ],
                "correct": 1,
                "explanation": "Off-grid means the site operates independently of the utility grid and relies on PV/generator + batteries for supply.",
            },
            {
                "question": "Most system losses typically occur in:",
                "options": [
                    "A) Solar glass",
                    "B) Wiring insulation",
                    "C) Inverter conversion and cabling",
                    "D) The house DB board only",
                ],
                "correct": 2,
                "explanation": "Major losses are usually from conversion (inverter/charger) and resistive losses in cabling/connectors, especially at high current.",
            },
            {
                "question": "Well-designed systems typically deliver approximately:",
                "options": [
                    "A) 60–70% of PV energy to loads",
                    "B) 75–80%",
                    "C) 90–95%",
                    "D) 100%",
                ],
                "correct": 2,
                "explanation": "A well-designed system typically delivers most of the generated energy to loads, with losses commonly leaving around ~90–95% usable.",
            },
            {
                "question": "Which of the following helps minimise system losses?",
                "options": [
                    "A) Longer cable runs",
                    "B) Undersized conductors",
                    "C) High-efficiency inverters and correct cable sizing",
                    "D) Ignoring firmware updates",
                ],
                "correct": 2,
                "explanation": "Efficient conversion equipment and correctly sized cables reduce conversion losses and I²R heating losses.",
            },
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

    @staticmethod
    def quiz_module_2_assessment() -> List[Dict]:
        """Module 2 assessment: Electrical Fundamentals."""
        return [
            {
                "question": "1. Voltage (V) represents:",
                "options": [
                    "A) Energy stored over time",
                    "B) Electrical pressure",
                    "C) Cable thickness",
                    "D) Resistance",
                ],
                "correct": 1,
                "explanation": "Voltage is the electrical pressure that pushes current through a circuit.",
            },
            {
                "question": "2. Current (A) determines:",
                "options": [
                    "A) Inverter frequency",
                    "B) Battery chemistry",
                    "C) Cable and breaker sizing",
                    "D) Solar panel tilt",
                ],
                "correct": 2,
                "explanation": "Higher current requires correct cable thickness and protective device sizing.",
            },
            {
                "question": "3. Power is calculated using:",
                "options": [
                    "A) V ÷ I",
                    "B) V × I",
                    "C) I × R",
                    "D) P × t",
                ],
                "correct": 1,
                "explanation": "Electrical power is calculated as voltage multiplied by current.",
            },
            {
                "question": "4. Energy (kWh) is calculated using:",
                "options": [
                    "A) Voltage × Current",
                    "B) Current ÷ Voltage",
                    "C) Power × Time",
                    "D) Resistance × Voltage",
                ],
                "correct": 2,
                "explanation": "Energy over time is calculated by multiplying power by time.",
            },
            {
                "question": "5. A 5 kW inverter running at 48 V draws approximately:",
                "options": [
                    "A) 48 A",
                    "B) 104 A",
                    "C) 240 A",
                    "D) 500 A",
                ],
                "correct": 1,
                "explanation": "Current is approximately 5 000 W ÷ 48 V = 104 A.",
            },
            {
                "question": "6. If voltage increases and power stays the same, current will:",
                "options": [
                    "A) Increase",
                    "B) Stay the same",
                    "C) Decrease",
                    "D) Double",
                ],
                "correct": 2,
                "explanation": "For the same power, higher voltage means lower current.",
            },
            {
                "question": "7. Resistance increases when:",
                "options": [
                    "A) Cable length decreases",
                    "B) Cable thickness increases",
                    "C) Cable length increases",
                    "D) Voltage increases",
                ],
                "correct": 2,
                "explanation": "Longer cable runs increase resistance and therefore voltage drop and heating risk.",
            },
            {
                "question": "8. DC is considered less forgiving because:",
                "options": [
                    "A) It changes direction constantly",
                    "B) It produces lower voltage",
                    "C) Polarity errors can cause immediate damage",
                    "D) It cannot carry high current",
                ],
                "correct": 2,
                "explanation": "On DC systems, reverse polarity can damage equipment immediately and DC arcs are harder to interrupt.",
            },
            {
                "question": "9. Most battery-side installation faults occur on:",
                "options": [
                    "A) AC output",
                    "B) Grid connection",
                    "C) DC side",
                    "D) Monitoring software",
                ],
                "correct": 2,
                "explanation": "Battery-side issues usually show up on the DC side through polarity, terminations, cable sizing, or protection problems.",
            },
            {
                "question": "10. AC in South Africa operates at:",
                "options": [
                    "A) 110 V / 60 Hz",
                    "B) 230 V / 50 Hz",
                    "C) 48 V / 50 Hz",
                    "D) 400 V DC",
                ],
                "correct": 1,
                "explanation": "Standard South African household AC supply is about 230 V at 50 Hz.",
            },
            {
                "question": "11. Earth leakage nuisance trips are usually related to:",
                "options": [
                    "A) DC cable size",
                    "B) AC bonding or neutral issues",
                    "C) Battery SOC",
                    "D) PV string voltage",
                ],
                "correct": 1,
                "explanation": "Nuisance tripping is commonly caused by AC-side neutral, bonding, or earthing issues.",
            },
            {
                "question": "12. The inverter in a hybrid system primarily acts as:",
                "options": [
                    "A) A simple DC charger",
                    "B) A voltage regulator only",
                    "C) A traffic controller between AC and DC",
                    "D) A fuse replacement",
                ],
                "correct": 2,
                "explanation": "A hybrid inverter manages power flow between PV, battery, loads, and grid across AC and DC sides.",
            },
            {
                "question": "13. In a series battery connection:",
                "options": [
                    "A) Voltage stays the same",
                    "B) Capacity increases",
                    "C) Voltage increases",
                    "D) Current doubles",
                ],
                "correct": 2,
                "explanation": "In series, voltage adds while capacity stays the same.",
            },
            {
                "question": "14. In a parallel battery connection:",
                "options": [
                    "A) Voltage increases",
                    "B) Capacity increases",
                    "C) Voltage halves",
                    "D) Resistance doubles",
                ],
                "correct": 1,
                "explanation": "In parallel, capacity increases while voltage stays the same.",
            },
            {
                "question": "15. Unequal parallel cable lengths can cause:",
                "options": [
                    "A) Higher efficiency",
                    "B) Equal current sharing",
                    "C) Uneven battery loading",
                    "D) Lower voltage",
                ],
                "correct": 2,
                "explanation": "Different cable lengths create different resistance paths, leading to uneven current sharing.",
            },
            {
                "question": "16. Most REVOV LV systems expand using:",
                "options": [
                    "A) Series only",
                    "B) Parallel only",
                    "C) AC coupling",
                    "D) Step-down transformers",
                ],
                "correct": 1,
                "explanation": "Low-voltage REVOV systems are typically expanded by adding compatible batteries in parallel.",
            },
            {
                "question": "17. Undersized DC cables can cause:",
                "options": [
                    "A) Higher SOC",
                    "B) Voltage drop and overheating",
                    "C) Increased efficiency",
                    "D) Faster charging",
                ],
                "correct": 1,
                "explanation": "Small DC cables increase resistance, which causes voltage drop and heat build-up.",
            },
            {
                "question": "18. A loose DC lug increases:",
                "options": [
                    "A) Voltage",
                    "B) Current",
                    "C) Resistance",
                    "D) Frequency",
                ],
                "correct": 2,
                "explanation": "A poor termination increases resistance and can create heat under load.",
            },
            {
                "question": "19. The main purpose of a DC breaker near the battery is to:",
                "options": [
                    "A) Increase voltage",
                    "B) Protect cables and equipment",
                    "C) Improve efficiency",
                    "D) Boost inverter output",
                ],
                "correct": 1,
                "explanation": "The breaker provides fault protection for the connected conductors and equipment.",
            },
            {
                "question": "20. A DC isolator is important because:",
                "options": [
                    "A) It improves battery lifespan",
                    "B) It allows safe shutdown for maintenance",
                    "C) It increases grid export",
                    "D) It reduces SOC",
                ],
                "correct": 1,
                "explanation": "A DC isolator allows the circuit to be safely disconnected before maintenance or inspection.",
            },
            {
                "question": "21. Before energising a battery connection, you must:",
                "options": [
                    "A) Check SOC",
                    "B) Measure polarity with a multimeter",
                    "C) Increase inverter voltage",
                    "D) Reset the BMS",
                ],
                "correct": 1,
                "explanation": "Always verify polarity with a multimeter before making a live DC connection.",
            },
            {
                "question": "22. Reverse polarity on DC can damage:",
                "options": [
                    "A) AC breakers only",
                    "B) Solar panels only",
                    "C) Internal inverter components",
                    "D) Earth rods",
                ],
                "correct": 2,
                "explanation": "Reverse polarity can damage internal electronics in the inverter or connected DC equipment.",
            },
            {
                "question": "23. A 3 kW load running on a 48 V system draws approximately:",
                "options": [
                    "A) 6 A",
                    "B) 30 A",
                    "C) 62 A",
                    "D) 144 A",
                ],
                "correct": 2,
                "explanation": "Current is approximately 3 000 W ÷ 48 V = 62.5 A, so about 62 A.",
            },
            {
                "question": "24. High current combined with resistance results in:",
                "options": [
                    "A) Cooling",
                    "B) Heat build-up",
                    "C) Higher frequency",
                    "D) Reduced voltage rating",
                ],
                "correct": 1,
                "explanation": "High current through resistance produces heat, which is why cable size and terminations matter.",
            },
            {
                "question": "25. The safest professional practice before working on DC systems is:",
                "options": [
                    "A) Assume system is safe",
                    "B) Work quickly",
                    "C) Isolate, test for dead, and wear PPE",
                    "D) Disconnect the grid only",
                ],
                "correct": 2,
                "explanation": "Safe DC work starts with isolation, confirming the system is de-energised, and using proper PPE.",
            },
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
