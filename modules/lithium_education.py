"""
Lithium Battery & Cell Educational Module
Teaches fundamentals about how to install and operate a lithium ion battery modules
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

    # NOTE (2026-02): Fundamentals content has been updated to Module 1
    # "Introduction to Energy Storage & Modern Energy Systems".
    # The previous cell-behavior fundamentals were removed to avoid content mixups.
    MODULE_1_FUNDAMENTALS = {
        "module_title": "MODULE 1 - Introduction to Energy Storage & Modern Energy Systems",
        "module_subtitle": "Core concepts installers need before tools, cables, or settings.",
        "sections": [
            {
                "title": "Contents",
                "bullets": [
                    "1.1 Module 1 Learning Outcomes",
                    "1.2 Why Energy Storage Matters in South Africa",
                    "1.3 Power vs Energy — The Most Important Concept",
                    "1.4 How to Calculate Backup Requirements",
                    "1.5 AC vs DC — How Electricity Moves Through the System",
                    "1.6 Core Components of a Modern Energy System",
                    "1.7 How Lithium Batteries Fit into the System",
                    "1.8 The Four Main System Types",
                    "1.9 Energy Flow and System Operation",
                    "1.10 Efficiency and System Losses",
                    "1.11 Where REVOV Fits into these Systems",
                ],
            },
            {
                "title": "1.1 Module 1 Learning Outcomes",
                "paragraphs": [
                    "Before you start working with systems, it's important to understand the \"language\" of energy storage. This module lays the foundation for everything that follows — from system design and sizing through to installation, configuration, and long-term maintenance.",
                    "Think of this as your baseline knowledge. If you understand this module well, the rest of the training becomes much easier and far more practical.",
                    "By the end of this module, you will be able to:",
                ],
                "bullets": [
                    "Explain why energy storage is critical in South Africa",
                    "Clearly differentiate between power (kW) and energy (kWh)",
                    "Understand AC vs DC and how conversion happens",
                    "Identify the core system components and what each one does",
                    "Understand where batteries fit into the system",
                    "Describe the four main system types",
                    "Perform a basic backup sizing calculation",
                    "Recognise how energy flows through a modern system",
                    "Understand where system losses happen and how to reduce them",
                ],
            },
        ],
    }

    MODULE_1_ASSESSMENT = {
        "title": "Module 1 Assessment",
        "questions": [
            {
                "question": "1. Why has energy storage become so important in South Africa?",
                "options": [
                    "A) Because solar panels only work at night",
                    "B) Because the grid is stable and predictable",
                    "C) Because loadshedding, poor grid reliability and rising tariffs affect homes and businesses",
                    "D) Because batteries replace all electrical infrastructure"
                ],
                "answer": "C"
            },
        ]
    }

    MODULE_2_ELECTRICAL_FUNDAMENTALS = {
        "module_title": "MODULE 2 – Electrical Fundamentals",
        "sections": []
    }

MODULE_2_ASSESSMENT = {
    "title": "Module 2 Assessment",
    "questions": []
}

MODULE_3_BATTERY_FUNDAMENTALS = {
    "module_title": "MODULE 3 — Battery Fundamentals",
    "sections": []
}

MODULE_3_ASSESSMENT = {
    "title": "Module 3 Assessment",
    "questions": []
}

MODULE_4_BMS = {
    "module_title": "MODULE 4 — The Battery Management System (BMS)",
    "sections": []
}

MODULE_4_ASSESSMENT = {
    "title": "Module 4 Assessment",
    "questions": []
}

MODULE_5_ENERGY_SYSTEM_DESIGN = {
    "module_title": "MODULE 5 — Energy System Design & Sizing",
    "sections": []
}

MODULE_5_ASSESSMENT = {
    "title": "Module 5 Assessment",
    "questions": []
}

MODULE_6_INSTALLATION_WIRING = {
    "module_title": "MODULE 6 — REVOV System Installation, Wiring & Integration",
    "sections": []
}

MODULE_6_ASSESSMENT = {
    "title": "Module 6 Assessment",
    "questions": []
}

MODULE_7_SYSTEM_CONFIG = {
    "module_title": "MODULE 7 — System Configuration, Communication & Firmware",
    "sections": []
}

MODULE_7_ASSESSMENT = {
    "title": "Module 7 Assessment",
    "questions": []
}

MODULE_8_MONITORING_TROUBLESHOOTING = {
    "module_title": "MODULE 8 — Monitoring, Optimisation, Troubleshooting & Fault Finding",
    "module_subtitle": "How to monitor, diagnose, optimise and maintain systems",
    "sections": [
        {
            "title": "8.1 Module Learning Outcomes",
            "paragraphs": [
                "This module focuses on how to monitor system behaviour, identify abnormal operation, diagnose faults, optimise performance, maintain system health, and troubleshoot problems using a structured approach.",
                "By the end of this module, you will be able to:",
            ],
            "bullets": [
                "Understand the role of monitoring in modern lithium systems",
                "Use monitoring data to assess system performance",
                "Identify early warning signs before major faults occur",
                "Understand normal and abnormal system behaviour",
                "Diagnose faults using a structured troubleshooting process",
                "Break systems into logical sections during fault finding",
                "Understand common real-world faults and behaviours",
                "Perform routine maintenance and system inspections",
                "Optimise settings for better efficiency and battery lifespan",
                "Understand seasonal and usage-related system changes",
                "Use monitoring data to guide troubleshooting decisions",
                "Reduce unnecessary call-outs through proactive system management",
                "Communicate faults and system behaviour clearly to customers",
            ],
        },
        {
            "title": "8.2 Why Monitoring Matters",
            "paragraphs": [
                "Modern lithium systems are intelligent energy systems.",
                "Monitoring allows installers to understand system behaviour and identify problems early.",
            ],
        },
        {
            "title": "8.17 Remote Monitoring & Proactive Support",
            "paragraphs": [
                "Professional installers increasingly use remote monitoring before visiting site.",
                "Remote monitoring allows reviewing fault history, analysing charging behaviour, and checking system trends.",
            ],
            "images": [
                {
                    "src": "images/wrapping up module 8.png",
                    "alt": "",
                },
            ],
        },
    ],
}

MODULE_8_ASSESSMENT = {
    "title": "Module 8 Assessment",
    "subtitle": "Configuration, Monitoring, Maintenance & Troubleshooting",
    "questions": [
        {
            "question": "1. The main purpose of system configuration is to:",
            "options": [
                "A) Increase solar panel size",
                "B) Ensure all system components operate together correctly",
                "C) Reduce battery weight",
                "D) Increase cable length",
            ],
            "answer": "B",
            "explanation": "Configuration ensures all components operate together as an intelligent integrated system.",
        },
    ]
}

MODULE_9_ECOSYSTEM_AND_PRODUCT_RANGE = {
    "module_title": "MODULE 9 — REVOV Ecosystem, Product Range & Installer Best Practices",
    "sections": []
}

MODULE_10_INSTALLER_GUIDES_AND_RESOURCES = {
    "module_title": "MODULE 10 — Installer Guides & Resources",
    "sections": []
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
        }
    
    @staticmethod
    def dod_explanation() -> Dict:
        """Explain Depth of Discharge and its impact"""
        return {
            "definition": "DOD is the percentage of a battery's capacity that has been discharged",
        }
    
    @staticmethod
    def calculate_cycle_life(chemistry: CellChemistry, dod_percent: int, base_cycles: int) -> int:
        """Estimate cycle life based on DOD"""
        return int(base_cycles * 1.0)


class CRate:
    """Educational module about C-rates and charging/discharging"""
    
    @staticmethod
    def crate_explanation() -> Dict:
        """Explain what C-rate means"""
        return {
            "definition": "C-rate is the charging/discharging current relative to the cell's capacity",
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
        return 0.95


class BatteryLifeAndCycles:
    """Educational module about cycle life and battery aging"""
    
    @staticmethod
    def cycle_definition() -> Dict:
        """Explain what a battery cycle is"""
        return {
            "definition": "One complete charge-discharge cycle from 0% to 100% and back to 0%",
        }
    
    @staticmethod
    def get_cycle_life_estimate(chemistry: CellChemistry, dod: int) -> Dict:
        """Get cycle life estimates for different chemistries at different DOD"""
        return {
            "chemistry": chemistry.value,
            "dod": f"{dod}%",
        }
    
    @staticmethod
    def degradation_factors() -> Dict:
        """Explain what causes battery degradation"""
        return {
            "main_factors": {
                "cycling": "Charge/discharge cycles cause structural changes",
            }
        }
