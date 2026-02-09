"""
Lithium Battery & Cell Educational Module
Teaches fundamentals about lithium cells and battery packs
"""

from dataclasses import dataclass
from enum import Enum
from typing import Dict, List, Tuple
import math


class CellChemistry(Enum):
    """Supported lithium chemistry types"""
    LI_ION = "Li-ion"
    LIFEPO4 = "LiFePO4"
    LI_POLYMER = "Li-Po"
    NCA = "NCA"
    NCM = "NCM"


@dataclass
class CellSpecifications:
    """Standard cell specifications"""
    nominal_voltage_v: float  # Typical: 3.7V (Li-ion), 3.2V (LiFePO4)
    capacity_mah: float
    chemistry: CellChemistry
    min_voltage_v: float  # Cutoff voltage (typically 2.5-3.0V)
    max_voltage_v: float  # Charge complete (typically 4.2V or 3.65V)
    
    def voltage_range(self) -> float:
        """Total usable voltage range"""
        return self.max_voltage_v - self.min_voltage_v
    
    def energy_wh(self) -> float:
        """Cell energy in watt-hours"""
        return (self.capacity_mah / 1000) * self.nominal_voltage_v


@dataclass
class CellHealthMetrics:
    """Metrics to assess cell health during operation"""
    voltage_v: float
    capacity_mah: float
    internal_resistance_ohms: float
    cycle_count: int
    temperature_celsius: float
    
    def state_of_charge(self, nominal_min: float, nominal_max: float) -> float:
        """Calculate SOC based on voltage"""
        if self.voltage_v <= nominal_min:
            return 0.0
        elif self.voltage_v >= nominal_max:
            return 100.0
        else:
            soc = ((self.voltage_v - nominal_min) / (nominal_max - nominal_min)) * 100
            return max(0, min(100, soc))
    
    def is_healthy(self, nominal_capacity: float) -> bool:
        """Determine if cell is healthy"""
        capacity_retention = (self.capacity_mah / nominal_capacity) * 100
        return capacity_retention >= 80 and self.internal_resistance_ohms < 150


class LithiumBatteryFundamentals:
    """Educational content about lithium batteries"""
    
    CELL_BEHAVIORS = {
        "good_cell_operation": {
            "title": "Good Cell Behavior During Operation",
            "characteristics": [
                "Smooth, gradual voltage decline during discharge",
                "Consistent capacity across charge cycles",
                "Minimal voltage sag under load",
                "Internal resistance stable over time",
                "Temperature rise modest (< 5°C above ambient)",
                "Quick recovery to open circuit voltage after load"
            ],
            "voltage_profile": "Smooth S-curve from 4.2V to 2.5V"
        },
        
        "bad_cell_detection": {
            "title": "How to Detect a Bad Cell",
            "signs": [
                "Rapid voltage drop under load (high internal resistance)",
                "Voltage doesn't recover after rest (dead short)",
                "Lower capacity than expected (< 80% of nominal)",
                "Excessive heat generation (> 10°C above ambient)",
                "Bulging or physical deformation",
                "Erratic voltage readings",
                "Premature voltage cutoff during discharge"
            ],
            "measurements": {
                "open_circuit_voltage": "Should be nominal ± 0.1V",
                "internal_resistance": "Should be < 100 mOhms (fresh cell)",
                "capacity_retention": "Should be > 80% after 500 cycles"
            }
        },
        
        "pack_imbalance": {
            "title": "Cell Imbalance in Packs",
            "low_cell_issues": [
                "Limited by lowest cell (can't fully utilize other cells)",
                "Over-discharge risk during heavy loads",
                "Increased strain on good cells to compensate",
                "Potential for reverse polarity damage"
            ],
            "high_cell_issues": [
                "Over-charge risk if controlled to pack voltage",
                "Early aging of high cell",
                "Potential for thermal runaway in extreme cases"
            ],
            "mitigation": [
                "Cell balancing circuits (passive or active)",
                "Pack management system (BMS) monitoring",
                "Matched cells during pack assembly",
                "Regular capacity checks"
            ]
        }
    }
    
    CHEMISTRY_PROPERTIES = {
        CellChemistry.LI_ION: {
            "description": "Lithium-ion (traditional NMC/NCA based)",
            "nominal_voltage": "3.7V",
            "charge_voltage": "4.2V",
            "discharge_cutoff": "2.5V",
            "cycle_life": "500-1000 cycles",
            "energy_density": "150-250 Wh/kg",
            "advantages": ["High energy density", "Good power delivery", "Widely available"],
            "disadvantages": ["Thermal sensitivity", "Lower cycle life", "Risk of thermal runaway"],
            "ideal_dod": "80%",
            "ideal_temperature": "15-35°C"
        },
        CellChemistry.LIFEPO4: {
            "description": "Lithium Iron Phosphate (safest chemistry)",
            "nominal_voltage": "3.2V",
            "charge_voltage": "3.65V",
            "discharge_cutoff": "2.0V",
            "cycle_life": "2000-3000+ cycles",
            "energy_density": "90-160 Wh/kg",
            "advantages": ["Excellent cycle life", "Very safe", "Stable temperature"],
            "disadvantages": ["Lower energy density", "Lower nominal voltage"],
            "ideal_dod": "90-100%",
            "ideal_temperature": "15-45°C"
        },
        CellChemistry.NCA: {
            "description": "Nickel Cobalt Aluminum (high energy density)",
            "nominal_voltage": "3.7V",
            "charge_voltage": "4.2-4.3V",
            "discharge_cutoff": "2.5V",
            "cycle_life": "500-1000 cycles",
            "energy_density": "200-250 Wh/kg",
            "advantages": ["Highest energy density", "Long shelf life"],
            "disadvantages": ["Expensive", "Thermal risks", "Shorter cycle life"],
            "ideal_dod": "70-80%",
            "ideal_temperature": "20-30°C"
        },
        CellChemistry.LI_POLYMER: {
            "description": "Lithium Polymer (flexible, lightweight)",
            "nominal_voltage": "3.7V",
            "charge_voltage": "4.2V",
            "discharge_cutoff": "2.5V",
            "cycle_life": "300-500 cycles",
            "energy_density": "100-150 Wh/kg",
            "advantages": ["Flexible form factor", "Lightweight", "No liquid electrolyte"],
            "disadvantages": ["Shorter cycle life", "Lower energy density", "More fragile"],
            "ideal_dod": "80%",
            "ideal_temperature": "15-35°C"
        },
        CellChemistry.NCM: {
            "description": "Nickel Cobalt Manganese (balanced performance)",
            "nominal_voltage": "3.7V",
            "charge_voltage": "4.2-4.3V",
            "discharge_cutoff": "2.5V",
            "cycle_life": "1000-2000 cycles",
            "energy_density": "150-220 Wh/kg",
            "advantages": ["Good balance of energy/cycle life", "Safe", "Widely used"],
            "disadvantages": ["Contains cobalt", "Moderate thermal sensitivity"],
            "ideal_dod": "80%",
            "ideal_temperature": "15-35°C"
        }
    }


class CapacityAndDOD:
    """Educational module about Capacity and Depth of Discharge"""
    
    @staticmethod
    def capacity_explanation() -> Dict:
        """Explain what battery capacity means"""
        return {
            "definition": "Capacity is the total amount of charge a cell can store, measured in mAh (milliamp-hours) or Ah (amp-hours)",
            "energy_vs_capacity": {
                "capacity_mah": "Charge quantity (current × time)",
                "energy_wh": "Actual usable energy (capacity × voltage)",
                "formula": "Energy (Wh) = Capacity (Ah) × Nominal Voltage (V)"
            },
            "nominal_vs_practical": {
                "nominal": "Rated capacity under standard conditions (25°C, constant discharge)",
                "practical": "Actual available capacity varies with temperature, discharge rate, and age"
            },
            "factors_affecting_capacity": [
                "Discharge rate (C-rate) - faster discharge = less available capacity",
                "Temperature - cold reduces capacity, heat accelerates aging",
                "Age and cycles - capacity fades over time",
                "Internal resistance - builds up, reducing discharge capability"
            ]
        }
    
    @staticmethod
    def dod_explanation() -> Dict:
        """Explain Depth of Discharge and its impact"""
        return {
            "definition": "DOD is the percentage of a battery's capacity that has been discharged, expressed as a percentage of total capacity",
            "dod_vs_soc": {
                "dod": "How much was used (100% - SOC)",
                "soc": "How much is currently stored (0-100%)",
                "relationship": "DOD + SOC = 100%"
            },
            "cycle_life_impact": {
                "explanation": "Deeper discharges accelerate aging, shallower discharges extend cycle life",
                "examples": {
                    "100_percent_dod": {
                        "dod": "100% (fully discharged each cycle)",
                        "lifepo4_cycles": "2000 cycles",
                        "liion_cycles": "500 cycles"
                    },
                    "80_percent_dod": {
                        "dod": "80% (leave 20% charged)",
                        "lifepo4_cycles": "2500 cycles (25% improvement)",
                        "liion_cycles": "700 cycles (40% improvement)"
                    },
                    "50_percent_dod": {
                        "dod": "50% (use only middle range)",
                        "lifepo4_cycles": "4000+ cycles",
                        "liion_cycles": "1200+ cycles"
                    }
                }
            },
            "practical_recommendations": {
                "everyday_use": "Keep between 20-80% SOC (80% DOD) for longevity",
                "critical_applications": "Never go below 10% or above 90%",
                "lifepo4_advantage": "Can safely do 100% DOD, better for energy storage systems"
            }
        }
    
    @staticmethod
    def calculate_cycle_life(chemistry: CellChemistry, dod_percent: int, base_cycles: int) -> int:
        """Estimate cycle life based on DOD"""
        dod_multipliers = {
            100: 1.0,
            80: 1.25,
            60: 1.6,
            50: 2.0,
            40: 2.5,
            20: 4.0
        }
        multiplier = dod_multipliers.get(dod_percent, 1.0)
        return int(base_cycles * multiplier)


class CRate:
    """Educational module about C-rates and charging/discharging"""
    
    @staticmethod
    def crate_explanation() -> Dict:
        """Explain what C-rate means"""
        return {
            "definition": "C-rate is the charging/discharging current relative to the cell's capacity",
            "formula": "C-rate = Current (A) / Capacity (Ah)",
            "examples": {
                "1c": {
                    "description": "1C rate (standard rate)",
                    "meaning": "Discharge cell in exactly 1 hour",
                    "example": "2000 mAh cell at 1C = 2000 mA = 2A current"
                },
                "2c": {
                    "description": "2C rate (fast discharge)",
                    "meaning": "Discharge cell in 30 minutes",
                    "example": "2000 mAh cell at 2C = 4000 mA = 4A current"
                },
                "0_5c": {
                    "description": "0.5C rate (slow discharge)",
                    "meaning": "Discharge cell in 2 hours",
                    "example": "2000 mAh cell at 0.5C = 1000 mA = 1A current"
                }
            },
            "impact_on_capacity": {
                "lower_crate": "Slower discharge = more capacity available",
                "higher_crate": "Faster discharge = less capacity available (internal resistance losses)"
            }
        }
    
    @staticmethod
    def calculate_discharge_time(capacity_mah: float, current_ma: float) -> float:
        """Calculate discharge time in hours"""
        if current_ma <= 0:
            return 0
        return capacity_mah / current_ma
    
    @staticmethod
    def calculate_crate(current_a: float, capacity_ah: float) -> float:
        """Calculate C-rate"""
        if capacity_ah <= 0:
            return 0
        return current_a / capacity_ah
    
    @staticmethod
    def get_capacity_derating(crate: float, chemistry: CellChemistry) -> float:
        """Get capacity deration factor based on C-rate"""
        # Higher C-rates result in lower available capacity
        crate_derating = {
            CellChemistry.LI_ION: {
                0.2: 1.0,
                0.5: 0.98,
                1.0: 0.95,
                2.0: 0.90,
                5.0: 0.75
            },
            CellChemistry.LIFEPO4: {
                0.2: 1.0,
                0.5: 0.99,
                1.0: 0.98,
                2.0: 0.96,
                5.0: 0.88
            }
        }
        
        rates = crate_derating.get(chemistry, {})
        if crate <= 0.2:
            return rates.get(0.2, 1.0)
        elif crate >= 5.0:
            return rates.get(5.0, 0.7)
        else:
            # Linear interpolation between known points
            return 0.95


class BatteryLifeAndCycles:
    """Educational module about cycle life and battery aging"""
    
    @staticmethod
    def cycle_definition() -> Dict:
        """Explain what a battery cycle is"""
        return {
            "definition": "One complete charge-discharge cycle from 0% to 100% and back to 0%",
            "variations": {
                "full_cycle": "Complete 0% → 100% → 0%",
                "partial_cycles": "20% → 80% counts as 0.6 of a cycle",
                "example": "If you charge from 20% to 80% and back to 20%, that's 0.6 cycles"
            },
            "cycle_counting": [
                "Total cycles is cumulative over life of battery",
                "End of life typically defined as 80% of original capacity",
                "Each battery chemistry has different cycle life expectations"
            ]
        }
    
    @staticmethod
    def get_cycle_life_estimate(chemistry: CellChemistry, dod: int) -> Dict:
        """Get cycle life estimates for different chemistries at different DOD"""
        base_cycles = {
            CellChemistry.LI_ION: 800,
            CellChemistry.LIFEPO4: 2500,
            CellChemistry.LI_POLYMER: 500,
            CellChemistry.NCA: 800,
            CellChemistry.NCM: 1000
        }
        
        cycles = CapacityAndDOD.calculate_cycle_life(chemistry, dod, base_cycles.get(chemistry, 500))
        
        return {
            "chemistry": chemistry.value,
            "dod": f"{dod}%",
            "estimated_cycles": cycles,
            "years_at_daily_cycle": cycles,  # Rough estimate
            "calendar_years": f"5-10 years (depends on storage conditions)"
        }
    
    @staticmethod
    def degradation_factors() -> Dict:
        """Explain what causes battery degradation"""
        return {
            "main_factors": {
                "cycling": "Charge/discharge cycles cause structural changes",
                "temperature": "Heat accelerates degradation (primary factor)",
                "voltage_stress": "Operating at limits (too high/low voltage) stresses cell",
                "time": "Calendar aging even without use",
                "overcharging": "Charging above max voltage damages material",
                "over_discharge": "Discharging below min voltage causes plating"
            },
            "degradation_mechanisms": [
                "SEI layer growth - solid electrolyte interphase thickens",
                "Electrolyte decomposition - loss of ion conductivity",
                "Active material loss - cathode and anode particles dissolve",
                "Electrode cracking - repeated expansion/contraction"
            ],
            "mitigation_strategies": [
                "Keep cool (store at 15-25°C, avoid >35°C)",
                "Limit charge voltage (keep below max)",
                "Avoid deep discharges (use 20-80% SOC range)",
                "Consistent C-rates (avoid extreme currents)",
                "Regular use (better than long storage)",
                "Cell balancing in packs"
            ]
        }
