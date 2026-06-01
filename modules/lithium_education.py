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
                    "Before you start working with systems, it's important to understand the \"language\" of energy storage. This module lays the foundation for everything that follows — from system design to installation and troubleshooting.",
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
            {
                "title": "1.2 Why Energy Storage Matters in South Africa",
                "paragraphs": [
                    "To understand why battery systems are growing so fast, you need to look at the real conditions on the ground. In South Africa, electricity supply is not always stable or predictable, and this directly affects daily life and business operations.",
                    "Loadshedding, voltage instability, and rising electricity costs have changed the way people think about power. Energy is no longer something you simply \"use\" — it's something you need to manage, control, and protect.",
                    "Battery storage solves real problems:",
                ],
                "bullets": [
                    "It keeps essential systems running during outages",
                    "It protects equipment from unstable supply",
                    "It reduces reliance on the grid",
                    "It allows solar energy to be used when it's actually needed",
                    "It provides seamless, automatic backup without user intervention",
                ],
                "paragraphs_after": [
                    "When a business loses power, it doesn't just lose electricity — it loses productivity, revenue, and sometimes customer trust.",
                ],
                "images": [
                    {
                        "src": "images/Example A small shop loses +- R2000 per hour when fridge shut down, card machines go offline, secu.png",
                        "alt": "Example of a small shop losing money during a power outage because the fridge shuts down, card machines go offline, and security systems are compromised."
                    },
                    {
                        "src": "images/Tip battery storage is nolonger Luxury it is a core infras.png",
                        "alt": "Tip battery storage is nolonger Luxury it is a core infras.png"
                    }
                ]
            },
            {
                "title": "1.3 Power vs Energy — The Most Important Concept",
                "paragraphs": [
                    "This is one of the most important concepts you will learn as an installer. Many system design mistakes happen because this is misunderstood.",
                    "Power and energy are related, but they are not the same — and each one plays a different role in system design.",
                    "Power (kW) — What is happening right now",
                    "Power tells you how much electricity is being used at a specific moment.",
                    "If too many appliances run at the same time and exceed the inverter capacity, the system will trip or shut down.",
                    "Think of power like the width of a water pipe – how much water can flow at one moment.",
                    "Examples:",
                ],
                "bullets": [
                    "Kettle = high power, short time",
                    "Geyser = high power, longer time",
                    "Lights = low power",
                ],
                "paragraphs_after": [
                    "If multiple appliances run at the same time, their kW adds up.",
                ],
                "images": [
                    {
                        "src": "images/Tip power determines how big your inverter must be.png",
                        "alt": "Tip: Power determines how big your inverter must be."
                    },
                ],
                "subsections": [
                    {
                        "heading": "Energy (kWh) — What happens over time",
                        "paragraphs": [
                            "Energy tells you how much electricity is used over a period of time. Even small loads can drain a battery if they run long enough.",
                            "Think of energy like the size of a water tank – how much water you have stored.",
                            "A 10 kWh REVOV battery can supply",
                        ],
                        "bullets": [
                            "1kW for 10 hours",
                            "2kW for 5 hours",
                            "5kW for 2 hours",
                        ],
                        "images": [
                        {
                        "src": "images/Example, if house essesntilas loads avaerage 1kw and outage lasts 5hours.png",
                        "alt": "Example, if house essesntilas loads avaerage 1kw and outage lasts 5hours.png",
                         },
                         {
                        "src": "images/Tip Energy determines how big your battery must be.png",
                        "alt": "images/Tip Energy determines how big your battery must be.png",
                         },

                           {
                        "src": "images/Key Electrical Terms.png",
                        "alt": "images/Key Electrical Terms.png",
                         },
                        ],
                    },
                   
                     
                ],
               
                
            
            },
            {
                "title": "1.4 How to Calculate Backup Requirements",
                "paragraphs": [
                    "Once you understand power and energy, the next step is applying that knowledge in a practical way. This is where theory becomes real-world system design.",
                    "A clear method ensures accurate and confident sizing to calculate backup requirements.",
                ],
                "subsections": [
                    {
                        "heading": "Step 1: Identify Essential Loads (kW)",
                        "paragraphs": [
                            "Start by deciding what must stay on during an outage.",
                            "This usually includes:",
                        ],
                        "bullets": [
                            "Lights",
                            "WiFi",
                            "Security systems",
                            "Fridges",
                            "Basic plug loads",
                        ],
                        "paragraphs_after": [
                            "This gives you your total power requirement (kW)",
                        ],
                        "images": [
                        {
                        "src": "images/Example lights,wifi + router, tv fri.png",
                        "alt": "Example lights,wifi + router, tv fri.png",
                         },
                        
                        ],
                    },
                    {
                        "heading": "Step 2: Determine Outage Duration (hours)",
                        "paragraphs": [
                            "How long must the system run without grid power?",
                            "This depends on:",
                        ],
                        "bullets": [
                            "Loadshedding schedules",
                            "Customer expectations",
                            "Site requirements",
                        ],
                    },
                    {
                        "heading": "Step 3: Calculate Energy Requirement",
                        "paragraphs": [
                            "Multiply load by time:",
                        ],
                        "highlights": [
                            "Load (kW) × Hours = Battery Size (kWh)",
                        
                        ],
                        "images" :[
                            {
                                "src": "images/Example, Total eesentials.png",
                                "alt": "images/Example, Total eesentials.png",
                            },
                        ],
                    },
                    {
                        "heading": "Step 4: Adjust for Real Life",
                        "paragraphs": [
                            "Real systems are not perfect. Always allow for:",
                        ],
                        "bullets": [
                            "Battery depth of discharge limits",
                            "System inefficiencies",
                            "Future expansion",
                        ],
                        "images" :[
                            {
                                "src": "images/Example, you should never size battery for 100% DOD.png",
                                "alt": "Example, you should never size battery for 100% DOD.png"
                            },
                        ],
                    },
                ],
            },
            {
                "title": "1.5 AC vs DC — How Electricity Moves Through the System",
                "paragraphs": [
                    "Every system you install will contain both AC and DC electricity. Understanding how these interact is essential for installation, configuration, and troubleshooting.",
                    "These are not just technical terms — they represent two completely different electrical environments.",
                    "🔌 AC (Alternating Current) - AC is the electricity used by most homes and businesses. It",
                ],
                "bullets": [
                    "Comes from Eskom/grid",
                    "Powers household plugs and appliances",
                    "Must comply with electrical standards",
                ],
                
                "subsections": [
                    {
                        "heading": "🔋 DC (Direct Current)",
                        "paragraphs": [
                            "DC is the electricity produced and stored inside the energy system. It",
                        ],
                        "bullets": [
                            "Produced by solar panels",
                            "Is stored in batteries",
                            "Is used internally by inverters before converting to AC",
                        ],
                        "images": [
                            {
                                "src": "images/Tip,so in simple terms, homes run on AC.png",
                                "alt": "images/Tip,so in simple terms, homes run on AC.png",
                            },
                        ],
                    },
                    {
                        
                        "paragraphs": [
                            "This is why the inverter is essential. The Inverter's connects these two worlds. It doesn't just convert power — it manages:",
                        ],
                        "bullets": [
                            "Energy flow",
                            "Charging and discharging",
                            "System protection",
                            "Grid interaction",
                        ],
                        "paragraphs_after": [
                            "Without the inverter, the system cannot function as a complete unit.",
                        ],
                        "images": [
                            {
                                "src": "images/most of the faults.png",
                                "alt": "images/most of the faults.png",
                            },
                        ],
                    },
                ],
            },
            {
                "title": "1.6 Core Components of a Modern Energy System",
                "paragraphs": [
                    "Every energy system, no matter how simple or complex, is built using the same core components. Understanding these components helps you visualise how the system works as a whole.",
                    "Instead of seeing separate parts, think of the system as a process:",
                ],
                "images" :[
                            {
                                "src": "images/Tip Energy is.png",
                                "alt": "images/Tip Energy is.png",
                            },
                        ],
                "subsections": [
                    {
                        "heading": "PV Array — Generation",
                        "paragraphs": [
                            "Function: Converts sunlight into direct current (DC) electricity.",
                            "Key Points:",
                        ],
                        "bullets": [
                            "Efficiency depends on orientation, tilt angle, and shading.",
                            "Proper design ensures maximum energy yield throughout the day.",
                            "Usually installed on rooftops or ground mounts facing north in the Southern Hemisphere.",
                        ],
                    },
                    {
                        "heading": "Battery Bank — Storage",
                        "paragraphs": [
                            "Function: Stores electrical energy for later use.",
                            "Key Points:",
                        ],
                        "bullets": [
                            "LiFePO₄ (Lithium Iron Phosphate) batteries provide high safety, high efficiency (~95%), and long cycle life (6 000+).",
                            "Stores energy during low-demand or high-generation periods.",
                            "Supplies backup power during load-shedding or night-time hours.",
                        ],
                    },
                    {
                        "heading": "Inverter — Conversion & Control",
                        "paragraphs": [
                            "Function: Converts DC power from PV or batteries into AC power for use by appliances and the grid.",
                            "Key Points:",
                        ],
                        "bullets": [
                            "Acts as the system's control hub, balancing energy flow between PV, battery, and loads.",
                            "Types include string, hybrid, and off-grid inverters.",
                            "Modern inverters also manage data monitoring, safety isolation, and firmware control.",
                        ],
                    },
                    {
                        "heading": "Load — Energy Consumption",
                        "paragraphs": [
                            "Function: Represents devices and appliances that consume electrical power.",
                            "Key Points:",
                        ],
                        "bullets": [
                            "Includes lighting, electronics, pumps, and industrial machinery.",
                            "Load management ensures balanced and efficient power use.",
                            "Smart load prioritisation can improve battery life and reduce energy costs.",
                        ],
                    },
                    {
                        "heading": "Grid / Generator",
                        "paragraphs": [
                            "Function: Provides supplemental or backup power when solar or battery capacity is insufficient.",
                            "Key Points:",
                        ],
                        "bullets": [
                            "The grid supplies additional power and can export excess energy in grid-tied systems.",
                            "Generators act as off-grid or emergency sources in remote locations.",
                            "Integration requires proper switching and safety compliance (SANS 10142-1).",
                        ],
                        "images" :[
                            {
                                "src": "images/Core components of Energy system.png",
                                "alt": "images/Core components of Energy system.png",
                            },
                        ],
                    },
                ],
            },
            {
                "title": "1.7 How Lithium Batteries Fit into the System",
                "paragraphs": [
                    "At this stage, it's important to keep things simple and focus on function rather than internal design.",
                    "The battery acts as the system's energy reserve. It allows energy to be stored when available and used when needed.",
                    "This changes how energy is used:",
                ],
                "bullets": [
                    "Solar energy is no longer limited to daylight",
                    "Power becomes available during outages",
                    "Energy can be shifted based on demand",
                ],
                "images" :[
                            {
                                "src": "images/Tip battery gives the system flex.png",
                                "alt": "images/Tip battery gives the system flex.png",
                            },
                        ],
                "paragraphs_after": [
                    "We will break down exactly how lithium batteries work, how cells behave, and how battery performance is managed in Module 3.",
                ],
            },
            {
                "title": "1.8 The Four Main System Types",
                "paragraphs": [
                    "Not all systems are built the same. The design depends on the customer's needs, budget, and site conditions.",
                    "Understanding system types helps you recommend the right solution and avoid incorrect installations.",
                    "Each system is defined by how it:",
                ],
                "bullets": [
                    "Uses the grid",
                    "Stores energy",
                    "Supplies power",
                ],
                "subsections": [
                    {
                        "heading": "Backup System (No Solar)",
                        "images": [
                            {
                                "src": "images/Backup System.png",
                                "alt": "Backup System (No Solar)",
                            },
                        ],
                    },
                    {
                        "heading": "Grid-Tied Solar (No Batteries)",
                        "images": [
                            {
                                "src": "images/Grid-tied solar Sytem.png",  
                                "alt": "Grid-Tied Solar (No Batteries)",
                            },
                        ],
                    },
                    {
                        "heading": "Hybrid System (Solar + Battery + Grid)",
                        "images": [
                            {
                                "src": "images/Hybrid Solar System.png",
                                "alt": "Hybrid System (Solar + Battery + Grid)",
                            },
                        ],
                    },
                    {
                        "heading": "Fully Off-Grid System",
                        "images": [
                            {
                                "src": "images/Fully OFF-GRID.png",
                                "alt": "Fully Off-Grid System",
                            },
                        ],
                    },
                ],
            },
            {
                "title": "1.9 Energy Flow and System Operation",
                "paragraphs": [
                    "To properly install and troubleshoot systems, you need to understand how energy moves through them.",
                    "Energy does not flow randomly — it follows a controlled path based on system logic and available sources.",
                    "A hybrid system is the best example because it includes all components.",
                    "Throughout the day, the system constantly makes decisions:",
                ],
                "bullets": [
                    "Use solar first",
                    "Store excess energy",
                    "Use battery when needed",
                    "Use grid as backup",
                ],
                "images" :[
                            {
                                "src": "images/Energy Flow & system operation.png",
                                "alt": "images/Energy Flow & system operation.png",
                            },
                             {
                                "src": "images/Summary of power flow.png",
                                "alt": "images/Summary of power flow.png",
                            },
                            
                        ],
               
            },
            {
                "title": "1.10 Efficiency and System Losses",
                "paragraphs": [
                    "No system is perfectly efficient. Every time energy is converted, stored, or transferred, some of it is lost.",
                    "These losses may seem small individually, but together they affect overall system performance.",
                    "As an installer, your goal is to minimise these losses through:",
                ],
                "bullets": [
                    "Good design",
                    "Correct installation",
                    "Quality components",
                ],
                "images" :[
                            {
                                "src": "images/Tip Small improvements.png",
                                "alt": "images/Tip Small improvements.png",
                            },
                             {
                                "src": "images/Energy Flow & losses.png",
                                "alt": "images/Energy Flow & losses.png",
                            },
                             {
                                "src": "images/Typical system losses.png",
                                "alt": "images/Typical system losses.png",
                            },
                        ],
                
                "subsections": [
                    {
                        "heading": "How to Minimise Losses",
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
                                "images": [
                                    {
                                        "src": "images/Tip-Energy lost in bad design.png",
                                        "alt": "images/Tip-Energy lost in bad design.png",
                                    },
                                ],
                            },
                           
                          
               
                        ],
                    },
                ],
            },
            {
                "title": "1.11 Where REVOV Fits into these Systems",
                "paragraphs": [
                    "REVOV batteries form the storage part of the system, and their performance depends heavily on correct installation and configuration.",
                    "A high-quality battery will only perform well if:",
                ],
                "bullets": [
                    "It is correctly sized",
                    "Properly installed",
                    "Correctly configured",
                ],
                "images": [
                    {
                        "src": "images/Tip-revov product.png",
                        "alt": "images/Tip-revov product.png",
                    },
                    {
                        "src": "images/Revov batteries Benefits.png",
                        "alt": "images/Revov batteries Benefits.png",
                    },
                    {
                        "src": "images/wrapping up module 1.png",
                        "alt": "images/wrapping up module 1.png",
                    },
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
            {
                "question": "2. Which of the following is a major benefit of battery storage?",
                "options": [
                    "A) It increases grid frequency",
                    "B) It provides automatic backup during outages",
                    "C) It removes the need for an inverter",
                    "D) It eliminates all system losses"
                ],
                "answer": "B"
            },
            {
                "question": "3. In practical terms, battery storage helps customers by:",
                "options": [
                    "A) Making all appliances use less power instantly",
                    "B) Saving energy for later use",
                    "C) Replacing the PV array",
                    "D) Increasing the grid voltage"
                ],
                "answer": "B"
            },
            {
                "question": "4. Power (kW) refers to:",
                "options": [
                    "A) Total electricity used over time",
                    "B) Electrical pressure",
                    "C) The rate at which electricity is used right now",
                    "D) Battery lifespan"
                ],
                "answer": "C"
            },
            {
                "question": "5. Energy (kWh) refers to:",
                "options": [
                    "A) The speed of current flow",
                    "B) Total stored or used electricity over time",
                    "C) Cable thickness",
                    "D) Instantaneous load only"
                ],
                "answer": "B"
            },
            {
                "question": "6. Power mainly determines the size of the:",
                "options": [
                    "A) Battery bank",
                    "B) Inverter",
                    "C) PV frame",
                    "D) Earth spike"
                ],
                "answer": "B"
            },
            {
                "question": "7. Energy mainly determines the size of the:",
                "options": [
                    "A) Battery bank",
                    "B) AC breaker only",
                    "C) Inverter fan",
                    "D) Generator enclosure"
                ],
                "answer": "A"
            },
            {
                "question": "8. If a house runs a 1 kW essential load for 5 hours, how much energy is needed?",
                "options": [
                    "A) 1 kWh",
                    "B) 5 kWh",
                    "C) 10 kWh",
                    "D) 0.5 kWh"
                ],
                "answer": "B"
            },
            {
                "question": "9. Why should battery systems not usually be sized around 100% discharge?",
                "options": [
                    "A) Because voltage becomes AC",
                    "B) Because it improves cable size",
                    "C) Because it can shorten battery life and leaves no room for real-world variation",
                    "D) Because batteries cannot store DC energy"
                ],
                "answer": "C"
            },
            {
                "question": "10. The basic formula for battery energy needed is:",
                "options": [
                    "A) Battery size = Voltage × Current",
                    "B) Battery size = Load (kW) × Time (hours)",
                    "C) Battery size = Frequency × Voltage",
                    "D) Battery size = Current ÷ Voltage"
                ],
                "answer": "B"
            },
            {
                "question": "11. What is the first step when calculating backup requirements?",
                "options": [
                    "A) Choose the inverter brand",
                    "B) Identify the essential loads",
                    "C) Set the battery to 100% DoD",
                    "D) Measure grid frequency"
                ],
                "answer": "B"
            },
            {
                "question": "12. If essential loads total 1 kW and the outage duration is 4 hours, the minimum energy needed is:",
                "options": [
                    "A) 1 kWh",
                    "B) 2 kWh",
                    "C) 4 kWh",
                    "D) 8 kWh"
                ],
                "answer": "C"
            },
            {
                "question": "13. In South Africa, typical household AC supply operates at:",
                "options": [
                    "A) 110 V / 60 Hz",
                    "B) 48 V DC",
                    "C) 230 V / 50 Hz",
                    "D) 400 V / 25 Hz"
                ],
                "answer": "C"
            },
            {
                "question": "14. Solar panels and batteries mainly operate in:",
                "options": [
                    "A) AC",
                    "B) DC",
                    "C) Mixed frequency AC",
                    "D) Pulsed AC only"
                ],
                "answer": "B"
            },
            {
                "question": "15. Household plugs and most appliances use:",
                "options": [
                    "A) DC only",
                    "B) AC",
                    "C) Battery voltage directly",
                    "D) PV string voltage"
                ],
                "answer": "B"
            },
            {
                "question": "16. The inverter is essential because it:",
                "options": [
                    "A) Stores solar energy directly in the DB board",
                    "B) Converts between AC and DC and manages power flow",
                    "C) Replaces the battery",
                    "D) Removes the need for grid protection"
                ],
                "answer": "B"
            },
            {
                "question": "17. A useful installer reminder is that most wiring faults happen on the:",
                "options": [
                    "A) AC side",
                    "B) DC side",
                    "C) Load side only",
                    "D) Neutral bar only"
                ],
                "answer": "B"
            },
            {
                "question": "18. Which of the following correctly matches the component with its function?",
                "options": [
                    "A) Battery bank — generates AC power",
                    "B) Inverter — stores energy chemically",
                    "C) PV array — generates DC electricity",
                    "D) Load — converts AC to DC"
                ],
                "answer": "C"
            },
            {
                "question": "19. The main job of the battery bank in a modern energy system is to:",
                "options": [
                    "A) Change frequency",
                    "B) Store energy for later use",
                    "C) Generate sunlight",
                    "D) Replace the inverter"
                ],
                "answer": "B"
            },
            {
                "question": "20. The inverter is best described as the system's:",
                "options": [
                    "A) Mounting frame",
                    "B) Control and conversion hub",
                    "C) Earthing rod",
                    "D) Fuel source"
                ],
                "answer": "B"
            },
            {
                "question": "21. Loads in an energy system are:",
                "options": [
                    "A) Devices and appliances that consume power",
                    "B) Only the battery chargers",
                    "C) Only grid-connected circuits",
                    "D) The inverter settings menu"
                ],
                "answer": "A"
            },
            {
                "question": "22. A backup system with no solar includes:",
                "options": [
                    "A) Solar + battery only",
                    "B) Inverter + battery only",
                    "C) Solar + grid only",
                    "D) Generator only"
                ],
                "answer": "B"
            },
            {
                "question": "23. A hybrid system typically includes:",
                "options": [
                    "A) Solar, battery and grid",
                    "B) Battery only",
                    "C) Solar only",
                    "D) Grid and generator only"
                ],
                "answer": "A"
            },
            {
                "question": "24. In a hybrid system, if PV output drops and the load still needs power, the next source is usually the:",
                "options": [
                    "A) Earth conductor",
                    "B) Battery",
                    "C) PV frame",
                    "D) AC isolator"
                ],
                "answer": "B"
            },
            {
                "question": "25. In a well-designed system, roughly how much of the generated energy is effectively used after typical losses?",
                "options": [
                    "A) 50–60%",
                    "B) 65–75%",
                    "C) 90–95%",
                    "D) 100% exactly"
                ],
                "answer": "C"
            }
        ]
    }

    MODULE_2_ELECTRICAL_FUNDAMENTALS = {
    "module_title": "MODULE 2 – Electrical Fundamentals",
    "module_subtitle": "Electrical basics needed to wire safely, size correctly, and troubleshoot faster.",
    "sections": [
        {
            "title": "Contents",
            "bullets": [
                "2.1 Module 2 Learning Outcomes",
                "2.2 The Core Electrical Terms You Must Be Comfortable With",
                "2.3 AC vs DC in Practice",
                "2.4 Series & Parallel Connections Explained",
                "2.5 Electrical Components",
                "2.6 Earthing & Bonding — The Safety Backbone",
                "2.7 Electrical Safety — Non-Negotiable Rules",
                "2.8 Practical Installer Examples (What Can Go Wrong + How to Fix It)",
            ],
        },
        {
            "title": "2.1 Module 2 Learning Outcomes",
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
            "paragraphs": [
                "These are the terms you will use every day when sizing, wiring, testing and fault finding.",
            ],
            "subsections": [
                {
                    "heading": "Voltage (V) — “Electrical Pressure”",
                    "images": [
                        {
                            "src": "images/Voltage v electrical pressure.png",
                            "alt": "images/Voltage v electrical pressure.png",
                        },
                    ],
                   
                },
                {
                    "heading": "Current (A) — “How Much is Flowing”",
                    "images": [
                        {
                            "src": "images/Current A.png",
                            "alt": "images/Current A.png",
                        },
                    ],
                },
                {
                    "heading": "Resistance (Ω) — “Opposition to Flow”",
                    "images": [
                        {
                            "src": "images/resistance oms.png",
                            "alt": "images/resistance oms.png",
                        },
                    ],
                   
                },
                {
                    "heading": "Power (W / kW) — “How Fast Energy is Used”",
                    "images": [
                        {
                            "src": "images/Power w,kw.png",
                            "alt": "images/Power w,kw.png",
                        },
                    ],
                    
                },
                {
                    "heading": "Energy (Wh / kWh) — “Power Over Time”",
                    "images": [
                        {
                            "src": "images/energy wh,kwh.png",
                            "alt": "images/energy wh,kwh.png",
                        },
                         {
                            "src": "images/Electrical Fundamental.png",
                            "alt": "images/Electrical Fundamental.png",
                        },
                    ],
                    
                },
            ],
        },
        {
            "title": "2.3 AC vs DC in Practice",
            "paragraphs": [
                "This section explains what AC and DC do in the system, why they behave differently, and what that means for wiring, protection and fault finding.",
            ],
            "subsections": [
                {
                    "heading": "In every system",
                    "paragraphs": [
                        "You’re dealing with two completely different electrical environments:",
                    ],
                },
                {
                    "heading": "🔌 AC (Alternating Current)",
                    "paragraphs": [
                        "Household power and comes from Eskom or generator.",
                    ],
                },
                {
                    "heading": "🔋 DC (Direct Current)",
                    "paragraphs": [
                        "Comes from solar panels and batteries.",
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
                            "images":[
                            {
                                "src": "images/if system rumdomly shut.png",
                                "alt": "images/if system rumdomly shut.png",
                            },
                        ],
                        },
                        
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
                            "heading": "AC brings a different set of considerations",
                            "bullets": [
                                "The inverter must match the grid’s voltage and frequency before connecting.",
                                "Neutral and earth must be handled correctly — this is where many nuisance trips start.",
                                "Earth leakage placement matters.",
                                "Protection must comply with SANS wiring standards.",
                            ],
                            "images":[
                            {
                                "src": "images/if customer complains.png",
                                "alt": "images/if customer complains.png",
                            },
                            ]

                        },
                    ],
                },
                {
                    "heading": "The Inverter — The Electrical Traffic Controller",
                    "paragraphs": [
                        "The inverter isn’t just converting power. It’s managing two completely different electrical environments at the same time.",
                        "On one side: DC from PV and battery.",
                        "On the other side: AC for loads and grid.",
                    ],
                    "bullets": [
                        "Where power goes",
                        "When batteries charge/discharge",
                        "When to use grid vs solar",
                        "When to protect the system",
                    ],
                },
                {
                    "heading": "What This Looks Like in Real Life",
                    "images": [
                        {
                            "src": "images/AC,DC ROLE.png",
                            "alt": "images/AC,DC ROLE.png",
                        }
                    ],
                    
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
                            "images": [
                                {
                                    "src": "images/TIP IF YOU SAPARATE AC AND DC MENTALLY.png",
                                    "alt": "images/TIP IF YOU SAPARATE AC AND DC MENTALLY.png",
                                },
                            ],
                        },
                    ],
                },
            ],
        },
        {
            "title": "2.4 Series & Parallel Connections Explained",
            "paragraphs": [
                "One battery is often not enough for a full solar or backup system. Batteries are connected together in series or parallel when a single battery is not enough to meet the voltage or energy requirements of a system.",
                "Sometimes you need:",
            ],
            "bullets": [
                "a higher voltage for the inverter to operate properly",
                "more energy storage",
                "longer backup time",
                "the ability to run bigger appliances",
            ],
            "subsections": [
                {
                    "heading": "Series Connection – Voltage Adds",
                    "paragraphs": [
                        "In a series connection, the batteries are connected positive to negative like a chain.",
                        "The voltage increases, but the storage capacity (Ah) stays the same.",
                        "Think of it like stacking batteries end-to-end to create more push for the electrical system.",
                    ],
                    "bullets": [
                        "You use series when:",
                        "the inverter needs 24V, 48V, etc.",
                        "you need higher system voltage",
                        "you want lower current and more efficient power transfer",
                    ],
                    "images": [
                        {
                            "src": "images/SERIES CONNECTION.png",
                            "alt": "images/SERIES CONNECTION.png",
                        },
                    ],
                },
                {
                    "heading": "Parallel Connection – Capacity Adds",
                    "paragraphs": [
                        "In a parallel connection, all positives connect together and all negatives connect together.",
                        "The voltage stays the same, but the storage capacity increases.",
                        "Imagine two water tanks feeding the same house. The water pressure stays the same, but there is now twice as much water available.",
                    ],
                    "bullets": [
                        "You use parallel when:",
                        "you want longer backup time",
                        "you need more energy storage",
                        "your inverter already works on 12V",
                    ],
                    "images": [
                        {
                            "src": "images/parallel connection.png",
                            "alt": "images/parallel connection.png",
                        },
                         {
                            "src": "images/TIP WHEN CONNECTING.png",
                            "alt": "images/TIP WHEN CONNECTING.png",
                        },
                         {
                            "src": "images/series vs parallel.png",
                            "alt": "images/series vs parallel.png",
                        },
                    ],
                },
                {
                    "heading": "Understanding the Difference",
                    "paragraphs": [
                        "Imagine you have a small backup system with an inverter and two 12V batteries. Depending on how you connect the batteries, the system will behave very differently.",
                    ],
                    "images": [
                        {
                            "src": "images/EXAMPLE, ONE SETUP,TWO WAYS.png",
                            "alt": "images/EXAMPLE, ONE SETUP,TWO WAYS.png",
                        },
                         {
                            "src": "images/series and parallel are not better or wor.png",
                            "alt": "images/series and parallel are not better or wor.png",
                        },
                    ]
                },
            ],
        },
        {
            "title": "2.5 Electrical Components",
            "paragraphs": [
                "Every electrical system needs to:",
            ],
            "bullets": [
                "move power",
                "control power",
                "protect equipment",
                "protect people",
                "manage voltage and current",
                "switch things on and off",
                "communicate between devices",
            ],
            "paragraphs_after": [
                "Electrical components make all this possible.",
                "Without the correct components, electricity would simply flow uncontrolled from the batteries to the equipment — which can lead to overheating, damaged equipment, poor performance, fires, system failures and serious safety risks.",
                "A good battery or solar system is not only about the batteries. The cables, lugs, isolators, fuses, breakers, and connections are just as important.",
            ],
            "subsections": [
                {
                    "heading": "Think of the system like the plumbing in a building",
                    "bullets": [
                        "The battery is the water tank",
                        "The cables are the pipes",
                        "The isolators and breakers are the valves",
                        "The fuses are the emergency safety devices",
                        "The lugs and terminations are the joints connecting everything together",
                    ],
                    "paragraphs_after": [
                        "If any one of these parts is poor quality or installed incorrectly, the whole system can fail.",
                    ],
                    "images": [
                        {
                            "src": "images/Cables carry current.png",
                            "alt": "images/Cables carry current.png",
                        },
                        {
                            "src": "images/Lugs and terminations.png",
                            "alt": "images/Lugs and terminations.png",
                        },
                        {
                            "src": "images/isolators.png",
                            "alt": "images/isolators.png",
                        },
                        {
                            "src": "images/fuses.png",
                            "alt": "images/fuses.png",
                        },
                        {
                            "src": "images/circuit breaker.png",
                            "alt": "images/circuit breaker.png",
                        },
                    ],
                },
            ],
            "notes": [
                "A battery system is only as strong as its weakest connection.",
            ],
            "paragraphs_before": [
                "Even the best battery can fail if:",
            ],
            "bullets_before": [
                "cables are undersized",
                "lugs are loose",
                "breakers are incorrect",
                "fuses are missing",
                "isolators are not installed properly",
            ],
            "paragraphs_after": [
                "Good electrical design is about:",
            ],
            "bullets": [
                "safety",
                "reliability",
                "efficiency",
                "long equipment life",
            ],
            "images": [
                {
                    "src": "images/simple summary.png",
                    "alt": "simple summary diagram",
                }
            ],
        },
        {
            "title": "2.6 Earthing & Bonding — The Safety Backbone",
            "paragraphs": [
                "Earthing and bonding are some of the most important safety parts of any electrical system.",
            ],
            "paragraphs_before": [
                "They help protect:",
            ],
            "bullets_before": [
                "people",
                "equipment",
                "buildings",
                "batteries",
                "inverters",
            ],
            "paragraphs_middle": [
                "Without proper earthing and bonding:",
            ],
            "bullets_middle": [
                "electric shocks can occur",
                "equipment can become damaged",
                "systems can behave unpredictably",
                "lightning damage becomes worse",
                "faults may not trip correctly",
                "fire risks increase",
            ],
            "paragraphs_after": [
                "A good way to understand this is:",
            ],
            "bullets": [
                "Earthing gives dangerous electricity a safe path to the ground",
                "Bonding keeps metal parts at the same electrical level so they cannot become dangerous",
            ],
            "notes": [
                "They work together to make electrical systems safe.",
            ],
                "images": [
                    {
                        "src": "images/Earthing safety first.png",
                        "alt": "images/earthing and bonding.png",
                    },
                      {
                        "src": "images/Bonding.png",
                        "alt": "images/Bonding.png",
                    },
                    
                ],
        },
        {
            "title": "2.7 Electrical Safety — Non-Negotiable Rules",
            "paragraphs": [
                "Electrical safety is non-negotiable because electricity is invisible, extremely powerful, and can cause serious injury, death, fires, or catastrophic equipment damage in seconds if handled incorrectly.",
                "Unlike many other hazards, you often do not get a warning before something goes wrong, a loose connection, incorrect polarity, missing fuse, poor earthing, or accidental contact with live conductors can instantly create dangerous heat, electric shock, arc flash, or system failure.",
                "In battery and solar systems especially, large amounts of stored energy are always present, even when grid power is off, which means safe isolation, proper PPE, correct tools, testing procedures, and compliant installation practices are absolutely essential. Good electrical safety is not about slowing the job down, it is about ensuring that everyone goes home safely, equipment remains protected, and systems operate reliably for years to come.",
            ],
            "images": [
                    {
                        "src": "images/electrical safety.png",
                        "alt": "images of electrical safety",
                    },
                    
            ],    
        },
        {
            "title": "2.8 Practical Installer Examples (What Can Go Wrong + How to Fix It)",
            "paragraphs": [
                "This is where electrical theory becomes real-world consequences.",
                "On paper, these are formulas. On site, they become heat, trips, damage and call-backs.",
                "Let’s walk through real scenarios installers face every day.",
            ],
            "images": [
                    {
                        "src": "images/incorrect cable sizing.png",
                        "alt": "images of electrical safety",
                    },

                    {
                        "src": "images/swapped-reversed.png",
                        "alt": "images of electrical safety",
                    },

                    {
                        "src": "images/poor crimping.png",
                        "alt": "images of electrical safety",
                    },

                    {
                        "src": "images/no dc isolator installed.png",
                        "alt": "images of electrical safety",
                    },

                    {
                        "src": "images/unequal parallel cables.png",
                        "alt": "images of electrical safety",
                    },


                    {
                        "src": "images/wrapping up module 2.png",
                        "alt": "images of electrical safety",
                    },

                    
            ],    

        },
    ],
}
MODULE_2_ASSESSMENT = {
    "title": "Module 2 Assessment",
    "subtitle": "Electrical Fundamentals",
    "questions": [
        {
            "question": "1. Voltage (V) is best described as:",
            "options": [
                "A) The amount of energy stored",
                "B) The flow of electricity",
                "C) The electrical pressure that pushes current",
                "D) The resistance in a cable",
            ],
            "answer": "C",
            "explanation": "Voltage is the electrical potential difference or pressure that drives current flow through a circuit.",
        },
        {
            "question": "2. Current (A) refers to:",
            "options": [
                "A) Electrical pressure",
                "B) The amount of electricity flowing",
                "C) Total energy used over time",
                "D) System voltage",
            ],
            "answer": "B",
            "explanation": "Current is the flow of electricity through a conductor, measured in amperes (A).",
        },
        {
            "question": "3. Resistance (Ω) causes:",
            "options": [
                "A) Increased voltage",
                "B) Reduced cable size",
                "C) Heat, voltage drop and energy loss",
                "D) Higher battery capacity",
            ],
            "answer": "C",
            "explanation": "Resistance opposes current flow and creates heat, causing voltage drop and energy loss in conductors.",
        },
        {
            "question": "4. If voltage increases for the same power demand, current will:",
            "options": [
                "A) Increase",
                "B) Stay the same",
                "C) Decrease",
                "D) Stop flowing",
            ],
            "answer": "C",
            "explanation": "Current is inversely proportional to voltage when power is constant (P = V × I).",
        },
        {
            "question": "5. Why do higher voltage systems improve efficiency?",
            "options": [
                "A) They increase resistance",
                "B) They reduce current and heat losses",
                "C) They eliminate the need for cables",
                "D) They remove the inverter",
            ],
            "answer": "B",
            "explanation": "Higher voltage reduces current flow for the same power, which means less heat loss in cables (P = I²R).",
        },
            {
                "question": "6. Power (kW) refers to:",
                "options": [
                    "A) Total stored electricity",
                    "B) The rate at which energy is used",
                    "C) The resistance of the system",
                    "D) Battery lifespan"
                ],
                "answer": "B"
            },
            {
                "question": "7. The formula for power is:",
                "options": [
                  "A) Power = Current ÷ Voltage",
                  "B) Power = Voltage × Current",
                  "C) Power = Energy × Time",
                  "D) Power = Resistance × Current"
                ],
                "answer": "B"
            },
            {
                "question": "8. Energy (kWh) refers to?",
                "options": [
                    "A) Instantaneous load",
                    "B) Voltage level",
                    "C) Power used over time",
                    "D) Cable size"
                ],
                "answer": "C"
            },
            {
                "question": "9. If a system runs at 2 kW for 3 hours, how much energy is used?",
                "options": [
                    "A) 2 kWh",
                    "B) 3 kWh",
                    "C) 5 kWh",
                    "D) 6 kWh"
                ],
                "answer": "D"
            },
            {
                "question": "10. DC (Direct Current) flows:",
                "options": [
                    "A) In both directions",
                    "B) In one direction only",
                    "C) Only through the grid",
                    "D) Only through AC breakers"
                ],
                "answer": "B"
            },
            {
                "question": "11. One key risk of DC systems is that:",
                "options": [
                  "A) Voltage is always low",
                  "B) DC arcs can sustain and not easily extinguish",
                  "C) Current cannot flow",
                  "D) Polarity does not matter"
                ],
                "answer": "B"
            },
            {
                "question": "12. AC (Alternating Current) in South Africa operates at:",
                "options": [
                 "A) 110 V / 60 Hz",
                 "B) 48 V DC",
                 "C) 230 V / 50 Hz",
                 "D) 400 V / 25 Hz"
                ],
                "answer": "C"
            },
            {
                "question": "13. In South Africa, typical household AC supply operates at:",
                "options": [
                 "A) DC side",
                 "B) AC side",
                 "C) PV frame only",
                 "D) Battery enclosure only"
                ],
                "answer": "B"
            },
            {
                "question": "14. The inverter’s role is best described as:",
                "options": [
                "A) Only converting DC to AC",
                "B) Only storing energy",
                "C) Managing power flow between DC and AC systems",
                "D) Only protecting cables"


                ],
                "answer": "C"
            },
            {
                "question": "15. In a series connection, what happens?",
                "options": [
                  "A) Voltage stays the same, capacity increases",
                  "B) Voltage increases, capacity stays the same",
                  "C) Voltage decreases, capacity increases",
                  "D) Everything stays the same"
                ],
                "answer": "B"
            },
            {
                "question": "16. In a parallel connection, what happens?",
                "options": [
                   "A) Voltage increases",
                   "B) Capacity decreases",
                   "C) Voltage stays the same, capacity increases",
                   "D) Power is removed"
                ],
                "answer": "C"
            },
            {
                "question": "17. Two 48 V batteries connected in series will result in:",
                "options": [
                   "A) 48 V",
                   "B) 96 V",
                   "C) 24 V",
                   "D) 100 Ah"
                ],
                "answer": "B"
            },
            {
                "question": "18. Why must manufacturers’ rules be followed when connecting batteries?",
                "options": [
                    "A) To improve aesthetics",
                    "B) To avoid warranty issues and system damage",
                    "C) To reduce voltage",
                    "D) To increase resistance"
                ],
                "answer": "B"
            },
            {
                "question": "19. If a cable is undersized for the current, what is most likely to happen?",
                "options": [
                  "A) Voltage increases",
                  "B) Cable cools down",
                  "C) Heat builds up and voltage drops",
                  "D) Current disappears"
                ],
                "answer": "C"
            },
            {
                "question": "20. Proper crimping and torque are important because they:",
                "options": [
                    "A) Reduce voltage",
                    "B) Improve cable colour",
                    "C) Prevent resistance and overheating",
                    "D) Increase inverter size"
                ],
                "answer": "C"
            },
            {
                "question": "21. A DC breaker or fuse is mainly used to:",
                "options": [
                    "A) Increase voltage",
                    "B) Protect cables and equipment",
                    "C) Reduce battery capacity",
                    "D) Control AC frequency"
                ],
                "answer": "B"
            },
            {
                "question": "22. Where should battery protection devices ideally be installed?",
                "options": [
                   "A) At the DB board only",
                   "B) Close to the battery",
                   "C) On the roof",
                   "D) Inside the inverter only"
                ],
                "answer": "B"
            },
            {
                "question": "23. Earthing is used to:",
                "options": [
                    "A) Increase system voltage",
                    "B) Store energy",
                    "C) Provide safety and control fault conditions",
                    "D) Reduce inverter size"
                ],
                "answer": "C"
            },
            {
                "question": "24. One of the most important safety steps before working on a system is to:",
                "options": [
                    "A) Increase load",
                    "B) Turn on all breakers",
                    "C) Isolate and test for dead",
                    "D) Disconnect earth"
                ],
                "answer": "C"
            },
            {
                "question": "25. In a parallel battery system, unequal cable lengths can cause:",
                "options": [
                   "A) Equal current sharing",
                   "B) No effect",
                   "C) Uneven current flow and battery imbalance",
                   "D) Increased voltage"
                ],
                "answer": "C",
                "explanation": "Unequal cable lengths create different resistance paths, causing uneven current distribution and battery imbalance.",
            },
        ],
    },

MODULE_3_BATTERY_FUNDAMENTALS = {
    "module_title": "MODULE 3 — Battery Fundamentals",
    "module_subtitle": "Understanding Battery Ratings, Performance, and Installer Considerations",
    "sections": [
        {
            "title": "3.1 Module 3 Learning Outcomes",
            "paragraphs": [
                "This module takes you inside the battery — not just what it does, but how it actually works and behaves on site.",
                "By the end of this module, you will be able to:",
            ],
        },
        {
            "title": "3.2 Understanding Different Battery Types",
            "paragraphs": [
                "There are many different types of batteries used in electrical and energy storage systems, and each type behaves differently in terms of performance, lifespan, safety, charging, maintenance, and cost. ",
                "Common battery technologies include lead-acid, AGM, gel, lithium-ion, and lithium iron phosphate (LiFePO4) batteries.  Understanding the differences is important because each battery type has specific operating requirements, advantages, limitations, and safety considerations that affect how systems are designed, installed, and maintained.  ",
                "Choosing the wrong battery type or treating one technology like another can lead to poor performance, reduced lifespan, or even safety risks. ",
                "For the purposes of this manual, we will focus specifically on lithium iron phosphate (LiFePO4) batteries, as this is the primary battery technology used in modern REVOV energy storage systems.",
            ],
             "images": [
                    {
                        "src": "images/comparing defferences in batteries.png",
                        "alt": "images of battery comparisons",
                    },
                    
            ],    

            

        },
        {
            "title": "3.3 What the Battery Actually Does in the System",
            "paragraphs": [
                "Before you can work confidently with batteries, it is important to understand what the battery is doing in the system.",
                "A battery is a storage device that holds electrical energy chemically and releases it again when the system needs it.",
                "In a solar-battery system, energy is not always used at the same time it is produced.  During the day, solar panels may produce more power than the loads need.  At night, during bad weather, or during outages, there may be little or no solar available. That is where the battery becomes essential.",
                "The battery acts as the system’s energy reserve.",
            ],
            "bullets": [
                "Solar panels generate DC energy",
                "The battery stores that DC energy",
                "The inverter controls when the battery charges or discharges",
                "The loads use battery power when solar is not available or when backup is needed",
            ],
            "paragraphs_after": [
                "A simple way to think about it is this:",
                "The battery is what allows the system to “save power for later.”",
                "Without storage, solar can only help while the sun is shining.",
                "With storage, the system becomes far more flexible, reliable and useful.",
            ],
             "images": [
                    {
                        "src": "images/battery is not there just to add backup.png",
                        "alt": "images of battery is not there just to add backup",
                    },
                    
            ],    
        },
        {
            "title": "3.4 What Is a Lithium-Ion Battery",
            "paragraphs": [
                "A lithium-ion battery is not just a box that holds power.  It is a controlled energy storage system made up of several parts working together.",
                "Inside a typical lithium battery are:",
            ],
            "bullets": [
                "Lithium cells",
                "A Battery Management System (BMS)",
                "Temperature sensors",
                "Voltage and current monitoring",
                "Protection circuits",
                "Communication hardware",
            ],
             "images": [
                    {
                        "src": "images/what is a lithium battery.png",
                        "alt": "images of lithium-ion battery",
                    },
                    
            ],    
            "subsections": [
                {
                    "heading": None,
                    "paragraphs": [
                        "REVOV uses Lithium Iron Phosphate (LiFePO₄) chemistry because it offers the right balance of:",
                    ],
                    "bullets": [
                        "Safety",
                        "Stability",
                        "Long service life",
                        "High efficiency",
                        "Good compatibility with modern inverter systems",
                    ]
                },
                {
                    "heading": None,
                    "paragraphs": [
                        "That is why lithium, and specifically LiFePO₄, has become the preferred choice in modern residential, commercial and industrial storage systems.",
                    ]
                }
            ],
        },
        {
            "title": "3.5 How a Lithium Battery Works",
            "paragraphs": [
                "Now that we understand the battery’s role in the system, the next step is to look at what is happening inside the battery during charging and discharge.",
                "Inside each cell, lithium ions move back and forth. That movement is what allows the battery to store and release energy.",
            ],
            "subsections": [
                {
                    "heading": "Charging (Storing Energy)",
                    "paragraphs": [
                        "When the battery receives power from the inverter or PV system",
                    ],
                    "bullets": [
                        "Lithium ions move from the cathode to the anode",
                        "Energy is stored chemically inside the cell",
                        "The battery “fills up”",
                    ],
                },
                {
                    "heading": "Discharging (Using Energy)",
                    "paragraphs": [
                        "When the system needs power:",
                    ],
                    "bullets": [
                        "Lithium ions move back from the anode to the cathode",
                        "The battery releases usable DC energy",
                        "The inverter then uses that energy to support the load",
                    ],
                    "images": [
                             {
                               "src":"images/how  a lithium ion battery works.png",
                               "alt": "image of how lthium ion battery works.",
                             },

                    ],
                },
            ],
            "paragraphs_after": [
                "That is what makes lithium systems powerful — but also why settings, communication and installation quality matter so much.",
            ],
        },
        {
            "title": "3.6 Inside the Cell",
            "paragraphs": [
                "A single lithium-ion cell is the smallest working unit of the battery. ",
                "The installer does not work with a single cell, you work with the finished battery product. But understanding the cell building blocks helps you understand why voltage, balancing and protection matter so much.  ",
                "What matters is that you understand battery behaviour, because:",
            ],
            "bullets": [
                "Voltage limits come from cell chemistry",
                "Temperature limits come from cell stability",
                "BMS decisions are based on what is happening at cell level.",
            ],
             "images": [
                             {
                               "src":"images/inside a lithium ion cell.png",
                               "alt": "image of inside a lithium ion cell.",
                             },
                              {
                               "src":"images/YOU MAY NEVER OPEN A CELL BUT YOU DEAL WITH THE.png",
                               "alt": "image of you may never open a cell but you deal with the finished product.",
                             },

                    ],
        },
        {
            "title": "REVOV Cell Configuration",
            "paragraphs": [
                "Each LiFePO₄ cell provides a nominal voltage of about 3.2 V. REVOV combine these cells in series and, where required, in parallel to build battery systems suitable for real inverter applications.",
            ],
            "paragraphs_before": [
                "Examples:",
            ],
            "bullets_before": [
                "R100 → ~5.12 kWh (16 cells in series)",
                "R200 → ~10.24 kWh (2 × 16 cell packs in parallel)",
                "C8 Module → high-density rack unit for scalable BESS installations",
            ],
            "paragraphs_middle": [
                "This modular design allows REVOV batteries to deliver:",
            ],
            "bullets_middle": [
                "Stable voltage",
                "Good scalability",
                "Balanced performance",
                "Strong compatibility with modern systems",
            ],
            "paragraphs_section": [
                "Why LiFePO₄?",
            ],
            "paragraphs_after": [
                "Not all lithium chemistries behave the same. The LiFePO₄ composition used by REVOV offers the safest and most durable option available in the market today.",
                "Compared with other battery types or less stable lithium chemistries, LiFePO₄ offers clear practical advantages.",
            ],
            "images": [
                            {
                            "src":"images/feature explanation benefits.png",
                            "alt": "image of feature explanation benefits.",
        
                            },
                           
    
                    ],
            "notes": [
                "That is why LiFePO₄ has become the preferred chemistry for serious backup and hybrid systems.",
            ],
        },
        {
            "title": "3.7 Battery Voltage, Capacity, Power and Energy",
            "paragraphs": [
                "When installers read a battery datasheet, four terms come up again and again: Voltage, Capacity, Energy, Power. These values are related, but they do not mean the same thing.  And if they are confused, batteries are often sized incorrectly.",
            ],
            "subsections": [
                {
                    "heading": "Battery Voltage (V)",
                    "paragraphs": [
                        "Voltage is the electrical pressure of the battery.  Most REVOV low-voltage batteries operate around 48 V / 51.2 V nominal, which makes them suitable for common residential and commercial inverter systems.",
                        "Higher voltage allows the battery to deliver the same power at lower current, which reduces heat and cable sizing.",
                    ],
                    "bullets": [
                        "Less heat",
                        "Smaller cable requirements",
                        "Lower losses",
                        "Better efficiency",
                    ],
                },
                {
                    "heading": "Battery Capacity (Ah)",
                    "paragraphs": [
                        "Capacity, measured in amp-hours (Ah), tells you how much current the battery can supply over time.",
                    ],
                    "images" : [
                        {
                            "src":"images/A 100ah Battery can supply.png",
                            "alt" : "image of a 100ah battery can supply 100 amps for one hour.",
                        }
                    ],
                },
                {
                    "heading": "Battery Energy (kWh)",
                    "paragraphs": [
                        "Energy, measured in kilowatt-hours (kWh), tells you how much total work the battery can do over time.",
                        "Formula: Energy (kWh) = Voltage (V) × Capacity (Ah) ÷ 1000",
                    ],
                    "images" : [
                        {
                            "src":"images/formula Energy(kwh) =.png",
                            "alt" : "image of formula Energy(kwh).",
                        }
                    ],
                },
                {
                    "heading": "Battery Power (kW)",
                    "paragraphs": [
                        "Power tells you how fast the battery can deliver that stored energy.  This is not the same as capacity.",
                    ],
                    "images" : [
                        {
                            "src":"images/a battery may have enough stored energy.png",
                            "alt" : "image of a battery may have enough stored energy.",
                        }
                    ],
                    "images" : [
                        {
                            "src":"images/so in simple terms energy(kwh) tells.png",
                            "alt" : "image of so in simple terms energy(kwh) tells.",
                        },
                        {
                            "src":"images/factors, what it meants.png,",
                            "alt" : "image of so in simple terms energy(kwh) tells.",
                        },
                    ],

                },
            ],
        },
        {
            "title": "3.8 What Is C-Rate?",
            "paragraphs": [
                "One of the most important battery ratings an installer can understand is C-rate, because it tells you how fast the battery can safely charge or discharge.",
                "In simple terms, C-rate tells you the battery's working speed. It tells you how hard the battery can be pushed.",
            ],
            "bullets": [
                "1C Explained = A 1C battery can be charged or discharged fully in 1 hour.",
                "0.5C Explained = A 0.5C battery takes 2 hours to charge or discharge fully.",
            ],
             "images" : [
                        {
                            "src":"images/if battery stores 5kwh and is rated at 1C.png",
                            "alt" : "image of if battery stores 5kwh and is rated at 1C.",
                        }
                    ],

            "paragraphs_after": [
                "So even if two batteries have the same storage capacity, they may not support the same load.",
                "That is a very important installer point. A battery must not only be large enough — it must also be fast enough.",
            ],
            "paragraphs_section": [
                "Why C-Rate Matters",
            ],
            "notes": [
                "If battery demand exceeds its C-rate:",
            ],
            "bullets_final": [
                "The BMS may limit output",
                "The battery may trip on overcurrent",
                "SOC may become unstable or inaccurate",
                "Battery life may reduce",
                "Warranty may be affected",
            ],
            "images" : [
                {
                    "src":"images/Alaways check both energy capcity and power capabilty.png",
                    "alt": " image of capcity check and warnings"
                },
            ],
        },
        {
            "title": "3.9 Key Battery Concepts Installers Must Know",
            "paragraphs": [
                "Now that the main ratings make sense, the next step is to understand the core concepts that affect battery behaviour, lifespan and performance in real installations.",
            ],
            "subsections": [
                {
                    "heading": "Cycle",
                   
                    "images": [
                        {
                            "src": "images/cycle module 3 new.png",
                            "alt": "Cycle diagram",
                        },
                    ],
                },
                {
                    "heading": "State of Charge (SOC)",
                  
                    "images": [
                        {
                            "src": "images/state-of-charge.png",
                            "alt": "State of Charge diagram",
                        },
                    ],
                },
                {
                    "heading": "Depth of Discharge",
                 
                    "images": [
                        {
                            "src": "images/depth-of-discharge.png",
                            "alt": "Depth of Discharge diagram",
                        },
                    ],
                },
                {
                    "heading": "Efficiency",
                 
                    "images": [
                        {
                            "src": "images/efficiency3.png",
                            "alt": "Efficiency diagram",
                        },
                    ],
                },
                {
                    "heading": "Battery Management System (BMS)",
                 
                    "images": [
                        {
                            "src": "images/bms3.png",
                            "alt": "Battery Management System diagram",
                        },
                    ],
                },
                {
                    "heading": "Summary",
                  
                    "images": [
                        {
                            "src": "images/summary.png",
                            "alt": "Summary diagram",
                        },
                    ],
                },
            ],
        },
        {
            "title": "3.10 Temperature Effects — One of the Biggest Battery Killers",
            "paragraphs": [
                "Battery performance is not only about the product itself. Where and how the battery is installed has a major impact on how long it will last and how well it will perform.",
                "Lithium batteries do not like excessive heat.",
                "Heat speeds up degradation, reduces cycle life and may force the BMS to protect the battery by limiting current or shutting the system down.",
                "A practical operating range is usually around 15°C to 35°C",
            ],
            "paragraphs_before": [
                "If temperatures rise too high:",
            ],
            "bullets": [
                "Cycle life shortens",
                "BMS may reduce charging/discharge current",
                "Battery may alarm or shut down",
                "Performance becomes inconsistent",
            ],
            "images": [
                        {
                            "src": "images/DO NOT INSTALL BATTERIES, IN CEILING SPACES.png",
                            "alt": "DO NOT INSTALL BATTERIES, IN CEILING SPACES diagram",
                        },
                    ],
        },
        {
            "title": "3.11 How REVOV Batteries Are Designed",
            "paragraphs": [
                "Once you understand what makes a good battery on paper, the next question is what makes REVOV suitable for real South African installations.",
                "REVOV batteries are designed as complete energy storage products, not just a collection of cells in a box.",
            ],
            "paragraphs_before": [
                "They are built with:",
            ],
            "bullets_before": [
                "LiFePO₄ cell chemistry",
                "Smart BMS with CAN / RS485 communication",
                "Accurate monitoring and protection",
                "Stable voltage performance",
                "Scalable configurations",
                "Rack or floor-mounted product options",
                "High cycle life and strong efficiency",
            ],
            "paragraphs_middle": [
                "This makes them suitable for:",
            ],
            "bullets_middle": [
                "Backup systems",
                "Hybrid systems",
                "Commercial systems",
                "Scalable battery banks",
                "South African operating conditions",
            ],
            "subsections": [
                {
                    "heading": "Why This Matters to Installers",
                    "paragraphs": [
                        "A battery is not just about kWh.",
                        "You also need:",
                    ],
                    "bullets": [
                        "Good communication with the inverter",
                        "Reliable protection",
                        "Stable discharge behaviour",
                        "Proper scalability",
                        "Product support and compatibility",
                    ],
                    "paragraphs_after": [
                        "That is where REVOV fits strongly into the market.",
                        "It gives installers a battery solution designed for real-world use, not just a spec sheet.",
                    ],
                },
            ],
        },
        {
            "title": "3.12 Practical Installer Examples",
            "paragraphs": [
                "Battery theory can look simple on paper. In the field, though, problems usually start when ratings, settings or installation quality do not match the real application.",
            ],
            "images": [
                {
                    "src":"images/a wrong battery for the load.png",
                    "alt": "image for what happens if using wrong battery for the load",
                },
                 {
                    "src":"images/SOC DROPS TOO FAST.png",
                    "alt": "image for what causes soc to trop fast",
                },
                 {
                    "src":"images/BATTERY NEVER REACHES 100%.png",
                    "alt": "image for what makes battery not reach 100%",
                },
            ],
           
        },
        {
            "title": "3.13 Safety When Working with Batteries",
            "paragraphs": [
                "Working safely around batteries is non-negotiable, because stored energy can still be dangerous even when the system looks “off.” ",
            ],
             "images": [
                {
                    "src":"images/SAFETY WHEN WORKING WITH BATTERIES.png",
                    "alt": "image for SAFETY WHEN WORKING WITH BATTERIES.",
                },
                 {
                    "src":"images/BATTERY DOES NOT NEED TO BE ON TO BE DANGEROUS.png",
                    "alt": "image (BATTERY DOES NOT NEED TO BE ON TO BE DANGEROUS.png) for battery can be dangerous even when off.",
                },
                 {
                    "src":"images/WRAPPING UP MODULE 3.png",
                    "alt": "image (WRAPPING UP MODULE 3).",
                },
            ],
           
        },
    ],
}

MODULE_3_ASSESSMENT = {
    "title": "Module 3 Assessment",
    "questions": [
        {
            "question": "1. What is the main job of a battery in an energy system?",
            "options": [
                "A) To generate AC power",
                "B) To store energy for later use",
                "C) To regulate grid voltage",
                "D) To cool the inverter"
            ],
            "answer": "B",
            "explanation": "The battery stores energy and releases it when the system needs it.",
        },
        {
            "question": "2. Why do REVOV systems use LiFePO4 battery chemistry?",
            "options": [
                "A) It is the cheapest battery chemistry available",
                "B) It offers a balance of safety, stability, long life, and efficiency",
                "C) It has the highest energy density of all batteries",
                "D) It is only compatible with generators"
            ],
            "answer": "B",
            "explanation": "LiFePO4 is chosen for safety, stability, long life and efficiency in REVOV systems.",
        },
        {
            "question": "3. What does a Battery Management System (BMS) do?",
            "options": [
                "A) It charges the solar panels",
                "B) It manages and protects the battery cells",
                "C) It converts AC to DC",
                "D) It controls the lights in the house"
            ],
            "answer": "B",
            "explanation": "The BMS monitors, protects and balances the battery cells.",
        },
        {
            "question": "4. What is the primary reason for using a lithium battery instead of a lead-acid battery in modern systems?",
            "options": [
                "A) Lithium batteries are heavier",
                "B) Lithium batteries have better cycle life and efficiency",
                "C) Lead-acid batteries charge faster",
                "D) Lead-acid batteries are more environmentally friendly"
            ],
            "answer": "B",
            "explanation": "Lithium batteries offer better cycle life and efficiency compared to lead-acid.",
        },
        {
            "question": "5. What does the term 'C-rate' describe?",
            "options": [
                "A) The size of the battery",
                "B) How quickly a battery charges or discharges relative to its capacity",
                "C) The battery voltage",
                "D) The number of cells in the battery"
            ],
            "answer": "B",
            "explanation": "C-rate describes charge/discharge speed relative to battery capacity.",
        },
        {
            "question": "6. What happens to battery life if you discharge it more deeply (higher DoD)?",
            "options": [
                "A) Battery life improves",
                "B) Battery life decreases",
                "C) Battery life remains the same",
                "D) Battery life becomes unpredictable"
            ],
            "answer": "B",
            "explanation": "Deeper discharge generally reduces battery cycle life.",
        },
        {
            "question": "7. Which of the following is a common reason to avoid charging batteries in very low temperatures?",
            "options": [
                "A) Charging is faster in low temperatures",
                "B) Low temperatures can cause lithium plating",
                "C) The battery will become too efficient",
                "D) The battery voltage increases automatically"
            ],
            "answer": "B",
            "explanation": "Low-temperature charging can cause lithium plating, damaging the battery.",
        },
        {
            "question": "8. What is SOC?",
            "options": [
                "A) State of Charge",
                "B) Standard Output Current",
                "C) Series of Cells",
                "D) Safety of Circuit"
            ],
            "answer": "A",
            "explanation": "SOC stands for State of Charge.",
        },
        {
            "question": "9. What is DoD?",
            "options": [
                "A) Depth of Discharge",
                "B) Degree of Difference",
                "C) Duration of Discharge",
                "D) Device over Drive"
            ],
            "answer": "A",
            "explanation": "DoD means Depth of Discharge.",
        },
        {
            "question": "10. Which value tells you how much stored energy a battery can deliver over time?",
            "options": [
                "A) Voltage",
                "B) Capacity",
                "C) Energy",
                "D) Power"
            ],
            "answer": "C",
            "explanation": "Energy (kWh) tells you how much stored energy is available over time.",
        },
        {
            "question": "11. What term describes the amount of electrical pressure in a battery?",
            "options": [
                "A) Capacity",
                "B) Energy",
                "C) Voltage",
                "D) Power"
            ],
            "answer": "C",
            "explanation": "Voltage is the electrical pressure in a battery.",
        },
        {
            "question": "12. What does the BMS do when it detects an unsafe battery temperature?",
            "options": [
                "A) It ignores the temperature",
                "B) It may reduce charge/discharge current or disconnect the battery",
                "C) It increases charging speed",
                "D) It changes the battery chemistry"
            ],
            "answer": "B",
            "explanation": "The BMS protects the battery by reducing current or disconnecting it.",
        },
        {
            "question": "13. Which of these is not a component usually found inside a battery enclosure?",
            "options": [
                "A) Cells",
                "B) BMS",
                "C) Temperature sensors",
                "D) Solar panels"
            ],
            "answer": "D",
            "explanation": "Solar panels are not inside the battery enclosure.",
        },
        {
            "question": "14. Which best describes why REVOV selects LiFePO4 chemistry?",
                "options": [
                "A) It is most compact",
                "B) It balances safety, lifespan, efficiency, and reliability",
                "C) It is the most expensive",
                "D) It charges in one minute"
            ],
            "answer": "B",
            "explanation": "REVOV selects LiFePO4 for safety, lifespan, efficiency and reliability.",
        },
        {
            "question": "15. Why is internal resistance important?",
            "options": [
                "A) It makes the battery lighter",
                "B) It affects heat generation and efficiency",
                "C) It increases voltage automatically",
                "D) It prevents the battery from charging"
            ],
            "answer": "B",
            "explanation": "Internal resistance affects heat, efficiency, and performance.",
        },
        {
            "question": "16. What is one effect of using a battery at too high a discharge current?",
            "options": [
                "A) The battery becomes safer",
                "B) The battery may overheat and age faster",
                "C) The battery voltage becomes stable",
                "D) The battery gains capacity"
            ],
            "answer": "B",
            "explanation": "High discharge current can overheat the battery and shorten its life.",
        },
        {
            "question": "17. Which of the following is true about series connections?",
            "options": [
                "A) Voltage adds and capacity stays the same",
                "B) Capacity adds and voltage stays the same",
                "C) Both voltage and capacity add",
                "D) The battery stops working"
            ],
            "answer": "A",
            "explanation": "In series connections, voltage adds while capacity remains the same.",
        },
        {
            "question": "18. Which of the following is true about parallel connections?",
            "options": [
                "A) Voltage adds and capacity stays the same",
                "B) Capacity adds and voltage stays the same",
                "C) Both voltage and capacity add",
                "D) The battery stops working"
            ],
            "answer": "B",
            "explanation": "In parallel connections, capacity adds and voltage stays the same.",
        },
        {
            "question": "19. Which factor is most likely to reduce battery cycle life?",
            "options": [
                "A) Shallow discharge",
                "B) Moderate temperature",
                "C) High temperature and deep discharge",
                "D) Proper charging"
            ],
            "answer": "C",
            "explanation": "High temperature and deep discharge reduce cycle life.",
        },
        {
            "question": "20. What is a safe approach for charging batteries in hot conditions?",
            "options": [
                "A) Charge faster to finish quickly",
                "B) Allow cooling and reduce charge current if needed",
                "C) Leave the battery in direct sun",
                "D) Disconnect the BMS"
            ],
            "answer": "B",
            "explanation": "In hot conditions, allow cooling and reduce charge current when necessary.",
        },
        {
            "question": "21. What does a battery do when there is no solar and the load still needs power?",
            "options": [
                "A) It powers the load from stored energy",
                "B) It generates solar energy",
                "C) It disconnects the inverter",
                "D) It converts DC to AC"
            ],
            "answer": "A",
            "explanation": "The battery supplies stored energy when solar is unavailable.",
        },
        {
            "question": "22. A backup system with no solar includes:",
            "options": [
                "A) Solar + battery only",
                "B) Inverter + battery only",
                "C) Solar + grid only",
                "D) Generator only"
            ],
            "answer": "B",
            "explanation": "A backup system without solar still needs an inverter and battery.",
        },
        {
            "question": "23. A hybrid system typically includes:",
            "options": [
                "A) Solar, battery and grid",
                "B) Battery only",
                "C) Solar only",
                "D) Grid and generator only"
            ],
            "answer": "A",
            "explanation": "Hybrid systems usually include solar, battery and grid.",
        },
        {
            "question": "24. In a hybrid system, if PV output drops and the load still needs power, the next source is usually the:",
            "options": [
                "A) Earth conductor",
                "B) Battery",
                "C) PV frame",
                "D) AC isolator"
            ],
            "answer": "B",
            "explanation": "When solar drops, the battery is usually the next power source.",
        },
        {
            "question": "25. In a well-designed system, roughly how much of the generated energy is effectively used after typical losses?",
            "options": [
                "A) 50–60%",
                "B) 65–75%",
                "C) 90–95%",
                "D) 100% exactly"
            ],
            "answer": "C",
            "explanation": "A well-designed system typically uses 90–95% of generated energy after losses.",
        }
    ]
}


MODULE_4_BMS = {
    "module_title": "MODULE 4 — The Battery Management System (BMS)",
    "module_subtitle": "The brain and protector of every REVOV lithium battery",
    "sections": [
        {
            "title": "4.1 Module 4 Learning Outcomes",
            "paragraphs": [
                "This module takes you inside the control system of the battery — the part that keeps everything safe, stable, and working properly.",
                "By the end of this module, you will be able to:",
            ],
            "bullets": [
                "Explain what a Battery Management System (BMS) is and why it is essential",
                "Understand what the BMS monitors and how it protects the battery",
                "Identify the key protection triggers (overvoltage, undervoltage, temperature, current)",
                "Explain how cell balancing works and why it matters",
                "Understand how the BMS calculates and manages SOC",
                "Understand how communication between the battery and inverter works (CAN, RS485)",
                "Interpret basic battery status indicators and warning signals",
                "Reset and troubleshoot common BMS protection events",
                "Apply correct installer practices when working with BMS-based systems",
            ],
        },
        {
            "title": "4.2 What Is a BMS?",
            "paragraphs": [
                "Before anything else — understand this:",
                "👉 A lithium battery is not just storage.",
                "👉 It is a managed system.",
                "The BMS (Battery Management System) is the “brain” inside the battery.  It",
            ],
            "bullets": [
                "Measures",
                "Controls",
                "Protects",
                "Balances",
                "Communicates",
            ],
            "paragraphs_after": [
                "Without a BMS, lithium batteries would be unsafe, unstable and unreliable.",
                "What the BMS is constantly watching",
                "The BMS constantly monitors the battery in real time:",
            ],
            "bullets_after": [
                "Cell voltages",
                "Cell temperatures",
                "Battery current",
                "SOC (State of Charge)",
                "Charge/discharge limits",
                "Total voltage",
                "Internal resistance",
                "Safety conditions",
            ],
                "images": [
                                {
                                "src":"images/if bms unhappy.png",
                                "alt": "image if bms unhappy.png.",
                                },
                               
    
                        ],
        },
        {
            "title": "4.3 Why the BMS Exists",
            "paragraphs": [
                "A BMS exists to protect the battery, the connected equipment, and the user by ensuring the battery always operates within safe limits. ",
                "",
                "Lithium batteries are powerful and efficient, but they are also sensitive to conditions such as overcharging, deep discharging, excessive current, overheating, and cell imbalance.   Without protection and monitoring, these conditions could damage the battery, shorten its lifespan, reduce performance, or create serious safety risks. ",
                "",
                "The BMS continuously monitors the battery and automatically takes action when something is outside of safe operating conditions. ",
                "",
                "In simple terms, the BMS exists to keep the battery safe, stable, efficient, and reliable while maximizing its performance and lifespan.",
                "",
                "Think of the BMS as a combination of:",
            ],
            "bullets": [
                "A doctor (health monitoring)",
                "A security guard (blocking danger)",
                "A manager (controlling limits)",
                "A translator (communicating with the inverter)",
            ],
        },
        {
            "title": "4.4 What the BMS Monitors",
            "paragraphs": [
                "The BMS constantly monitors important battery conditions to ensure the system operates safely, efficiently, and within its designed limits.  ",
                "It acts like the battery’s intelligent safety controller, continuously checking key values such as voltage, temperature, current flow, state of charge, and overall battery health.  ",
                "If any of these conditions move outside of safe operating ranges, the BMS can automatically take protective action to prevent damage, unsafe conditions, or reduced battery performance.",
                "Let’s break it down in a practical way.",
            ],
            "images": [
                                {
                                
                                "src":"images/what the bms monitor.png",
                                "alt": "image of what the bms monitor.png.",
                                },
                                
                                
                                {
                                "src":"images/the bms sess problems before.png",
                                "alt": "image of the bms sess problems before.png.",
                                },
                               
    
                        ],

        },
        {
            "title": "4.5 Cell Balancing — The Most Important BMS Function",
            "paragraphs": [
                "One of the most important jobs of the BMS is cell balancing.",
                "A lithium battery is not made up of one single large cell. Inside the battery are many smaller individual cells connected together to create the required voltage and capacity. For the battery to operate properly, all these cells must work together evenly.",
                "However, no two cells are ever 100% identical. Over time, small differences naturally develop between the cells due to:",
            ],
            "bullets": [
                "manufacturing tolerances",
                "temperature differences",
                "charging and discharging patterns",
                "age and usage",
            ],
            "paragraphs_after": [
                "This means that some cells may charge slightly faster or discharge slightly faster than others.",
            ],
            "subsections": [
                {
                    "heading": "What does Balancing Mean?",
                    "paragraphs": [
                        "Cell balancing means keeping all the cells at a similar voltage and state of charge so that they work together evenly as one healthy battery pack.",
                        "Think of it like a group of people carrying a heavy table.",
                    ],
                    "description_bullets": [
                        {
                            "condition": "If:",
                            "items": [
                                "everyone lifts evenly → the table stays balanced and moves smoothly",
                                "one person lifts higher or lower than the others → the table tilts and becomes unstable",
                            ],
                        },
                    ],
                    "paragraphs_mid": [
                        "Cell balancing works the same way inside the battery.",
                        "The BMS constantly checks each cell and helps ensure that no individual cell moves too far away from the others.",
                    ],
                },
                {
                    "heading": "Why is Balancing necessary?",
                    "paragraphs": [
                        "The entire battery can only perform as well as its weakest or highest cell.",
                        "If one cell becomes:",
                    ],
                    "bullets": [
                        "too high in voltage",
                        "too low in voltage",
                    ],
                    "paragraphs_after": [
                        "the BMS may need to reduce performance or even shut the battery down to protect it.",
                        "Even if the rest of the cells are healthy, one badly balanced cell can affect the entire battery.",
                    ],
                    "images": [
                        {
                            "src":"images/imagine a battery made up of.png",
                            "alt": "image of imagine a battery made up of.",
                        },
                    ]
                },
                {
                    "heading": "What happens without Balancing?",
                    "paragraphs": [
                        "Without proper balancing:",
                    ],
                    "bullets": [
                        "cell voltages drift further apart over time",
                        "usable battery capacity reduces",
                        "charging becomes less efficient",
                        "the battery may trip more often",
                        "stress on certain cells increases",
                        "lifespan becomes shorter",
                    ],
                    "paragraphs_after": [
                        "Eventually:",
                    ],
                    "bullets_after": [
                        "some cells may become damaged permanently",
                    ],
                },
                {
                    "heading": "How the BMS Balances Cells",
                    "paragraphs": [
                        "The BMS continuously monitors the voltage of every individual cell.",
                        "When it notices certain cells becoming higher than others, it can:",
                    ],
                    "bullets": [
                        "reduce charge to those cells",
                        "bleed small amounts of energy away from high cells",
                        "allow lower cells time to catch up",
                    ],
                    "paragraphs_after": [
                        "This process helps keep the entire battery pack balanced and stable.",
                    ],
                    "images": [
                        {
                            "src": "images/cell balancing.png",
                            "alt": "image of cell balancing",
                        },
                    ],
                },
                {
                    "heading": "Why Initial Full Charge is Critical for Balancing",
                    "paragraphs": [
                        "The BMS can only properly balance the cells when the battery reaches its full charging range. This is because the balancing process typically happens near the top end of the charge cycle, where the BMS can clearly identify which cells are charging faster or reaching higher voltages than the others.",
                        "If the battery never reaches full charge, the BMS does not get the opportunity to correct these small differences between the cells. Over time, the cells can drift further apart, causing imbalance within the battery pack.",
                        "Think of it like trying to level a group of runners in a race — if the race never reaches the finish line, you cannot clearly see who arrived first or last. The same happens inside the battery. The BMS needs the battery to reach full charge so it can properly compare, adjust, and balance the cells.",
                        "This is why the initial full charge is so important after installation or commissioning. It allows the BMS to synchronize and balance the cells correctly from the beginning, helping ensure:",
                    ],
                    "bullets": [
                        "maximum usable capacity",
                        "stable performance",
                        "accurate state of charge readings",
                        "proper battery operation",
                        "longer battery lifespan",
                    ],
                    "paragraphs_after": [
                        "Without reaching full charge regularly, the battery may eventually show reduced performance, premature shutdowns, or inaccurate battery readings even though the cells still contain energy.",
                    ],
                        "images": [
                            {
                                "src": "images/bms can not balance.png",
                                "alt": "image of bms can not balance",
                            },
                        ],
                },
            ],
        },
        {
            "title": "4.6 Protection Modes — Why the BMS Shuts Down",
            "paragraphs": [
                "When the BMS trips, it’s not a fault — it’s protection.",
                "The BMS will shut down if it detects:",
            ],
            "bullets": [
                "❗ Overvoltage",
                "Charging pushed too high (wrong inverter settings).",
                "❗ Undervoltage",
                "Battery drained too far.",
                "❗ Overtemperature",
                "Hot environment or poor airflow ",
                "❗ Undertemperature",
                "Charging at sub-zero temperatures.",
                "❗ Overcurrent",
                "Load exceeds battery capability ",
                "❗ Short circuit",
                "Instant disconnect for safety.",
            ],
            "images": [
                {
                    "src": "images/bms will always choose safety over c.png.",
                    "alt": "image of bms will always choose safety over c.png",
                },
            ],
        },
                {
            "title": "4.7 BMS Communication Protocols",
            "paragraphs": [
                "Modern lithium batteries do not work alone, they constantly communicate with other devices in the system. This communication happens through what are called communication protocols.",
                "A communication protocol is simply a language that allows the battery's BMS and other equipment, such as the inverter, to exchange information and work together correctly.",
                "Think of it like two people trying to have a conversation. If both people speak the same language, communication is clear and everything works properly. If they speak different languages, misunderstandings happen.",
                "The same applies to batteries and inverters.",
            ],
            "subsections": [
                {
                    "heading": "Why Communication is Important",
                    "paragraphs": [
                        "The BMS continuously monitors important battery information such as:",
                    ],
                    "bullets": [
                        "battery voltage",
                        "current flow",
                        "temperature",
                        "state of charge (SOC)",
                        "alarms and warnings",
                        "charging limits",
                        "battery health",
                    ],
                    "paragraphs_after": [
                        "The BMS then sends this information to the inverter or other system devices so the entire system can operate safely and efficiently.",
                        "Without communication:",
                    ],
                    "bullets_after": [
                        "the inverter is mostly guessing",
                        "charging may not be optimized",
                        "battery protection becomes limited",
                        "performance may reduce",
                        "faults and shutdowns become more likely",
                    ],
                },
                {
                    "heading": "What the BMS Communicates",
                    "paragraphs": [
                        "The BMS may communicate:",
                    ],
                    "bullets": [
                        "how full the battery is",
                        "maximum charge current allowed",
                        "maximum discharge current allowed",
                        "battery temperature",
                        "warnings or fault conditions",
                        "whether charging should stop",
                        "whether discharge should stop",
                    ],
                    "paragraphs_after": [
                        "This helps protect the battery while improving performance and lifespan.",
                    ],
                },
                {
                    "heading": "Common Communication Protocols",
                    "paragraphs": [
                        "Different manufacturers use different communication protocols, which are simply different languages that batteries, inverters, and other devices use to communicate with each other.",
                        "Some of the most common protocols used in battery systems include:",
                    ],
                    "bullets": [
                        "CAN Bus (CAN communication)",
                        "RS485",
                        "Modbus",
                        "RS232",
                    ],
                    "paragraphs_after": [
                        "For proper system operation, the battery and inverter must be able to understand the same communication language. Even if the battery is connected correctly and the voltage matches the inverter requirements, poor or incompatible communication can still lead to problems such as",
                    ],
                    "bullets_after": [
                        "inaccurate state of charge readings,",
                        "poor charging performance,",
                        "limited battery protection,",
                        "nuisance alarms, or",
                        "unstable system behaviour.",
                    ],
                    "paragraphs_final": [
                        "Proper protocol compatibility ensures that all devices in the system can communicate effectively and operate safely, efficiently, and reliably together.",
                    ],
                    "images": [
                        {
                            "src": "images/imagine .png",
                            "alt": "image of communication protocols.png",
                        },
                    ]
                },
                {
                    "heading": "Battery-to-Battery Communication",
                    "paragraphs": [
                        "In systems where multiple lithium batteries are connected in parallel, the batteries also need to communicate with each other, not just with the inverter. This allows all the batteries in the system to operate together as one coordinated battery bank instead of as separate independent batteries.",
                        "Think of it like a team carrying a heavy object together. If everyone lifts and walks at the same pace, the load is shared evenly and the job becomes stable and efficient. But if one person carries more weight or moves faster than the others, the load becomes uneven and problems start to occur. Battery-to-battery communication works in a very similar way.",
                        "The batteries continuously exchange important information such as:",
                    ],
                    "bullets": [
                        "voltage",
                        "current",
                        "temperature",
                        "state of charge",
                        "alarms and warnings",
                        "charging and discharge limits",
                    ],
                    "paragraphs_after": [
                        "This communication allows the system to:",
                    ],
                    "bullets_after": [
                        "balance the workload evenly between batteries",
                        "synchronize charging and discharge behaviour",
                        "improve battery protection",
                        "improve system stability",
                        "prevent one battery from working harder than the others",
                    ],
                    "paragraphs_final": [
                        "In most parallel battery systems, one battery is automatically assigned as the master battery. The master battery communicates with the inverter and coordinates the operation of the other batteries, commonly referred to as slave batteries.",
                        "The slave batteries then follow the instructions and operating parameters of the master battery so that the entire battery bank functions as one unified system.",
                        "Without proper battery-to-battery communication, the batteries may not share load evenly, charging may become inconsistent, alarms may occur more frequently, and overall system performance and battery lifespan may be reduced.",
                    ],

                    "images": [
                        {
                            "src": "images/master battery and slave.png",
                            "alt": "image of master battery and slave.png",
                        }
                    ]
                },
            ],
        },
        {
            "title": "4.8 How the BMS Calculates SOC Accurately",
            "paragraphs": [
                "State of Charge, or SOC, is the battery’s estimated “fuel level”, similar to the fuel gauge in a vehicle. It tells the user approximately how much usable energy remains in the battery, usually shown as a percentage from 0% to 100%.",
                "Calculating SOC accurately in a lithium battery is actually quite complex.  Unlike a fuel tank, you cannot simply “look inside” the battery to see how full it is.  Instead, the BMS uses a combination of measurements, calculations, and historical data to estimate the battery’s charge level as accurately as possible.",
            ],
            "paragraphs_after": [
                "The BMS Uses Multiple Factors",
                "The BMS constantly monitors and calculates:",
            ],
            "bullets_after": [
                "voltage ",
                "current flow ",
                "charging and discharge activity ",
                "battery temperature ",
                "cell behaviour ",
                "historical energy usage ",
            ],
            "paragraphs_after2": [
                "It then combines all this information to estimate the remaining battery capacity.",
                "",
                "Coulomb Counting – Tracking Energy In and Out",
                "One of the main methods used is called coulomb counting.",
            ],
            "paragraphs_after3": [
                "This means the BMS continuously measures:",
                "• how much energy goes into the battery during charging ",
                "• how much energy leaves during discharge ",
            ],
            "subsections": [
                {
                    "heading": "Think of it like tracking money in a bank account:",
                    "bullets": [
                        "deposits increase the balance",
                        "withdrawals reduce the balance",
                    ],
                    "paragraphs_after": [
                        "The BMS does something very similar with battery energy.",
                    ],
                    "images": [
                        {
                            "src": "images/imagine a 100ah.png",
                            "alt": "image of imagine a 100ah battery.png",
                        },
                    ]
                },
                {
                    "heading": "Why Voltage Alone Cannot Determine SOC",
                    "paragraphs": [
                        "Many people assume battery voltage directly indicates how full the battery is, but lithium batteries behave differently from older battery technologies.",
                        "A lithium battery can maintain a very similar voltage across a large portion of its charge range. This means:",
                    ],
                    "bullets": [
                        "a battery at 80% SOC",
                        "and a battery at 40% SOC",
                    ],
                    "paragraphs_after": [
                        "may still display very similar voltage readings.",
                        "This is why the BMS cannot rely on voltage alone and instead uses multiple measurements and calculations together to determine SOC more accurately.",
                    ],
                },
                {
                    "heading": "Why Full Charge is Important for SOC Accuracy",
                    "paragraphs": [
                        "Over time, small calculation deviations naturally occur during normal operation.",
                        "To maintain accurate SOC readings, the BMS requires reference points to recalibrate itself, with a full charge being one of the most important.",
                        "When the battery reaches full charge:",
                    ],
                    "bullets": [
                        "the BMS can synchronize and balance the cells",
                        "verify the battery is fully charged",
                        "correct small SOC calculation inaccuracies",
                        "improve overall SOC accuracy",
                    ],
                    "paragraphs_after": [
                        "This is why allowing the battery to periodically reach full charge is important for maintaining accurate battery readings and stable system operation.",
                    ],
                },
                {
                    "heading": "Temperature and Cell Balancing Also Affect SOC",
                    "paragraphs": [
                        "Battery temperature and cell balance directly influence SOC calculations.",
                        "Changes in temperature affect battery performance and energy delivery, while unbalanced cells can reduce calculation accuracy and usable capacity.",
                        "The BMS therefore continuously monitors:",
                    ],
                    "bullets": [
                        "battery temperature",
                        "cell voltages",
                        "balancing status",
                    ],
                    "paragraphs_after": [
                        "to improve SOC estimation and maintain safe operation.",
                    ],
                },
                {
                    "heading": "Why Accurate SOC Matters",
                    "paragraphs": [
                        "Accurate SOC calculation is critical for:",
                    ],
                    "bullets": [
                        "reliable runtime estimation",
                        "proper inverter operation",
                        "battery protection",
                        "efficient charging and discharging",
                        "overall system stability",
                    ],
                    "paragraphs_after": [
                        "Incorrect SOC readings can result in:",
                    ],
                    "bullets_after": [
                        "unexpected shutdowns",
                        "reduced battery performance",
                        "inaccurate runtime estimates",
                        "charging problems",
                        "poor system behaviour",
                    ],
                    "paragraphs_final": [
                        "The BMS therefore plays a critical role in ensuring the SOC displayed to the user is as accurate and reliable as possible.",
                    ],
                },
            ],
        },
        {
            "title": "4.9 LED Indicators & Display Messages",
            "paragraphs": [
                "Each battery model varies, but typically LEDs show:",
            ],
            "bullets": [
                "Running (normal operation)",
                "Charging",
                "Discharging",
                "BMS warning",
                "BMS error/trip",
            ],
            "paragraphs_after": [
                "Always check the manual for LED meaning for the specific REVOV model.",
            ],
        },
        {
            "title": "4.10 Resetting a BMS Protection Event",
            "paragraphs": [
                "A BMS protection event occurs when the Battery Management System detects an unsafe operating condition and temporarily protects the battery by limiting or stopping charging and/or discharging. ",
                "This is a normal safety function designed to prevent damage to the battery, connected equipment, or the user.",
            ],
            "paragraphs_after": [
                "Common protection events may include:",
            ],
            "bullets_after": [
                "overvoltage ",
                "undervoltage ",
                "overcurrent ",
                "short circuit ",
                "overtemperature ",
                "communication faults ",
                "cell imbalance ",
            ],
            "subsections": [
                {
                    "heading": "Key First Step",
                    "paragraphs": [
                        "When a protection event occurs, the first step is always to identify and correct the cause of the fault before attempting to reset the battery.",
                    ],
                    "images": [
                        {
                            "src": "images/safety never repeatedly reset.png",
                            "alt": "image of first step.png",
                        },
                    ],  
                },
                {
                    "heading": "General Reset Process",
                    "paragraphs": [
                        "The exact reset procedure may vary depending on the battery manufacturer and system design, but the following process is commonly used in lithium battery systems.",
                    ],
                    "subsections": [
                        {
                            "heading": "Step 1 – Identify the Fault",
                            "paragraphs": [
                                "Check:",
                            ],
                            "bullets": [
                                "inverter alarms",
                                "battery indicators",
                                "monitoring software",
                                "communication messages",
                            ],
                            "paragraphs_after": [
                                "Determine what caused the protection event. For example:",
                            ],
                            "bullets_after": [
                                "low battery voltage",
                                "excessive load",
                                "overheating",
                                "incorrect settings",
                                "communication failure",
                            ],
                            "paragraphs_footer": [
                                "The fault condition must be corrected first.",
                            ],
                        },
                        {
                            "heading": "Step 2 – Remove the Cause of the Fault",
                            "paragraphs": [
                                "Before resetting:",
                            ],
                            "bullets": [
                                "reduce or disconnect excessive loads",
                                "allow the battery to cool down if overheated",
                                "verify correct inverter and charging settings",
                                "inspect cables and connections",
                                "check communication cables",
                                "ensure voltage is within safe operating range",
                            ],
                            "paragraphs_after": [
                                "The BMS may not reset if the unsafe condition still exists.",
                            ],
                        },
                        {
                            "heading": "Step 3 – Isolate the Battery (If Required)",
                            "paragraphs": [
                                "In some systems, the battery may need to be safely isolated by:",
                            ],
                            "bullets": [
                                "switching off the inverter",
                                "opening the battery isolator or breaker",
                                "disconnecting charging sources if required",
                            ],
                            "paragraphs_after": [
                                "Always follow manufacturer procedures and safe isolation practices.",
                            ],
                        },
                        {
                            "heading": "Step 4 – Restart the Battery",
                            "paragraphs": [
                                "Depending on the battery design, the reset may occur by:",
                            ],
                            "bullets": [
                                "pressing the battery power/reset button",
                                "cycling the battery off and back on",
                                "reconnecting the breaker or isolator",
                                "applying a charging source",
                                "allowing the BMS to automatically recover",
                            ],
                            "paragraphs_after": [
                                "Some low-voltage protection events automatically reset once charging is detected.",
                            ],
                        },
                    ],
                },
                {
                    "heading": "Why the BMS Sometimes 'Locks' the Battery",
                    "paragraphs": [
                        "Some serious protection events may place the battery into a locked protection state to prevent repeated damage.",
                        "This may happen after:",
                    ],
                    "bullets": [
                        "severe undervoltage",
                        "repeated faults",
                        "internal BMS errors",
                        "short circuits",
                    ],
                    "paragraphs_after": [
                        "In these cases:",
                    ],
                    "bullets_after": [
                        "special reset procedures",
                        "software tools",
                        "or technical support",
                    ],
                    "paragraphs_footer": [
                        "may be required.",
                    ],
                },
                {
                    "heading": "Important Installer Considerations",
                    "paragraphs": [
                        "When troubleshooting protection events, always verify:",
                    ],
                    "bullets": [
                        "correct inverter settings",
                        "correct battery communication",
                        "proper cable sizing",
                        "secure terminations",
                        "correct breaker and fuse sizing",
                        "adequate ventilation",
                        "proper commissioning procedure",
                    ],
                    "images": [
                        {
                            "src": "images/many protection events are caused by.png",
                            "alt": "image of important installer considerations.png",
                        },
                    ],
                },
            ],
        },
        {
            "title": "4.11 Practical Installer Examples",
            "paragraphs": [
                "",
            ],
             "images": [
                        {
                            "src": "images/over c trip.png",
                            "alt": "image of important installer considerations.png",
                        },
                        {
                            "src": "images/soc drop trip.png",
                            "alt": "image of important installer considerations.png",
                        },
                        {
                            "src": "images/overvoltage warning.png",
                            "alt": "image of important installer considerations.png",
                        },
                        {
                            "src": "images/temperature shutdown.png",
                            "alt": "image of important installer considerations.png",
                        },
                        {
                            "src": "images/low voltage protec.png",
                            "alt": "image of important installer considerations.png",
                        },
                        {
                            "src": "images/short circuit.png",
                            "alt": "image of important installer considerations.png",
                        },
                    ],
        },
        {
            "title": "4.12 Installer Rules When Working With BMS-Based Batteries",
            "paragraphs": [
                "",
            ],
               "images": [
                   {
                      "src": "images/installer rule when working with bms.png",
                      "alt": "image of installer rules when working with bms based batteries.png",
                   },
                   {
                      "src": "images/wrapping up module 4.png",
                      "alt": "image of installer rules when working with bms based batteries.png",
                   },

               ],
        },
    ],
}

MODULE_4_ASSESSMENT = {
    "title": "Module 4 Assessment",
    "questions": [
        {
            "question": "1. The BMS is best described as:",
            "options": [
                "A) A backup power source",
                "B) The brain and control system of the battery",
                "C) A DC isolator",
                "D) A type of inverter",
            ],
            "answer": "B",
            "explanation": "The BMS is the brain and control system that manages the battery.",
        },
        {
            "question": "2. Without a BMS, a lithium battery would be:",
            "options": [
                "A) More efficient",
                "B) Safer",
                "C) Unsafe and unreliable",
                "D) Easier to install",
            ],
            "answer": "C",
            "explanation": "A BMS is essential for safety and reliability in lithium batteries.",
        },
        {
            "question": "3. The BMS is responsible for:",
            "options": [
                "A) Generating AC power",
                "B) Monitoring, protecting and controlling the battery",
                "C) Increasing battery voltage",
                "D) Replacing protection devices",
            ],
            "answer": "B",
            "explanation": "The BMS monitors, protects and controls the battery system.",
        },
        {
            "question": "4. Which of the following does the BMS monitor?",
            "options": [
                "A) Cell voltage only",
                "B) Grid frequency only",
                "C) Voltage, temperature, current and SOC",
                "D) Only inverter output",
            ],
            "answer": "C",
            "explanation": "The BMS monitors voltage, temperature, current and SOC among other things.",
        },
        {
            "question": "5. If one cell voltage becomes too high or too low, the BMS will:",
            "options": [
                "A) Ignore it",
                "B) Increase current",
                "C) Stop charging or discharging",
                "D) Increase inverter size",
            ],
            "answer": "C",
            "explanation": "The BMS will protect the battery by stopping charge or discharge when a cell is outside safe limits.",
        },
        {
            "question": "6. Why is temperature monitoring important?",
            "options": [
                "A) It improves cable colour",
                "B) Lithium batteries must operate within safe temperature limits",
                "C) It increases capacity",
                "D) It removes the need for ventilation",
            ],
            "answer": "B",
            "explanation": "Lithium batteries must operate within safe temperatures to remain safe and reliable.",
        },
        {
            "question": "7. Internal resistance in a battery can indicate:",
            "options": [
                "A) Improved performance",
                "B) Battery aging or connection issues",
                "C) Increased inverter output",
                "D) Higher SOC",
            ],
            "answer": "B",
            "explanation": "High internal resistance is often a sign of aging or connection issues.",
        },
        {
            "question": "8. The BMS protects the battery from:",
            "options": [
                "A) Only overcharging",
                "B) Only undervoltage",
                "C) Multiple conditions like overcurrent, temperature and voltage issues",
                "D) Only grid faults",
            ],
            "answer": "C",
            "explanation": "The BMS protects against multiple conditions including overcurrent, temperature and voltage problems.",
        },
        {
            "question": "9. If inverter settings push voltage too high during charging, the BMS will trigger:",
            "options": [
                "A) Overcurrent",
                "B) Overvoltage protection",
                "C) Temperature shutdown",
                "D) SOC reset",
            ],
            "answer": "B",
            "explanation": "The BMS will activate overvoltage protection if charging voltage becomes too high.",
        },
        {
            "question": "10. If the battery is drained too far, the BMS will trigger:",
            "options": [
                "A) Overvoltage",
                "B) Undervoltage protection",
                "C) Overcurrent",
                "D) Communication fault",
            ],
            "answer": "B",
            "explanation": "The BMS protects the battery by triggering undervoltage protection when it is drained too far.",
        },
        {
            "question": "11. The BMS will always prioritise:",
            "options": [
                "A) Customer convenience",
                "B) Maximum output",
                "C) Safety",
                "D) Speed of charging",
            ],
            "answer": "C",
            "explanation": "The BMS always prioritises safety above all else.",
        },
        {
            "question": "12. Cell balancing ensures that:",
            "options": [
                "A) All batteries charge faster",
                "B) All cells stay at the same voltage",
                "C) Voltage increases",
                "D) Current is reduced",
            ],
            "answer": "B",
            "explanation": "Cell balancing keeps all cells at similar voltages.",
        },
        {
            "question": "13. Poor balancing can lead to:",
            "options": [
                "A) Improved efficiency",
                "B) Longer lifespan",
                "C) Reduced capacity and inaccurate SOC",
                "D) Higher inverter output",
            ],
            "answer": "C",
            "explanation": "Poor balancing can reduce capacity and make SOC estimates inaccurate.",
        },
        {
            "question": "14. When does balancing usually occur?",
            "options": [
                "A) At low SOC",
                "B) During system shutdown",
                "C) Near full charge",
                "D) Only during discharge",
            ],
            "answer": "C",
            "explanation": "Cell balancing normally happens near full charge.",
        },
        {
            "question": "15. Why is reaching 100% charge important occasionally?",
            "options": [
                "A) To increase voltage",
                "B) To allow proper cell balancing and SOC calibration",
                "C) To reduce inverter size",
                "D) To increase cable current",
            ],
            "answer": "B",
            "explanation": "Occasional full charges help with cell balancing and SOC calibration.",
        },
        {
            "question": "16. Communication between battery and inverter typically uses:",
            "options": [
                "A) Ethernet only",
                "B) CAN, RS485 or Modbus",
                "C) AC cabling",
                "D) Fibre optics only",
            ],
            "answer": "B",
            "explanation": "Battery-to-inverter communication commonly uses CAN, RS485 or Modbus.",
        },
        {
            "question": "17. If communication is incorrect or missing, one likely issue is:",
            "options": [
                "A) Improved efficiency",
                "B) Accurate SOC",
                "C) SOC drift and incorrect behaviour",
                "D) Reduced battery temperature",
            ],
            "answer": "C",
            "explanation": "Missing or incorrect communication can cause SOC drift and wrong behaviour.",
        },
        {
            "question": "18. The most accurate method the BMS uses to calculate SOC is:",
            "options": [
                "A) Voltage reading only",
                "B) Coulomb counting",
                "C) Temperature measurement",
                "D) Resistance calculation",
            ],
            "answer": "B",
            "explanation": "Coulomb counting is the most accurate SOC estimation method used by the BMS.",
        },
        {
            "question": "19. Voltage-based SOC estimation is mainly used:",
            "options": [
                "A) At full or empty states",
                "B) During charging only",
                "C) During discharge only",
                "D) Instead of BMS",
            ],
            "answer": "A",
            "explanation": "Voltage-based SOC estimation is mainly reliable at full or empty states.",
        },
        {
            "question": "20. A battery shutting down under load is often:",
            "options": [
                "A) A manufacturing defect",
                "B) The BMS protecting the battery",
                "C) A cable colour issue",
                "D) A grid fault only",
            ],
            "answer": "B",
            "explanation": "A shutdown under load is often the BMS protecting the battery.",
        },
        {
            "question": "21. If a battery never reaches 100% SOC over long periods, a likely issue is:",
            "options": [
                "A) Too much balancing",
                "B) Poor balancing and SOC inaccuracy",
                "C) Increased efficiency",
                "D) Reduced voltage",
            ],
            "answer": "B",
            "explanation": "A battery that never reaches full SOC likely has poor balancing and inaccurate SOC estimates.",
        },
        {
            "question": "22. High temperatures around the battery can cause:",
            "options": [
                "A) Improved performance",
                "B) Faster charging",
                "C) BMS shutdown or current limitation",
                "D) Increased SOC",
            ],
            "answer": "C",
            "explanation": "High temperatures can force the BMS to limit current or shut down for protection.",
        },
        {
            "question": "23. Before resetting a BMS fault, you should:",
            "options": [
                "A) Immediately restart the inverter",
                "B) Ignore the fault",
                "C) Identify the cause of the issue",
                "D) Increase load",
            ],
            "answer": "C",
            "explanation": "You should identify and resolve the cause before resetting a BMS fault.",
        },
        {
            "question": "24. Mixing different battery brands in one system can cause:",
            "options": [
                "A) Better performance",
                "B) No effect",
                "C) Conflicts in BMS logic and system instability",
                "D) Increased voltage",
            ],
            "answer": "C",
            "explanation": "Mixing brands can cause compatibility issues and unstable BMS logic.",
        },
        {
            "question": "25. Exceeding the battery’s C-rate can result in:",
            "options": [
                "A) Higher capacity",
                "B) BMS limiting or shutting down output",
                "C) Increased lifespan",
                "D) Lower current",
            ],
            "answer": "B",
            "explanation": "Exceeding C-rate often causes the BMS to limit or stop output to protect the battery.",
        },
    ],
},

MODULE_5_ENERGY_SYSTEM_DESIGN = {
    "module_title": "MODULE 5 — Energy System Design & Sizing",
    "module_subtitle": "How to design reliable, safe, high-performance solar + battery systems",
    "sections": [
        {
            "title": "5.1 Module 5 Learning Outcomes",
            "paragraphs": [
                "This module brings everything together — electrical fundamentals, batteries, BMS and real-world installation thinking.",
                "By the end of this module, you will be able to:",
            ],
            "bullets": [
                "Assess and calculate essential loads (kW and kWh)",
                "Size batteries correctly based on runtime requirements",
                "Select the correct inverter based on peak demand",
                "Size a solar array to support both loads and battery charging",
                "Understand how system components must work together",
                "Apply correct cable sizing and voltage drop principles",
                "Design systems that maximise battery lifespan and efficiency",
                "Identify common system design mistakes before installation",
                "Understand the basics of larger commercial and BESS systems",
            ],
        },
        {
            "title": "5.2 Why System Design Matters",
            "paragraphs": [
                "System design is one of the most important parts of any battery or solar installation because it determines how safely, efficiently, and reliably the entire system will operate.",
                "Even the best batteries and inverters can perform poorly or fail if the system is designed incorrectly. A properly designed system ensures that all components work together correctly, that the battery bank is sized appropriately for the application, that cables and protection devices are correctly selected, and that the inverter, battery, and loads are compatible with each other.",
                "Think of it like building a vehicle. A powerful engine alone does not guarantee a good car — the brakes, gearbox, fuel system, suspension, and tyres must all work together correctly.",
                "The same applies to energy storage systems. Every component must be correctly selected and properly matched to the rest of the system.",
                "Good system design helps ensure:",
            ],
            "bullets": [
                "stable and reliable operation",
                "correct battery charging and discharge behaviour",
                "improved safety",
                "longer battery lifespan",
                "proper load handling",
                "efficient energy usage",
                "reduced faults and downtime",
            ],
            "bullets_after": [
                "nuisance tripping",
                "overheating",
                "incorrect charging",
                "shortened battery life",
                "communication problems",
                "overloaded components",
                "unstable system behaviour",
                "safety risks",
            ],
            "images": [
                {
                    "src":"images/a properly designed system.png",
                    "alt":"A Properly Designed System"
                },
            ],
        },
                {
            "title": "5.3 Step 1 — Load Assessment: Understanding What Must Be Powered",
            "paragraphs": [
                "The first and most important step in designing any battery or solar system is understanding exactly what the system needs to power. This process is called a load assessment.",
                "A load assessment helps determine how much power the system must supply, how long the system must run, which appliances are critical, and how large the inverter and battery bank need to be.",
            ],
            "subsections": [
                {
                    "heading": "What is a 'Load'?",
                    "paragraphs": [
                        "A load is anything that consumes electrical power.",
                        "Examples include:",
                    ],
                    "bullets": [
                        "lights",
                        "TVs",
                        "Wi-Fi routers",
                        "fridges",
                        "computers",
                        "kettles",
                        "pumps",
                        "air conditioners",
                        "machinery",
                    ],
                    "paragraphs_after": [
                        "Every load uses a certain amount of power, usually measured in:",
                    ],
                    "bullets_after": [
                        "watts (W)",
                        "or kilowatts (kW)",
                    ],
                },
                {
                    "heading": "Why Load Assessment is So Important",
                    "paragraphs": [
                        "The battery and inverter can only supply a limited amount of power and energy.",
                        "If the system is not designed around the actual loads:",
                    ],
                    "bullets": [
                        "the inverter may overload",
                        "the batteries may drain too quickly",
                        "runtime may be much shorter than expected",
                        "equipment may trip or shut down",
                    ],
                    "paragraphs_after": [
                        "A proper load assessment ensures the system is designed realistically for the customer's needs.",
                    ],
                },
                {
                    "heading": "Understanding Two Important Things",
                    "paragraphs": [
                        "A load assessment looks at:",
                    ],
                    "numbered": [
                        "How much power is needed at one time",
                        "How long the loads must run",
                    ],
                    "paragraphs_after": [
                        "These are two different things.",
                    ],
                },
                {
                    "heading": "1. Power Requirement (Instant Demand)",
                    "paragraphs": [
                        "This is the total power the system must supply at a specific moment.",
                    ],
                    "images": [
                        {
                            "src": "images/Appliance ,power.png",
                            "alt" : "image of power requirement",

                        },
                    ],
                    "subsections": [
                        {
                            "heading": "Peak Loads and Startup Loads",
                            "paragraphs": [
                                "Some appliances require extra power when starting.",
                                "Examples:",
                            ],
                            "bullets": [
                                "fridges",
                                "pumps",
                                "compressors",
                                "air conditioners",
                            ],
                            "paragraphs_after": [
                                "A fridge may normally run at:",
                            ],
                            "bullets_after": [
                                "150W",
                            ],
                            "paragraphs_footer": [
                                "But during startup it may briefly draw 600W or more.",
                                "The inverter must be able to handle these short startup surges.",
                            ],
                        },
                    ],
                },
                {
                    "heading": "2. Energy Requirement (Runtime)",
                    "paragraphs": [
                        "This determines how long the system must supply power.",
                        "Think of it like a fuel tank:",
                    ],
                    "bullets": [
                        "power = how hard the engine works",
                        "energy capacity = how long the fuel lasts",
                    ],
                    "images": [
                        {
                            "src" :"images/if a 500w load runs.png",
                            "alt" : "",
                        },
                    ],
                },
                {
                    "heading": "Critical Loads vs Non-Essential Loads",
                    "paragraphs": [
                        "Not everything needs backup power. A good load assessment helps identify:",
                    ],
                    "bullets": [
                        "critical loads",
                        "non-essential loads",
                    ],
                    "subsections": [
                        {
                            "heading": "Critical Loads",
                            "paragraphs": [
                                "These are the important items the customer wants to keep running during power outages.",
                                "Examples:",
                            ],
                            "bullets": [
                                "lights",
                                "internet",
                                "TV",
                                "security systems",
                                "computers",
                                "essential plugs",
                            ],
                        },
                        {
                            "heading": "Non-Essential Loads",
                            "paragraphs": [
                                "These are high-power appliances that may not need battery backup.",
                                "Examples:",
                            ],
                            "bullets": [
                                "ovens",
                                "geysers",
                                "kettles",
                                "pool pumps",
                                "large air conditioners",
                            ],
                            "paragraphs_after": [
                                "Excluding unnecessary loads helps:",
                            ],
                            "bullets_after": [
                                "reduce system cost",
                                "improve runtime",
                                "reduce battery stress",
                            ],
                            "images" : [
                                {
                                    "src" :"images/if a 500w load runs.png",
                                    "alt" : "",
                                },
                            ],
                        },
                    ],
                },
                {
                    "heading": "Why Accurate Information Matters",
                    "paragraphs": [
                        "Customers often underestimate their usage.",
                        "For example:",
                    ],
                    "bullets": [
                        "a kettle may use 2000W+",
                        "a hairdryer may use 1800W+",
                        "an air fryer may use 1500W+",
                    ],
                    "paragraphs_after": [
                        "Just one of these appliances can overload a small backup system.",
                        "This is why installers must properly assess the real expected loads.",
                    ],
                },
                {
                    "heading": "Future Expansion Must Also Be Considered",
                    "paragraphs": [
                        "Good system design also considers:",
                    ],
                    "bullets": [
                        "future appliances",
                        "additional batteries",
                        "solar expansion",
                        "changing customer needs",
                    ],
                    "paragraphs_after": [
                        "A system designed too tightly may become limiting later.",
                    ],
                    "images": [
                        {
                            "src":"images/essesntial loads calculations.png",
                            "alt":"Load Assessment"
                       },
                        {
                            "src":"images/customer always adds loads.png",
                            "alt":"Load Assessment"
                       },
                   ],

                },
            ],
            
        },
                {
            "title": "5.4 Step 2 — Calculate Backup Time Requirements (kWh)",
            "paragraphs": [
                "Once the loads have been identified, the next step is to determine how long the customer wants those loads to operate during a power outage. This is called the backup time requirement and is one of the most important factors when sizing a battery system.",
                "The backup time requirement determines:",
            ],
            "bullets": [
                "how much energy storage is needed",
                "how large the battery bank must be",
                "how long the system can support the required loads",
            ],
            "paragraphs_after": [
                "While inverter sizing is mainly based on power (kW), battery sizing is mainly based on energy storage capacity, usually measured in kilowatt-hours (kWh).",
            ],
            "subsections": {
                "Understanding the Difference Between kW and kWh": {
                    "paragraphs": [
                        "This is one of the most important concepts in battery system design.",
                    ],
                    "subsections": {
                        "kW (Kilowatts) = Power": {
                            "paragraphs": [
                                "This refers to how much power is being used at a specific moment.",
                            ],
                            "bullets": [
                                "Think of it like the speed of a vehicle",
                                "or how hard the engine is working",
                            ],
                        },
                        "kWh (Kilowatt-hours) = Energy": {
                            "paragraphs": [
                                "This refers to how much energy is used over time.",
                            ],
                            "bullets": [
                                "Think of it like how much fuel the vehicle uses during the trip",
                            ],
                        },
                    },
                },
                "Simple Formula": {
                    "paragraphs": [
                        "Backup energy requirement is calculated as:",
                    ],
                    "bullets": [
                        "Power (kW) × Time (Hours) = Energy Required (kWh)",
                    ],
                },
                "Why Backup Time Requirements Are So Important": {
                    "paragraphs": [
                        "Two customers may have exactly the same loads but completely different battery requirements depending on how long they want backup power.",
                    ],
                    "subsections": {
                        "Example Comparison": {
                            "paragraphs": [
                                "Customer A requires 2 hours of backup for a 1kW load",
                                "Customer B requires 10 hours of backup for a 1kW load",
                                "Even though the load is identical, Customer B needs a much larger battery bank",
                            ],
                        },
                    },
                },
            },
        },
        {
            "title": "5.5 Step 3 — Select the Correct Battery Size",
            "paragraphs": [
                "Once the load assessment and backup time requirements have been calculated, the next step is selecting the correct battery size.",
                "This is one of the most important parts of system design because the battery determines how much energy the system can store and how long the loads can operate during a power outage.",
                "The battery must be correctly sized to:",
            ],
            "bullets": [
                "support the required loads",
                "provide the required backup time",
                "operate safely within its limits",
                "allow for future expansion where necessary",
                "avoid excessive battery stress",
            ],
            "subsections": [
                {
                    "heading": "Battery Size Scenarios",
                    "subsections": [
                        {
                            "heading": "If the battery is too small:",
                            "bullets": [
                                "runtime will be shorter than expected",
                                "the battery may discharge too quickly",
                                "the system may shut down prematurely",
                                "battery lifespan may reduce due to excessive cycling",
                            ],
                        },
                        {
                            "heading": "If the battery is too large:",
                            "bullets": [
                                "system cost increases unnecessarily",
                                "charging times may become longer",
                                "the customer may pay for unused capacity",
                            ],
                        },
                    ],
                    "paragraphs_after": [
                        "The goal is therefore to select a battery size that is practical, efficient, reliable, and suitable for the customer's actual needs.",
                    ],
                },
                {
                    "heading": "Battery Capacity is Measured in kWh",
                    "paragraphs": [
                        "Battery size is usually measured in:",
                    ],
                    "bullets": [
                        "kilowatt-hours (kWh)",
                    ],
                    "paragraphs_after": [
                        "This represents:",
                    ],
                    "bullets_after": [
                        "how much energy the battery can store",
                    ],
                    "paragraphs_footer": [
                        "The larger the kWh rating:",
                    ],
                    "bullets_footer": [
                        "the longer the system can run the loads",
                    ],
                    "images": [
                        {
                            "src" : "images/load assesment requred runtime.png",
                            "alt" : "",
                        },
                    ],
                },
                {
                    "heading": "Why Additional Capacity is Important",
                    "paragraphs": [
                        "Real-world systems must account for:",
                    ],
                    "bullets": [
                        "inverter losses",
                        "reserve capacity",
                        "surge loads",
                        "battery aging",
                        "temperature effects",
                        "future expansion",
                        "depth of discharge limits",
                    ],
                    "paragraphs_after": [
                        "This means installers usually recommend a slightly larger battery than the minimum calculated requirement.",
                    ],
                    "subsections": [
                        {
                            "heading": "Example: From Calculation to Real-World Recommendation",
                            "paragraphs": [
                                "Although the calculation shows:",
                            ],
                            "bullets": [
                                "approximately 2kWh required",
                            ],
                            "paragraphs_after": [
                                "An installer may recommend:",
                            ],
                            "bullets_after": [
                                "a 5kWh battery",
                            ],
                            "paragraphs_footer": [
                                "Why? Because the larger battery:",
                            ],
                            "bullets_footer": [
                                "reduces battery stress",
                                "improves runtime stability",
                                "allows for future load growth",
                                "provides reserve capacity",
                                "improves battery lifespan",
                            ],
                        },
                    ],
                },
                {
                    "heading": "Matching Battery Size to Inverter Size",
                    "paragraphs": [
                        "The battery must also be suitable for the inverter's power requirements.",
                        "A very large inverter connected to a very small battery may:",
                    ],
                    "bullets": [
                        "overload the battery",
                        "exceed discharge limits",
                        "trigger BMS protection events",
                    ],
                    "paragraphs_after": [
                        "The battery and inverter must therefore be correctly matched.",
                    ],
                },
            ],
        },
                {
            "title": "5.6 Step 4 — Select the Correct Inverter Size",
            "paragraphs": [
                "Once the battery size has been determined, the next step is selecting the correct inverter size.",
                "The inverter is one of the most important components in the system because it converts the battery's DC power into usable AC power for appliances and electrical equipment.",
                "The inverter must be correctly sized to:",
            ],
            "bullets": [
                "safely handle the required loads",
                "support startup surges",
                "operate efficiently",
                "communicate correctly with the battery",
                "provide stable system performance",
            ],
            "subsections": [
                {
                    "heading": "Inverter Size Scenarios",
                    "subsections": [
                        {
                            "heading": "If the inverter is too small:",
                            "bullets": [
                                "it may overload",
                                "trip during operation",
                                "struggle with startup loads",
                                "shut down unexpectedly",
                            ],
                        },
                        {
                            "heading": "If the inverter is too large:",
                            "bullets": [
                                "system cost increases unnecessarily",
                                "efficiency at low loads may reduce",
                                "the battery may not be able to support the inverter properly",
                            ],
                        },
                    ],
                    "paragraphs_after": [
                        "The goal is to select an inverter that matches the real power requirements of the system while allowing reasonable operating headroom.",
                    ],
                },
                {
                    "heading": "Understanding Inverter Size",
                    "paragraphs": [
                        "Inverter size is usually measured in:",
                    ],
                    "bullets": [
                        "watts (W)",
                        "or kilowatts (kW)",
                    ],
                    "paragraphs_after": [
                        "This refers to:",
                    ],
                    "bullets_after": [
                        "how much power the inverter can supply at a specific moment",
                    ],
                    "paragraphs_footer": [
                        "Unlike battery sizing, which is mainly based on runtime and energy storage (kWh), inverter sizing is mainly based on instantaneous power demand.",
                    ],
                    "images" : [
                        {
                            "src" : "images/example inverter size.png",
                            "alt" : "",
                        },
                    ],
                },
                {
                    "heading": "Continuous Power vs Surge Power",
                    "paragraphs": [
                        "Most inverters have:",
                    ],
                    "bullets": [
                        "a continuous power rating",
                        "and a surge rating",
                    ],
                    "subsections": [
                        {
                            "heading": "Continuous Rating",
                            "paragraphs": [
                                "The power the inverter can safely supply continuously during normal operation.",
                            ],
                        },
                        {
                            "heading": "Surge Rating",
                            "paragraphs": [
                                "Some appliances draw much higher power when starting than during normal operation.",
                                "Examples include:",
                            ],
                            "bullets": [
                                "fridges",
                                "pumps",
                                "compressors",
                                "air conditioners",
                                "power tools",
                            ],
                            "paragraphs_after": [
                                "A fridge may normally use:",
                            ],
                            "bullets_after": [
                                "150W",
                            ],
                            "paragraphs_footer": [
                                "But during startup it may briefly draw 600W or more.",
                                "This is called a surge load or startup current.",
                                "The inverter must be capable of handling these short bursts of power without tripping or shutting down.",
                            ],
                             "images" : [
                                 {
                                   "src" : "images/inverter may be rated.png",
                                   "alt" : "",
                                 },
                            ],

                        },
                    ],
                },
                {
                    "heading": "Matching the Inverter to the Battery",
                    "paragraphs": [
                        "The inverter and battery must work together correctly.",
                        "A very large inverter connected to a very small battery may:",
                    ],
                    "bullets": [
                        "exceed the battery's discharge limits",
                        "trigger BMS protection events",
                        "cause voltage drops",
                        "reduce battery lifespan",
                    ],
                    "paragraphs_after": [
                        "The battery must be capable of supplying the current the inverter requires.",
                    ],
                },
                {
                    "heading": "Matching the Inverter to the System Voltage",
                    "paragraphs": [
                        "The inverter must also match the battery bank voltage.",
                        "For example:",
                    ],
                    "bullets": [
                        "a 48V inverter requires a 48V battery bank",
                        "a 24V inverter requires a 24V battery bank",
                    ],
                    "paragraphs_after": [
                        "Incorrect voltage matching can damage equipment or prevent operation entirely.",
                    ],
                },
                {
                    "heading": "Communication Compatibility",
                    "paragraphs": [
                        "Modern lithium systems also rely heavily on communication between:",
                    ],
                    "bullets": [
                        "the inverter",
                        "and the battery BMS",
                    ],
                    "paragraphs_after": [
                        "Compatible communication improves:",
                    ],
                    "bullets_after": [
                        "charging accuracy",
                        "protection",
                        "SOC accuracy",
                        "system stability",
                    ],
                    "paragraphs_footer": [
                        "Proper inverter selection therefore includes:",
                    ],
                    "bullets_footer": [
                        "electrical compatibility",
                        "communication compatibility",
                        "manufacturer support compatibility",
                    ],
                },
                {
                    "heading": "Installer Consideration",
                    "paragraphs": [
                        "Customers often focus only on: (How many appliances can the inverter run?)",
                        "But installers must also consider:",
                    ],
                    "bullets": [
                        "surge loads",
                        "battery capability",
                        "runtime expectations",
                        "future growth",
                        "charging requirements",
                        "system efficiency",
                    ],
                    "images": [
                        {
                            "src" : "images/PROPER INVERTER SIZING.png",
                            "alt" : "",
                        }
                    ]
                },
            ],
        },
                {
            "title": "5.7 Step 5 — Size the Solar PV Array",
            "paragraphs": [
                "Once the battery and inverter have been selected, the next step is sizing the solar PV array. The solar array is responsible for generating the energy that powers the loads and recharges the batteries.",
                "Correct solar sizing is extremely important because the solar panels must generate enough energy to:",
            ],
            "bullets": [
                "supply daytime loads",
                "recharge the batteries",
                "compensate for system losses",
                "support reliable system operation throughout the year",
            ],
            "subsections": [
                {
                    "heading": "Solar Array Size Scenarios",
                    "subsections": [
                        {
                            "heading": "If the solar array is too small:",
                            "bullets": [
                                "batteries may not fully recharge",
                                "backup time may reduce",
                                "the system may rely heavily on grid or generator support",
                                "battery lifespan may shorten due to chronic undercharging",
                            ],
                        },
                        {
                            "heading": "If the solar array is too large:",
                            "bullets": [
                                "equipment limits may be exceeded",
                                "unnecessary costs may increase",
                                "the inverter or charge controller may limit excess production",
                            ],
                        },
                    ],
                    "paragraphs_after": [
                        "The goal is therefore to design a solar array that provides sufficient energy generation while remaining within the safe operating limits of the system.",
                    ],
                },
                {
                    "heading": "Understanding Solar Panel Power",
                    "paragraphs": [
                        "Solar panels are usually rated in:",
                    ],
                    "bullets": [
                        "watts (W)",
                        "or kilowatts peak (kWp)",
                    ],
                    "paragraphs_after": [
                        "This rating indicates the maximum power the panel can produce under ideal test conditions.",
                    ],
                    "images" : [
                        {
                            "src" : "images/SOLAR PANNEL OWER 550W.png",
                            "alt" : "",
                        },
                    ],
                },
                {
                    "heading": "Solar Array Sizing Starts with Energy Usage",
                    "paragraphs": [
                        "The first step in PV sizing is understanding:",
                    ],
                    "bullets": [
                        "how much energy the system uses per day",
                    ],
                    "paragraphs_after": [
                        "This is usually measured in:",
                    ],
                    "bullets_after": [
                        "kWh per day",
                    ],
                    "paragraphs_footer": [
                        "Imagine the system uses 5kWh per day.",
                        "The solar array must generate enough energy to:",
                    ],
                    "bullets_footer": [
                        "run the daytime loads",
                        "recharge the battery for nighttime use",
                        "compensate for system losses",
                    ],
                    "paragraphs_extra": [
                        "In practice, the solar array must therefore generate more than the exact daily usage figure.",
                    ],
                },
                {
                    "heading": "Understanding Peak Sun Hours",
                    "paragraphs": [
                        "Solar panels do not produce full power all day long.",
                        "The amount of usable sunlight is often referred to as:",
                    ],
                    "bullets": [
                        "Peak Sun Hours (PSH)",
                    ],
                    "paragraphs_after": [
                        "This represents the average number of hours per day during which the solar panels produce near-rated output.",
                    ],
                    "images" : [
                        {
                            "src" : "images/SOLAR SIZING EXAMPLE.png",
                            "alt" : "",
                        },
                    ],
                },
                {
                    "heading": "Losses Must Be Considered",
                    "paragraphs": [
                        "Solar systems experience losses from:",
                    ],
                    "bullets": [
                        "inverter efficiency",
                        "temperature",
                        "cable losses",
                        "panel mismatch",
                        "dirt and dust",
                        "charging losses",
                        "shading",
                        "weather variation",
                    ],
                    "paragraphs_after": [
                        "Because of this, installers usually oversize the array slightly to ensure reliable performance.",
                    ],
                    "images" : [
                        {
                            "src" : "images/ALTHOUGH THE CALCULATIONS.png",
                            "alt" : "",
                        },
                    ],
                },
                {
                    "heading": "Panel Orientation and Tilt Matter",
                    "paragraphs": [
                        "Solar production is also heavily affected by:",
                    ],
                    "bullets": [
                        "roof direction",
                        "tilt angle",
                        "shading",
                    ],
                    "paragraphs_after": [
                        "Poor panel placement can significantly reduce performance.",
                        "For example: Partial shading on one panel may affect the output of an entire string.",
                        "This is why proper site assessment is important.",
                    ],
                },
                {
                    "heading": "Series and Parallel PV Design",
                    "paragraphs": [
                        "Solar panels can also be connected in:",
                    ],
                    "bullets": [
                        "series",
                        "parallel",
                    ],
                    "paragraphs_after": [
                        "Similar to batteries.",
                        "Series PV Connection = Increases voltage",
                        "Parallel PV Connection = Increases current",
                        "The PV array must be designed within:",
                    ],
                    "bullets_after": [
                        "inverter limits",
                        "MPPT voltage ranges",
                        "current limits",
                        "safety requirements",
                    ],
                },
                {
                    "heading": "Matching the PV Array to the Inverter",
                    "paragraphs": [
                        "The solar array must remain within the inverter's:",
                    ],
                    "bullets": [
                        "maximum PV voltage",
                        "maximum PV current",
                        "MPPT operating range",
                    ],
                    "paragraphs_after": [
                        "Incorrect PV sizing can:",
                    ],
                    "bullets_after": [
                        "damage equipment",
                        "prevent startup",
                        "reduce efficiency",
                        "trigger faults",
                    ],
                    "paragraphs_footer": [
                        "This is why solar design calculations are extremely important.",
                    ],
                    "images": [
                        {
                            "src" : "images/EXAMPLE SOLAR SIZING.png",
                            "alt" : "",
                        },
                    ],
                },
            ],
        },
                {
            "title": "5.8 Step 6 — Check Inverter-to-Battery Compatibility",
            "paragraphs": [
                "Once the battery, inverter, and solar array have been selected, it is critical to ensure that the inverter and battery are fully compatible with each other.",
                "This is one of the most important parts of system design because even high-quality equipment may not operate correctly if the devices are not properly matched.",
                "Many installation problems are not caused by faulty equipment, but rather by compatibility issues between the inverter and battery.",
                "The inverter and battery must work together correctly in terms of:",
            ],
            "bullets": [
                "voltage",
                "charging parameters",
                "communication protocols",
                "current limits",
                "operating logic",
                "protection settings",
            ],
            "paragraphs_after": [
                "If compatibility is poor, the system may still power on, but performance, reliability, and battery protection can be significantly affected.",
            ],
            "subsections": [
                {
                    "heading": "Why Compatibility Matters",
                    "paragraphs": [
                        "Modern lithium batteries are intelligent systems controlled by a BMS (Battery Management System). The inverter and BMS constantly exchange information to ensure the battery operates safely and efficiently.",
                        "The inverter relies on the battery BMS to provide information such as:",
                    ],
                    "bullets": [
                        "battery state of charge (SOC)",
                        "charge and discharge limits",
                        "battery temperature",
                        "alarms and warnings",
                        "battery protection status",
                    ],
                    "paragraphs_after": [
                        "If the inverter cannot properly communicate with the BMS:",
                    ],
                    "bullets_after": [
                        "charging may become inaccurate",
                        "battery protection may reduce",
                        "runtime estimates may be incorrect",
                        "nuisance faults may occur",
                        "battery lifespan may shorten",
                    ],
                },
                {
                    "heading": "Voltage Compatibility",
                    "paragraphs": [
                        "The first requirement is ensuring the inverter and battery operate at the same system voltage.",
                    ],
                    "images" : [
                        {
                            "src" : "images/VOLTAGE COMPATIBILTY.png",
                            "alt" : "Voltage Compatibility Diagram",
                        }
                    ]
                },
                {
                    "heading": "Communication Compatibility",
                    "paragraphs": [
                        "Modern lithium systems rely heavily on communication between:",
                    ],
                    "bullets": [
                        "the inverter",
                        "and the battery BMS",
                    ],
                    "paragraphs_after": [
                        "This communication usually occurs through:",
                    ],
                    "bullets_after": [
                        "CAN Bus",
                        "RS485",
                        "Modbus",
                    ],
                    "paragraphs_footer": [
                        "The inverter and battery must support compatible communication protocols and correct communication settings.",
                    ],
                },
                {
                    "heading": "Charge and Discharge Current Compatibility",
                    "paragraphs": [
                        "The battery must also be capable of safely supplying the current the inverter requires.",
                        "A large inverter connected to a very small battery may demand excessive current.",
                        "This can result in:",
                    ],
                    "bullets": [
                        "BMS overcurrent protection events",
                        "voltage drops",
                        "system shutdowns",
                        "excessive battery stress",
                    ],
                    "paragraphs_after": [
                        "The inverter and battery must therefore be sized appropriately together.",
                    ],
                },
                {
                    "heading": "Charging Parameter Compatibility",
                    "paragraphs": [
                        "The inverter charging settings must match the battery manufacturer's specifications, including:",
                    ],
                    "bullets": [
                        "charge voltage",
                        "float voltage",
                        "charge current",
                        "low-voltage cut-off",
                        "temperature behaviour",
                    ],
                    "paragraphs_after": [
                        "Incorrect charging settings can:",
                    ],
                    "bullets_after": [
                        "reduce battery lifespan",
                        "cause poor SOC accuracy",
                        "trigger BMS faults",
                        "prevent proper balancing",
                    ],
                },
                {
                    "heading": "Parallel Battery Compatibility",
                    "paragraphs": [
                        "If multiple batteries are installed in parallel:",
                    ],
                    "bullets": [
                        "battery firmware",
                        "communication settings",
                        "battery versions",
                        "addressing",
                    ],
                    "paragraphs_after": [
                        "must also be compatible.",
                        "Incorrect parallel configuration may lead to:",
                    ],
                    "bullets_after": [
                        "communication faults",
                        "uneven load sharing",
                        "unstable operation",
                        "protection events",
                    ],
                    "images": [
                        {
                            "src": "images/INVERTER TO BATTERY COMPATI.png",
                            "alt": "Parallel Battery Compatibility Diagram"
                        },
                    ],
                },
            ],
        },
        {
            "title": "5.9 Step 7 — Voltage Drop and Cable Sizing",
            "paragraphs": [
                "Correct cable sizing is a critical part of system design because cables are responsible for safely carrying power between the batteries, inverter, solar panels, and loads.",
                "Even the best inverter and battery system can perform poorly if the cables are undersized or installed incorrectly.",
                "Cables may seem simple, but they directly affect:",
            ],
            "bullets": [
                "system safety",
                "efficiency",
                "voltage stability",
                "charging performance",
                "inverter operation",
                "battery lifespan",
            ],
            "paragraphs_after": [
                "Incorrect cable sizing is one of the most common causes of:",
            ],
            "bullets_after": [
                "overheating",
                "inverter faults",
                "poor charging",
                "voltage instability",
                "nuisance tripping",
                "damaged terminals",
                "fire risks",
            ],
            "subsections": {
                "Understanding Voltage Drop": {
                    "paragraphs": [
                        "Voltage drop is the reduction in voltage that occurs as electricity travels through a cable.",
                        "As current flows through a cable:",
                    ],
                    "bullets": [
                        "the cable creates resistance",
                        "resistance causes energy loss",
                        "some voltage is lost along the cable",
                    ],
                },
                "Impact of Cable Length and Current": {
                    "paragraphs": [
                        "The longer the cable or the higher the current, the greater the voltage drop becomes.",
                    ],
                },
                "Effects of Excessive Voltage Drop": {
                    "paragraphs": [
                        "Excessive voltage drop can cause:",
                    ],
                    "bullets": [
                        "poor inverter performance",
                        "incorrect charging behaviour",
                        "low battery voltage alarms",
                        "reduced efficiency",
                        "excessive heat",
                        "unstable system operation",
                    ],
                },
                "Special Considerations for Battery Systems": {
                    "paragraphs": [
                        "In battery systems, this becomes especially important because battery systems often operate at:",
                        "These conditions make proper cable sizing critical for reliable operation.",
                    ],
                    "bullets": [
                        "high current",
                        "relatively low voltage",
                    ],
                    "images" : [
                        {
                            "src" : "images/EVEN SMALL VOLTAGE LOSSES.png",
                            "alt" : "Cable Sizing Illustration",
                        },
                         {
                            "src" : "images/EXAMPLE VOLTAGE DROP.png",
                            "alt" : "Cable Sizing Illustration",
                        },
                    ],
                },
            },
        },
        {
            "title": "5.10 Step 8 — Designing for Performance and Long Battery Life",
            "paragraphs": [
                "A good battery system should not only work today — it should continue operating safely, efficiently, and reliably for many years.",
                "This is why proper system design must always consider long-term battery performance and lifespan, not just whether the system can power the loads immediately after installation.",
                "Lithium batteries are a major investment, and the way the system is designed has a direct impact on:",
            ],
            "bullets": [
                "battery lifespan",
                "system reliability",
                "charging performance",
                "efficiency",
                "operating temperature",
                "long-term stability",
            ],
            "paragraphs_after": [
                "A poorly designed system may still function initially, but excessive stress, incorrect settings, or poor operating conditions can significantly shorten battery life over time.",
            ],
            "subsections": {
                "Batteries Perform Best Within Safe Operating Conditions": {
                    "paragraphs": [
                        "Lithium batteries are designed to operate within specific limits.",
                        "The BMS continuously protects the battery against:",
                    ],
                    "bullets": [
                        "overcharging",
                        "deep discharge",
                        "excessive current",
                        "overheating",
                        "unsafe operating conditions",
                    ],
                    "paragraphs_after": [
                        "However, good system design aims to avoid these conditions altogether rather than relying on the BMS to constantly intervene.",
                    ],
                },
                "Avoid Constant High Stress": {
                    "paragraphs": [
                        "Batteries last longer when they are not constantly pushed to their limits.",
                        "A system designed too tightly may cause:",
                    ],
                    "bullets": [
                        "deep daily discharges",
                        "high charging current",
                        "excessive discharge current",
                        "frequent protection events",
                        "increased operating temperatures",
                    ],
                    "paragraphs_after": [
                        "Over time, this increases battery wear and reduces lifespan.",
                    ],
                },
                "Depth of Discharge (DoD) Affects Lifespan": {
                    "paragraphs": [
                        "Although lithium batteries support deep discharge, constantly operating at maximum depth of discharge increases stress on the cells.",
                        "For example:",
                    ],
                    "bullets": [
                        "regularly cycling a battery from 100% to 0% creates more stress than:",
                        "cycling between 80% and 30%",
                    ],
                    "paragraphs_after": [
                        "Good system design considers:",
                    ],
                    "bullets_after": [
                        "realistic usable capacity",
                        "reserve margins",
                        "reduced battery stress",
                    ],
                    "paragraphs_footer": [
                        "to improve long-term performance.",
                    ],
                },
                "Temperature Has a Major Impact": {
                    "paragraphs": [
                        "Battery temperature significantly affects:",
                    ],
                    "bullets": [
                        "performance",
                        "charging behaviour",
                        "lifespan",
                    ],
                    "paragraphs_after": [
                        "Excessive heat is one of the biggest causes of accelerated battery aging.",
                        "Poor ventilation or incorrect installation locations can lead to:",
                    ],
                    "bullets_after": [
                        "overheating",
                        "reduced efficiency",
                        "shortened battery life",
                        "increased protection events",
                    ],
                    "paragraphs_footer": [
                        "This is why batteries should always be installed in:",
                    ],
                    "bullets_footer": [
                        "well-ventilated areas",
                        "clean environments",
                        "suitable operating temperatures",
                    ],
                },
                "Proper Charging is Critical": {
                    "paragraphs": [
                        "Correct charging settings are essential for battery health.",
                        "Incorrect:",
                    ],
                    "bullets": [
                        "charge voltage",
                        "charge current",
                        "float settings",
                        "inverter configuration",
                    ],
                    "paragraphs_after": [
                        "can:",
                    ],
                    "bullets_after": [
                        "reduce battery lifespan",
                        "prevent balancing",
                        "cause inaccurate SOC",
                        "trigger BMS alarms",
                    ],
                    "paragraphs_footer": [
                        "Good system design always follows manufacturer charging specifications.",
                    ],
                },
                "Correct Solar Sizing Improves Battery Health": {
                    "paragraphs": [
                        "A solar array that is too small may:",
                    ],
                    "bullets": [
                        "leave batteries partially charged for long periods",
                        "prevent balancing",
                        "reduce SOC accuracy",
                        "increase cycling stress",
                    ],
                    "paragraphs_after": [
                        "Proper solar sizing helps ensure:",
                    ],
                    "bullets_after": [
                        "healthy charging behaviour",
                        "regular full charge opportunities",
                        "stable system operation",
                    ],
                },
                "Cable Quality and Voltage Stability Matter": {
                    "paragraphs": [
                        "Undersized cables and poor terminations can cause:",
                    ],
                    "bullets": [
                        "voltage drops",
                        "unstable charging",
                        "excessive heat",
                        "inverter faults",
                    ],
                    "paragraphs_after": [
                        "Stable voltage and good power delivery improve:",
                    ],
                    "bullets_after": [
                        "battery performance",
                        "charging accuracy",
                        "system efficiency",
                    ],
                },
                "Communication Improves Long-Term Performance": {
                    "paragraphs": [
                        "Modern lithium systems rely heavily on proper communication between:",
                    ],
                    "bullets": [
                        "the inverter",
                        "and the battery BMS",
                    ],
                    "paragraphs_after": [
                        "Good communication allows:",
                    ],
                    "bullets_after": [
                        "smarter charging",
                        "improved protection",
                        "better balancing",
                        "accurate SOC calculations",
                        "stable system control",
                    ],
                    "paragraphs_footer": [
                        "Poor communication can reduce overall system performance and battery lifespan.",
                    ],
                    "images": [
                        {
                            "src": "images/EXAMPLE PERFORMANCE AND LONG BATTERY LIFE.png",
                            "alt": "Communication Compatibility Diagram",
                        },
                    ],
                },
               
            },
        },
        {
            "title": "5.11 Real-World System Design Examples",
            "paragraphs": [
                "Understanding the theory behind system design is important, but seeing how these principles are applied in real-world situations makes the concepts far easier to understand.",
                "Every installation is different, and factors such as load requirements, backup time expectations, budget, available space, and future expansion all influence the final system design.",
                "The following examples demonstrate how system sizing and component selection may differ depending on the application, while highlighting the practical thinking and decision-making that goes into designing safe, reliable, and efficient battery and solar systems.",
            ],
            "images": [
                {
                    "src": "images/SMALL HOUSE BACKUP.png",
                    "alt": "Real-World System Design Example",
                },
                 {
                    "src": "images/MEDIUM HOME BACKUP.png",
                    "alt": "Real-World System Design Example",
                },
                 {
                    "src": "images/LARGE HOME BACKUP.png",
                    "alt": "Real-World System Design Example",
                },
                 {
                    "src": "images/OFFICE BACKUP.png",
                    "alt": "Real-World System Design Example",
                },
                 {
                    "src": "images/RESTURANT BACKUP.png",
                    "alt": "Real-World System Design Example",
                },
                 {
                    "src": "images/COMMERCIAL BESS.png",
                    "alt": "Real-World System Design Example",
                },
            ],

        },
        {
            "title": "5.12 Common Mistakes Installers Must Avoid",
            "paragraphs": [
                "Good system design is about avoiding common mistakes before installation.",
                "Mistakes can include ignoring startup loads, undersizing cables, mismatching inverter and battery voltage, and failing to plan for future expansion.",
                "A careful design process helps prevent nuisance trips, overheating, incorrect charging, shortened battery life, communication faults, overloaded components, unstable system behaviour and safety risks.",
            ],
            "images": [
                {
                    "src": "images/COMMON MISTAKES INSTALLER MUST AVOID.png",
                    "alt": "Common Mistakes in System Design",
                },
                 {
                    "src": "images/WRAPPING UP MODULE 5.png",
                    "alt": "WRAPPING UP MODULE 5.",
                },

            ],
        },
    ],
}

MODULE_5_ASSESSMENT = {
    "title": "Module 5 Assessment",
    "questions": [
        {
            "question": "1. The most important starting point when designing a system is:",
            "options": [
                "A) Choosing the inverter",
                "B) Selecting the battery brand",
                "C) Load assessment",
                "D) Installing solar panels",
            ],
            "answer": "C",
            "explanation": "The first and most important step is to assess the loads the system must support.",
        },
        {
            "question": "2. Poor system design typically leads to:",
            "options": [
                "A) Better efficiency",
                "B) Longer battery life",
                "C) BMS trips and customer complaints",
                "D) Lower costs",
            ],
            "answer": "C",
            "explanation": "Poor design often causes protection trips, unstable performance and unhappy customers.",
        },
        {
            "question": "3. The correct design order is:",
            "options": [
                "A) Solar → Inverter → Battery → Loads",
                "B) Inverter → Battery → Solar → Loads",
                "C) Loads → Battery → Inverter → Solar",
                "D) Battery → Loads → Solar → Inverter",
            ],
            "answer": "C",
            "explanation": "Design should begin with loads, then size the battery, inverter, and solar.",
        },
        {
            "question": "4. Essential loads are defined as:",
            "options": [
                "A) All loads in the house",
                "B) Loads that must run during load shedding",
                "C) Only solar-powered loads",
                "D) High-power appliances",
            ],
            "answer": "B",
            "explanation": "Essential loads are those that must remain powered during outages or load shedding.",
        },
        {
            "question": "5. Which of the following is an essential load?",
            "options": [
                "A) Geyser",
                "B) Oven",
                "C) WiFi router",
                "D) Air conditioner",
            ],
            "answer": "C",
            "explanation": "A WiFi router is typically essential for communication and smart system control.",
        },
        {
            "question": "6. Which of the following is NOT an essential load?",
            "options": [
                "A) Fridge",
                "B) Lights",
                "C) Pool pump",
                "D) Alarm system",
            ],
            "answer": "C",
            "explanation": "A pool pump is usually non-essential during backup or load-shedding conditions.",
        },
        {
            "question": "7. Why must essential and non-essential loads be separated?",
            "options": [
                "A) To increase voltage",
                "B) To reduce inverter size",
                "C) To protect battery runtime and system performance",
                "D) To improve solar output",
            ],
            "answer": "C",
            "explanation": "Separating loads preserves battery runtime and keeps the system reliable.",
        },
        {
            "question": "8. Battery size is calculated using:",
            "options": [
                "A) Voltage × Current",
                "B) Load (kW) × Time (hours)",
                "C) Current × Resistance",
                "D) Solar output ÷ time",
            ],
            "answer": "B",
            "explanation": "Battery energy is found by multiplying load power by required runtime.",
        },
        {
            "question": "9. A 1 kW load running for 5 hours requires:",
            "options": [
                "A) 1 kWh",
                "B) 3 kWh",
                "C) 5 kWh",
                "D) 10 kWh",
            ],
            "answer": "C",
            "explanation": "Energy = 1 kW × 5 hours = 5 kWh.",
        },
        {
            "question": "10. Why should batteries not be sized exactly to calculated demand?",
            "options": [
                "A) To reduce voltage",
                "B) Because batteries must be oversized for safety margin and lifespan",
                "C) To reduce inverter size",
                "D) Because solar replaces batteries",
            ],
            "answer": "B",
            "explanation": "Batteries need extra capacity for margin, lifespan and reliable performance.",
        },
        {
            "question": "11. Typical usable battery capacity is approximately:",
            "options": [
                "A) 50%",
                "B) 70%",
                "C) 90%",
                "D) 100%",
            ],
            "answer": "C",
            "explanation": "Usable capacity is usually around 90%, not the full rated capacity.",
        },
        {
            "question": "12. The inverter must be sized based on:",
            "options": [
                "A) Battery size",
                "B) Solar size",
                "C) Peak load",
                "D) Cable size",
            ],
            "answer": "C",
            "explanation": "Inverter size depends on the peak load it must supply.",
        },
        {
            "question": "13. If the inverter is undersized, what happens?",
            "options": [
                "A) Better efficiency",
                "B) System instability and overload trips",
                "C) Lower voltage",
                "D) Increased battery life",
            ],
            "answer": "B",
            "explanation": "An undersized inverter causes instability and can trip under overload.",
        },
        {
            "question": "14. A typical inverter size for a medium home is:",
            "options": [
                "A) 1–2 kW",
                "B) 3–5 kW",
                "C) 5–8 kW",
                "D) 20 kW",
            ],
            "answer": "C",
            "explanation": "Medium homes commonly use inverters in the 5–8 kW range.",
        },
        {
            "question": "15. In South Africa, 1 kWp of solar typically produces:",
            "options": [
                "A) 1–2 kWh/day",
                "B) 2–3 kWh/day",
                "C) 4–6 kWh/day",
                "D) 10–12 kWh/day",
            ],
            "answer": "C",
            "explanation": "A realistic South African yield is around 4–6 kWh per day per kWp.",
        },
        {
            "question": "16. The main purpose of solar in a hybrid system is to:",
            "options": [
                "A) Replace the inverter",
                "B) Charge batteries and run daytime loads",
                "C) Increase voltage",
                "D) Reduce cable size",
            ],
            "answer": "B",
            "explanation": "Solar is used to charge batteries and supply daytime loads.",
        },
        {
            "question": "17. What happens if solar is undersized?",
            "options": [
                "A) Faster charging",
                "B) Battery never fully charges and system performs poorly",
                "C) Increased efficiency",
                "D) Reduced load",
            ],
            "answer": "B",
            "explanation": "Insufficient solar means the battery may never fully charge and performance suffers.",
        },
        {
            "question": "18. Why is inverter-to-battery communication important?",
            "options": [
                "A) It increases voltage",
                "B) It ensures proper control and prevents instability",
                "C) It reduces cable size",
                "D) It replaces protection devices",
            ],
            "answer": "B",
            "explanation": "Communication is needed for correct control and stable system operation.",
        },
        {
            "question": "19. Recommended maximum voltage drop in a system is:",
            "options": [
                "A) 10%",
                "B) 5%",
                "C) 3%",
                "D) 1%",
            ],
            "answer": "C",
            "explanation": "A 3% maximum voltage drop is commonly recommended for battery systems.",
        },
        {
            "question": "20. Undersized DC cables can cause:",
            "options": [
                "A) Improved efficiency",
                "B) Voltage drop, heat and BMS trips",
                "C) Higher SOC",
                "D) Lower inverter load",
            ],
            "answer": "B",
            "explanation": "Undersized cables cause voltage drop, overheating and protection trips.",
        },
        {
            "question": "21. A system with frequent shutdowns is most likely caused by:",
            "options": [
                "A) Customer usage",
                "B) Product defects",
                "C) Poor system design",
                "D) Solar panels",
            ],
            "answer": "C",
            "explanation": "Frequent shutdowns are usually the result of poor system design.",
        },
        {
            "question": "22. Running batteries below 20% SOC regularly will:",
            "options": [
                "A) Improve lifespan",
                "B) Increase efficiency",
                "C) Reduce battery life",
                "D) Increase voltage",
            ],
            "answer": "C",
            "explanation": "Deep discharging below 20% SOC regularly shortens battery life.",
        },
        {
            "question": "23. Installing batteries in a hot environment can cause:",
            "options": [
                "A) Better performance",
                "B) Increased capacity",
                "C) BMS trips and reduced lifespan",
                "D) Higher SOC",
            ],
            "answer": "C",
            "explanation": "Heat leads to protection trips and reduces battery lifespan.",
        },
        {
            "question": "24. Mixing battery brands in one system will likely result in:",
            "options": [
                "A) Improved performance",
                "B) No change",
                "C) System instability and communication issues",
                "D) Increased voltage",
            ],
            "answer": "C",
            "explanation": "Mixed brands often cause instability and control/communication problems.",
        },
        {
            "question": "25. The most common cause of customer complaints is:",
            "options": [
                "A) Solar panel colour",
                "B) Cable routing",
                "C) Poor system design and sizing",
                "D) Inverter brand",
            ],
            "answer": "C",
            "explanation": "Poor design and sizing is the most frequent source of complaints.",
        },
    ],
}

MODULE_6_INSTALLATION_WIRING = {
    "module_title": "MODULE 6 — REVOV System Installation, Wiring & Integration",
    "module_subtitle": "From Site Assessment to a Complete Working System",
    "sections": [
        {
            "title": "6.1 Module Learning Outcomes",
            "paragraphs": [
                "This module brings together the complete practical installation process — from site assessment and planning through to installation, wiring, integration and preparing the system for commissioning.",
                "By the end of this module, you will be able to:",
            ],
            "bullets": [
                "Conduct a proper site assessment before installation",
                "Understand customer requirements and identify essential loads",
                "Assess DB boards and existing electrical infrastructure",
                "Plan correct battery, inverter, and PV placement",
                "Install REVOV batteries safely and correctly",
                "Apply best practices for DC and AC wiring",
                "Perform proper cable terminations and crimping",
                "Implement correct earthing, bonding, and protection",
                "Integrate batteries, inverters, PV, grid, and generators correctly",
                "Understand and implement BMS communication wiring",
                "Wire parallel battery systems correctly and safely",
                "Identify and avoid common installation and wiring mistakes",
                "Deliver clean, safe, and professional installations",
                "Understand how installation quality affects system performance and battery lifespan",
            ],
        },
        {
            "title": "SECTION 1 — SITE ASSESSMENT & PRE-INSTALLATION PLANNING",
            "paragraphs": [],
        },
        {
            "title": "6.3 Why Site Assessment Matters",
            "paragraphs": [
                "A good installation starts before tools come out.  Many installation problems are actually planning problems.",
                "Poor site assessment often leads to:",
            ],
            "bullets": [
                "incorrect system sizing",
                "poor cable routing",
                "overheating batteries",
                "difficult installations",
                "excessive voltage drop",
                "communication issues",
                "rework and delays",
                "customer frustration",
                "reduced battery lifespan",
            ],
            "images" :[
                {
                    "src" : "images/best installer dont guess.png",
                    "alt" : "images about what installers must not do",
                },
            ],
        },
        {
            "title": "6.4 Understanding the Customer Requirement",
            "paragraphs": [
                "Before selecting equipment, the installer must first understand the customer's real needs.",
                "Many customers initially say:",
                "\"Everything must run during loadshedding.\"",
                "The installer's role is to translate this into a realistic and practical system design.",
                "Understanding the customer requirement helps guide:",
            ],
            "bullets": [
                "inverter sizing",
                "battery sizing",
                "solar sizing",
                "load separation",
                "expansion planning",
            ],
             "images" :[
                {
                    "src" : "images/good communicatiopn during.png",
                    "alt" : "images about good communicatiopn during site inspections",
                },
            ],
        },
        {
            "title": "6.5 Identifying Essential vs Non-Essential Loads",
            "paragraphs": [
                "One of the most important practical design decisions is identifying which loads require backup power.",
                "Essential loads are the circuits the customer wants powered during outages e.g lights, TV, WiFi etc",
                "Non-essential loads are usually high-power appliances that are excluded from backup e.g. geysers, ovens, pool pumps etc",
                "Separating these loads correctly:",
            ],
            "bullets": [
                "protects the inverter",
                "protects the battery",
                "improves runtime",
                "reduces system cost",
                "improves system stability",
            ],
             "images" :[
                {
                    "src" : "images/always walk through the property.png",
                    "alt" : "image ....",
                },
            ],
        },
        {
            "title": "6.6 DB Board Assessment",
            "paragraphs": [
                "The DB board should also be checked during this process to confirm how the circuits are currently configured.  A poor DB often creates future problems regardless of how good the battery or inverter is.",
                "The installer must check:",
            ],
            "bullets": [
                "space for additional breakers",
                "separation of essential and non-essential loads",
                "earth leakage configuration",
                "breaker sizing",
                "labelling",
                "cable condition",
                "overall DB compliance",
                "earthing quality",
            ],
             "images" :[
                {
                    "src" : "images/many nuisance tripps and system install.png",
                    "alt" : "",
                },
            ],
        },
        {
            "title": "6.7 Battery & Inverter Placement",
            "paragraphs": [
                "Where the equipment is installed is just as important as the equipment itself.",
                "REVOV lithium batteries perform best in cool, well-ventilated environments where airflow around the battery units is not restricted.",
                "Proper battery placement helps:",
            ],
            "bullets": [
                "improve battery lifespan",
                "improve charging performance",
                "reduce overheating",
                "reduce BMS protection events",
                "improve maintenance access",
            ],
            "paragraphs_after": [
                "Battery installation areas should:",
            ],
            "bullets_after": [
                "remain cool",
                "have good airflow",
                "stay dry",
                "remain clean",
                "allow easy service access",
                "allow communication cable access",
                "allow isolator access",
            ],
            "paragraphs_extra": [
                "Inverter placement should also consider:",
            ],
            "bullets_extra": [
                "short DC cable lengths",
                "airflow",
                "accessibility",
                "protection from moisture and dust",
                "proximity to the DB board",
            ],
            "images" :[
                {
                    "src" : "images/heat is one of the biggest causes.png",
                    "alt" : "",
                },
            ],
        },
        {
            "title": "6.8 Roof Assessment (Solar Systems)",
            "paragraphs": [
                "If solar is included, roof assessment becomes critical.",
                "The installer should assess:",
            ],
            "bullets": [
                "roof direction",
                "tilt angle",
                "shading",
                "roof condition",
                "waterproofing",
                "available installation space",
                "cable entry points",
                "structural suitability",
            ],
            "paragraphs_after": [
                "In South Africa, north-facing roofs generally provide the best solar production.",
                "Shading is extremely important.  Even small amounts of shading can significantly reduce solar performance.",
                "The installer must also plan:",
            ],
            "bullets_after": [
                "panel layout",
                "cable routes",
                "isolator positions",
                "conduit routing",
            ],
        },
        {
            "title": "6.9 Cable Routing & Layout Planning",
            "paragraphs": [
                "Good cable routing improves:",
            ],
            "bullets": [
                "safety",
                "reliability",
                "appearance",
                "future serviceability",
            ],
            "paragraphs_after": [
                "The installer should plan:",
            ],
            "bullets_after": [
                "battery cable routing",
                "AC cable routing",
                "PV cable routing",
                "communication cable routing",
            ],
            "paragraphs_extra": [
                "Important considerations include:",
            ],
            "bullets_extra": [
                "cable length",
                "voltage drop",
                "protection",
                "conduit/trunking",
                "physical damage risks",
                "heat exposure",
                "accessibility",
            ],
        },
        {
            "title": "6.10 Environmental & Safety Considerations",
            "paragraphs": [
                "The installation environment directly affects system performance and lifespan.",
                "The installer must assess:",
            ],
            "bullets": [
                "temperature",
                "ventilation",
                "moisture exposure",
                "dust",
                "fire risks",
                "physical security",
                "maintenance access",
                "exposure to chemicals or corrosive environments",
            ],
            "images" :[
                {
                    "src" : "images/high-quality system installed in apoor.png",
                    "alt" : "",
                },
                 {
                    "src" : "images/Children pets and.jpg",
                    "alt" : "",
                },
            ],
        },
        {
            "title": "6.11 Identifying Risks Before Installation",
            "paragraphs": [
                "Professional installers identify risks before installation starts.  Common risks include:",
            ],
            "bullets": [
                "long cable runs",
                "poor ventilation",
                "overloaded DB boards",
                "incorrect earthing",
                "no installation space",
                "shading issues",
                "roof structural problems",
                "inaccessible cable routes",
                "incompatible equipment",
            ],
            "paragraphs_after": [
                "Most installation problems were usually visible during the site assessment phase.",
            ],
        },
        {
            "title": "SECTION 2 — INSTALLATION FUNDAMENTALS & BEST PRACTICES",
            "paragraphs": [],
        },
        {
            "title": "6.12 Installation Sequence",
            "paragraphs": [
                "Professional installers follow a structured installation process.",
                "Recommended sequence:",
            ],
            "numbered": [
                "1. Confirm site assessment",
                "2. Mark equipment positions",
                "3. Install mounting structures",
                "4. Run cables",
                "5. Install inverter",
                "6. Install batteries",
                "7. Install protection devices",
                "8. Terminate cables",
                "9. Verify wiring",
                "10. Perform final inspection",
                "11. Prepare for commissioning",
            ],
             "images" :[
                {
                    "src" : "images/very important installer rule.png",
                    "alt" : "",
                },
            ],
        },
        {
            "title": "6.13 REVOV Battery Installation Best Practices",
            "paragraphs": [
                "REVOV batteries are intelligent lithium energy storage systems and must be installed correctly to ensure long-term performance and reliability.",
                "Best practices include:",
            ],
            "bullets": [
                "install on stable level surfaces",
                "allow airflow around batteries",
                "follow stacking rules",
                "maintain correct spacing",
                "secure units properly",
                "keep communication ports accessible",
                "use correct cable sizing",
                "install accessible battery isolation",
                "maintain short DC cable runs where possible",
            ],
        },
        {
            "title": "6.14 Inverter Installation Best Practices",
            "paragraphs": [
                "The inverter is the control centre of the system.",
                "Correct inverter installation improves:",
            ],
            "bullets": [
                "airflow",
                "cooling",
                "serviceability",
                "cable management",
                "system reliability",
            ],
            "paragraphs_after": [
                "Best practices include:",
            ],
            "bullets_after": [
                "secure mounting",
                "sufficient airflow clearance",
                "short DC cable runs",
                "proper AC cable routing",
                "installation close to the DB board",
                "protection from moisture and dust",
            ],
            "paragraphs_extra": [
                "Leave enough space around the inverter for future servicing.",
            ],
        },
        {
            "title": "6.15 DC Wiring Fundamentals",
            "paragraphs": [
                "The DC side of the system is one of the highest-risk areas of the installation.",
               
            ],
             "images" :[
                {
                    "src" : "images/battery system operate at.png",
                    "alt" : "",
                },
            ],
            "paragraphs_after": [
                 "Incorrect DC wiring can cause:",
            ],
            "bullets": [
                "overheating",
                "fire risks",
                "inverter damage",
                "battery damage",
                "BMS trips",
                "serious safety hazards",
            ],
            "paragraphs_after": [
                "DC wiring best practices include:",
            ],
            "bullets_after": [
                "correct cable sizing",
                "short cable runs",
                "correct polarity",
                "proper cable protection",
                "secure terminations",
                "correct isolators and breakers",
            ],
            "paragraphs_extra": [
                "Always:",
            ],
            "bullets_extra": [
                "verify polarity with a meter before connection",
                "inspect cable quality",
                "ensure clean contact surfaces",
            ],
        },
        {
            "title": "6.16 AC Wiring Fundamentals",
            "paragraphs": [
                "The AC side of the system must comply with electrical standards and safe wiring practices.",
                "Important considerations include:",
            ],
            "bullets": [
                "essential and non-essential load separation",
                "correct breaker sizing",
                "proper neutral separation",
                "earth leakage placement",
                "compliance with SANS standards",
            ],
            "paragraphs_after": [
                "Many nuisance trips are caused by:",
            ],
            "bullets_after": [
                "mixed neutrals",
                "incorrect earth leakage installation",
                "poor load separation",
            ],
        },
        {
            "title": "6.17 Cable Termination & Crimping",
            "paragraphs": [
                "Cable terminations are one of the most important practical skills in battery installations.",
                "A poor termination creates resistance.  Resistance creates heat.",
                "Heat leads to:",
            ],
            "bullets": [
                "voltage drop",
                "damaged terminals",
                "inverter faults",
                "battery shutdowns",
                "fire risks",
            ],
            "paragraphs_after": [
                "Best practices include:",
            ],
            "bullets_after": [
                "correct lug size",
                "hydraulic crimping",
                "clean surfaces",
                "correct torque settings",
                "heat shrink application",
                "post-installation re-checking",
            ],
             "images" :[
                {
                    "src" : "images/bad crimp = future failure.png",
                    "alt" : "",
                },
            ],
        },
        {
            "title": "6.18 Earthing & Bonding",
            "paragraphs": [
                "Proper earthing and bonding are critical for:",
            ],
            "bullets": [
                "safety",
                "fault protection",
                "system stability",
                "lightning protection",
                "inverter performance",
            ],
            "paragraphs_after": [
                "All metal components should be bonded correctly.",
                "This includes:",
            ],
            "bullets_after": [
                "inverter chassis",
                "battery racks",
                "DB boards",
                "conduit systems",
                "PV structures",
            ],
            "paragraphs_extra": [
                "Earth continuity should always be verified.  Good earthing improves overall system stability.",
            ],
        },
        {
            "title": "6.19 Protection Devices & Isolation",
            "paragraphs": [
                "Required protection devices may include:",
            ],
            "bullets": [
                "DC breakers",
                "battery fuses",
                "AC breakers",
                "PV isolators",
                "surge protection devices",
                "battery isolators",
            ],
            "paragraphs_after": [
                "Protection devices must be:",
            ],
            "bullets_after": [
                "correctly sized",
                "correctly located",
                "accessible",
                "properly labelled",
            ],
            "paragraphs_extra": [
                "If equipment cannot be safely isolated:",
                "the installation is unsafe.",
            ],
        },
        {
            "title": "SECTION 3 — SYSTEM WIRING & INTEGRATION",
            "paragraphs": [],
        },
        {
            "title": "6.20 Understanding Full System Flow",
            "paragraphs": [
                "Before wiring the system, the installer must understand how energy flows through the installation.",
                "A typical hybrid system includes:",
            ],
            "bullets": [
                "solar PV",
                "battery storage",
                "inverter",
                "loads",
                "grid supply",
                "optional generator support",
            ],
            "paragraphs_after": [
                "Simplified energy flow:",
            ],
            "numbered": [
                "1. Solar generates DC power",
                "2. Inverter powers loads",
                "3. Excess energy charges batteries",
                "4. Batteries support loads when PV reduces",
                "5. Grid or generator assists when needed",
            ],
            "paragraphs_extra": [
                "If the installer understands the energy flow, the wiring process becomes logical and easier to troubleshoot.",
            ],
        },
        {
            "title": "6.21 REVOV Battery Wiring",
            "paragraphs": [
                "Battery wiring must always follow manufacturer recommendations.",
                "Single battery systems are relatively simple.",
                "Parallel battery systems require far more attention.",
                "Important rules for parallel battery systems:",
            ],
            "bullets": [
                "same cable lengths",
                "same cable sizes",
                "same battery models",
                "correct communication wiring",
                "balanced load sharing",
            ],
            "paragraphs_after": [
                "Parallel systems must operate as one coordinated battery bank.",
            ],
        },
        {
            "title": "6.22 BMS Communication Integration",
            "paragraphs": [
                "Communication between the inverter and REVOV battery BMS is extremely important.",
                "Communication allows the inverter and battery to exchange information such as:",
            ],
            "bullets": [
                "SOC",
                "charge limits",
                "discharge limits",
                "battery temperature",
                "alarms",
                "protection status",
            ],
            "paragraphs_after": [
                "Installers should always:",
            ],
            "bullets_after": [
                "confirm communication wiring",
                "verify communication settings",
                "check supported inverter compatibility",
                "confirm active communication during commissioning",
            ],
        },
        {
            "title": "6.23 Essential & Non-Essential Load Integration",
            "paragraphs": [
                "Correct load separation is critical for system stability.",
                "Essential loads:",
            ],
            "bullets": [
                "connected to inverter output",
                "remain powered during outages",
            ],
            "paragraphs_after": [
                "Non-essential loads:",
            ],
            "bullets_after": [
                "remain on the main DB",
                "are not backed up by the inverter",
            ],
            "paragraphs_extra": [
                "Load separation protects both the inverter and battery system.",
            ],
        },
        {
            "title": "6.24 PV Integration",
            "paragraphs": [
                "Solar PV integrates into the inverter through the MPPT inputs.",
                "Important PV considerations include:",
            ],
            "bullets": [
                "correct string sizing",
                "correct polarity",
                "voltage limits",
                "current limits",
                "isolator installation",
                "surge protection",
            ],
            "paragraphs_after": [
                "Incorrect PV integration can damage equipment instantly.  PV design and integration must always remain within inverter specifications.",
            ],
        },
        {
            "title": "6.25 Grid & Generator Integration",
            "paragraphs": [
                "Grid supply normally connects to the inverter AC input.",
                "Generators may integrate through:",
            ],
            "bullets": [
                "manual changeover systems",
                "automatic transfer switches (ATS)",
            ],
            "paragraphs_after": [
                "Important considerations include:",
            ],
            "bullets_after": [
                "correct switching",
                "synchronization",
                "backfeed prevention",
                "correct generator sizing",
            ],
            "paragraphs_extra": [
                "Grid and generator supplies must never conflict.",
                "Incorrect generator integration can create serious safety risks.",
            ],
        },
        {
            "title": "SECTION 4 — PROFESSIONAL INSTALLATION STANDARDS",
            "paragraphs": [],
        },
        {
            "title": "6.26 Clean Installation Standards",
            "paragraphs": [
                "Customers do not only see system performance — they see installation quality.",
                "Professional installations include:",
            ],
            "bullets": [
                "straight cable runs",
                "proper trunking and conduit",
                "cable labelling",
                "neat layouts",
                "accessible equipment",
                "organised wiring",
            ],
            "paragraphs_after": [
                "Installers should aim for installations that look professional and reflect REVOV quality standards.",
            ],
        },
        {
            "title": "6.27 Ideal Installation System Examples",
            "paragraphs": [
                "A good installation is not only about making the system work — it is about creating a safe, reliable, efficient, and professional energy solution that will perform well for many years.",
                "The following examples demonstrate what a properly planned and professionally installed REVOV system should look like in real-world applications.",
                "Pay close attention to equipment placement, cable routing, ventilation, protection devices, communication wiring, and overall workmanship, as these small details often make the biggest difference in long-term system performance and reliability.",
            ],
             "images" :[
                {
                    "src" : "images/ideal installation-small system.png",
                    "alt" : "",
                },
            
                {
                    "src" : "images/ideal installation-medium system.png",
                    "alt" : "",
                },
           
                {
                    "src" : "images/ideal installtion -large system.png",
                    "alt" : "",
                },
            ],
        },
        {
            "title": "6.28 Common Installation Mistakes",
            "paragraphs": [],
            "images" :[
                {
                    "src" : "images/installer mistake.png",
                    "alt" : "",
                },
            ],
        },
         
        {
            "title": "6.29 Wrapping Up Module 6",
            "paragraphs": [],
            "images" :[
                {
                    "src" : "images/wrapping up module 6.png",
                    "alt" : "",
                },
            ],
        },
    ],
}

MODULE_6_ASSESSMENT = {
    "title": "Module 6 Assessment",
    "subtitle": "Energy System Design & Sizing",
    "questions": [
        {
            "question": "1. The most important starting point when designing a system is:",
            "options": [
                "A) Choosing the inverter",
                "B) Selecting the battery brand",
                "C) Load assessment",
                "D) Installing solar panels",
            ],
            "answer": "C",
            "explanation": "The first and most important step is to assess the loads the system must support.",
        },
        {
            "question": "2. Poor system design typically leads to:",
            "options": [
                "A) Better efficiency",
                "B) Longer battery life",
                "C) BMS trips and customer complaints",
                "D) Lower costs",
            ],
            "answer": "C",
            "explanation": "Poor design often causes protection trips, unstable performance and unhappy customers.",
        },
        {
            "question": "3. The correct design order is:",
            "options": [
                "A) Solar → Inverter → Battery → Loads",
                "B) Inverter → Battery → Solar → Loads",
                "C) Loads → Battery → Inverter → Solar",
                "D) Battery → Loads → Solar → Inverter",
            ],
            "answer": "C",
            "explanation": "Design should begin with loads, then size the battery, inverter, and solar.",
        },
        {
            "question": "4. Essential loads are defined as:",
            "options": [
                "A) All loads in the house",
                "B) Loads that must run during load shedding",
                "C) Only solar-powered loads",
                "D) High-power appliances",
            ],
            "answer": "B",
            "explanation": "Essential loads are those that must remain powered during outages or load shedding.",
        },
        {
            "question": "5. Which of the following is an essential load?",
            "options": [
                "A) Geyser",
                "B) Oven",
                "C) WiFi router",
                "D) Air conditioner",
            ],
            "answer": "C",
            "explanation": "A WiFi router is typically essential for communication and smart system control.",
        },
        {
            "question": "6. Which of the following is NOT an essential load?",
            "options": [
                "A) Fridge",
                "B) Lights",
                "C) Pool pump",
                "D) Alarm system",
            ],
            "answer": "C",
            "explanation": "A pool pump is usually non-essential during backup or load-shedding conditions.",
        },
        {
            "question": "7. Why must essential and non-essential loads be separated?",
            "options": [
                "A) To increase voltage",
                "B) To reduce inverter size",
                "C) To protect battery runtime and system performance",
                "D) To improve solar output",
            ],
            "answer": "C",
            "explanation": "Separating loads preserves battery runtime and keeps the system reliable.",
        },
        {
            "question": "8. Battery size is calculated using:",
            "options": [
                "A) Voltage × Current",
                "B) Load (kW) × Time (hours)",
                "C) Current × Resistance",
                "D) Solar output ÷ time",
            ],
            "answer": "B",
            "explanation": "Battery energy is found by multiplying load power by required runtime.",
        },
        {
            "question": "9. A 1 kW load running for 5 hours requires:",
            "options": [
                "A) 1 kWh",
                "B) 3 kWh",
                "C) 5 kWh",
                "D) 10 kWh",
            ],
            "answer": "C",
            "explanation": "Energy = 1 kW × 5 hours = 5 kWh.",
        },
        {
            "question": "10. Why should batteries not be sized exactly to calculated demand?",
            "options": [
                "A) To reduce voltage",
                "B) Because batteries must be oversized for safety margin and lifespan",
                "C) To reduce inverter size",
                "D) Because solar replaces batteries",
            ],
            "answer": "B",
            "explanation": "Batteries need extra capacity for margin, lifespan and reliable performance.",
        },
        {
            "question": "11. Typical usable battery capacity is approximately:",
            "options": [
                "A) 50%",
                "B) 70%",
                "C) 90%",
                "D) 100%",
            ],
            "answer": "C",
            "explanation": "Usable capacity is usually around 90%, not the full rated capacity.",
        },
        {
            "question": "12. The inverter must be sized based on:",
            "options": [
                "A) Battery size",
                "B) Solar size",
                "C) Peak load",
                "D) Cable size",
            ],
            "answer": "C",
            "explanation": "Inverter size depends on the peak load it must supply.",
        },
        {
            "question": "13. If the inverter is undersized, what happens?",
            "options": [
                "A) Better efficiency",
                "B) System instability and overload trips",
                "C) Lower voltage",
                "D) Increased battery life",
            ],
            "answer": "B",
            "explanation": "An undersized inverter causes instability and can trip under overload.",
        },
        {
            "question": "14. A typical inverter size for a medium home is:",
            "options": [
                "A) 1–2 kW",
                "B) 3–5 kW",
                "C) 5–8 kW",
                "D) 20 kW",
            ],
            "answer": "C",
            "explanation": "Medium homes commonly use inverters in the 5–8 kW range.",
        },
        {
            "question": "15. In South Africa, 1 kWp of solar typically produces:",
            "options": [
                "A) 1–2 kWh/day",
                "B) 2–3 kWh/day",
                "C) 4–6 kWh/day",
                "D) 10–12 kWh/day",
            ],
            "answer": "C",
            "explanation": "A realistic South African yield is around 4–6 kWh per day per kWp.",
        },
        {
            "question": "16. The main purpose of solar in a hybrid system is to:",
            "options": [
                "A) Replace the inverter",
                "B) Charge batteries and run daytime loads",
                "C) Increase voltage",
                "D) Reduce cable size",
            ],
            "answer": "B",
            "explanation": "Solar is used to charge batteries and supply daytime loads.",
        },
        {
            "question": "17. What happens if solar is undersized?",
            "options": [
                "A) Faster charging",
                "B) Battery never fully charges and system performs poorly",
                "C) Increased efficiency",
                "D) Reduced load",
            ],
            "answer": "B",
            "explanation": "Insufficient solar means the battery may never fully charge and performance suffers.",
        },
        {
            "question": "18. Why is inverter-to-battery communication important?",
            "options": [
                "A) It increases voltage",
                "B) It ensures proper control and prevents instability",
                "C) It reduces cable size",
                "D) It replaces protection devices",
            ],
            "answer": "B",
            "explanation": "Communication is needed for correct control and stable system operation.",
        },
        {
            "question": "19. Recommended maximum voltage drop in a system is:",
            "options": [
                "A) 10%",
                "B) 5%",
                "C) 3%",
                "D) 1%",
            ],
            "answer": "C",
            "explanation": "A 3% maximum voltage drop is commonly recommended for battery systems.",
        },
        {
            "question": "20. Undersized DC cables can cause:",
            "options": [
                "A) Improved efficiency",
                "B) Voltage drop, heat and BMS trips",
                "C) Higher SOC",
                "D) Lower inverter load",
            ],
            "answer": "B",
            "explanation": "Undersized cables cause voltage drop, overheating and protection trips.",
        },
        {
            "question": "21. A system with frequent shutdowns is most likely caused by:",
            "options": [
                "A) Customer usage",
                "B) Product defects",
                "C) Poor system design",
                "D) Solar panels",
            ],
            "answer": "C",
            "explanation": "Frequent shutdowns are usually the result of poor system design.",
        },
        {
            "question": "22. Running batteries below 20% SOC regularly will:",
            "options": [
                "A) Improve lifespan",
                "B) Increase efficiency",
                "C) Reduce battery life",
                "D) Increase voltage",
            ],
            "answer": "C",
            "explanation": "Deep discharging below 20% SOC regularly shortens battery life.",
        },
        {
            "question": "23. Installing batteries in a hot environment can cause:",
            "options": [
                "A) Better performance",
                "B) Increased capacity",
                "C) BMS trips and reduced lifespan",
                "D) Higher SOC",
            ],
            "answer": "C",
            "explanation": "Heat leads to protection trips and reduces battery lifespan.",
        },
        {
            "question": "24. Mixing battery brands in one system will likely result in:",
            "options": [
                "A) Improved performance",
                "B) No change",
                "C) System instability and communication issues",
                "D) Increased voltage",
            ],
            "answer": "C",
            "explanation": "Mixed brands often cause instability and control/communication problems.",
        },
        {
            "question": "25. The most common cause of customer complaints is:",
            "options": [
                "A) Solar panel colour",
                "B) Cable routing",
                "C) Poor system design and sizing",
                "D) Inverter brand",
            ],
            "answer": "C",
            "explanation": "Poor design and sizing is the most frequent source of complaints.",
        },
    ],
}

MODULE_7_SYSTEM_CONFIG = {
    "module_title": "MODULE 7 — System Configuration, Communication & Firmware",
    "module_subtitle": "Getting the system to think, communicate and behave correctly",
    "sections": [
        {
            "title": "7.1 Module Learning Outcomes",
            "paragraphs": [
                "This module focuses on the software and configuration side of the system — how inverter setup, battery pairing, communication, firmware and compatibility affect system behaviour, performance and reliability.",
                "By the end of this module, you will be able to:",
            ],
            "bullets": [
                "Understand why correct inverter setup is critical",
                "Pair the inverter correctly with the battery and BMS",
                "Configure charging, discharging and operating behaviour correctly",
                "Understand battery communication and protocol selection",
                "Understand what firmware is and why it matters",
                "Identify compatibility issues between inverter, battery and BMS",
                "Understand when firmware updates are required",
                "Perform safe high-level firmware update procedures",
                "Identify common setup, communication and firmware-related faults",
                "Understand how incorrect settings affect battery life, performance and warranty",
                "Perform a full setup and compatibility check before commissioning",
            ],
        },
        {
            "title": "SECTION 1 — UNDERSTANDING SYSTEM BEHAVIOUR",
            "paragraphs": [],
        },
        {
            "title": "7.2 Why System Setup Matters",
            "paragraphs": [
                "A system can be:",
            ],
            "bullets": [
                "installed neatly",
                "wired correctly",
                "sized properly",
                "fully compliant",
            ],
            "paragraphs_after": [
                "…and still perform badly because the system configuration is wrong.",
                "Many installers focus heavily on:",
            ],
            "bullets_after": [
                "hardware",
                "wiring",
                "installation quality",
            ],
            "paragraphs_extra": [
                "But modern lithium systems are intelligent systems. The software, communication and inverter settings now play a major role in how the entire system behaves.",
                "Poor setup can cause:",
            ],
            "bullets_extra": [
                "inaccurate SOC",
                "poor battery charging",
                "battery never reaching 100%",
                "balancing problems",
                "BMS trips",
                "poor solar usage",
                "unstable behaviour",
                "customer complaints",
                "shortened battery lifespan",
            ],
            "images" : [
                {
                    "src" : "images/not a battery fault.png",
                    "alt" : "image about inverter to battery installation issues!",
                },
            ],
        },
        {
            "title": "7.3 What the Inverter and BMS Are Actually Doing",
            "paragraphs": [
                "By now you understand:",
            ],
            "bullets": [
                "the inverter is not just a power converter",
                "the BMS is not just a safety device",
            ],
            "paragraphs_after": [
                "Together, they form the \"intelligence\" of the system.",
                "The inverter decides:",
            ],
            "bullets_after": [
                "when to use solar",
                "when to use battery",
                "when to charge",
                "when to discharge",
                "when to use grid",
                "how much current to allow",
                "which operating mode to follow",
            ],
            "paragraphs_extra": [
                "The BMS continuously monitors:",
            ],
            "bullets_extra": [
                "cell voltage",
                "battery temperature",
                "current flow",
                "SOC",
                "protection limits",
                "cell balancing",
                "battery health",
            ],
            "paragraphs_final": [
                "The BMS then communicates limits and instructions to the inverter.",
            ],
             "images" : [
                {
                    "src" : "images/very important concept.png",
                    "alt" : "image about importance of following the inverter to battery installations!",
                },
             ],
        },
        {
            "title": "SECTION 2 — SYSTEM CONFIGURATION & PAIRING",
            "paragraphs": [],
        },
        {
            "title": "7.4 Before You Start Configuration",
            "paragraphs": [
                "Before changing any settings, always confirm that the physical installation has been completed correctly.",
            ],
            "bullets": [
                "All DC and AC wiring completed",
                "Battery polarity correct",
                "Communication cable connected correctly",
                "Battery voltage within expected range",
                "PV polarity and voltage correct",
                "Breakers and isolators in correct position",
                "Essential and non-essential loads separated correctly",
                "Earthing and bonding completed",
                "Battery and inverter are compatible",
            ],
            "images" : [
                {
                    "src" : "images/do not use settings to fix.png",
                    "alt" : "",
                },
             ],
        },
        {
            "title": "7.5 Battery Pairing & Communication",
            "paragraphs": [
                "Pairing means correctly connecting and configuring the inverter and battery so they can communicate and operate together as one intelligent system.",
                "Modern lithium systems rely heavily on communication.",
                "  ",
                "When pairing is successful:",
            ],
            "bullets": [
                "the inverter can communicate with the battery BMS",
                "the battery can provide real-time operating limits",
                "the inverter can adjust its behaviour dynamically",
                "charging becomes smarter and safer",
                "battery protection improves significantly",
            ],
            "paragraphs_after": [
                "Without proper pairing:",
            ],
            "bullets_after": [
                "the inverter mostly operates blindly",
                "SOC accuracy reduces",
                "balancing may suffer",
                "battery protection becomes less intelligent",
                "instability increases",
            ],
            "paragraphs_extra": [
                "A system may still \"switch on\" without proper pairing, but it will not behave like a properly integrated lithium system.",
            ],
             "images" : [
                {
                    "src" : "images/signs communication is not working.png",
                    "alt" : "",
                },
             ],
        },
        {
            "title": "7.7 Practical Pairing Process — Step by Step",
            "paragraphs": [
                "Step 1 — Confirm Compatibility",
                "Before connecting communication cables, first confirm:",
            ],
            "bullets": [
                "inverter supports the battery",
                "battery supports the inverter",
                "correct communication protocol available",
                "firmware versions compatible",
                "approved battery profile available",
            ],
            "paragraphs_after": [
                "Always check:",
            ],
            "bullets_after": [
                "manufacturer compatibility lists",
                "approved inverter models",
                "supported firmware combinations",
                "communication protocol requirements",
            ],
             "images" : [
                {
                    "src" : "images/never assume two devices are compatible.png",
                    "alt" : "",
                },
             ],
            "paragraphs_extra": [
                "A battery and inverter may:",
            ],
            "bullets_extra": [
                "physically connect",
                "switch on successfully",
            ],
            "paragraphs_final": [
                "…but still communicate incorrectly because:",
                "• firmware versions differ",
                "• protocol unsupported",
                "• communication mapping different",
                "",
                "Result:",
                "❌ unstable behaviour",
                "❌ incorrect SOC",
                "❌ charging problems",
                "❌ nuisance trips",
                "",
                "Step 2 — Complete the Power Wiring First",
                "Before communication setup:",
            ],
            "bullets_step2": [
                "complete battery DC wiring",
                "complete inverter wiring",
                "install isolators and breakers",
                "verify polarity carefully",
            ],
            "paragraphs_step2": [
                "Check:",
            ],
            "bullets_check": [
                "positive to positive",
                "negative to negative",
                "correct cable sizing",
                "correct torque on lugs",
                "secure terminations",
            ],
            "images" : [
                {
                    "src" : "images/most communication troubleshooting.jpg",
                    "alt" : "",
                },
            ],
           
            "paragraphs_step3": [
                "",
                "Step 3 — Connect the Communication Cable",
                "The communication cable allows:",
            ],
            "bullets_step3": [
                "the inverter",
                "and battery BMS",
            ],
            "paragraphs_step3_extra": [
                "to exchange information continuously.",
                "",
                "Most systems use:",
            ],
            "bullets_step3_extra": [
                "CAN Bus",
                "or RS485 communication",
            ],
            "paragraphs_step3_final": [
                "The cable normally connects:",
                "• from the battery communication port",
                "to:",
                "• the inverter communication port",
                "",
                "What Communication Allows",
                "Once communication is active, the inverter can receive:",
            ],
            "bullets_communication": [
                "SOC",
                "battery voltage",
                "current limits",
                "charge limits",
                "discharge limits",
                "battery temperature",
                "alarms and warnings",
                "protection instructions",
            ],
            "paragraphs_communication": [
                "This allows the inverter to adjust behaviour dynamically based on real-time battery conditions.",
            ],
             "images" : [
                {
                    "src" : "images/connect the communication cable.png",
                    "alt" : "",
                },
            ],
        },
        {
            "title": " ",
            "paragraphs": [
                "Step 4 — Select the Correct Communication Port",
                "Many batteries and inverters contain multiple communication ports.",
                "Examples:",
            ],
            "bullets": [
                "CAN",
                "RS485",
                "RS232",
                "parallel communication ports",
                "BMS ports",
            ],
            "paragraphs_after": [
                "Always verify:",
            ],
            "bullets_after": [
                "correct inverter port",
                "correct battery port",
                "correct cable orientation",
                "correct communication direction",
            ],
            "paragraphs_extra": [
                "",
                "Step 5 — Configure Battery Addressing & Master/Slave Setup",
                "In parallel battery systems:",
            ],
            "bullets_extra": [
                "batteries often require addressing",
                "or DIP switch configuration",
            ],
            "paragraphs_final": [
                "This allows the batteries to organise communication correctly.",
                "",
                "Usually:",
                "• one battery becomes the master battery",
                "• the others become slave batteries",
                "",
                "The master battery communicates directly with the inverter.",
                "The slave batteries communicate through the master battery.",
                "",
                "Why Master/Slave Communication Matters",
                "This helps:",
            ],
            "bullets_master": [
                "coordinate charging",
                "coordinate discharge behaviour",
                "balance battery workload",
                "synchronize protection behaviour",
                "improve system stability",
            ],
        },
        {
            "title": " ",
            "paragraphs": [
                "Step 6 — Power Up the System in the Correct Sequence",
                "Startup sequence matters.",
                "",
                "Many communication problems are caused simply by incorrect startup order.",
                "",
                "Typical startup sequence:",
            ],
            "numbered": [
                "1. Turn on batteries first",
                "2. Allow BMS startup",
                "3. Close battery breaker/isolator",
                "4. Turn on inverter",
                "5. Allow inverter to detect battery",
            ],
            "paragraphs_after": [
                "Some systems require:",
            ],
            "bullets_after": [
                "the battery BMS fully operational before inverter startup",
            ],
            "paragraphs_extra": [
                "Otherwise:",
                "❌ communication may fail",
                "❌ battery detection may fail",
                "❌ incorrect startup behaviour may occur",
                "",
                "Step 7 — Configure Battery Type in the Inverter",
                "Inside the inverter settings:",
            ],
            "images" : [
                {
                   "src" : "images/always follow manufacuter.png",
                    "alt" : "",
                },
            ],
            "bullets_extra": [
                "select the correct battery type",
                "or approved lithium protocol",
            ],
            "paragraphs_step7": [
                "Typical options may include:",
            ],
            "bullets_step7": [
                "lead-acid",
                "AGM",
                "GEL",
                "lithium",
                "user-defined",
                "manufacturer-specific battery profiles",
            ],
            "paragraphs_step7_extra": [
                "Always use:",
            ],
            "bullets_step7_extra": [
                "approved lithium profile",
                "supported battery protocol",
            ],
            "paragraphs_step7_final": [
                "where possible.",
                "",
                "Why Correct Battery Selection Matters",
                "Correct battery selection allows:",
            ],
            "bullets_step7_final": [
                "proper communication",
                "correct charging behaviour",
                "proper protection logic",
                "accurate SOC calculation",
                "correct balancing behaviour",
            ],
             "images" : [
                {
                   "src" : "images/never gues battery seetings.png",
                    "alt" : "",
                },
            ],
        },
        {
            "title": " ",
            "paragraphs": [
                "Step 8 — Select the Correct Communication Protocol",
                "Some inverters allow protocol selection during setup.",
                "",
                "The selected protocol tells the inverter:",
            ],
            "bullets": [
                "how to interpret battery information correctly",
            ],
            "paragraphs_after": [
                "If the wrong protocol is selected:",
            ],
            "bullets_after": [
                "communication may partially work",
                "but information may be interpreted incorrectly",
            ],
            "paragraphs_extra": [
                "This can cause:",
                "❌ inaccurate SOC",
                "❌ unstable charging",
                "❌ incorrect current limits",
                "❌ communication alarms",
                "",
                "Step 9 — Configure Charge & Discharge Settings",
                "Some systems configure these automatically through communication and other systems require manual configuration.",
                "",
                "Important settings include:",
                "",
                "These settings directly affect:",
            ],
            "bullets_extra": [
                "battery lifespan",
                "balancing",
                "performance",
                "runtime",
                "system stability",
            ],
            "paragraphs_charge": [
                "Charge Voltage",
                "This controls how high the inverter charges the battery.",
                "",
                "If charge voltage is too high:",
                "❌ battery stress increases",
                "❌ overvoltage trips may occur",
                "❌ battery lifespan may reduce",
                "",
                "If charge voltage is too low:",
                "❌ battery may never fully charge",
                "❌ balancing may never complete",
                "❌ SOC drift may develop",
                "",
                "Charge Current",
                "This controls how fast the inverter charges the battery.",
                "",
                "If charge current is too high:",
                "❌ battery temperature increases",
                "❌ BMS trips may occur",
                "❌ unnecessary stress increases",
                "",
                "If too low:",
                "❌ charging becomes slow",
                "❌ battery may not recover between outages",
                "",
                "Discharge Current",
                "This controls how much current the inverter may draw from the battery.",
                "",
                "If discharge current is too high:",
                "❌ battery trips may occur",
                "❌ voltage sag increases",
                "❌ battery stress increases",
                "VERY IMPORTANT",
            ],
            "images" : [
                {
                    "src" : "images/even with manual settings.png",
                    "alt" : "",
                },
            ],
        },
        {
            "title": "7.8 SOC Accuracy, Calibration & Full Charge Synchronisation",
            "paragraphs": [
                "This is one of the most misunderstood areas in lithium systems.",
                "",
                "The BMS calculates SOC using:",
            ],
            "bullets": [
                "voltage",
                "current flow",
                "battery history",
                "balancing information",
                "charge/discharge behaviour",
            ],
            "paragraphs_after": [
                "Over time:",
            ],
            "bullets_after": [
                "small inaccuracies naturally develop",
            ],
            "paragraphs_extra": [
                "The battery therefore requires:",
            ],
            "bullets_extra": [
                "full charge cycles",
                "balancing opportunities",
                "stable communication",
            ],
            "paragraphs_final": [
                "to maintain accurate SOC.",
                "",
                "Why Full Charge Matters",
                "The BMS normally performs balancing near full charge.",
                "",
                "If the battery NEVER reaches full charge:",
                "❌ balancing may not complete",
                "❌ SOC drift develops",
                "❌ runtime estimates become inaccurate",
                "❌ battery behaviour becomes unstable",
            ],
             "images" : [
                {
                    "src" : "images/many battery complains.png",
                    "alt" : "",
                },
            ],
        },
        {
            "title": "7.9 Operating Modes & System Behaviour",
            "paragraphs": [
                "Operating mode selection dramatically affects how the system behaves.",
                "",
                "Two identical systems can behave completely differently simply because different operating modes are selected.",
                "",
                "Backup Priority Mode",
                "In backup mode:",
            ],
            "bullets": [
                "the battery is preserved mainly for outages",
                "grid support may be prioritised",
                "reserve capacity maintained",
            ],
            "paragraphs_after": [
                "Best for:",
            ],
            "bullets_after": [
                "loadshedding backup",
                "uptime-focused customers",
                "critical load protection",
            ],
            "paragraphs_extra": [
                "",
                "Self-Consumption / Hybrid Mode",
                "In self-consumption mode:",
            ],
            "bullets_extra": [
                "solar powers loads first",
                "excess solar charges batteries",
                "batteries discharge later to reduce grid usage",
            ],
            "paragraphs_extra2": [
                "Best for:",
            ],
            "bullets_extra2": [
                "reducing electricity costs",
                "maximising solar usage",
                "hybrid energy management",
            ],
            "paragraphs_extra3": [
                "",
                "Time-of-Use (TOU) Mode",
                "In TOU mode:",
            ],
            "bullets_extra3": [
                "Charging and discharging occur according to schedules",
                "The inverter responds to electricity tariff periods",
            ],
            "paragraphs_extra4": [
                "Best for:",
            ],
            "bullets_extra4": [
                "commercial systems",
                "tariff optimisation",
                "scheduled energy management",
            ],
             "images" : [
                {
                    "src" : "images/the wrong operating mode.png",
                    "alt" : "",
                },
            ],
        },
        {
            "title": "7.10 Reserve SOC & Backup Behaviour",
            "paragraphs": [
                "Reserve SOC determines:",
            ],
            "bullets": [
                "how much battery capacity is preserved",
                "how deeply the battery may discharge",
            ],
            "paragraphs_after": [
                "If reserve SOC is set to:",
            ],
            "bullets_after": [
                "20%",
            ],
            "paragraphs_extra": [
                "the inverter attempts to preserve:",
            ],
            "bullets_extra": [
                "approximately 20% battery capacity",
            ],
            "paragraphs_final": [
                "for:",
            ],
            "bullets_final": [
                "backup reserve",
                "battery protection",
                "emergency operation",
            ],
            "images" : [
                {
                    "src" : "images/reserve soc.png",
                    "alt" : "",
                },
            ],
        },
        {
            "title": "7.11 Grid Charging & Solar Charging Behaviour",
            "paragraphs": [
                "Some systems allow:",
            ],
            "bullets": [
                "grid charging",
                "scheduled charging",
                "generator charging",
            ],
            "paragraphs_after": [
                "This controls when the inverter may charge the battery using:",
            ],
            "bullets_after": [
                "utility power",
                "generator input",
                "solar energy",
            ],
            "paragraphs_extra": [
                "Solar Charging Priority",
                "The inverter must also determine:",
            ],
            "bullets_extra": [
                "how solar energy is prioritised",
            ],
            "paragraphs_extra2": [
                "Options may include:",
            ],
            "bullets_extra2": [
                "solar to loads first",
                "solar to battery first",
                "export priority",
                "self-use optimisation",
            ],
            "paragraphs_extra3": [
                "These settings affect:",
            ],
            "bullets_extra3": [
                "battery cycling",
                "savings",
                "runtime",
                "system efficiency",
            ],
        },
        {
            "title": "7.12 Time, Date & Timezone Settings",
            "paragraphs": [
                "This section is extremely important and often overlooked.",
                "",
                "Many inverter functions rely heavily on accurate:",
            ],
            "bullets": [
                "time",
                "date",
                "timezone",
            ],
            "paragraphs_after": [
                "Incorrect time settings affect:",
            ],
            "bullets_after": [
                "TOU schedules",
                "grid charging",
                "backup scheduling",
                "reporting accuracy",
                "operating behaviour",
            ],
            "images" : [
                {
                    "src" : "images/if inverter time is incorrect.png",
                    "alt" :  "",
                },
            ],
        },
        {
            "title": "7.13 Monitoring & Connectivity Setup",
            "paragraphs": [
                "Modern systems rely heavily on:",
            ],
            "bullets": [
                "WiFi",
                "Ethernet",
                "cloud monitoring",
                "mobile apps",
                "installer monitoring portals",
            ],
            "paragraphs_after": [
                "Monitoring allows:",
            ],
            "bullets_after": [
                "remote troubleshooting",
                "firmware visibility",
                "alarm tracking",
                "customer support",
                "performance analysis",
            ],
        },
        {
            "title": "7.14 Final Configuration Verification",
            "paragraphs": [
                "Before completing setup, verify:",
            ],
            "bullets": [
                "communication stable",
                "inverter recognises battery correctly",
                "SOC stable and accurate",
                "charge/discharge limits updating correctly",
                "operating mode correct",
                "reserve SOC correct",
                "charging behaviour stable",
                "monitoring online",
                "no active alarms present",
            ],
        },
        {
            "title": "SECTION 3 — FIRMWARE & COMPATIBILITY",
            "paragraphs": [],
        },
        {
            "title": "7.9 What Is Firmware?",
            "paragraphs": [
                "Firmware is the internal software that controls how a device behaves.",
                "",
                "Every major system component has firmware:",
            ],
            "bullets": [
                "inverter",
                "BMS",
                "communication modules",
                "monitoring devices",
            ],
            "paragraphs_after": [
                "Think of it like this:",
                "👉 Hardware = the body",
                "👉 Firmware = the instructions",
                "",
                "Firmware controls:",
            ],
            "bullets_after": [
                "charging behaviour",
                "communication",
                "protection logic",
                "fault handling",
                "operating modes",
            ],
        },
        {
            "title": "7.10 Why Firmware Matters",
            "paragraphs": [
                "Outdated or incompatible firmware can cause:",
            ],
            "bullets": [
                "communication failures",
                "incorrect SOC",
                "BMS trips",
                "unstable charging",
                "inverter instability",
                "strange system behaviour",
            ],
            "paragraphs_after": [
                "Correct firmware improves:",
            ],
        },
        {
            "title": "7.11 Firmware Compatibility & Version Matching",
            "paragraphs": [
                "Not all firmware versions work correctly together.",
                "",
                "Always consider:",
            ],
            "bullets": [
                "inverter firmware version",
                "battery firmware version",
                "communication protocol version",
                "supported compatibility lists",
            ],
            "images" : [
                {
                    "src" : "images/firmware version mattching.png",
                    "alt" : "",
                },
            ],
        },
        {
            "title": "7.12 When to Update Firmware (and When NOT To)",
            "paragraphs": [
                "Good Reasons to Update",
            ],
            "bullets": [
                "known communication issue",
                "manufacturer recommendation",
                "compatibility issue",
                "abnormal system behaviour",
                "new battery/inverter combination",
            ],
        },
        {
            "title": "7.13 Safe Firmware Update Process",
            "paragraphs": [
                "Step 1 — Confirm Need",
                "Identify:",
            ],
            "bullets": [
                "actual problem",
                "expected improvement",
            ],
            "paragraphs_after": [
                "Step 2 — Check Compatibility",
                "Verify:",
            ],
            "bullets_after": [
                "supported versions",
                "compatibility lists",
                "manufacturer guidance",
            ],
            "paragraphs_extra": [
                "Step 3 — Prepare System",
                "Ensure:",
            ],
            "bullets_extra": [
                "stable power supply",
                "correct update tools",
                "settings backup where possible",
            ],
            "paragraphs_extra2": [
                "Step 4 — Perform Update",
                "Use:",
            ],
            "bullets_extra2": [
                "approved process",
                "approved software",
                "approved cables",
            ],
            "paragraphs_extra3": [
                "NEVER interrupt the process.",
                "",
                "Step 5 — Verify System",
                "After updating:",
            ],
            "bullets_extra3": [
                "check communication",
                "check charging",
                "verify SOC",
                "verify operating mode",
                "check for faults",
            ],
            "paragraphs_critical": [
                "Critical Warning",
                "Interrupting firmware updates may:",
            ],
            "bullets_critical": [
                "❌corrupt devices",
                "❌damage communication",
                "❌require factory recovery",
            ],
        },
        {
            "title": "SECTION 4 — SYSTEM STABILITY & TROUBLESHOOTING",
            "paragraphs": [],
        },
        {
            "title": "7.14 Common Setup, Communication & Firmware Problems",
            "paragraphs": [
                "Communication Problems",
                "Symptoms:",
            ],
            "bullets": [
                "❌frozen SOC",
                "❌communication alarms",
                "❌battery not recognised",
            ],
            "paragraphs_after": [
                "Possible causes:",
            ],
            "bullets_after": [
                "wrong protocol",
                "bad communication cable",
                "incorrect firmware",
                "wrong port",
                "unsupported battery profile",
            ],
            "paragraphs_extra": [
                "Charging Problems",
                "Symptoms:",
            ],
            "bullets_extra": [
                "❌battery never reaches 100%",
                "❌poor runtime",
                "❌balancing issues",
            ],
            "paragraphs_charging": [
                "Possible causes:",
            ],
            "bullets_charging": [
                "low charge voltage",
                "incorrect battery type",
                "communication failure",
                "insufficient PV",
            ],
            "paragraphs_soc": [
                "SOC Problems",
                "Symptoms:",
            ],
            "bullets_soc": [
                "❌SOC jumps suddenly",
                "❌inaccurate runtime",
                "❌battery switches off unexpectedly",
            ],
            "paragraphs_soc_causes": [
                "Possible causes:",
            ],
            "bullets_soc_causes": [
                "no full charges",
                "poor balancing",
                "communication issues",
                "SOC drift",
            ],
            "paragraphs_firmware": [
                "Firmware Problems",
                "Symptoms:",
            ],
            "bullets_firmware": [
                "❌unstable behaviour",
                "❌random faults",
                "❌intermittent communication",
            ],
            "paragraphs_firmware_causes": [
                "Possible causes:",
            ],
            "bullets_firmware_causes": [
                "incompatible versions",
                "failed update",
                "unsupported firmware combinations",
            ],
            
        },
        {
            "title": "7.15 Practical Installer Examples",
            "paragraphs": [],
            "images"  : [
                {
                    "src" : "images/faulty battery lets look at the real cause.png",
                    "alt" : "",
                },
                 {
                    "src" : "images/battery never full.png",
                    "alt" : "",
                },
                 {
                    "src" : "images/communication fault.png",
                    "alt" : "",
                },
                 {
                    "src" : "images/bad run time.png",
                    "alt" : "",
                },
                 {
                    "src" : "images/empty battery.png",
                    "alt" : "",
                },
            ],
        },
        {
            "title": "7.16 Installer Rules for Stable Systems",
            "paragraphs": [],
            "images"  : [
                {
                    "src" : "images/installer rules for stable.png",
                    "alt" : "",
                },

                {
                    "src" : "images/wrapping up module 7.png",
                    "alt" : "",
                },
            ],
            
        },
    ],
}

MODULE_7_ASSESSMENT = {
    "title": "Module 7 Assessment",
    "subtitle": "System Installation, Wiring & Integration",
    "questions": [
        {
            "question": "1. The primary goal of a professional installation is to:",
            "options": [
                "A) Reduce inverter weight",
                "B) Create a safe, reliable and serviceable system",
                "C) Maximise cable length",
                "D) Increase battery voltage",
            ],
            "answer": "B",
            "explanation": "Professional installations prioritize safety, reliability, and the ability to service the system.",
        },
        {
            "question": "2. Before starting any installation, the installer should first:",
            "options": [
                "A) Power on the inverter",
                "B) Connect the batteries",
                "C) Review the system design and installation plan",
                "D) Update firmware",
            ],
            "answer": "C",
            "explanation": "Always review the design and plan before beginning any physical installation work.",
        },
        {
            "question": "3. One of the biggest causes of system failures is:",
            "options": [
                "A) Battery colour",
                "B) Poor workmanship and loose connections",
                "C) Solar panel size",
                "D) WiFi speed",
            ],
            "answer": "B",
            "explanation": "Loose connections and poor workmanship are major causes of system failures and overheating.",
        },
        {
            "question": "4. Batteries should ideally be installed in:",
            "options": [
                "A) Direct sunlight",
                "B) Hot roof spaces",
                "C) A cool, dry and ventilated area",
                "D) Completely sealed containers with no airflow",
            ],
            "answer": "C",
            "explanation": "Cool, dry, well-ventilated areas protect battery performance and lifespan.",
        },
        {
            "question": "5. Poor battery ventilation can lead to:",
            "options": [
                "A) Increased efficiency",
                "B) Reduced cable size",
                "C) Overheating and reduced lifespan",
                "D) Higher solar production",
            ],
            "answer": "C",
            "explanation": "Poor ventilation causes overheating, BMS trips, and shortened battery lifespan.",
        },
        {
            "question": "6. Why is neat cable routing important?",
            "options": [
                "A) It improves WiFi connection",
                "B) It reduces installation professionalism",
                "C) It improves safety, airflow and future servicing",
                "D) It increases battery voltage",
            ],
            "answer": "C",
            "explanation": "Neat cable routing improves safety, cooling, and makes future maintenance easier.",
        },
        {
            "question": "7. DC cables should always be:",
            "options": [
                "A) Mixed randomly with AC cables",
                "B) Routed separately where possible",
                "C) Installed without protection",
                "D) Shorted together for balancing",
            ],
            "answer": "B",
            "explanation": "DC and AC cables should be routed separately to avoid interference and safety issues.",
        },
        {
            "question": "8. Incorrect cable sizing can cause:",
            "options": [
                "A) Better efficiency",
                "B) Voltage drop and excessive heat",
                "C) Improved inverter performance",
                "D) Faster battery charging",
            ],
            "answer": "B",
            "explanation": "Undersized cables cause voltage drop, overheating, and fire risks.",
        },
        {
            "question": "9. All battery terminations should be:",
            "options": [
                "A) Hand-tightened only",
                "B) Properly crimped and torqued",
                "C) Installed without lugs",
                "D) Left loose for expansion",
            ],
            "answer": "B",
            "explanation": "Proper crimping and torque settings ensure secure, low-resistance connections.",
        },
        {
            "question": "10. The purpose of a DC breaker or fuse is to:",
            "options": [
                "A) Increase battery capacity",
                "B) Protect the system from overcurrent and faults",
                "C) Improve inverter communication",
                "D) Increase solar production",
            ],
            "answer": "B",
            "explanation": "DC breakers and fuses protect the system from overcurrent and fault conditions.",
        },
        {
            "question": "11. What is one major danger of reverse polarity?",
            "options": [
                "A) Reduced solar generation",
                "B) Immediate equipment damage",
                "C) Improved efficiency",
                "D) Lower inverter load",
            ],
            "answer": "B",
            "explanation": "Reverse polarity causes immediate, catastrophic damage to inverter and BMS.",
        },
        {
            "question": "12. Before connecting batteries, installers should always:",
            "options": [
                "A) Assume polarity is correct",
                "B) Check voltage and polarity using a meter",
                "C) Connect batteries live",
                "D) Disable the BMS permanently",
            ],
            "answer": "B",
            "explanation": "Always verify voltage and polarity with a meter before making any connections.",
        },
        {
            "question": "13. Why are communication cables important in lithium systems?",
            "options": [
                "A) They increase voltage",
                "B) They allow intelligent control between battery and inverter",
                "C) They replace DC cables",
                "D) They increase battery capacity",
            ],
            "answer": "B",
            "explanation": "Communication enables the inverter and battery to work as an intelligent system.",
        },
        {
            "question": "14. CAN Bus and RS485 are examples of:",
            "options": [
                "A) Cooling systems",
                "B) Communication protocols",
                "C) Earthing methods",
                "D) AC protection devices",
            ],
            "answer": "B",
            "explanation": "CAN Bus and RS485 are communication protocols used for system integration.",
        },
        {
            "question": "15. Incorrect battery communication setup can result in:",
            "options": [
                "A) Better charging",
                "B) System instability and charging problems",
                "C) Increased inverter size",
                "D) Lower battery temperatures",
            ],
            "answer": "B",
            "explanation": "Poor communication causes system instability, incorrect SOC, and charging problems.",
        },
        {
            "question": "16. Earthing and bonding are important because they:",
            "options": [
                "A) Increase battery runtime",
                "B) Improve solar irradiance",
                "C) Protect people and equipment from faults",
                "D) Increase inverter output",
            ],
            "answer": "C",
            "explanation": "Proper earthing and bonding protect people and equipment from electrical hazards.",
        },
        {
            "question": "17. AC and DC isolators are installed to:",
            "options": [
                "A) Increase voltage",
                "B) Safely isolate parts of the system",
                "C) Improve battery balancing",
                "D) Replace circuit breakers",
            ],
            "answer": "B",
            "explanation": "Isolators allow safe disconnection of system components for maintenance and safety.",
        },
        {
            "question": "18. Which of the following is considered good installer practice?",
            "options": [
                "A) Leaving cables unsupported",
                "B) Mixing communication and power cables randomly",
                "C) Labelling all breakers and isolators clearly",
                "D) Installing batteries without protection devices",
            ],
            "answer": "C",
            "explanation": "Clear labelling improves safety, understanding, and future maintenance.",
        },
        {
            "question": "19. Before powering up a system for the first time, installers should:",
            "options": [
                "A) Disconnect all protection devices",
                "B) Perform a full commissioning inspection",
                "C) Remove communication cables",
                "D) Increase inverter voltage manually",
            ],
            "answer": "B",
            "explanation": "A full commissioning inspection ensures everything is correct before operation.",
        },
        {
            "question": "20. A system should NEVER be energised if:",
            "options": [
                "A) Labels are installed",
                "B) Torque checks are complete",
                "C) Wiring and polarity have not been verified",
                "D) Batteries are fully charged",
            ],
            "answer": "C",
            "explanation": "Never power up a system until all wiring and polarity have been verified.",
        },
        {
            "question": "21. Why is torque important on battery terminals?",
            "options": [
                "A) Loose connections can create heat and failures",
                "B) It improves solar production",
                "C) It increases battery voltage",
                "D) It changes inverter frequency",
            ],
            "answer": "A",
            "explanation": "Proper torque ensures secure connections and prevents heat-related failures.",
        },
        {
            "question": "22. One common cause of nuisance tripping is:",
            "options": [
                "A) Proper earthing",
                "B) Correct cable sizing",
                "C) Incorrect neutral-earth configuration",
                "D) Proper commissioning",
            ],
            "answer": "C",
            "explanation": "Incorrect neutral-earth configuration causes nuisance earth leakage trips.",
        },
        {
            "question": "23. Professional installers build systems that are:",
            "options": [
                "A) Difficult to service",
                "B) Easy to understand, maintain and troubleshoot",
                "C) Hidden behind walls completely",
                "D) Designed without labels",
            ],
            "answer": "B",
            "explanation": "Professional systems are designed for easy understanding, maintenance, and troubleshooting.",
        },
        {
            "question": "24. What should installers do after completing installation?",
            "options": [
                "A) Leave without testing",
                "B) Immediately disconnect the batteries",
                "C) Test system operation and verify functionality",
                "D) Remove all warning labels",
            ],
            "answer": "C",
            "explanation": "Test and verify system operation before handing over to the customer.",
        },
        {
            "question": "25. A professional installation reflects on:",
            "options": [
                "A) Only the inverter brand",
                "B) Only the customer",
                "C) The installer, the product and the REVOV brand",
                "D) The solar panel manufacturer only",
            ],
            "answer": "C",
            "explanation": "Professional work reflects on the installer, product quality, and the REVOV brand reputation.",
        },
    ],
}

MODULE_8_MONITORING_TROUBLESHOOTING = {
    "module_title": "MODULE 8 — Monitoring, Optimisation, Troubleshooting & Fault Finding",
    "module_subtitle": "How to monitor, diagnose, optimise and maintain systems",
    "sections": [
        {
            "title": "8.1 Module Learning Outcomes",
            "paragraphs": [
                "This module focuses on how to monitor system behaviour, identify abnormal operation, diagnose faults, optimise performance, maintain system health, and troubleshoot problems using a structured professional approach.",
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
            "title": "SECTION 1 — MONITORING & UNDERSTANDING SYSTEM BEHAVIOUR",
            "paragraphs": [],
        },
        {
            "title": "8.2 Why Monitoring Matters",
            "paragraphs": [
                "Modern lithium systems are intelligent energy systems.",
                "",
                "They are no longer:",
            ],
            "bullets": [
                "simple backup systems",
                "\"install and forget\" systems",
            ],
            "paragraphs_after": [
                "Modern systems rely heavily on:",
            ],
            "bullets_after": [
                "communication",
                "monitoring",
                "real-time data",
                "inverter behaviour",
                "BMS intelligence",
                "remote diagnostics",
            ],
            "paragraphs_extra": [
                "Monitoring allows installers to:",
            ],
            "bullets_extra": [
                "understand system behaviour",
                "identify developing problems early",
                "diagnose faults faster",
                "optimise performance",
                "improve customer support",
                "reduce unnecessary call-outs",
            ],
            "paragraphs_extra2": [
                "Without monitoring:",
            ],
            "bullets_extra2": [
                "installers often guess",
                "faults become harder to diagnose",
                "customer complaints increase",
                "hidden problems develop unnoticed",
            ],
            "paragraphs_final": [
                "Good monitoring changes troubleshooting from:",
                "❌ reacting to failures",
                "to:",
                "✔ proactively managing system health",
            ],
        },
        {
            "title": "8.3 What Monitoring Actually Shows You",
            "paragraphs": [
                "Monitoring allows installers to see how the system behaves in real-world operation.",
                "",
                "Depending on the inverter and battery platform, monitoring may show:",
            ],
            "bullets": [
                "battery SOC",
                "battery voltage",
                "battery current",
                "charging behaviour",
                "discharge behaviour",
                "PV production",
                "grid usage",
                "load consumption",
                "battery temperature",
                "alarms and warnings",
                "fault history",
                "historical trends",
            ],
            "paragraphs_after": [
                "This information becomes extremely valuable during:",
            ],
            "bullets_after": [
                "troubleshooting",
                "optimisation",
                "maintenance",
                "customer support",
            ],
        },
        {
            "title": "8.3.1 Why Smart Monitoring Matters in Modern REVOV Systems",
            "paragraphs": [
                "Modern REVOV Batteries systems are designed as intelligent lithium systems with integrated communication and monitoring capabilities.",
                "",
                "Depending on the system design, REVOV systems may support:",
            ],
            "bullets": [
                "CAN Bus communication",
                "RS485 communication",
                "Bluetooth monitoring",
                "inverter monitoring platforms",
                "cloud monitoring portals",
                "remote monitoring apps",
            ],
            "paragraphs_after": [
                "This allows installers and users to monitor:",
            ],
            "bullets_after": [
                "battery behaviour",
                "charging activity",
                "balancing behaviour",
                "faults and warnings",
                "battery health",
                "system performance trends",
            ],
            "paragraphs_extra": [
                "in real time.",
            ],
        },
        {
            "title": "8.4 Understanding Daily System Behaviour",
            "paragraphs": [
                "One of the most important troubleshooting skills is understanding what a system should normally do throughout a typical day.",
                "",
                "A healthy system follows predictable daily behaviour patterns.",
                "",
                "Why Understanding Daily Behaviour Matters",
                "If installers understand normal behaviour:",
            ],
            "bullets": [
                "abnormal behaviour becomes easier to identify",
            ],
            "paragraphs_after": [
                "Without understanding normal behaviour:",
            ],
            "bullets_after": [
                "installers often misdiagnose healthy systems",
            ],
        },
        {
            "title": "8.5 What \"Normal\" Looks Like",
            "paragraphs": [
                "A healthy lithium system should normally show:",
            ],
            "bullets": [
                "stable SOC movement",
                "predictable charging behaviour",
                "smooth battery discharge",
                "stable communication",
                "realistic PV production",
                "balanced battery behaviour",
                "consistent operating patterns",
            ],
            "paragraphs_after": [
                "Normal systems:",
            ],
            "bullets_after": [
                "behave logically",
                "follow settings correctly",
                "respond predictably",
            ],
            "paragraphs_extra": [
                "Examples of Normal Behaviour",
            ],
            "bullets_extra": [
                "SOC decreasing at night",
                "lower winter solar production",
                "battery charging slower during cloudy weather",
                "increased grid usage during poor solar conditions",
            ],
            "paragraphs_final": [
                "These are not faults.",
            ],
        },
        {
            "title": "SECTION 2 — MONITORING-LED TROUBLESHOOTING",
            "paragraphs": [],
        },
        {
            "title": "8.6 Using Monitoring to Diagnose Problems",
            "paragraphs": [
                "Monitoring should always be the installer's first troubleshooting tool.",
                "",
                "Before:",
            ],
            "bullets": [
                "replacing equipment",
                "changing settings randomly",
                "disconnecting components",
            ],
            "paragraphs_after": [
                "first:",
            ],
            "bullets_after": [
                "review system behaviour",
                "check historical trends",
                "analyse charging behaviour",
                "review fault history",
            ],
            "paragraphs_extra": [
                "Good monitoring often reveals:",
            ],
            "bullets_extra": [
                "the actual cause quickly",
            ],
        },
        {
            "title": "8.7 The Installer Mindset — Stop Guessing, Start Diagnosing",
            "paragraphs": [
                "Professional troubleshooting follows logic.",
            ],
            "bullets": [
                "follows evidence",
                "checks data first",
                "isolates sections logically",
                "verifies before acting",
            ],
        },
        {
            "title": "8.8 Break the System Into Sections",
            "paragraphs": [
                "Professional installers divide systems into logical sections during troubleshooting.",
                "",
                "This prevents confusion and unnecessary part replacement.",
            ],
        },
        {
            "title": "8.9 The 5-Step Troubleshooting Flow",
            "paragraphs": [
                "Professional troubleshooting should always follow a structured process.",
            ],
        },
        {
            "title": "SECTION 3 — PRACTICAL FAULT FINDING",
            "paragraphs": [],
        },
        {
            "title": "8.10 Using Symptoms to Read the System",
            "paragraphs": [
                "Symptoms provide clues.  Professional installers learn to \"read\" the system.",
            ],
        },
        {
            "title": "SECTION 4 — MAINTENANCE & OPTIMISATION",
            "paragraphs": [],
        },
        {
            "title": "8.13 Routine Maintenance",
            "paragraphs": [
                "Even high-quality systems require periodic inspection.",
                "",
                "Routine maintenance should include:",
            ],
            "bullets": [
                "cable inspections",
                "checking lugs and torque",
                "ventilation inspection",
                "dust removal",
                "checking for overheating",
                "monitoring review",
                "firmware review",
                "communication verification",
            ],
            "paragraphs_after": [
                "Why Maintenance Matters",
                "Small problems become large problems if ignored.",
                "",
                "Routine inspections help identify:",
            ],
            "bullets_after": [
                "loose connections",
                "overheating",
                "abnormal behaviour",
                "declining performance",
            ],
            "paragraphs_extra": [
                "before major failures occur.",
            ],
        },
        {
            "title": "8.14 Battery Health & Lifespan Optimisation",
            "paragraphs": [
                "Battery lifespan depends heavily on:",
            ],
            "bullets": [
                "temperature",
                "charging behaviour",
                "cycling behaviour",
                "system sizing",
                "operating conditions",
            ],
            "paragraphs_after": [
                "Optimisation Best Practices",
            ],
            "bullets_after": [
                "maintain proper ventilation",
                "allow periodic full charges",
                "maintain stable communication",
                "avoid excessive discharge",
                "use correct operating modes",
                "avoid excessive heat",
            ],
        },
        {
            "title": "8.15 System Optimisation",
            "paragraphs": [
                "Optimisation means improving:",
            ],
            "bullets": [
                "efficiency",
                "runtime",
                "battery protection",
                "solar usage",
                "customer experience",
            ],
            "paragraphs_after": [
                "Optimisation Examples",
            ],
            "bullets_after": [
                "adjusting reserve SOC",
                "improving operating modes",
                "changing charging schedules",
                "reducing unnecessary grid usage",
                "improving solar utilisation",
            ],
        },
        {
            "title": "8.16 Seasonal Changes & Customer Behaviour",
            "paragraphs": [
                "System behaviour changes throughout the year.",
                "",
                "Winter may cause:",
            ],
            "bullets": [
                "lower solar production",
                "increased battery cycling",
                "more grid support",
            ],
            "paragraphs_after": [
                "Summer may cause:",
            ],
            "bullets_after": [
                "higher solar production",
                "earlier full charging",
            ],
            "paragraphs_extra": [
                "Customer Behaviour Also Matters",
                "Customers may:",
            ],
            "bullets_extra": [
                "add appliances",
                "change usage patterns",
                "increase nighttime loads",
            ],
            "paragraphs_final": [
                "Monitoring helps installers identify these changes.",
            ],
        },
        {
            "title": "8.17 Remote Monitoring & Proactive Support",
            "paragraphs": [
                "Professional installers increasingly use remote monitoring before visiting site.",
                "",
                "Remote monitoring allows:",
            ],
            "bullets": [
                "reviewing fault history",
                "analysing charging behaviour",
                "checking system trends",
                "identifying abnormal patterns",
                "reducing unnecessary call-outs",
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
        {
            "question": "2. Incorrect inverter settings can result in:",
            "options": [
                "A) Better battery life",
                "B) Charging problems and system instability",
                "C) Higher solar production",
                "D) Lower current flow",
            ],
            "answer": "B",
            "explanation": "Wrong settings cause charging problems, instability, and poor system performance.",
        },
        {
            "question": "3. Battery communication allows the inverter to:",
            "options": [
                "A) Increase PV voltage",
                "B) Monitor and control battery operation intelligently",
                "C) Replace protection devices",
                "D) Improve WiFi signal strength",
            ],
            "answer": "B",
            "explanation": "Communication enables intelligent monitoring and control of battery operation.",
        },
        {
            "question": "4. CAN Bus and RS485 are used for:",
            "options": [
                "A) Cooling systems",
                "B) Communication between devices",
                "C) Earthing systems",
                "D) AC synchronisation only",
            ],
            "answer": "B",
            "explanation": "CAN Bus and RS485 are communication protocols for device integration.",
        },
        {
            "question": "5. If inverter-to-battery communication is lost, the system may:",
            "options": [
                "A) Operate normally with full functionality",
                "B) Shut down or operate with limited control",
                "C) Increase battery capacity automatically",
                "D) Improve charging efficiency",
            ],
            "answer": "B",
            "explanation": "Lost communication causes system shutdown or limited operation with reduced functionality.",
        },
        {
            "question": "6. The first thing installers should check when troubleshooting a fault is:",
            "options": [
                "A) Battery colour",
                "B) What changed in the system",
                "C) Solar panel orientation",
                "D) Roof condition",
            ],
            "answer": "B",
            "explanation": "Understanding what changed helps identify the actual cause of the problem.",
        },
        {
            "question": "7. One of the most common causes of communication problems is:",
            "options": [
                "A) Correct DIP switch settings",
                "B) Incorrect communication cables or settings",
                "C) Proper earthing",
                "D) Clean solar panels",
            ],
            "answer": "B",
            "explanation": "Incorrect communication cables and settings are major causes of communication failures.",
        },
        {
            "question": "8. DIP switches are commonly used to:",
            "options": [
                "A) Increase battery voltage",
                "B) Configure communication and battery addressing",
                "C) Replace breakers",
                "D) Improve inverter cooling",
            ],
            "answer": "B",
            "explanation": "DIP switches configure communication protocols and battery addressing in the system.",
        },
        {
            "question": "9. Why is battery addressing important in parallel systems?",
            "options": [
                "A) It increases solar output",
                "B) It allows batteries to communicate correctly within the system",
                "C) It changes AC frequency",
                "D) It reduces cable size",
            ],
            "answer": "B",
            "explanation": "Battery addressing ensures correct communication and coordination in parallel systems.",
        },
        {
            "question": "10. Firmware updates are important because they can:",
            "options": [
                "A) Increase battery weight",
                "B) Improve system stability and compatibility",
                "C) Eliminate the need for maintenance",
                "D) Reduce inverter size",
            ],
            "answer": "B",
            "explanation": "Firmware updates improve stability, fix bugs, and enhance compatibility.",
        },
        {
            "question": "11. A battery operating at very high temperatures may:",
            "options": [
                "A) Improve lifespan",
                "B) Increase efficiency permanently",
                "C) Trigger protection alarms or reduce performance",
                "D) Increase solar generation",
            ],
            "answer": "C",
            "explanation": "High temperatures trigger BMS protection and accelerate battery degradation.",
        },
        {
            "question": "12. State of Charge (SOC) refers to:",
            "options": [
                "A) Battery temperature",
                "B) Available battery energy remaining",
                "C) Cable resistance",
                "D) Inverter output frequency",
            ],
            "answer": "B",
            "explanation": "SOC is the percentage of energy remaining in the battery.",
        },
        {
            "question": "13. State of Health (SOH) refers to:",
            "options": [
                "A) Battery communication speed",
                "B) Overall battery condition and aging",
                "C) Solar production",
                "D) AC voltage stability",
            ],
            "answer": "B",
            "explanation": "SOH indicates the overall condition and remaining lifespan of the battery.",
        },
        {
            "question": "14. Which of the following is considered good maintenance practice?",
            "options": [
                "A) Ignoring warning alarms",
                "B) Regular inspection of cables and terminations",
                "C) Disabling protection devices",
                "D) Running batteries to 0% daily",
            ],
            "answer": "B",
            "explanation": "Regular inspections help identify loose connections and potential problems early.",
        },
        {
            "question": "15. Thermal inspections are important because they help identify:",
            "options": [
                "A) Internet issues",
                "B) Hot spots and loose connections",
                "C) Solar shading",
                "D) Inverter colour differences",
            ],
            "answer": "B",
            "explanation": "Thermal imaging detects hot spots caused by loose connections and resistance.",
        },
        {
            "question": "16. One major cause of voltage drop is:",
            "options": [
                "A) Oversized cables",
                "B) Undersized or loose connections",
                "C) Correct torque settings",
                "D) Proper earthing",
            ],
            "answer": "B",
            "explanation": "Undersized cables and loose connections create resistance and cause voltage drop.",
        },
        {
            "question": "17. If a battery is not charging properly, installers should check:",
            "options": [
                "A) Communication, settings and available charging sources",
                "B) Roof paint colour",
                "C) Solar frame size",
                "D) Airflow only",
            ],
            "answer": "A",
            "explanation": "Check communication, settings, and available charging sources (solar, grid) first.",
        },
        {
            "question": "18. Monitoring platforms allow installers to:",
            "options": [
                "A) Increase inverter voltage remotely",
                "B) View system performance and diagnose faults",
                "C) Replace the BMS",
                "D) Eliminate maintenance completely",
            ],
            "answer": "B",
            "explanation": "Monitoring platforms provide visibility into system performance and help diagnose issues.",
        },
        {
            "question": "19. Why are event logs useful during troubleshooting?",
            "options": [
                "A) They improve battery lifespan",
                "B) They help identify when and why faults occurred",
                "C) They increase solar generation",
                "D) They reduce current flow",
            ],
            "answer": "B",
            "explanation": "Event logs provide a timeline of system events and help identify root causes.",
        },
        {
            "question": "20. Frequent inverter overload alarms usually indicate:",
            "options": [
                "A) Proper sizing",
                "B) Excessive load demand or poor system design",
                "C) Improved battery performance",
                "D) Better efficiency",
            ],
            "answer": "B",
            "explanation": "Overload alarms suggest loads exceed inverter capacity or poor system sizing.",
        },
        {
            "question": "21. A professional troubleshooting process should be:",
            "options": [
                "A) Random and based on guessing",
                "B) Logical and systematic",
                "C) Focused only on replacing parts",
                "D) Based only on customer opinion",
            ],
            "answer": "B",
            "explanation": "Professional troubleshooting follows a logical, systematic approach with evidence.",
        },
        {
            "question": "22. One major advantage of remote monitoring is:",
            "options": [
                "A) Reduced battery voltage",
                "B) Faster fault identification and support",
                "C) Elimination of all onsite visits",
                "D) Increased inverter capacity",
            ],
            "answer": "B",
            "explanation": "Remote monitoring enables faster identification and support without visiting site first.",
        },
        {
            "question": "23. If battery SOC suddenly drops under load, this may indicate:",
            "options": [
                "A) Normal operation only",
                "B) Voltage sag, excessive load or battery issues",
                "C) Increased battery lifespan",
                "D) Improved communication",
            ],
            "answer": "B",
            "explanation": "SOC drop under load indicates voltage sag, overload, or battery degradation.",
        },
        {
            "question": "24. Preventative maintenance helps to:",
            "options": [
                "A) Increase fault frequency",
                "B) Reduce long-term system reliability",
                "C) Identify issues before major failures occur",
                "D) Eliminate the need for installers",
            ],
            "answer": "C",
            "explanation": "Preventative maintenance catches problems early and prevents major failures.",
        },
        {
            "question": "25. Professional installers understand that troubleshooting starts with:",
            "options": [
                "A) Replacing equipment immediately",
                "B) Understanding system behaviour and operating conditions",
                "C) Disconnecting communication cables",
                "D) Increasing inverter settings",
            ],
            "answer": "B",
            "explanation": "Understanding normal system behaviour is essential to identify abnormal operation.",
        },
    ],
}

MODULE_9_ECOSYSTEM_AND_PRODUCT_RANGE = {
    "module_title": "MODULE 9 — REVOV Ecosystem, Product Range & Installer Best Practices",
    "module_subtitle": "Understanding REVOV's Mission, Philosophy, and Product Portfolio",
    "sections": [
        {
            "title": "9.1 The REVOV Story",
            "paragraphs": [
                "South Africa's energy landscape has changed dramatically over the last decade. Loadshedding, rising electricity costs, unstable grid supply, and increasing energy demands have forced homes and businesses to rethink how they use and store power.",
                "REVOV was built in response to this challenge. REVOV Batteries is a South African energy storage company focused on reliable, practical, and intelligent lithium battery solutions for residential, commercial, and industrial applications.",
                "The company was founded with a clear purpose: to help people and businesses take control of their energy future.",
                "From the beginning, REVOV focused on energy storage systems designed for real-world African conditions — systems capable of handling unstable grids, demanding environments, and the growing need for dependable backup and solar energy storage solutions.",
            ],
        },
        {
            "title": "9.2 Built Around Energy Independence",
            "paragraphs": [
                "REVOV believes energy storage is no longer a luxury. It has become essential infrastructure.",
                "Modern homes and businesses rely on stable electricity for:",
            ],
            "bullets": [
                "security systems",
                "internet connectivity",
                "refrigeration",
                "communication",
                "business operations",
                "production environments",
                "essential daily living",
            ],
            "paragraphs_after": [
                "When power fails, productivity, security, and comfort are immediately affected.",
                "REVOV systems are designed to:",
            ],
            "bullets_after": [
                "provide reliable backup power",
                "reduce dependence on the grid",
                "support solar self-consumption",
                "improve energy efficiency",
                "reduce long-term energy costs",
                "support off-grid and hybrid energy solutions",
            ],
            "paragraphs_final": [
                "The goal is not simply to store energy. The goal is to create reliable, intelligent, and scalable energy systems that allow customers to continue operating with confidence.",
            ],
        },
        {
            "title": "9.3 A Strong Focus on Lithium Iron Phosphate (LiFePO₄)",
            "paragraphs": [
                "REVOV specialises in Lithium Iron Phosphate (LiFePO₄) battery technology.",
                "LiFePO₄ chemistry has become one of the preferred battery technologies for modern energy storage because it offers:",
            ],
            "bullets": [
                "high safety",
                "long cycle life",
                "high efficiency",
                "strong thermal stability",
                "low maintenance",
                "excellent long-term reliability",
            ],
            "paragraphs_after": [
                "REVOV systems are designed for integration with modern inverter-controlled backup and solar systems used in:",
            ],
            "bullets_after": [
                "homes",
                "offices",
                "farms",
                "retail environments",
                "commercial buildings",
                "industrial applications",
            ],
            "paragraphs_final": [
                "Many REVOV systems use automotive-grade lithium cells designed to withstand demanding operating conditions, vibration, temperature fluctuations, and continuous cycling.",
            ],
        },
        {
            "title": "9.4 Innovation Through Practical Engineering",
            "paragraphs": [
                "REVOV's approach has always been strongly practical and installer-focused.",
                "The company understands that a battery is only one part of a complete energy system. Long-term performance depends on:",
            ],
            "bullets": [
                "correct system design",
                "inverter compatibility",
                "proper protection",
                "good installation practices",
                "communication integration",
                "commissioning quality",
                "firmware management",
                "after-sales support",
            ],
            "paragraphs_after": [
                "For this reason, REVOV works closely with:",
            ],
            "bullets_after": [
                "installers",
                "engineers",
                "distributors",
                "technical support teams",
                "renewable energy professionals",
            ],
            "paragraphs_final": [
                "The focus is not only on selling batteries, but on helping create stable, safe, and professionally designed energy systems.",
            ],
        },
        {
            "title": "9.5 Knowledge, Training & Installer Development",
            "paragraphs": [
                "REVOV believes that better installer knowledge leads to better system performance.",
                "A lithium battery system is only as good as:",
            ],
            "bullets": [
                "the installation,",
                "the configuration,",
                "and the commissioning process behind it.",
            ],
            "paragraphs_after": [
                "This is why training, technical support, and installer education form an important part of the REVOV approach.",
                "Professional installers must understand:",
            ],
            "bullets_after": [
                "system behaviour",
                "energy flow",
                "battery communication",
                "inverter logic",
                "protection systems",
                "troubleshooting methodology",
                "and safe installation practices",
            ],
            "paragraphs_final": [
                "The goal is not simply to create installers who can connect equipment. The goal is to help develop installers who can design, commission, troubleshoot, and support reliable energy systems professionally.",
            ],
        },
        {
            "title": "9.6 The REVOV Philosophy",
            "paragraphs": [
                "At its core, REVOV is built around a simple idea: Reliable energy creates progress.",
                "Reliable energy allows:",
            ],
            "bullets": [
                "businesses to operate,",
                "families to feel secure,",
                "installers to build professionally,",
                "and customers to become less dependent on an unstable grid.",
            ],
            "paragraphs_after": [
                "As the energy industry continues to evolve, REVOV continues focusing on:",
            ],
            "bullets_after": [
                "practical innovation,",
                "reliable storage,",
                "professional support,",
                "installer partnerships,",
                "and long-term energy resilience.",
            ],
            "paragraphs_final": [
                "REVOV is not only part of the backup power industry. It is part of the transition toward smarter, more independent energy systems across South Africa and beyond.",
            ],
        },
        {
            "title": "9.7 REVOV Product Range Overview",
            "paragraphs": [
                "REVOV offers a range of lithium energy storage solutions designed for residential, commercial, and industrial energy systems.",
                "The product range is built around modularity, scalability, reliability, and compatibility with modern hybrid and backup inverter systems.",
                "Each product is designed for a specific application and energy requirement, allowing installers to select the correct solution based on:",
            ],
            "bullets": [
                "backup requirements,",
                "inverter size,",
                "daily energy usage,",
                "scalability needs,",
                "installation space,",
                "and customer expectations.",
            ],
            "paragraphs_final": [
                "REVOV's product ecosystem ranges from compact residential backup batteries to large-scale commercial and high-voltage energy storage systems.",
            ],
        },
        {
            "title": "9.8 The REVOV Product Philosophy",
            "paragraphs": [
                "REVOV products are designed around several key principles:",
            ],
            "bullets": [
                "Reliable backup performance",
                "Long cycle life",
                "Safe LiFePO₄ chemistry",
                "Modular scalability",
                "Intelligent battery management",
                "Strong inverter compatibility",
                "Practical installation flexibility",
                "Real-world South African operating conditions",
            ],
        },
        {
            "title": "9.9 REVOV 12V LiFePO4 product range",
            "paragraphs": [
                "REVOV 12V lithium battery range is designed to deliver compact, lightweight and dependable energy storage solutions for applications where mobility, flexibility and reliable power are essential.",
                "Engineered for both portable and stationary applications, the REVOV 12V range combines long-term performance, intelligent battery management and rugged durability in a compact form factor suitable for demanding environments.",
                "With integrated Bluetooth-enabled BMS functionality, excellent temperature resilience and an IP55-rated design, these batteries provide reliable low-maintenance power for recreational, marine, off-grid, emergency backup and industrial applications.",
                "The REVOV 12V range is ideal for RVs, camping, boating, remote sites, telecoms backup systems, portable power solutions and niche mobility applications such as golf carts, utility vehicles and small electric boats where dependable energy storage and continuous operation are critical.",
            ],
            "images" : [
                {
                  "src" : "images/12v100ah.png",
                    "alt" : "image for Revov 12V100Ah battery ",
                },
                {
                  "src" : "images/12v200ah.png",
                    "alt" : "image for Revov 12v200ah.png battery ",
                },
            ],
        },
        {
            "title": "9.10 REVOV 24V LiFePO4 product range",
            "paragraphs": [
                "REVOV 24V lithium battery range is designed to provide dependable, compact and efficient energy storage solutions for smaller-scale backup and critical power applications where reliability and uptime are essential.",
                "Engineered for flexibility and durability, these batteries are ideal for installations requiring stable power in demanding environments, including telecoms infrastructure, remote sites, UPS systems, security and CCTV applications.",
                "The REVOV 24V range combines intelligent battery management with Bluetooth monitoring capability, robust environmental protection and excellent temperature resilience to ensure reliable performance in harsh operating conditions.",
                "With an IP55-rated design and long service life, these batteries deliver practical, low-maintenance lithium energy storage solutions for applications where space, reliability and continuous operation are critical.",
            ],
            "images" : [
                {
                   "src" : "images/24v100ah.png",
                    "alt" : "image of a REVOV 24V100AH BATTERY",
                },
            ],
        },
        {
            "title": "9.11 REVOV 51.2V LiFePO4 product range",
            "paragraphs": [
                "REVOV 51.2V lithium battery range is designed to deliver dependable, scalable and high-performance energy storage solutions for residential, commercial and industrial applications where reliable power is essential.",
                "Engineered for both hybrid and renewable energy systems, the REVOV 51.2V range provides efficient backup, primary and secondary power solutions with a strong focus on long-term performance, intelligent battery management and real-world durability.",
                "Built to handle demanding African operating conditions, including high temperatures, humidity and altitude, these modular lithium battery systems offer flexible expansion from smaller residential backup systems through to larger commercial energy storage installations.",
                "With advanced BMS protection, high round-trip efficiency, fast charging capability and compatibility with a wide range of trusted third-party monitoring and integration platforms, the REVOV 51.2V range is ideal for residential solar systems, off-grid and hybrid installations, commercial backup applications, telecoms, data centres, security infrastructure and critical power environments where stability, scalability and business continuity are critical.",
            ],
             "images" : [
                {
                   "src" : "images/e100.png",
                    "alt" : "image of a REVOV E100 BATTERY",
                },
                  {
                   "src" : "images/e300.png",
                    "alt" : "image of a REVOV E300 BATTERY",
                },
            ],
        },
        {
            "title": "9.12 High Voltage LiFePO4 product range",
            "paragraphs": [
                "REVOV High Voltage battery solutions are designed for larger energy applications where higher power demands, larger storage capacity, and improved system efficiency are required.",
                "High Voltage systems operate at significantly higher voltages than traditional low-voltage battery systems, allowing for lower current flow, smaller cable diameters, improved efficiency, and easier scalability for larger installations.",
                "These systems are ideal for large residential properties, commercial and industrial applications, agricultural operations, security infrastructure, and grid-scale energy solutions where reliability, performance, and business continuity are critical.",
                "REVOV High Voltage solutions are highly scalable, with systems under 150kWh available as standard modular solutions, while larger systems can be expanded using multiple battery modules or custom engineered by REVOV Energy Projects for large industrial and utility-scale applications exceeding 1MWh.",
            ],
            "images" : [
                {
                   "src" : "images/cfe 61.44.png",
                    "alt" : "image of a REVOV CFE 61.44 BATTERY",
                },
                  {
                   "src" : "images/energy core 51.2.png",
                    "alt" : "image of a REVOV energy core 51.2 BATTERY",
                },
            ],
        },
    ],
}

MODULE_10_INSTALLER_GUIDES_AND_RESOURCES = {
    "module_title": "MODULE 10 — Installer Guides & Resources",
    "module_subtitle": "Professional Installation Support, Best Practices, and Practical Field Resources",
    "sections": [
        {
            "title": "Module 10 — Installer Guides & Resources",
            "paragraphs": [
                "A professional installer is only as good as the tools, knowledge, and support available to them in the field.",
                "Even experienced installers rely on quick-reference guides, checklists, wiring diagrams, troubleshooting resources, and best-practice documentation to ensure systems are installed safely, configured correctly, and supported properly over time.",
                "This module provides a collection of practical installer resources designed to support you before, during, and after installation. These guides are intended to help simplify real-world work onsite, improve installation quality, reduce faults and callbacks, and assist with faster troubleshooting and commissioning.",
                "Throughout this module, you will find useful resources.",
                "As the REVOV product ecosystem continues to grow and evolve, additional guides, technical bulletins, compatibility updates, and installer resources may also be shared to help keep installers informed and supported.",
                "Remember: Good installations do not happen by accident. They are the result of good preparation, attention to detail, correct procedures, and continuous learning.",
                "These resources are designed to help you build systems that are:",
            ],
            "bullets": [
                "safe,",
                "reliable,",
                "professional,",
                "easy to maintain,",
                "and trusted by customers for years to come.",
            ],
             "images" : [
                {
                   "src" : "images/installer design guid.png",
                    "alt" : "image of a installation guid for the installers",
                },
                  {
                   "src" : "images/how to read revov batter.png",
                    "alt" : "image of how to read revov spec sheets.",
                },
            
                {
                   "src" : "images/revov e100 fault.png",
                    "alt" : "image of a REVOV E100 BATTERY",
                },
                  {
                   "src" : "images/revov e300 fault.png",
                    "alt" : "image of a REVOV E300 BATTERY fault finding",
                },
            
                {
                   "src" : "images/cfe 61.44 fault.png",
                    "alt" : "image of a REVOV CFE 61.44 BATTERY fault finding",
                },
                  {
                   "src" : "images/energy core 51,2 fault.png",
                    "alt" : "image of a REVOV energy core 51.2 fault finding.",
                },
            ],
        },
    ],
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

