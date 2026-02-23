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
                        "paragraphs": [
                            "If a house essential loads average 1 kW and loadshedding lasts 5 hours:",
                        ],
                        "highlights": [
                            "1 kW × 5 hours = 5 kWh of energy is needed",
                        ],
                        "paragraphs_after": [
                            "But … you should never size a battery for 100% discharge.",
                            "The recommended practical design is to install 8 – 10 kWh to protect battery lifespan, allow for surge loads, and allow for growth.",
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
                            "Example: 1 kW × 4 hours = 4 kWh needed",
                        ],
                        "paragraphs": [
                            "But… you should NEVER size a battery for 100% depth of discharge.",
                        ],
                        "notes": [
                            "📘 Safe recommended battery: 8–10 kWh REVOV (longer life + future expansion)",
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
                        "heading": "📐 Basic Flow Diagram",
                        "preformatted": "☀️ PV (DC)\n↓\n🔋 Battery (DC)\n↓\n⚙️ Inverter (DC ↔ AC)\n↓\n🏠 Loads (AC)\n↔\n⚡ Grid (AC)",
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
                            },
                        ],
                        "notes": [
                            "💡 Think of it as a reversible chemical pump — charging pushes energy in; discharging releases it.",
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
                        "notes": [
                            "Example: Charging from 20% → 100% and discharging back to 20% equals one full cycle.",
                            "Daily cycling under normal conditions provides 10–15 years of service life for REVOV LiFePO₄ batteries.",
                        ],
                    },
                    {
                        "heading": "⚡ State of Charge (SOC)",
                        "paragraphs": [
                            "The State of Charge shows how much energy remains in the battery, expressed as a percentage of its total capacity.",
                            "Think of SOC as the “fuel gauge” of the battery — showing how full or empty it is.",
                        ],
                        "notes": [
                            "Example: If a 10 kWh battery shows an SOC of 60%, it still holds 6 kWh of usable energy.",
                            "Monitored continuously by the Battery Management System (BMS).",
                            "Ideal operating range for lithium-ion: 20% – 90% SOC to extend lifespan.",
                        ],
                    },
                    {
                        "heading": "🔋 Depth of Discharge (DoD)",
                        "paragraphs": [
                            "The Depth of Discharge measures how much of the battery’s capacity is used during one cycle, expressed as a percentage.",
                        ],
                        "notes": [
                            "Example: Using 8 kWh from a 10 kWh battery means a DoD of 80%.",
                            "The deeper the discharge, the shorter the overall lifespan.",
                            "Limiting DoD to 80–90% helps protect lithium-ion cells.",
                            "Most BMS systems automatically prevent over-discharge for safety.",
                        ],
                    },
                    {
                        "heading": "⚙️ Efficiency",
                        "paragraphs": [
                            "Battery efficiency measures how much of the stored energy can be recovered during discharge compared to what was put in during charging.",
                        ],
                        "notes": [
                            "Example: If 10 kWh is charged into the battery and 9.5 kWh is discharged, efficiency = 95%.",
                            "Lithium-ion systems typically operate at 93–97% efficiency.",
                            "Temperature, age, and inverter quality can affect performance.",
                        ],
                    },
                    {
                        "heading": "🧠 Battery Management System (BMS)",
                        "paragraphs": [
                            "The Battery Management System (BMS) is the electronic control unit that monitors and protects every cell within the battery pack.",
                            "It acts as the “brain” of the battery, ensuring safe operation, balanced performance, and efficient communication with the inverter.",
                            "Think of the BMS as the “control tower” that constantly checks battery health, regulates energy flow, and prevents unsafe conditions.",
                        ],
                        "notes": [
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
                        "notes": [
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
                            "Not common in SA because people need backup.",
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
                        "notes": [
                            "Example Hybrid Setup: 5 kW Hybrid Inverter + 5 kWp PV + 10 kWh REVOV battery → Can run the house during day AND night.",
                        ],
                    },
                    {
                        "heading": "🏠 Fully Off-Grid System",
                        "paragraphs": [
                            "Operates independently from the grid, relying entirely on solar panels, battery storage, and often a backup generator.",
                            "Designed for areas with no grid access or where independence and energy resilience are priorities.",
                        ],
                        "bullets": [
                            "Purpose: No Eskom connection.",
                            "Pros: Full independence",
                            "Cons: Expensive + complex",
                        ],
                        "notes": [
                            "Requires large inverter, large battery bank, large solar array, and a backup generator.",
                            "These systems MUST be sized correctly to avoid failure.",
                        ],
                    },
                ],
            },
            {
                "title": "1.10 Energy Flow and System Operation",
                "icon": "🔄",
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
                "icon": "📉",
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
                "title": "1.12 Where REVOV Fits into these Systems",
                "icon": "🏷️",
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
                ],
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
