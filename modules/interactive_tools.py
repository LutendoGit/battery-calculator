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
        """Quiz on capacity and DOD"""
        return [
            {
                "question": "What does 80% DOD mean?",
                "options": [
                    "The battery is 80% charged",
                    "80% of the capacity has been used in this cycle",
                    "The battery is 80% discharged",
                    "The battery can do 80% of its rated cycles"
                ],
                "correct": 1,
                "explanation": "DOD (Depth of Discharge) is the percentage of capacity that has been used. 80% DOD means 20% SOC remains."
            },
            {
                "question": "Which relationship between SOC and DOD is correct?",
                "options": [
                    "SOC + DOD = 50%",
                    "SOC + DOD = 100%",
                    "SOC = DOD",
                    "SOC = 100% - (2 × DOD)"
                ],
                "correct": 1,
                "explanation": "SOC is the remaining charge percentage, DOD is the used percentage, so SOC + DOD = 100%."
            },
            {
                "question": "Capacity in mAh is best described as…",
                "options": [
                    "Energy (power × time)",
                    "Charge quantity (current × time)",
                    "Voltage (potential difference)",
                    "Resistance (opposition to current)"
                ],
                "correct": 1,
                "explanation": "mAh (or Ah) is charge: current × time. Energy depends on voltage too (Wh = Ah × V)."
            },
            {
                "question": "A 2.0Ah cell at 3.7V nominal contains approximately how much energy?",
                "options": [
                    "2.0 Wh",
                    "3.7 Wh",
                    "7.4 Wh",
                    "13.7 Wh"
                ],
                "correct": 2,
                "explanation": "Energy (Wh) ≈ Capacity (Ah) × Voltage (V) = 2.0 × 3.7 = 7.4 Wh."
            },
            {
                "question": "Which factor usually REDUCES practical capacity compared to the rated (nominal) capacity?",
                "options": [
                    "Warm temperature around 25°C",
                    "Slower discharge (lower C-rate)",
                    "Cold temperature",
                    "Resting the cell after discharge"
                ],
                "correct": 2,
                "explanation": "Cold temperature increases internal resistance and reduces effective capacity and power delivery."
            },
            {
                "question": "What generally happens to cycle life when you reduce DOD from 100% to 80%?",
                "options": [
                    "Cycle life decreases",
                    "Cycle life increases",
                    "Cycle life is unchanged",
                    "Cycle life becomes unpredictable"
                ],
                "correct": 1,
                "explanation": "Shallower cycles reduce stress on electrodes, typically increasing cycle life."
            },
            {
                "question": "If you cycle a LiFePO4 cell at 100% DOD, how many cycles does it typically get?",
                "options": ["500 cycles", "1000 cycles", "2000 cycles", "5000 cycles"],
                "correct": 2,
                "explanation": "LiFePO4 cells can handle 2000+ cycles at 100% DOD due to their stable chemistry."
            },
            {
                "question": "If a battery is at 30% SOC, what is its DOD?",
                "options": ["30%", "70%", "130%", "Depends on chemistry"],
                "correct": 1,
                "explanation": "DOD = 100% − SOC, so 100 − 30 = 70% DOD."
            },
            {
                "question": "Why is 'Wh' often a better comparison than 'mAh' when comparing different batteries?",
                "options": [
                    "Because Wh includes voltage and represents energy",
                    "Because Wh ignores voltage and represents charge",
                    "Because mAh is only used for lead-acid",
                    "Because Wh is always larger than mAh"
                ],
                "correct": 0,
                "explanation": "Two packs can have the same mAh but different voltage; Wh captures total energy."
            },
            {
                "question": "How can you extend battery cycle life?",
                "options": [
                    "Keep it always fully charged",
                    "Use shallower DOD (e.g., 80% instead of 100%)",
                    "Discharge it completely each cycle",
                    "Keep it at very high temperature"
                ],
                "correct": 1,
                "explanation": "Shallower DOD reduces stress on the battery, extending cycle life significantly."
            },
            {
                "question": "Which is the most accurate statement about rated capacity?",
                "options": [
                    "It is always achieved in real use",
                    "It is measured under standard conditions and can vary with temperature, C-rate, and aging",
                    "It is the same as internal resistance",
                    "It depends only on pack configuration (series vs parallel)"
                ],
                "correct": 1,
                "explanation": "Manufacturers rate capacity under standard test conditions; real-world capacity depends on conditions and cell age."
            }
        ]
    
    @staticmethod
    def quiz_crate() -> List[Dict]:
        """Quiz on C-rates"""
        return [
            {
                "question": "What is the C-rate for a 2000mAh cell discharging at 1A current?",
                "options": ["0.5C", "1C", "2C", "0.25C"],
                "correct": 0,
                "explanation": "C-rate = Current / Capacity. 1A / 2A (2000mAh = 2Ah) = 0.5C"
            },
            {
                "question": "A 3Ah cell discharged at 6A is operating at approximately…",
                "options": ["0.5C", "1C", "2C", "6C"],
                "correct": 2,
                "explanation": "C-rate = I / Ah = 6A / 3Ah = 2C."
            },
            {
                "question": "What does a 1C discharge rate mean (idealized)?",
                "options": [
                    "The cell will discharge in about 1 hour",
                    "The cell will discharge in about 10 minutes",
                    "The cell will discharge in about 2 hours",
                    "The cell voltage is 1V"
                ],
                "correct": 0,
                "explanation": "By definition, 1C corresponds to a 1-hour discharge (for an ideal cell at rated capacity)."
            },
            {
                "question": "If you discharge a 2Ah cell at 0.25C, the ideal discharge time is about…",
                "options": ["15 minutes", "30 minutes", "1 hour", "4 hours"],
                "correct": 3,
                "explanation": "Time (hours) ≈ 1 / C-rate = 1 / 0.25 = 4 hours (idealized)."
            },
            {
                "question": "If you discharge a 2000mAh cell at 1C rate, how long until it's empty?",
                "options": ["30 minutes", "1 hour", "2 hours", "4 hours"],
                "correct": 1,
                "explanation": "1C rate means discharge in exactly 1 hour. A 1C rate discharge always takes 1 hour by definition."
            },
            {
                "question": "Which outcome is MOST associated with very high C-rate discharge?",
                "options": [
                    "Less voltage sag and less heat",
                    "More voltage sag and more heat",
                    "No change in voltage sag",
                    "Higher usable capacity than rated"
                ],
                "correct": 1,
                "explanation": "High current increases I×R losses, leading to voltage sag and heating."
            },
            {
                "question": "A 5Ah battery rated for 10A continuous has a continuous C-rate rating of roughly…",
                "options": ["0.2C", "1C", "2C", "10C"],
                "correct": 2,
                "explanation": "C-rate ≈ 10A / 5Ah = 2C continuous."
            },
            {
                "question": "Higher C-rates result in...",
                "options": [
                    "More available capacity",
                    "Less available capacity",
                    "No difference in capacity",
                    "Longer discharge time"
                ],
                "correct": 1,
                "explanation": "Higher C-rates mean faster discharge, which causes more voltage sag and uses less of the total capacity."
            },
            {
                "question": "If a cell has high internal resistance, what will you observe at a given C-rate?",
                "options": [
                    "Less voltage sag",
                    "More voltage sag",
                    "Higher SOC",
                    "Higher nominal voltage"
                ],
                "correct": 1,
                "explanation": "Voltage sag under load increases with resistance: ΔV ≈ I × R."
            },
            {
                "question": "Which is the correct formula for C-rate?",
                "options": [
                    "C-rate = Capacity (Ah) / Current (A)",
                    "C-rate = Current (A) / Capacity (Ah)",
                    "C-rate = Voltage (V) / Capacity (Ah)",
                    "C-rate = Power (W) / Voltage (V)"
                ],
                "correct": 1,
                "explanation": "C-rate is normalized current: Current divided by capacity in Ah."
            },
            {
                "question": "A '2C' charge rate on a 3Ah cell corresponds to approximately…",
                "options": ["1.5A", "3A", "6A", "12A"],
                "correct": 2,
                "explanation": "I = C-rate × Ah = 2 × 3Ah = 6A."
            }
        ]
    
    @staticmethod
    def quiz_cell_health() -> List[Dict]:
        """Quiz on detecting bad cells"""
        return [
            {
                "question": "Which is NOT a sign of a bad cell?",
                "options": [
                    "Rapid voltage drop under load",
                    "Slow, gradual voltage decline during discharge",
                    "Excessive heat (>10°C above ambient)",
                    "Capacity < 80% of nominal"
                ],
                "correct": 1,
                "explanation": "A slow, gradual voltage decline is normal and healthy. Rapid drops and heat are warning signs."
            },
            {
                "question": "A cell that shows a large voltage drop only when a load is applied most likely has…",
                "options": [
                    "Low internal resistance",
                    "High internal resistance",
                    "Higher nominal voltage",
                    "Higher capacity than rated"
                ],
                "correct": 1,
                "explanation": "Under load, voltage sag is largely caused by internal resistance (ΔV ≈ I × R)."
            },
            {
                "question": "What is the best way to detect a weak cell in a pack?",
                "options": [
                    "Visual inspection",
                    "Weight measurement",
                    "Monitor individual cell voltages under load",
                    "Feel the temperature"
                ],
                "correct": 2,
                "explanation": "Monitoring individual cell voltages under load shows voltage sag differences caused by high resistance."
            },
            {
                "question": "In a series pack, why can one weak cell reduce usable pack capacity?",
                "options": [
                    "Series connections increase capacity",
                    "The weakest cell hits voltage cutoff first and limits the pack",
                    "Only the highest-voltage cell matters",
                    "Because temperature sensors average the readings"
                ],
                "correct": 1,
                "explanation": "In series strings, current is the same through all cells; the first cell to reach cutoff limits the whole pack."
            },
            {
                "question": "How much voltage imbalance in a pack is concerning?",
                "options": [
                    "> 0.05V", "> 0.1V", "> 0.2V", "> 0.5V"
                ],
                "correct": 2,
                "explanation": "Voltage imbalance > 0.1-0.2V indicates cell imbalance. > 0.2V requires immediate balancing."
            },
            {
                "question": "Which measurement is MOST useful for estimating state-of-charge (SOC) in a resting lithium cell?",
                "options": [
                    "Open-circuit voltage (after rest)",
                    "Pack label color",
                    "Cell weight",
                    "Wire thickness"
                ],
                "correct": 0,
                "explanation": "After resting, open-circuit voltage is a practical (though imperfect) SOC indicator for lithium chemistries."
            },
            {
                "question": "Which action is generally appropriate when you see large cell-to-cell imbalance in a pack?",
                "options": [
                    "Ignore it; imbalance always self-corrects",
                    "Balance the pack and investigate the weak cell",
                    "Increase discharge current to “even them out”",
                    "Remove the BMS"
                ],
                "correct": 1,
                "explanation": "Significant imbalance should be corrected by balancing and diagnosing the underlying cell issue."
            },
            {
                "question": "A cell that heats much more than others at the same current is often…",
                "options": [
                    "Lower resistance than others",
                    "Higher resistance than others",
                    "Higher capacity than others",
                    "Always safer than others"
                ],
                "correct": 1,
                "explanation": "Extra heat at the same current often indicates higher internal resistance (more I²R loss)."
            },
            {
                "question": "Capacity below about 80% of nominal is commonly used as a threshold for…",
                "options": [
                    "End-of-life / degraded cell",
                    "Brand-new cell",
                    "Perfectly balanced pack",
                    "Fully charged cell"
                ],
                "correct": 0,
                "explanation": "A common health metric is capacity retention; <80% is often considered degraded/end-of-life for many uses."
            },
            {
                "question": "Which is the BEST indicator of a weak cell during a discharge test?",
                "options": [
                    "The cell that stays highest voltage under load",
                    "The cell with the largest voltage sag under load and earliest cutoff",
                    "The cell that is physically largest",
                    "The cell with the newest wrapper"
                ],
                "correct": 1,
                "explanation": "Weak cells show more sag and reach cutoff earlier when stressed."
            }
        ]

    @staticmethod
    def quiz_chemistry() -> List[Dict]:
        """Quiz on lithium cell chemistries"""
        return [
            {
                "question": "Which chemistry is generally known for the best cycle life and stability?",
                "options": ["Li-ion (NMC/NCA)", "LiFePO4", "Li-Po", "NCA"],
                "correct": 1,
                "explanation": "LiFePO4 is widely used where long cycle life and safety are prioritized."
            },
            {
                "question": "Typical nominal voltage of a LiFePO4 cell is closest to…",
                "options": ["2.0V", "3.2V", "3.7V", "4.2V"],
                "correct": 1,
                "explanation": "LiFePO4 nominal voltage is about 3.2V (vs ~3.7V for many Li-ion chemistries)."
            },
            {
                "question": "A common full-charge voltage for many Li-ion (NMC/NCA) cells is…",
                "options": ["3.65V", "4.20V", "4.80V", "2.50V"],
                "correct": 1,
                "explanation": "Many Li-ion cells charge to 4.2V per cell (some variants slightly higher)."
            },
            {
                "question": "If you want maximum energy density (Wh/kg), which chemistry is most likely the best choice?",
                "options": ["LiFePO4", "NCA", "Lead-acid", "NiMH"],
                "correct": 1,
                "explanation": "NCA is commonly associated with very high energy density among lithium chemistries."
            },
            {
                "question": "Which statement is MOST accurate?",
                "options": [
                    "All lithium chemistries have the same charge voltage",
                    "LiFePO4 typically charges to a lower voltage per cell than Li-ion",
                    "LiFePO4 has higher nominal voltage than Li-ion",
                    "Chemistry does not affect safety"
                ],
                "correct": 1,
                "explanation": "LiFePO4 typically uses ~3.65V max vs ~4.2V for many Li-ion cells."
            },
            {
                "question": "Which chemistry is generally considered safer and more thermally stable?",
                "options": ["LiFePO4", "NCA", "Li-Po (generic)", "NMC"],
                "correct": 0,
                "explanation": "LiFePO4 is known for strong thermal stability and reduced thermal runaway risk compared to some high-energy chemistries."
            },
            {
                "question": "Two cells both read 3.7V at rest. Which conclusion is best?",
                "options": [
                    "They have the same SOC regardless of chemistry",
                    "They have the same energy regardless of capacity",
                    "SOC interpretation depends on chemistry and voltage-SOC curve",
                    "They must both be fully charged"
                ],
                "correct": 2,
                "explanation": "Voltage-to-SOC mapping depends on chemistry and the cell's voltage curve, especially for LFP which is flatter."
            },
            {
                "question": "Which chemistry typically has a flatter voltage curve (harder to estimate SOC from voltage alone)?",
                "options": ["LiFePO4", "NCA", "NMC", "Li-ion (general)"] ,
                "correct": 0,
                "explanation": "LiFePO4 has a relatively flat discharge curve across much of its SOC range."
            }
        ]

    @staticmethod
    def quiz_cycles_aging() -> List[Dict]:
        """Quiz on cycles, aging, and degradation"""
        return [
            {
                "question": "What is 'calendar aging'?",
                "options": [
                    "Degradation caused by charge/discharge cycles only",
                    "Degradation over time even without cycling",
                    "A method to count cycles in a BMS",
                    "A test done once per year"
                ],
                "correct": 1,
                "explanation": "Calendar aging is time-based degradation that occurs even if the battery is not actively cycled."
            },
            {
                "question": "What is 'cycle aging'?",
                "options": [
                    "Degradation over time without use",
                    "Degradation driven by charge/discharge cycling",
                    "The same as calendar aging",
                    "Only happens at low temperature"
                ],
                "correct": 1,
                "explanation": "Cycle aging is wear from charging and discharging (throughput, depth, and current matter)."
            },
            {
                "question": "Which operating condition generally accelerates degradation the MOST?",
                "options": [
                    "Moderate temperature and shallow cycles",
                    "High temperature and high SOC storage",
                    "Cool temperature and partial cycles",
                    "Resting at mid-SOC"
                ],
                "correct": 1,
                "explanation": "High temperature and high SOC storage are common accelerators of lithium battery degradation."
            },
            {
                "question": "Reducing DOD from 100% to 50% generally…",
                "options": ["Reduces cycle life", "Increases cycle life", "Has no effect", "Only matters for lead-acid"],
                "correct": 1,
                "explanation": "Shallower cycling usually increases cycle life because it reduces mechanical/chemical stress."
            },
            {
                "question": "Two 50% DOD cycles are approximately equivalent to…",
                "options": ["One 100% DOD equivalent full cycle", "Half a cycle", "Two full cycles", "Zero cycles"],
                "correct": 0,
                "explanation": "Battery wear is often tracked as equivalent full cycles (EFC): 2 × 50% ≈ 1 EFC."
            },
            {
                "question": "Why can very high C-rate discharging reduce usable capacity?",
                "options": [
                    "Because the cell voltage sags and hits cutoff earlier",
                    "Because SOC increases under load",
                    "Because internal resistance becomes zero",
                    "Because voltage rises with higher current"
                ],
                "correct": 0,
                "explanation": "High current increases voltage sag; the cell can reach cutoff voltage before all capacity is used."
            },
            {
                "question": "Which is a good long-term storage practice for many lithium packs?",
                "options": [
                    "Store fully charged at high temperature",
                    "Store near 40–60% SOC in a cool place",
                    "Store at 0% SOC",
                    "Store with no BMS connected"
                ],
                "correct": 1,
                "explanation": "Mid-SOC and cool temperatures typically reduce calendar aging for many lithium chemistries."
            },
            {
                "question": "Internal resistance typically…",
                "options": [
                    "Decreases as the battery ages",
                    "Increases as the battery ages",
                    "Is unrelated to performance",
                    "Only changes with voltage"
                ],
                "correct": 1,
                "explanation": "Internal resistance usually increases with aging, which increases heat and voltage sag under load."
            }
        ]

    @staticmethod
    def quiz_pack_design() -> List[Dict]:
        """Quiz on pack design (series/parallel basics)"""
        return [
            {
                "question": "In a series connection (e.g., 4S), what increases?",
                "options": ["Voltage", "Capacity (Ah)", "Both voltage and capacity", "Neither"],
                "correct": 0,
                "explanation": "Series adds voltage (cell voltages sum). Capacity (Ah) stays roughly the same as one cell."
            },
            {
                "question": "In a parallel connection (e.g., 4P), what increases?",
                "options": ["Voltage", "Capacity (Ah)", "Voltage rating only", "Cell charge voltage"],
                "correct": 1,
                "explanation": "Parallel adds capacity and current capability; voltage stays the same as one cell."
            },
            {
                "question": "A 10S pack using 3.7V nominal cells has a nominal pack voltage of about…",
                "options": ["3.7V", "10V", "37V", "42V"],
                "correct": 2,
                "explanation": "Nominal voltage ≈ 10 × 3.7V = 37V. (42V would be near full charge at 4.2V/cell.)"
            },
            {
                "question": "If one cell in a series string is weak, the pack usable capacity is often limited by…",
                "options": ["The strongest cell", "The weakest cell", "Ambient temperature only", "The charger"],
                "correct": 1,
                "explanation": "In series, all cells carry the same current; the weakest cell hits cutoff first."
            },
            {
                "question": "A 4S2P pack made from 2Ah cells has pack capacity closest to…",
                "options": ["2Ah", "4Ah", "8Ah", "16Ah"],
                "correct": 1,
                "explanation": "Parallel count sets Ah: 2P of 2Ah cells ≈ 4Ah. Series does not increase Ah."
            },
            {
                "question": "Why is cell matching important when building packs?",
                "options": [
                    "To make the pack heavier",
                    "To reduce imbalance and uneven aging",
                    "To increase nominal voltage",
                    "To eliminate the need for a BMS"
                ],
                "correct": 1,
                "explanation": "Similar capacity/resistance cells share load more evenly and reduce imbalance and stress."
            },
            {
                "question": "If a 4S pack is discharged at 20A, what current flows through each series cell (idealized)?",
                "options": ["5A", "10A", "20A", "80A"],
                "correct": 2,
                "explanation": "In series, the same current flows through each cell: 20A through each cell in the string."
            },
            {
                "question": "What does 'energy' of a pack depend on most directly?",
                "options": ["Voltage only", "Capacity (Ah) only", "Voltage and capacity (Wh = V × Ah)", "Connector type"],
                "correct": 2,
                "explanation": "Energy in watt-hours depends on both pack voltage and pack capacity (Ah)."
            }
        ]

    @staticmethod
    def quiz_bms_balancing() -> List[Dict]:
        """Quiz on BMS fundamentals and balancing"""
        return [
            {
                "question": "What is a primary job of a BMS?",
                "options": [
                    "Increase cell nominal voltage",
                    "Protect cells from over-voltage/under-voltage and monitor safety limits",
                    "Replace weak cells automatically",
                    "Charge the battery without a charger"
                ],
                "correct": 1,
                "explanation": "A BMS monitors cell/pack conditions and enforces safety protections (OV/UV, over-current, temperature)."
            },
            {
                "question": "Cell balancing is primarily used to…",
                "options": [
                    "Make the pack voltage higher",
                    "Equalize cell SOC/voltage to prevent one cell from drifting high/low",
                    "Increase cell capacity beyond rating",
                    "Reduce nominal voltage per cell"
                ],
                "correct": 1,
                "explanation": "Balancing reduces cell-to-cell differences so the string can be charged/discharged safely and fully."
            },
            {
                "question": "Passive balancing typically works by…",
                "options": [
                    "Moving charge from high cells to low cells efficiently",
                    "Bleeding energy from higher-voltage cells as heat",
                    "Increasing charger voltage",
                    "Disconnecting the pack permanently"
                ],
                "correct": 1,
                "explanation": "Passive balancing uses resistors to bleed the highest cells, converting extra energy into heat."
            },
            {
                "question": "Active balancing differs from passive balancing because it…",
                "options": [
                    "Only works on LiFePO4",
                    "Transfers energy between cells instead of burning it as heat",
                    "Eliminates the need for cell voltage measurement",
                    "Always balances only at 0% SOC"
                ],
                "correct": 1,
                "explanation": "Active balancing can move energy from higher cells to lower cells with better efficiency."
            },
            {
                "question": "Why is per-cell monitoring important in series packs?",
                "options": [
                    "Pack voltage alone guarantees all cells are safe",
                    "A single cell can overcharge/overdischarge even when pack voltage seems normal",
                    "It is only needed for parallel packs",
                    "It increases energy density"
                ],
                "correct": 1,
                "explanation": "Cells can drift; pack voltage can hide a dangerously high/low individual cell."
            },
            {
                "question": "Which condition most commonly triggers balancing on many consumer-grade BMS boards?",
                "options": [
                    "Mid-SOC during discharge",
                    "Near top-of-charge (higher voltages)",
                    "Only when the pack is empty",
                    "Only when the pack is disconnected"
                ],
                "correct": 1,
                "explanation": "Many BMS designs balance near the top because voltage differences are easier to detect and correct there."
            },
            {
                "question": "A BMS over-current protection is designed to…",
                "options": [
                    "Allow unlimited current",
                    "Disconnect or limit current if current exceeds safe limits",
                    "Increase capacity",
                    "Make balancing faster"
                ],
                "correct": 1,
                "explanation": "Over-current protection prevents overheating, wiring damage, and unsafe operation."
            },
            {
                "question": "If one cell consistently reaches high voltage before others during charge, what is a likely cause?",
                "options": [
                    "That cell has lower capacity than the others",
                    "That cell has infinite capacity",
                    "The pack has too many cells in parallel",
                    "The charger is too small"
                ],
                "correct": 0,
                "explanation": "Lower-capacity cells fill up sooner (reach upper voltage earlier), causing imbalance and limiting pack charge."
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
