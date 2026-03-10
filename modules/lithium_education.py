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

    # NOTE (2026-02): Fundamentals content has been updated to Module 1
    # "Introduction to Energy Storage & Modern Energy Systems".
    # The previous cell-behavior fundamentals were removed to avoid content mixups.
    MODULE_1_FUNDAMENTALS = {
        "module_title": "MODULE 1 - Introduction to Energy Storage & Modern Energy Systems",
        "module_subtitle": "Core concepts installers need before tools, cables, or settings.",
        "sections": [
            {
                "title": "Contents",
                "icon": "📚",
                "bullets": [
                    "1.1 Module 1 Learning Outcomes",
                    "1.2 Why Energy Storage Matters in South Africa",
                    "1.3 Power vs Energy — The Most Important Concept",
                    "1.4 How to Calculate Backup Requirements",
                    "1.5 AC vs DC — How Electricity Moves Through the System",
                    "1.6 Core Components of a Modern Energy System",
                    "1.7 How Lithium-Ion Batteries Work",
                    "1.8 Key Battery Concepts Installers Must Know",
                    "1.9 The Four Main System Types (Explained Simply)",
                    "1.10 Energy Flow and System Operation",
                    "1.11 Efficiency and System Losses",
                    "1.12 Where REVOV Fits into these Systems",
                ],
            },
            {
                "title": "1.1 Module 1 Learning Outcomes",
                "icon": "🎯",
                "paragraphs": [
                    "This module builds the core knowledge you need before touching tools, cables or settings.",
                    "By the end of this module, you will be able to:",
                ],
                "bullets": [
                    "Explain why energy storage is critical in South Africa",
                    "Clearly differentiate between power (kW) and energy (kWh)",
                    "Understand AC vs DC and how conversion happens",
                    "Identify all core system components and their functions",
                    "Explain how lithium-ion batteries store and release energy",
                    "Describe the four main system types",
                    "Perform a basic backup sizing calculation",
                    "Understand core battery performance concepts (SOC, DoD, Cycles, Efficiency, BMS)",
                    "Recognise energy flow paths and system losses",
                ],
            },
            {
                "title": "1.2 Why Energy Storage Matters in South Africa",
                "icon": "⚡",
                "paragraphs": [
                    "South Africa’s grid is unpredictable, affecting homes and businesses daily.",
                    "Loadshedding, voltage dips, transformer failures and tariff increases are driving rapid adoption of solar and battery systems.",
                ],
                "subsections": [
                    {
                        "heading": "🔋 Battery storage provides:",
                        "bullets": [
                            "Immediate backup during outages",
                            "Protection from voltage fluctuations",
                            "Energy independence from the grid",
                            "Lower electricity costs when paired with solar",
                            "Silent, automatic backup compared to generators",
                        ],
                    },
                    {
                        "heading": "📈 Installer Example",
                        "variant": "installer-example",
                        "paragraphs": [
                            "A small shop loses ±R2 000 per hour when fridges shut down, card machines go offline, security systems drop etc.",
                            "A properly sized 5 kVA inverter with a 10 kWh REVOV battery keeps essentials running and protects revenue.",
                            "Battery storage is no longer a luxury - it is core infrastructure.",
                        ],
                    },
                ],
            },
            {
                "title": "1.3 Power vs Energy — The Most Important Concept",
                "icon": "⚡",
                "paragraphs": [
                    "A clear understanding of power versus energy is the foundation of correct system sizing.",
                ],
                "subsections": [
                    {
                        "heading": "Power (kW)",
                        "paragraphs": [
                            "Power is the rate at which electricity is being used right now. It determines the inverter size.",
                            "Think of power like the width of a water pipe – how much water can flow at one moment.",
                        ],
                        "bullets": [
                            "Kettle = 2 kW",
                            "Microwave = 1.2 kW",
                            "Geyser = 3–4 kW",
                        ],
                        "notes": [
                            "If multiple appliances run at the same time, their kW adds up.",
                        ],
                    },
                    {
                        "heading": "Energy (kWh)",
                        "paragraphs": [
                            "Energy is the total amount of electricity stored or used over time. This determines battery size.",
                            "Think of energy like the size of a water tank – how much water you have stored.",
                            "A 10 kWh REVOV battery can supply:",
                        ],
                        "bullets": [
                            "1 kW for 10 hours",
                            "2 kW for 5 hours",
                            "5 kW for 2 hours",
                        ],
                    },
                    {
                        "heading": "📈 Installer Example",
                        "variant": "installer-example",
                        "paragraphs": [
                            "If a house essential loads average 1 kW and loadshedding lasts 5 hours:",
                        ],
                        "highlights": [
                            "1 kW × 5 hours = 5 kWh of energy is needed",
                        ],
                        "paragraphs_after": [
                            "But … you should never size a battery for 100% discharge.",
                            "The recommended practical design is to install 8 – 10 kWh to: ",
                            "- protect battery lifespan",
                            "- allow for surge loads",
                            "- allow for growth",
                        ],
                    },
                    {
                        "heading": "📐 Quick Comparison Table",
                        "table": {
                            "headers": ["Term", "Meaning", "Measured In", "Installer Understanding"],
                            "rows": [
                                ["Power", "Rate of use", "kW", "Determines inverter size"],
                                ["Energy", "Total stored/used", "kWh", "Determines battery bank size"],
                                ["Voltage", "Electrical pressure", "V", "System compatibility"],
                                ["Current", "Flow of electrons", "A", "Determines cable thickness"],
                            ],
                        },
                    },
                ],
            },
            {
                "title": "1.4 How to Calculate Backup Requirements",
                "icon": "🧮",
                "paragraphs": [
                    "This is one of the most important practical skills in system design.",
                    "A clear method ensures accurate and confident sizing to calculate backup requirements.",
                ],
                "subsections": [
                    {
                        "heading": "Step 1: Identify Essential Loads (kW)",
        
                        "bullets": [
                            "Lights = 0.2 kW",
                            "WiFi + Router = 0.05 kW",
                            "TV = 0.1 kW",
                            "Fridge = 0.2 kW",
                        ],
                        "notes": [
                            "Total essentials example = 1 kW",
                        ],
                    },
                    {
                        "heading": "Step 2: Determine Outage Duration (hours)",
                        "notes": [
                            "Example = 4 hours",
                        ],
                    },
                    {
                        "heading": "Step 3: Calculate the battery size needed",
                        "highlights": [
                            "Battery Size (kWh) = Load (kW) × Hours",
                        ],
                        "subsections": [
                            {
                                "heading": "📈 Installer Example",
                                "variant": "installer-example",
                                "highlights": [
                                    "1 kW × 4 hours = 4 kWh needed",
                                ],
                                "paragraphs": [
                                    "But…",
                                    "You should NEVER size a battery for 100% depth of discharge.",
                                ],
                                "notes": [
                                    "📘 Safe recommended battery: 8–10 kWh REVOV (longer life + future expansion)",
                                ],
                            }
                        ],
                    },
                ],
            },
            {
                "title": "1.5 AC vs DC — How Electricity Moves Through the System",
                "icon": "🔌",
                "paragraphs": [
                    "Modern systems use both AC and DC power. Understanding how they interact is critical for installation and troubleshooting.",
                ],
                "subsections": [
                    {
                        "heading": "🔌 AC (Alternating Current)",
                        "bullets": [
                            "Comes from Eskom/grid",
                            "Powers household plugs",
                            "Operates at 230 V, 50 Hz in South Africa",
                            "Changes direction 50 times per second (50 Hz)",
                        ],
                    },
                    {
                        "heading": "🔋 DC (Direct Current)",
                        "bullets": [
                            "Produced by solar panels",
                            "Stored in batteries",
                            "Flows in one direction",
                            "Used internally by inverters before converting to AC",
                        ],
                    },
                    {
                        "heading": "🔌 Homes run on AC",
                        "paragraphs": [
                            "🔋 Solar panels and batteries operate in DC",
                            "This is why the inverter is essential",
                        ],
                    },
                    {
                        "heading": "⚙️ The Inverter’s Role",
                        "paragraphs": [
                            "The inverter:",
                        ],
                        "bullets": [
                            "Converts DC → AC for loads",
                            "Converts AC → DC when charging batteries",
                            "Controls energy flow between PV, battery and grid",
                        ],
                    },
                    {
                        "image": {
                            "src": "images/Solar + grid integration.png",
                            "alt": "Solar + grid integration diagram",
                        },
                    },
                    {
                        "heading": "🛠️ Installer Tip",
                        "bullets": [
                            "Most wiring faults occur on the DC side.",
                            "Most customer complaints come from the AC side.",
                        ],
                        "notes": [
                            "Understanding both clearly improves fault finding dramatically.",
                        ],
                    },
                ],
            },
            {
                "title": "1.6 Core Components of a Modern Energy System",
                "icon": "🧱",
                "paragraphs": [
                    "Each energy system is made up of key building blocks that work together to generate, store, convert, and deliver power efficiently.",
                    "Every installation includes four stages:",
                ],
                "numbered": [
                    "Generation",
                    "Storage",
                    "Conversion",
                    "Distribution",
                ],
                "subsections": [
                    {
                        "heading": "☀️ PV Array — Generation",
                        "paragraphs": [
                            "Function: Converts sunlight into direct current (DC) electricity.",
                        ],
                        "bullets": [
                            "Efficiency depends on orientation, tilt angle, and shading.",
                            "Proper design ensures maximum energy yield throughout the day.",
                            "Usually installed on rooftops or ground mounts facing north in the Southern Hemisphere.",
                        ],
                    },
                    {
                        "heading": "🔋 Battery Bank — Storage",
                        "paragraphs": [
                            "Function: Stores electrical energy for later use.",
                        ],
                        "bullets": [
                            "LiFePO₄ (Lithium Iron Phosphate) batteries provide high safety, high efficiency (~95%), and long cycle life (6 000+).",
                            "Stores energy during low-demand or high-generation periods.",
                            "Supplies backup power during load-shedding or night-time hours.",
                        ],
                    },
                    {
                        "heading": "⚙️ Inverter — Conversion & Control",
                        "paragraphs": [
                            "Function: Converts DC power from PV or batteries into AC power for use by appliances and the grid.",
                        ],
                        "bullets": [
                            "Acts as the system’s control hub, balancing energy flow between PV, battery, and loads.",
                            "Types include string, hybrid, and off-grid inverters.",
                            "Modern inverters also manage data monitoring, safety isolation, and firmware control.",
                        ],
                    },
                    {
                        "heading": "🏠 Load — Energy Consumption",
                        "paragraphs": [
                            "Function: Represents devices and appliances that consume electrical power.",
                        ],
                        "bullets": [
                            "Includes lighting, electronics, pumps, and industrial machinery.",
                            "Load management ensures balanced and efficient power use.",
                            "Smart load prioritisation can improve battery life and reduce energy costs.",
                        ],
                    },
                    {
                        "heading": "⚡ Grid / Generator",
                        "paragraphs": [
                            "Function: Provides supplemental or backup power when solar or battery capacity is insufficient.",
                        ],
                        "bullets": [
                            "The grid supplies additional power and can export excess energy in grid-tied systems.",
                            "Generators act as off-grid or emergency sources in remote locations.",
                            "Integration requires proper switching and safety compliance (SANS 10142-1).",
                        ],
                    },

                    {
                        "image": {
                            "src": "images/core-components-of-energy-system.png",
                            "alt": "Core components of energy system diagram",
                        },
                    },
                ],
                "notes": [
                    "Now that we understand system basics, let’s look inside the battery itself.",
                ],
            },
            {
                "title": "1.7 How Lithium-Ion Batteries Work",
                "icon": "🧪",
                "paragraphs": [
                    "REVOV systems use Lithium Iron Phosphate (LiFePO₄) lithium-ion chemistry because it combines safety, stability, and long service life — key requirements for residential, commercial, and industrial energy systems.",
                    "Unlike older chemistries such as lead-acid or Nickel-Manganese-Cobalt (NMC), LiFePO₄ cells are thermally stable, non-flammable, and deliver more usable energy across thousands of charge and discharge cycles.",
                ],
                "subsections": [
                    {
                        "image": {
                            "src": "images/How-lithium-works.png",
                            "alt": "How lithium-ion batteries work diagram",
                        },
                    },
                    {
                        "heading": "Cell Structure and Function",
                        "paragraphs": [
                            "A single lithium-ion cell is the smallest working unit of the battery. It contains four main components:",
                        ],
                        "table": {
                            "headers": ["Component", "Description", "Function in Operation"],
                            "rows": [
                                ["Anode (–)", "Usually made of graphite.", "Stores lithium ions during charging; releases them during discharge."],
                                ["Cathode (+)", "Made of lithium iron phosphate (LiFePO₄).", "Releases lithium ions during charging and receives them during discharge."],
                                ["Electrolyte", "A conductive medium, typically a lithium-salt solution.", "Enables ion movement between the anode and cathode inside the cell."],
                                ["Separator", "A porous membrane between anode and cathode.", "Physically prevents short circuits while allowing ions to pass through safely."],
                            ],
                        },
                    },
                    {
                        "image": {
                            "src": "images/Cell-structure-and-functionality.png",
                            "alt": "How lithium-ion batteries work diagram",
                        },
                    },

                    {
                        "heading": "How the Cell Works",
                        "subsections": [
                            {
                                "heading": "Charging",
                                "paragraphs": [
                                    "When the battery receives power from the inverter or PV system, lithium ions move from the cathode to the anode through the electrolyte.",
                                    "Electrons travel in the external circuit to the anode to balance charge, and energy is stored in the cell as chemical potential.",
                                ],
                            },
                            {
                                "heading": "Discharging",
                                "paragraphs": [
                                    "When energy is needed, ions flow back from the anode to the cathode through the electrolyte while electrons travel through the external circuit toward the load, delivering usable DC power.",
                                ],
                                "notes": [
                                    "💡 Think of it as a reversible chemical pump — charging pushes energy in; discharging releases it.",
                                ],
                            },
                        ],
                    },
                    {
                        "heading": "REVOV Cell Configuration",
                        "paragraphs": [
                            "Each LiFePO₄ cell provides a nominal voltage of 3.2 V.",
                            "REVOV batteries combine these cells in series and parallel to achieve system-level voltages of approximately 48–51.2 V, ideal for most hybrid and off-grid inverter systems.",
                        ],
                        "bullets": [
                            "R100 → ~5.12 kWh (16 cells in series)",
                            "R200 → ~10.24 kWh (2 × 16 cell packs in parallel)",
                            "C8 Module → high-density rack unit for scalable BESS installations",
                        ],
                        "paragraphs_after": [
                            "The modular cell design ensures that each REVOV battery maintains stable voltage, balanced performance, and excellent scalability — from a single home backup to a large-scale commercial energy system.",
                        ],
                    },
                    {
                        "heading": "Why LiFePO₄?",
                        "paragraphs": [
                            "A lithium-ion cell stores energy chemically and releases it electrically through the movement of lithium ions.",
                            "The LiFePO₄ composition used by REVOV offers the safest and most durable option available in the market today.",
                        ],
                        "table": {
                            "headers": ["Feature", "Explanation", "Benefit"],
                            "rows": [
                                ["Thermal Stability", "LiFePO₄ does not undergo runaway heating.", "Safer in high-temperature or high-load environments."],
                                ["Long Cycle Life", "Typically 6 000+ full cycles at 80 % DoD.", "Up to 15 years of reliable use."],
                                ["High Efficiency", "~95 % round-trip charge/discharge.", "Less wasted energy."],
                                ["Flat Voltage Curve", "Delivers consistent power output throughout discharge.", "Reliable system performance."],
                                ["Low Environmental Impact", "Contains no cobalt or heavy metals.", "Easier recycling and safer disposal."],
                            ],
                        },
                    },
                ],
            },
            {
                "title": "1.8 Key Battery Concepts Installers Must Know",
                "icon": "🧠",
                "paragraphs": [
                    "Understanding these core terms helps technicians assess battery health, performance, and expected lifespan.",
                    "Each parameter plays a key role in how effectively the system stores and delivers energy.",
                ],
                "subsections": [
                    {
                        "heading": "🔁 Cycle",
                        "paragraphs": [
                            "A cycle refers to one complete process of charging the battery and then discharging it.",
                            "A battery rated for “6000 cycles” can perform roughly 6000 full charge–discharge events before its capacity drops to about 80% of original.",
                        ],
                        "highlights": [
                            "Example: Charging from 20% → 100% and discharging back to 20% equals one full cycle.",
                            
                       
                        ],
                         "bullets": [
                            "Daily cycling under normal conditions provides 10–15 years of service life for REVOV LiFePO₄ batteries.",
                        ]

                          
                        
                    },
                    {
                        "image": {
                            "src": "images/Cycle.png",
                            "alt": "How lithium-ion batteries work diagram",
                        },
                    },

                    {
                        "heading": "⚡ State of Charge (SOC)",
                        "paragraphs": [
                            "The State of Charge shows how much energy remains in the battery, expressed as a percentage of its total capacity.",
                            "Think of SOC as the “fuel gauge” of the battery — showing how full or empty it is.",
                        ],
                        "highlights": [
                            "Example: If a 10 kWh battery shows an SOC of 60%, it still holds 6 kWh of usable energy.",
                           
                        ],
                        "bullets": [ 
                             "Monitored continuously by the Battery Management System (BMS).",
                             "Ideal operating range for lithium-ion: 20% – 90% SOC to extend lifespan.",
                        ],
                    

                    },
                    {
                        "image": {
                            "src": "images/State-of-Charge(SOC).png",
                            "alt": "How lithium-ion batteries work diagram",
                        },
                    },
                    {
                        "heading": "🔋 Depth of Discharge (DoD)",
                        "paragraphs": [
                            "The Depth of Discharge measures how much of the battery’s capacity is used during one cycle, expressed as a percentage.",
                        ],
                        "highlights": [
                            "Example: Using 8 kWh from a 10 kWh battery means a DoD of 80%. The deeper the discharge, the shorter the overall lifespan.",
                           
                        ],
                        "bullets": [
                             
                            "Limiting DoD to 80–90% helps protect lithium-ion cells.",
                            "Most BMS systems automatically prevent over-discharge for safety.",
                        ],
                


                    },
                    {  "image": {
                            "src": "images/Depth-of-discharge(DOD).png",
                            "alt": "Depth of Discharge (DoD) diagram"

                    },

                    },
                    {
                        "heading": "⚙️ Efficiency",
                        "paragraphs": [
                            "Battery efficiency measures how much of the stored energy can be recovered during discharge compared to what was put in during charging.",
                        ],
                        "highlights": [
                            "Example: If 10 kWh is charged into the battery and 9.5 kWh is discharged, efficiency = 95%.",
                           
                        ],
                        "bullets": [
                             "Lithium-ion systems typically operate at 93–97% efficiency.",
                            "Temperature, age, and inverter quality can affect performance.",

                        ]
                    },
                    {
                        "image": {
                            "src": "images/Efficiency.png",
                            "alt": "Efficiency diagram"
                        }
                    },
                    {
                        "heading": "🧠 Battery Management System (BMS)",
                        "paragraphs": [
                            "The Battery Management System (BMS) is the electronic control unit that monitors and protects every cell within the battery pack.",
                            "It acts as the “brain” of the battery, ensuring safe operation, balanced performance, and efficient communication with the inverter.",
                            "Think of the BMS as the “control tower” that constantly checks battery health, regulates energy flow, and prevents unsafe conditions.",
                        ],
                        "highlights": [
                            "Example: If one cell in a battery starts charging faster than the others, the BMS will reduce current flow to that cell and balance the pack to avoid overheating or overvoltage.",
                        ],
                        "bullets": [
                            "Monitors voltage, current, and temperature of each cell in real time.",
                            "Balances cells to maintain equal charge and even wear across the battery.",
                            "Protects against overcharge, over-discharge, short circuits, and extreme temperature.",
                            "Communicates with the inverter via CAN or RS485 for coordinated charge/discharge control.",
                            "Logs data such as cycle count, SOC, and fault history for performance tracking.",
                        ],
                    },
                    {
                        "image":{
                            "src": "images/BMS.png",
                            "alt": "Battery Management System(BMS) diagram",
                        }

                    },
                    {
                        "heading": "Summary",
                        "table": {
                            "headers": ["Term", "Symbol", "What It Means", "Practical Range / Example"],
                            "rows": [
                                ["Cycle", "🔁", "One full charge and discharge", "6000+ cycles typical lifespan"],
                                ["State of Charge (SOC)", "%", "Remaining energy in the battery", "20–90% operating range"],
                                ["Depth of Discharge (DoD)", "%", "Energy used per cycle", "Typically, 70–90%"],
                                ["Efficiency", "η", "Ratio of discharge to charge energy", "93–97% for LiFePO₄ batteries"],
                                ["Battery Management System (BMS)", "🧠", "Monitors, protects, balances cells, and communicates with inverter", "Manages ~3.2 V nominal cells, temperature, and current"],
                            ],
                        },
                    },
                ],
            },
            {
                "title": "1.9 The Four Main System Types (Explained Simply)",
                "icon": "🧩",
                "paragraphs": [
                    "Different solar energy systems are designed according to how they interact with the grid, store energy, and supply power.",
                    "Understanding these configurations is essential for selecting the right system for each site or customer need.",
                ],
                "subsections": [
                    {
                        "heading": "🧩 Backup System (No Solar)",
                        "paragraphs": [
                            "Connected to the utility grid and includes an inverter and battery storage, but no solar panels.",
                            "The battery charges from the grid when power is available and automatically supplies energy to essential loads during outages.",
                        ],
                        "bullets": [
                            "Components: Inverter + Battery Only",
                            "Purpose: Keep essentials on during outages.",
                            "Pros: Cheap, simple, reliable",
                            "Cons: No savings",
                        ],
                        "highlights": [
                            "Example: A home using 3 kW during outages needs: 5 kVA inverter + 10 kWh REVOV battery",
                        ],
                    },
                    {
                        "heading": "☀️ Grid-Tied Solar (No Batteries)",
                        "paragraphs": [
                            "Directly connected to the utility grid and does not include any battery storage.",
                            "Power is produced by the PV array and converted by the inverter for immediate use.",
                        ],
                        "bullets": [
                            "Components: Solar + Inverter",
                            "Purpose: Reduce electricity bill",
                            "Pros: Cheap, high savings",
                            "Cons: No backup during outages",
                        ],
                        "notes": [
                            "🛠️Not common in SA because people need backup.",
                        ],
                    },
                    {
                        "heading": "⚡ Hybrid System (Solar + Battery)",
                        "paragraphs": [
                            "Combines solar (PV), battery storage, and grid connection.",
                            "It intelligently manages energy to optimise self-consumption, reduce grid dependency, and provide backup power during outages.",
                        ],
                        "bullets": [
                            "Components: Solar + Battery + Grid",
                            "Purpose: Provide backup + savings",
                            "Pros: Provide backup power and reduce grid reliance",
                            "Cons: More expensive upfront",
                        ],
                        "highlights": [
                            "Example Hybrid Setup: 5 kW Hybrid Inverter + "
                            "5 kWp PV + 10 kWh REVOV battery "
                            "→ Can run the house during day AND night.",
                        ],
                    },
                    {
                        "heading": "🏠 Fully Off-Grid System",
                        "paragraphs": [
                            "An off-grid system operates independently from the grid, relying entirely on solar panels, "
                            "battery storage, and often a backup generator.",
                            "It is designed for areas with no grid access or where independence and energy resilience are priorities.",
                        ],
                        "bullets": [
                            "Purpose: No Eskom connection.",
                            "Pros: Full independence",
                            "Cons: Expensive + complex",
                        ],
                        "bullets": [
                          "Requires: ",
                            "large inverter"
                            " large battery bank"
                            " large solar array, and a backup generator.",
                            
                        ],
                        "notes": [
                            "🛠️These systems MUST be sized correctly to avoid failure.",
                        ]
                    },
                ],
            },
            {
                "image": {
                    "src": "images/Module1-system-types.png",
                    "alt": "Diagram showing the four main system types: Backup, Grid-Tied, Hybrid, Off-Grid",
                },
            },
            {
                "title": "1.10 Energy Flow and System Operation",
                #"icon": "🔄",
                "paragraphs": [
                    "The hybrid energy system intelligently manages power flow between solar panels (PV), batteries, inverter, grid, and loads to ensure optimal efficiency and uninterrupted supply.",
                    "Understanding how these components interact under different conditions is key to effective installation, setup, and troubleshooting.",
                ],
                "subsections": [
                    {
                        "heading": "Example: Hybrid System Operation",
                        "numbered": [
                            "PV Array Generates DC Power",
                            "Inverter Supplies Loads and Charges the Battery",
                            "When PV Output Decreases, Battery Discharges",
                            "Grid Supplements Energy When Required",
                            "Excess Energy Can Be Exported to the Grid",
                        ],
                        "subsections": [
                            {
                                "heading": "1. PV Array Generates DC Power",
                                "bullets": [
                                    "During daylight, solar modules produce direct current (DC) electricity.",
                                    "The inverter receives this DC power and manages how it’s distributed to loads, batteries, or the grid.",
                                ],
                            },
                            {
                                "heading": "2. Inverter Supplies Loads and Charges the Battery",
                                "bullets": [
                                    "The inverter converts DC from the PV array into alternating current (AC) to power connected loads.",
                                    "At the same time, it directs any surplus solar energy to charge the battery bank.",
                                    "The BMS controls the charging rate, preventing overcharging and balancing cells for optimal performance.",
                                ],
                            },
                            {
                                "heading": "3. When PV Output Decreases, Battery Discharges",
                                "bullets": [
                                    "As sunlight drops (cloudy conditions or night), the inverter automatically draws energy from the battery to continue supplying the loads.",
                                    "The system prioritises maintaining power stability and protecting the battery from deep discharge.",
                                ],
                            },
                            {
                                "heading": "4. Grid Supplements Energy When Required",
                                "bullets": [
                                    "If both PV and battery energy are insufficient, the inverter synchronises with the grid, drawing the shortfall to maintain supply.",
                                    "In some configurations, the grid can also charge the batteries, particularly during low-tariff (off-peak) hours to reduce energy costs.",
                                ],
                            },
                            {
                                "heading": "5. Excess Energy Can Be Exported to the Grid",
                                "bullets": [
                                    "When generation exceeds load and battery capacity, excess solar power can be fed back into the grid, if the inverter is configured for export mode.",
                                    "This requires appropriate settings and utility approval to ensure compliance with grid-tie regulations.",
                                ],
                            },
                        ],
                    },
                    {
                        "heading": "Summary of Power Flow",
                        "table": {
                            "headers": ["Source", "Flow Direction", "Destination", "Description"],
                            "rows": [
                                ["PV Array", "DC Power →", "Inverter", "Generates solar energy"],
                                ["Inverter", "AC Power →", "Load", "Supplies usable energy"],
                                ["Inverter ↔ Battery", "Bidirectional DC", "Stores/Delivers", "Stores or delivers energy as needed"],
                                ["Inverter ↔ Grid", "Bidirectional AC", "Draws/Exports", "Draws or exports energy"],
                                ["Battery → Load", "DC via Inverter", "Loads", "Provides stored backup energy"],
                            ],
                        },
                    },
                ],
            },
            {
                "title": "1.11 Efficiency and System Losses",
                #"icon": "📉",
                "paragraphs": [
                    "Every energy system experiences some level of loss as electricity moves through different components.",
                    "These losses reduce the total amount of energy that finally reaches the load.",
                    "Understanding where losses occur and how to minimise them is key to designing high-performing systems.",
                ],
                "subsections": [
                    {
                        "heading": "⚡ Typical System Losses",
                        "table": {
                            "headers": ["Stage", "Component", "Typical Loss (%)", "Cause / Explanation"],
                            "rows": [
                                ["1", "Inverter", "~5%", "Power lost during DC–AC conversion, heat generation, and internal electronics inefficiency."],
                                ["2", "Cabling & Connectors", "~2%", "Voltage drop due to resistance in wires, long cable runs, or undersized conductors."],
                                ["3", "Battery (Charge/Discharge)", "~3%", "Energy loss during chemical conversion and BMS operation."],
                            ],
                        },
                        "preformatted": "[ PV Array ] → (Cabling Loss) → [ Inverter ] → (Conversion Loss) → [ Battery ] → (Charge/Discharge Loss) → [ Load ]\nEach arrow represents a conversion stage where a small percentage of energy is lost.",
                        "highlights": [
                            "Roughly 90%–95% of the energy produced by the PV array is effectively used to power loads in well-designed systems.",
                        ],
                    },
                    {
                        "image": {
                            "src": "images/Module-1-system-losses.png",
                            "alt": "Diagram showing typical system losses at each stage: Inverter, Cabling, Battery",
                        },

                    },
                    {
                        "heading": "💡 How to Minimise Losses",
                        "numbered": [
                            "Correct Cable Sizing",
                            "Shorter Cable Runs",
                            "High-Quality Components",
                            "System Design Optimisation",
                            "Regular Maintenance",
                        ],
                        "subsections": [
                            {
                                "heading": "1. Correct Cable Sizing",
                                "bullets": [
                                    "Use conductors sized to handle current with minimal voltage drop (<2–3%).",
                                    "Refer to SANS 10142-1 or manufacturer specifications for sizing charts.",
                                ],
                            },
                            {
                                "heading": "2. Shorter Cable Runs",
                                "bullets": [
                                    "Keep cables as short as possible between PV array, inverter, and battery bank.",
                                    "Use busbars or junction boxes strategically to reduce cable lengths.",
                                ],
                            },
                            {
                                "heading": "3. High-Quality Components",
                                "bullets": [
                                    "Choose high-efficiency inverters (>96%) and low-resistance connectors.",
                                    "Ensure tight, corrosion-free terminations to avoid hot spots or energy waste.",
                                ],
                            },
                            {
                                "heading": "4. System Design Optimisation",
                                "bullets": [
                                    "Position inverter close to batteries and main distribution board.",
                                    "Use parallel strings for large systems to maintain voltage stability.",
                                    "Ensure firmware updates are applied for smart efficiency improvements.",
                                ],
                            },
                            {
                                "heading": "5. Regular Maintenance",
                                "bullets": [
                                    "Clean PV panels to maintain generation efficiency.",
                                    "Inspect cables and connectors for wear, corrosion, or loose fittings.",
                                    "Monitor inverter logs for energy loss anomalies or unbalanced loads.",
                                ],
                            },
                        ],
                    },
                ],
            },
            {
                "image":{
                    "src": "images/Module-1-how-to-minimise-system-losses.png",
                    "alt": "Diagram showing tips to minimise system losses: Correct cable sizing, shorter cable runs, high-quality components, system design optimisation, regular maintenance",
                },

            },
            {
                "title": "1.12 Where REVOV Fits into these Systems",
                #"icon": "🏷️",
                "paragraphs": [
                    "REVOV supplies high-quality lithium energy storage solutions designed for residential, commercial and industrial systems.",
                ],
                "subsections": [
                    {
                        "heading": "🔋 REVOV Benefits",
                        "bullets": [
                            "Long life: 6 000+ cycles",
                            "Safe LiFePO₄ chemistry",
                            "Strong BMS for communication",
                            "Scalable (parallel or series for HV)",
                            "High efficiency (95%+)",
                            "1C and 0.5C options",
                            "Works with most popular inverters",
                        ],
                    },
                   
                    {
                        "heading": "🛠️ Installer Tip",
                        "paragraphs": [
                            "REVOV batteries perform best when:",
                        ],
                        "bullets": [
                            "Configured correctly",
                            "Charged fully after installation",
                            "Installed with proper DC protection",
                            "Cables are correctly sized",
                            "Communication is tested",
                            "Firmware is updated",
                        ],
                    },
                    {
                      "image": {
                         "src": "images/Module-1-Where-revov-fits-into-the-system.png",
                         "alt": "Diagram showing where REVOV batteries fit into the system: connected to the inverter, which manages energy flow between PV array, battery, grid, and loads",
                         },
                    },
                ],
            },
           
        ],
    }

    MODULE_2_ELECTRICAL_FUNDAMENTALS = {
        "module_title": "MODULE 2 – Electrical Fundamentals",
        "module_subtitle": "Electrical basics needed to wire safely, size correctly, and troubleshoot faster.",
        "sections": [
            {
                "title": "Contents",
                "icon": "📚",
                "bullets": [
                    "2.1 Module 2 Learning Outcomes",
                    "2.2 The Core Electrical Terms You Must Be Comfortable With",
                    "2.3 AC vs DC in Practice",
                    "2.4 Series & Parallel — Explained for Installers",
                    "2.5 Electrical Components",
                    "2.6 Earthing & Bonding — The Safety Backbone",
                    "2.7 Electrical Safety — Non-Negotiable Installer Rules",
                    "2.8 Practical Installer Examples (What Can Go Wrong + How to Fix It)",
                ],
            },
            {
                "title": "2.1 Module 2 Learning Outcomes",
                "icon": "🎯",
                "paragraphs": [
                    "This module gives you the electrical basics needed to wire safely, size correctly, and troubleshoot faster.",
                    "By the end of this module, you will be able to:",
                ],
                "bullets": [
                    "Explain the core electrical terms used in solar and battery systems (V, A, W, kW, Wh, kWh)",
                    "Apply the key formulas used in installer work (Ohm’s Law + power and energy equations)",
                    "Understand how series and parallel wiring changes voltage and capacity",
                    "Make better decisions on cable sizing, terminations and protection devices",
                    "Understand earthing and bonding basics for safe, stable systems",
                    "Identify common electrical installation errors before they cause failures",
                ],
            },
            {
                "title": "2.2 The Core Electrical Terms You Must Be Comfortable With",
                "icon": "🧠",
                "paragraphs": [
                    "These are the everyday terms you’ll use when sizing, wiring, testing and fault finding.",
                ],
                "subsections": [
                    {
                        "heading": "⚡ Voltage (V) — “Electrical Pressure”",
                        "paragraphs": [
                            "Voltage is the electrical pressure that pushes current through a circuit.",
                            "Think of it like water pressure in a pipe.",
                            "More pressure = stronger push",
                            "More voltage = stronger push",
                            "Why this matters to you:",
                        ],
                        "bullets": [
                            "Higher voltage systems carry the same power with lower current",
                            "Lower current means thinner cables and less heat",
                            "That’s why modern lithium systems run at 48 V / 51.2 V",
                        ],
                        "highlights": [
                            "Example: If you need 5 kW of power → 12 V: 5 000 ÷ 12 = 417 A · 48 V: 5 000 ÷ 48 = 104 A",
                        ],
                        "notes": [
                            "Same power. Very different current. That difference changes everything in cable sizing and safety.",
                        ],
                    },
                    {
                        "heading": "🔌 Current (A) — “How Much is Flowing”",
                        "paragraphs": [
                            "Current is the amount of electricity flowing through a cable.",
                            "More current means:",
                        ],
                        "bullets": [
                            "Thicker cables",
                            "Larger breakers",
                            "More heat",
                            "Higher fire risk if undersized",
                        ],
                        "notes": [
                            "If voltage is pressure, current is the volume of water flowing.",
                            "Most battery-side problems happen because current was underestimated.",
                        ],
                    },
                    {
                        "heading": "⚙️ Resistance (Ω) — “Opposition to Flow”",
                        "paragraphs": [
                            "Resistance is what “fights” current flow — and cables have resistance.",
                            "Long cables = more resistance.",
                            "Thin cables = more resistance.",
                            "Loose lugs = more resistance.",
                            "Resistance causes:",
                        ],
                        "bullets": [
                            "Voltage drop",
                            "Heat",
                            "Efficiency loss",
                            "Shutdowns under load",
                        ],
                        "notes": [
                            "Resistance is invisible — but you see its effects.",
                        ],
                    },
                    {
                        "heading": "⚡ Power (W / kW) — “How Fast Energy is Used”",
                        "paragraphs": [
                            "Power is the rate at which energy is being used right now.",
                        ],
                        "highlights": [
                            "Power (W) = Voltage (V) × Current (A)",
                            "Example: 50 V × 50 A = 2 500 W = 2.5 kW",
                        ],
                        "notes": [
                            "This is why power determines inverter size (Module 1).",
                        ],
                    },
                    {
                        "heading": "🔋 Energy (Wh / kWh) — “Power Over Time”",
                        "paragraphs": [
                            "Energy is how much electricity is used or stored over time.",
                        ],
                        "highlights": [
                            "Energy (kWh) = Power (kW) × Time (hours)",
                            "Example: 1 kW load for 5 hours = 5 kWh battery usage",
                        ],
                    },
                    {
                        "heading": "📐 Quick Summary Table",
                        "table": {
                            "headers": ["Term", "Meaning", "Unit", "Installer Use"],
                            "rows": [
                                ["Voltage", "Push / pressure", "V", "System design voltage"],
                                ["Current", "Flow", "A", "Cable + breaker sizing"],
                                ["Resistance", "Opposition", "Ω", "Voltage drop + heat"],
                                ["Power", "Rate of use", "W / kW", "Inverter sizing"],
                                ["Energy", "Total over time", "Wh / kWh", "Battery sizing"],
                            ],
                        },
                    },
                ],
            },
            {

               "image": {
                   "src": "images/WattWorks_Essential_E_Terms.png",
                   "alt": "Diagram of essential electrical terms",
               },
            },
            {
                "title": "2.3 AC vs DC in Practice",
                "icon": "🔌",
                "paragraphs": [
                    "This section explains what AC and DC do in the system, why they behave differently, and what that means for wiring, protection and fault finding.",
                ],
                "subsections": [
                    {
                        "heading": "🔌 AC (Alternating Current)",
                        "bullets": [
                            "Household power and comes from Eskom or generator",
                        ],
                    },
                    {
                        "heading": "🔋 DC (Direct Current)",
                        "bullets": [
                            "Comes from solar panels and batteries",
                        ],
                    },
                    {
                        "heading": "🔋 DC (Direct Current) — “High Current, High Consequence”",
                        "paragraphs": [
                            "DC flows in one direction. Simple in theory… but in practice, it demands respect.",
                            "In our systems, DC is used for:",
                        ],
                        "bullets": [
                            "PV strings feeding the inverter",
                            "Battery charge and discharge",
                            "High-current battery cables",
                            "DC breakers and isolators",
                        ],
                        "subsections": [
                            {
                                "heading": "DC does not forgive mistakes",
                                "bullets": [
                                    "Polarity matters — reverse it and you can damage equipment instantly.",
                                    "DC arcs don’t “let go” easily like AC does. If something sparks, it can keep sparking.",
                                    "High battery currents mean heat becomes a real issue if cables or lugs are undersized.",
                                    "Small mistakes (loose lug, wrong torque, bad crimp) show up quickly under load.",
                                ],
                            },
                        ],
                        "notes": [
                            "If a system randomly shuts down when loads increase, don’t immediately blame the inverter. Check the DC side first — cable size, voltage drop, loose lugs, breaker ratings, battery comms.",
                            "A large percentage of real-world faults live on the DC side.",
                        ],
                    },
                    {
                        "heading": "🔌 AC (Alternating Current) — Where Compliance and Stability Matter",
                        "paragraphs": [
                            "AC changes direction 50 times per second (50 Hz). That constant switching is what allows it to travel long distances efficiently and power homes safely.",
                            "On your installs, AC is used for:",
                        ],
                        "bullets": [
                            "Inverter output to essential loads",
                            "Grid input",
                            "Generator connection (where applicable)",
                        ],
                        "subsections": [
                            {
                                "heading": "AC-side considerations",
                                "bullets": [
                                    "The inverter must match the grid’s voltage and frequency before connecting.",
                                    "Neutral and earth must be handled correctly — this is where many nuisance trips start.",
                                    "Earth leakage placement matters.",
                                    "Protection must comply with SANS wiring standards.",
                                ],
                            },
                        ],
                        "notes": [
                            "If customers complain about earth leakage tripping, strange inverter behaviour, or “getting shocked” from metal surfaces — you’re usually dealing with AC-side bonding, neutral or earthing issues.",
                        ],
                    },
                    {
                        "heading": "⚙️ The Inverter — The Electrical Traffic Controller",
                        "paragraphs": [
                            "The inverter isn’t just converting power. It’s managing two completely different electrical environments at the same time.",
                            "On one side: DC from PV and battery.",
                            "On the other side: AC for loads and grid.",
                            "It constantly decides:",
                        ],
                        "bullets": [
                            "Should solar power the loads?",
                            "Should excess solar charge the battery?",
                            "Should the battery discharge to support the load?",
                            "Should we draw from the grid?",
                            "Should we export (if allowed)?",
                        ],
                        "notes": [
                            "In a hybrid system, it’s a traffic controller, not just a converter.",
                        ],
                        
                    },
                    {
                      "heading": "📐What This Looks Like In Real Life",
                      "image":{
                          "src" : "images/WattWorks_AC-DC-INVERTER.png",
                          "alt": "Diagram showing the inverter managing DC input from PV and battery, and AC output to loads and grid",

                      },
                    },
                    {
                        "heading": "What You Should Be Checking on Site",
                        "paragraphs": [
                            "When you’re troubleshooting, think in two halves. If you can mentally separate AC and DC while diagnosing a fault, your troubleshooting becomes much faster.",
                        ],
                        "subsections": [
                            {
                                "heading": "DC Side Checks (heat, polarity, voltage drop, high current)",
                                "bullets": [
                                    "Polarity correct",
                                    "Cable size correct",
                                    "Lugs properly crimped and torqued",
                                    "DC breaker rated for DC",
                                    "PV voltage within limits",
                                    "Battery communication working",
                                ],
                            },
                            {
                                "heading": "AC Side Checks (compliance, synchronisation, bonding, protection)",
                                "bullets": [
                                    "Essential and non-essential loads separated correctly",
                                    "Neutral correctly installed",
                                    "Earth leakage correctly placed",
                                    "Grid settings configured properly",
                                    "Earthing and bonding done to standard",
                                ],
                            },
                        ],
                    },
                ],
            },
            {
                "title": "2.4 Series & Parallel — Explained for Installers",
                "icon": "🧩",
                "paragraphs": [
                    "This section helps you expand systems correctly without damaging equipment or voiding warranties.",
                    "You only have two ways to connect batteries: series or parallel. Each changes the system differently.",
                ],
                "subsections": [
                    {
                        "heading": "🔌 Series Connection – Voltage Adds",
                        "paragraphs": [
                            "When batteries are connected positive to negative:",
                        ],
                        "bullets": [
                            "Voltage adds up",
                            "Capacity (Ah) stays the same",
                        ],
                        "highlights": [
                            "Example: 48 V + 48 V = 96 V (capacity stays the same)",
                        ],
                        "paragraphs_after": [
                            "Think of it like stacking batteries on top of each other to create more pressure.",
                            "Used for: high-voltage stacks and some commercial/BESS systems.",
                        ],
                        "notes": [
                            "Never series-connect batteries unless the manufacturer and product design specifically allow it.",
                        ],
                    },
                    {
                        "heading": "🔋 Parallel Connection – Capacity Adds",
                        "paragraphs": [
                            "When batteries are connected positive to positive and negative to negative:",
                        ],
                        "bullets": [
                            "Voltage stays the same",
                            "Capacity increases",
                        ],
                        "highlights": [
                            "Example: Two 200 Ah batteries at 48 V in parallel → 400 Ah at 48 V",
                        ],
                        "paragraphs_after": [
                            "Think of it like widening the water tank — same pressure, more stored volume.",
                            "Used for expanding capacity in most home and SME installs.",
                        ],
                        "notes": [
                            "Most REVOV LV setups are typically parallel expansion — always follow product rules and inverter limits.",
                        ],
                    },
                    {
                        "heading": "📐 Quick Comparison Table",
                        "table": {
                            "headers": ["Connection", "Voltage", "Capacity", "Typical Use"],
                            "rows": [
                                ["Series", "Increases", "Same", "HV banks / specific stacks"],
                                ["Parallel", "Same", "Increases", "Most LV systems"],
                            ],
                        },
                    },
                ],
            },
            {
                "title": "2.5 Electrical Components",
                "icon": "🧰",
                "paragraphs": [
                    "This is where safety, reliability, and warranty protection really live.",
                ],
                "subsections": [
                    {
                        "heading": "Cable Thickness Matters",
                        "paragraphs": [
                            "If cables are too thin (or runs are too long):",
                        ],
                        "bullets": [
                            "They heat up",
                            "Voltage drops under load",
                            "BMS/inverter may trip or shut down",
                            "Fire risk increases",
                        ],
                        "notes": [
                            "Rule of thumb: Always follow inverter + battery manufacturer specs first — then verify against current, run length and installation environment.",
                        ],
                    },
                    {
                        "heading": "Lugs & Terminations (Do it once, do it right)",
                        "paragraphs": [
                            "Good terminations prevent heat, faults, and failures.",
                            "Best practice checklist:",
                        ],
                        "bullets": [
                            "Correct lug size (match cable + terminal)",
                            "Hydraulic crimp (not “hammer crimp”)",
                            "Heat-shrink on lug",
                            "Clean contact surfaces",
                            "Torque to manufacturer spec",
                            "Re-check after initial commissioning (because copper settles)",
                        ],
                        "notes": [
                            "Loose DC lugs = hot terminals = shutdowns = warranty issues.",
                        ],
                    },
                    {
                        "heading": "Fuses, Breakers, Isolators & Protection",
                        "paragraphs": [
                            "Protection devices are there to stop fires and save expensive equipment.",
                        ],
                        "subsections": [
                            {
                                "heading": "Battery Fuse/Breaker (DC)",
                                "bullets": [
                                    "Protects battery cables and equipment",
                                    "Must match maximum expected current",
                                    "Install as close as possible to the battery side (where applicable)",
                                ],
                                "notes": [
                                    "Example: If expected current is ±100 A, use a breaker/fuse sized appropriately for the design and manufacturer guidelines (often the next rating up, e.g. 125 A — but follow spec).",
                                ],
                            },
                            {
                                "heading": "AC Breakers",
                                "paragraphs": [
                                    "Protect AC output circuits and distribution boards.",
                                ],
                            },
                            {
                                "heading": "DC Isolator",
                                "paragraphs": [
                                    "Used between PV and inverter/MPPT to allow safe shutdown and maintenance.",
                                ],
                            },
                        ],
                    },
                ],
            },
            {
                "image" : {
                    "src" : "images/Fuses-breakers-isolators.png",
                    "alt" : "Diagram showing examples of fuses, breakers and isolators used in solar and battery systems"


                },
            },
            {
                "title": "2.6 Earthing & Bonding — The Safety Backbone",
                "icon": "🛡️",
                "paragraphs": [
                    "This section explains the grounding basics that keep systems safe and stable.",
                ],
                "bullets": [
                    "Earthing = connecting the system to ground for safety and surge control",
                    "Bonding = linking metal parts together so they are at the same potential",
                ],
                "subsections": [
                    {
                        "heading": "Why it matters",
                        "bullets": [
                            "Reduces shock risk",
                            "Improves protection performance",
                            "Reduces nuisance faults / unstable readings",
                            "Supports inverter stability",
                        ],
                    },
                ],
                "notes": [
                    "Incorrect earthing and bonding can cause “weird” issues like nuisance alarms, noise, unstable inverter behaviour, or unsafe touch voltages.",
                    "Always install to SANS 10142-1 and project requirements.",
                ],
            },
            {
                "title": "2.7 Electrical Safety — Non-Negotiable Installer Rules",
                "icon": "⛑️",
                "paragraphs": [
                    "This is the minimum standard for working safely and professionally.",
                    "Before you touch anything:",
                ],
                "bullets": [
                    "Isolate power properly",
                    "Lockout/tagout where possible",
                    "Test for dead (don’t assume)",
                    "Double-check polarity on DC",
                    "Use insulated tools",
                    "Wear PPE (gloves, boots, eyewear)",
                    "Never work alone around live DC systems",
                ],
                "notes": [
                    "DC can be extremely dangerous because it can maintain continuous current flow — treat it with respect.",
                ],
            },
            {
                "title": "2.8 Practical Installer Examples (What Can Go Wrong + How to Fix It)",
                "icon": "🛠️",
                "paragraphs": [
                    "This is where electrical theory becomes real-world consequences.",
                    "On paper, voltage, current and resistance are just formulas.",
                    "On site, they become heat, sparks, shutdowns and unhappy clients.",
                    "Let’s walk through real scenarios installers face every day.",
                ],
                "subsections": [
                    {
                        "heading": "📈 Example 1 — Incorrect Cable Size",
                        "variant": "installer-example",
                        "subsections": [
                            {
                                "heading": "What Happened",
                                "paragraphs": [
                                    "An installer connects a 5 kW inverter to a 48 V battery using 10 mm² cable.",
                                    "A 5-kW inverter at 48 V draws:",
                                ],
                                "highlights": [
                                    "I = P / V = 5 000 ÷ 48 = 104 A",
                                ],
                                "notes": [
                                    "Can 10 mm² cable safely carry 100+ amps continuously? Usually not.",
                                ],
                            },
                            {
                                "heading": "What Happens Next",
                                "bullets": [
                                    "Cable starts heating up",
                                    "Voltage drop increases",
                                    "Battery sees unstable voltage",
                                    "BMS detects abnormal conditions",
                                    "Inverter throws DC undervoltage faults",
                                    "Customer calls complaining about shutdowns",
                                ],
                                "paragraphs_after": [
                                    "In worst cases: melted insulation, burnt terminals, and fire risk.",
                                ],
                            },
                            {
                                "heading": "Why This Happens (Electrical Principle)",
                                "paragraphs": [
                                    "High current + undersized cable = higher resistance → heat → voltage drop → instability.",
                                    "Resistance increases with smaller cables and longer runs.",
                                ],
                            },
                            {
                                "heading": "✅ The Fix",
                                "bullets": [
                                    "Calculate current first",
                                    "Check inverter manual",
                                    "Check battery manual",
                                    "Consider cable length",
                                    "Typically use 16–25 mm² for this size system (depending on run)",
                                ],
                                "notes": [
                                    "Never size cable by guesswork. Always size by current.",
                                ],
                            },
                        ],
                    },
                    {
                        "image": {
                            "src": "images/Under_sized_cable_overheating.png",
                            "alt": "Photo showing an example of an under-sized cable overheating with melted insulation and burnt terminals",

                        },
                    },
                    {
                        "heading": "📈 Example 2 — Swapped Polarity",
                        "variant": "installer-example",
                        "subsections": [
                            {
                                "heading": "What Happened",
                                "paragraphs": [
                                    "Installer connects battery negative to inverter positive during commissioning.",
                                    "This usually happens because:",
                                ],
                                "bullets": [
                                    "Cables are not labelled",
                                    "Installer is rushing",
                                    "No final polarity check",
                                ],
                            },
                            {
                                "heading": "What Happens Next",
                                "bullets": [
                                    "Loud spark",
                                    "Inverter may instantly shut down",
                                    "Possible blown internal fuse",
                                    "BMS protection triggers",
                                    "Worst case: permanent damage",
                                ],
                                "notes": [
                                    "DC does not forgive mistakes. Unlike AC, DC polarity matters.",
                                ],
                            },
                            {
                                "heading": "Why This Happens (Electrical Principle)",
                                "paragraphs": [
                                    "Batteries supply constant DC current.",
                                    "Reverse polarity forces current in the wrong direction through internal components.",
                                    "That can destroy: capacitors, MOSFETs, and internal protection circuits.",
                                ],
                            },
                            {
                                "heading": "✅ The Fix",
                                "paragraphs": [
                                    "Before energising:",
                                ],
                                "bullets": [
                                    "Use a multimeter",
                                    "Confirm voltage",
                                    "Confirm polarity",
                                    "Label positive (red) and negative (black) clearly",
                                    "Never assume — always test",
                                ],
                                "notes": [
                                    "Meter first. Energise second.",
                                ],
                            },
                        ],
                    },
                    {
                        "image" :{
                            "src": "images/reverse_polarity_connection.png",
                            "alt": "Photo showing an example of a reverse polarity connection with a spark and damaged inverter components",
                        },
                    },
                    {
                        "heading": "📈 Example 3 — Poor Crimping / Loose Lug",
                        "variant": "installer-example",
                        "subsections": [
                            {
                                "heading": "What Happened",
                                "paragraphs": [
                                    "Installer uses a manual crimper instead of hydraulic.",
                                    "Lug looks tight but isn’t properly compressed.",
                                    "Everything works at commissioning. Two weeks later the customer reports the inverter randomly shutting down.",
                                ],
                            },
                            {
                                "heading": "What’s Actually Happening",
                                "paragraphs": [
                                    "The loose connection creates micro-resistance and heat build-up. Under load you see:",
                                ],
                                "bullets": [
                                    "Terminal discoloration",
                                    "Voltage fluctuation",
                                    "Eventually a melted lug",
                                ],
                            },
                            {
                                "heading": "Why This Happens (Electrical Principle)",
                                "paragraphs": [
                                    "Loose connection = increased resistance.",
                                    "Resistance × high current = heat.",
                                    "Heat damages cable insulation, battery terminals, and inverter studs.",
                                    "Heat increases resistance further — creating a failure loop.",
                                ],
                            },
                            {
                                "heading": "✅ The Fix",
                                "bullets": [
                                    "Use hydraulic crimpers only",
                                    "Correct lug size for cable",
                                    "Heat shrink after crimp",
                                    "Torque to manufacturer specification",
                                    "Re-check torque after commissioning",
                                ],
                                "notes": [
                                    "DC connections must be mechanically tight AND electrically sound.",
                                ],
                            },
                        ],
                    },
                    {
                        "image": {
                            "src":"images/reverse_polarity_connection.png",
                            "alt": "image showing the effect of poor crimping on cable lugs",
                        },
                    },
                    {
                        "heading": "📈 Example 4 — No DC Isolator Installed",
                        "variant": "installer-example",
                        "subsections": [
                            {
                                "heading": "What Happened",
                                "paragraphs": [
                                    "Installer connects battery directly to inverter with no DC isolator.",
                                    "Everything works — until service is required.",
                                    "Now to work safely, the technician must disconnect live battery cables manually.",
                                ],
                            },
                            {
                                "heading": "What Happens Next",
                                "bullets": [
                                    "High arc risk",
                                    "Spark hazard",
                                    "Personal injury risk",
                                    "Equipment damage",
                                ],
                                "notes": [
                                    "Lithium batteries deliver high current instantly.",
                                ],
                            },
                            {
                                "heading": "Why This Matters",
                                "paragraphs": [
                                    "DC arcs do not self-extinguish like AC arcs. They sustain longer and burn hotter.",
                                ],
                            },
                            {
                                "heading": "✅ The Fix",
                                "paragraphs": [
                                    "Always install:",
                                ],
                                "bullets": [
                                    "DC breaker or fuse close to battery",
                                    "Proper DC isolator",
                                    "Label isolators clearly",
                                ],
                                "notes": [
                                    "If you cannot safely isolate it, you installed it wrong.",
                                ],
                            },
                        ],
                    },
                    {
                        "images": {
                            "src":"images/No_dc-isolator_installed.png",
                            "alt": "image showing the risks of not having a DC isolator with a photo of a technician trying to disconnect live battery cables with sparks flying",

                        },
                    },
                    {
                        "heading": "📈 Example 5 — Unequal Parallel Battery Cables",
                        "variant": "installer-example",
                        "subsections": [
                            {
                                "heading": "What Happened",
                                "paragraphs": [
                                    "Two batteries are connected in parallel, but one cable is longer than the other.",
                                    "Installer thinks: “It’s fine.”",
                                ],
                            },
                            {
                                "heading": "What Actually Happens",
                                "paragraphs": [
                                    "Current does not split equally. The shorter cable carries more current, so that battery works harder.",
                                ],
                                "bullets": [
                                    "Uneven cycling",
                                    "One battery ages faster",
                                    "Premature failure",
                                    "BMS imbalance warnings",
                                ],
                            },
                            {
                                "heading": "Why This Happens",
                                "paragraphs": [
                                    "Current takes the path of least resistance.",
                                    "Longer cable = more resistance, so current favours the shorter cable.",
                                ],
                            },
                            {
                                "heading": "✅ The Fix",
                                "bullets": [
                                    "Use equal cable lengths",
                                    "Use proper busbars for parallel banks",
                                    "Follow manufacturer wiring diagrams",
                                ],
                                "notes": [
                                    "Parallel batteries must be electrically balanced.",
                                ],
                            },
                        ],
                    },
                ],
            },
            {
                "image": {
                    "src": "images/Un_equal_cables.png",
                    "alt": "image showing the effect of poor crimping on cable lugs",
                }, 
            },
               
        ],
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
