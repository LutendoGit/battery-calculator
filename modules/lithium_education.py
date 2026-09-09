

from dataclasses import dataclass
from enum import Enum
from typing import Dict, List, Tuple


class LithiumBatteryFundamentals:
    """Educational content about lithium batteries"""

    # NOTE (2026-02): Fundamentals content has been updated to Module 1
    # "Introduction to Energy Storage & Modern Energy Systems".
    # The previous cell-behavior fundamentals were removed to avoid content mixups.
    DISCLAIMER = {
        "page_title": "Disclaimer",
        "module_title": "Disclaimer",
        "sections": [
            {
                "title": "DISCLAIMER",
                "icon": "",
                "paragraphs": [
                    "<br><strong>IMPORTANT TRAINING DISCLAIMER🧾</strong>",
                    "This manual is provided for training and general technical guidance purposes. Completion of this training does not, on its own, qualify, certify, register or legally authorise a person to perform electrical installation work. ",
                    "⚡All electrical work must be carried out by appropriately qualified, competent and/or registered persons where required, in accordance with applicable legislation, standards, manufacturer specifications and current REVOV technical documentation.",
                    "<br><strong>Images & Diagrams📐</strong>",
                    "Images, diagrams and system illustrations in this manual are provided for training and explanatory purposes and may be simplified. ",
                    "They should not be used as installation drawings or wiring instructions. Always refer to the applicable REVOV product manual, manufacturer documentation, approved system design, and current electrical requirements before installation."
                ],
                "highlights": [
                    "This training supports education only and does not replace professional electrical compliance or site-specific design controls."
                ],
            },
        ],
    }
    MODULE_1_FUNDAMENTALS = {
        "module_title": "MODULE 1 - Introduction to Energy Storage & Modern Energy Systems",
        "module_subtitle": "Core concepts installers need before tools, cables, or settings.",
        "sections": [
            {
                "title": "1.1 Module 1 Learning Outcomes",
                "paragraphs": [
                    "Before you start working with systems, it's important to understand the \"language\" of energy storage. This module lays the foundation for everything that follows — from system design to installation and troubleshooting.",
                    "Think of this as your baseline knowledge. If you understand this module well, the rest of the training becomes much easier and far more practical.",
                    "<br><strong>By the end of this module, you will be able to:</strong>",
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
                    "",
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
                    "",
                    "<br><u><strong>Power (kW) — What is happening right now</strong></u>",
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
                        "heading": "",
                        "paragraphs": [
                            "<br><u><strong>Energy (kWh) —What happens over time</strong></u>",
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
                            "This gives you your <strong>total power requirement (kW)</strong>",
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
                            "<span class=\"formula-highlight\">Load (kW) × Hours = Battery Size (kWh)</span>",
                        
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
                ],
                "subsections": [
                    {
                        "heading": "🔌 AC (Alternating Current)",
                        "paragraphs": [
                            "AC is the electricity used by most homes and businesses. It",
                            "Key Characteristics:",
                        ],
                        "bullets": [
                            "Supplied by Eskom/grid",
                            "Powers household plugs, lighting, and appliances",
                            "Operates at 230V/50Hz in most South African installations",
                            "Must comply with electrical standards",
                        ],
                    },
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
                            "This is why the inverter is essential. The inverter connects these two worlds. It doesn't just convert power — it manages:",
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
                            "<strong>Function: Converts sunlight into direct current (DC) electricity.</strong>",
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
                            "<strong>Function: Stores electrical energy for later use.</strong>",
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
                            "<strong>Function: Converts DC power from PV or batteries into AC power for use by appliances and the grid.</strong>",
                            "Role: Acts as the system's power electronics and control centre, providing protection, monitoring, and management features required for safe, efficient operation."
                        ],
                        "bullets": [
                            "Manages charging and discharging priorities between PV, battery, and loads",
                            "Provides essential protections (anti-islanding, overcurrent, thermal) and isolation",
                            "Available types: string inverters, hybrid inverter-chargers, and off-grid inverter systems",
                            "Includes data monitoring, logging, firmware updates, and remote management in modern models",
                            "Selection affects cable sizing, protection devices, and integration complexity"
                        ],
                    },
                    {
                        "heading": "Load — Energy Consumption",
                        "paragraphs": [
                            "<strong>Function: Represents devices and appliances that consume electrical power.</strong>",
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
                            "<strong>Function: Provides supplemental or backup power when solar or battery capacity is insufficient.</strong>",
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
                    "<br><strong>This changes how energy is used:</strong>",
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
                "paragraphs_footer": [
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
                        "paragraphs": [
                            "A backup system stores energy in batteries and uses an inverter to supply power during outages or when needed.",
                        ],
                        "images": [
                            {
                                "src": "images/Backup System.png",
                                "alt": "Backup System (No Solar)",
                            },
                        ],
                    },
                    {
                        "heading": "Grid-Tied Solar (No Batteries)",
                        "paragraphs": [
                            "A grid-tied solar system generates electricity from solar panels and feeds it directly to the grid to power your home or business.",
                        ],
                        "images": [
                            {
                                "src": "images/Grid-tied solar Sytem.png",  
                                "alt": "Grid-Tied Solar (No Batteries)",
                            },
                        ],
                    },
                    {
                        "heading": "Hybrid System (Solar + Battery + Grid)",
                        "paragraphs": [
                            "A hybrid system uses solar panels, batteries, and the grid together to provide reliable, efficient power day and night.",
                        ],
                        "images": [
                            {
                                "src": "images/Hybrid Solar System.png",
                                "alt": "Hybrid System (Solar + Battery + Grid)",
                            },
                        ],
                    },
                    {
                        "heading": "Fully Off-Grid System",
                        "paragraphs": [
                            "A fully off-grid solar system generates and stores all the energy you need, completely independent of the utility grid.",
                        ],
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
                        "paragraphs": [
                            "<br>While some system losses are unavoidable, a well-designed and professionally installed system can significantly reduce unnecessary energy losses. As an installer, many of the factors that affect efficiency are within your control. Correct cable sizing, quality workmanship, appropriate component selection, and ongoing maintenance all contribute to improved system performance, greater reliability, and better long-term energy yield.",
                            "The following best practices will help minimise losses and ensure the system operates as efficiently as possible.",
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
                    "<br>A high-quality battery will only perform well if:",
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
                   
                ],
            },
            {
              "title": "Wrapping Up Module 1",
              "page_break": True,
              "images": [
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
                "question": " Why has energy storage become so important in South Africa?",
                "options": [
                    "A) Because solar panels only work at night",
                    "B) Because the grid is stable and predictable",
                    "C) Because loadshedding, poor grid reliability and rising tariffs affect homes and businesses",
                    "D) Because batteries replace all electrical infrastructure"
                ],
                "answer": "C"
            },
            {
                "question": " Which of the following is a major benefit of battery storage?",
                "options": [
                    "A) It increases grid frequency",
                    "B) It provides automatic backup during outages",
                    "C) It removes the need for an inverter",
                    "D) It eliminates all system losses"
                ],
                "answer": "B"
            },
            {
                "question": " In practical terms, battery storage helps customers by:",
                "options": [
                    "A) Making all appliances use less power instantly",
                    "B) Saving energy for later use",
                    "C) Replacing the PV array",
                    "D) Increasing the grid voltage"
                ],
                "answer": "B"
            },
            {
                "question": " Power (kW) refers to:",
                "options": [
                    "A) Total electricity used over time",
                    "B) Electrical pressure",
                    "C) The rate at which electricity is used right now",
                    "D) Battery lifespan"
                ],
                "answer": "C"
            },
            {
                "question": "Energy (kWh) refers to:",
                "options": [
                    "A) The speed of current flow",
                    "B) Total stored or used electricity over time",
                    "C) Cable thickness",
                    "D) Instantaneous load only"
                ],
                "answer": "B"
            },
            {
                "question": "Power mainly determines the size of the:",
                "options": [
                    "A) Battery bank",
                    "B) Inverter",
                    "C) PV frame",
                    "D) Earth spike"
                ],
                "answer": "B"
            },
            {
                "question": "Energy mainly determines the size of the:",
                "options": [
                    "A) Battery bank",
                    "B) AC breaker only",
                    "C) Inverter fan",
                    "D) Generator enclosure"
                ],
                "answer": "A"
            },
            {
                "question": "If a house runs a 1 kW essential load for 5 hours, how much energy is needed?",
                "options": [
                    "A) 1 kWh",
                    "B) 5 kWh",
                    "C) 10 kWh",
                    "D) 0.5 kWh"
                ],
                "answer": "B"
            },
            {
                "question": "Why should battery systems not usually be sized around 100% discharge?",
                "options": [
                    "A) Because voltage becomes AC",
                    "B) Because it improves cable size",
                    "C) Because it can shorten battery life and leaves no room for real-world variation",
                    "D) Because batteries cannot store DC energy"
                ],
                "answer": "C"
            },
            {
                "question": "The basic formula for battery energy needed is:",
                "options": [
                    "A) Battery size = Voltage × Current",
                    "B) Battery size = Load (kW) × Time (hours)",
                    "C) Battery size = Frequency × Voltage",
                    "D) Battery size = Current ÷ Voltage"
                ],
                "answer": "B"
            },
            {
                "question": "What is the first step when calculating backup requirements?",
                "options": [
                    "A) Choose the inverter brand",
                    "B) Identify the essential loads",
                    "C) Set the battery to 100% DoD",
                    "D) Measure grid frequency"
                ],
                "answer": "B"
            },
            {
                "question": "If essential loads total 1 kW and the outage duration is 4 hours, the minimum energy needed is:",
                "options": [
                    "A) 1 kWh",
                    "B) 2 kWh",
                    "C) 4 kWh",
                    "D) 8 kWh"
                ],
                "answer": "C"
            },
            {
                "question": "In South Africa, typical household AC supply operates at:",
                "options": [
                    "A) 110 V / 60 Hz",
                    "B) 48 V DC",
                    "C) 230 V / 50 Hz",
                    "D) 400 V / 25 Hz"
                ],
                "answer": "C"
            },
            {
                "question": "Solar panels and batteries mainly operate in:",
                "options": [
                    "A) AC",
                    "B) DC",
                    "C) Mixed frequency AC",
                    "D) Pulsed AC only"
                ],
                "answer": "B"
            },
            {
                "question": "Household plugs and most appliances use:",
                "options": [
                    "A) DC only",
                    "B) AC",
                    "C) Battery voltage directly",
                    "D) PV string voltage"
                ],
                "answer": "B"
            },
            {
                "question": "The inverter is essential because it:",
                "options": [
                    "A) Stores solar energy directly in the DB board",
                    "B) Converts between AC and DC and manages power flow",
                    "C) Replaces the battery",
                    "D) Removes the need for grid protection"
                ],
                "answer": "B"
            },
            {
                "question": "A useful installer reminder is that most wiring faults happen on the:",
                "options": [
                    "A) AC side",
                    "B) DC side",
                    "C) Load side only",
                    "D) Neutral bar only"
                ],
                "answer": "B"
            },
            {
                "question": "Which of the following correctly matches the component with its function?",
                "options": [
                    "A) Battery bank — generates AC power",
                    "B) Inverter — stores energy chemically",
                    "C) PV array — generates DC electricity",
                    "D) Load — converts AC to DC"
                ],
                "answer": "C"
            },
            {
                "question": "The main job of the battery bank in a modern energy system is to:",
                "options": [
                    "A) Change frequency",
                    "B) Store energy for later use",
                    "C) Generate sunlight",
                    "D) Replace the inverter"
                ],
                "answer": "B"
            },
            {
                "question": "The inverter is best described as the system's:",
                "options": [
                    "A) Mounting frame",
                    "B) Control and conversion hub",
                    "C) Earthing rod",
                    "D) Fuel source"
                ],
                "answer": "B"
            },
            {
                "question": "Loads in an energy system are:",
                "options": [
                    "A) Devices and appliances that consume power",
                    "B) Only the battery chargers",
                    "C) Only grid-connected circuits",
                    "D) The inverter settings menu"
                ],
                "answer": "A"
            },
            {
                "question": "A backup system with no solar includes:",
                "options": [
                    "A) Solar + battery only",
                    "B) Inverter + battery only",
                    "C) Solar + grid only",
                    "D) Generator only"
                ],
                "answer": "B"
            },
            {
                "question": "A hybrid system typically includes:",
                "options": [
                    "A) Solar, battery and grid",
                    "B) Battery only",
                    "C) Solar only",
                    "D) Grid and generator only"
                ],
                "answer": "A"
            },
            {
                "question": "In a hybrid system, if PV output drops and the load still needs power, the next source is usually the:",
                "options": [
                    "A) Earth conductor",
                    "B) Battery",
                    "C) PV frame",
                    "D) AC isolator"
                ],
                "answer": "B"
            },
            {
                "question": "In a well-designed system, roughly how much of the generated energy is effectively used after typical losses?",
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
                "These are the terms you will use every day when sizing, wiring, testing, commissioning, and fault-finding energy systems.",
                "Understanding what each term means—and how they relate to one another is essential for designing safe, efficient, and reliable installations. ",
                "Before we look at more advanced concepts, let's first understand the five fundamental electrical principles that form the foundation of every battery and solar system.",
            ],
            "subsections": [
                {
                    "heading": "Voltage (V) — “Electrical Pressure”",
                    "paragraphs": [
                        "Voltage is the electrical pressure that drives electricity through a system.",
                    ],
                    "images": [
                        {
                            "src": "images/Voltage v electrical pressure.png",
                            "alt": "images/Voltage v electrical pressure.png",
                        },
                    ],
                   
                },
                {
                    "heading": "Current (A) — “How Much is Flowing”",
                    "paragraphs": [
                        "Current is the amount of electricity flowing through a conductor.",
                    ],
                    "images": [
                        {
                            "src": "images/Current A.png",
                            "alt": "images/Current A.png",
                        },
                    ],
                },
                {
                    "heading": "Resistance (Ω) — “Opposition to Flow”",
                    "paragraphs": [
                        "Resistance is anything that restricts or opposes the flow of energy."
                    ],
                    "images": [
                        {
                            "src": "images/resistance oms.png",
                            "alt": "images/resistance oms.png",
                        },
                    ],
                   
                },
                {
                    "heading": "Power (W / kW) — “How Fast Energy is Used”",
                    "paragraphs": [
                        "Power is how much electricity is being used or supplied at a specific moment.",
                    ],
                    "images": [
                        {
                            "src": "images/Power w,kw.png",
                            "alt": "images/Power w,kw.png",
                        },
                    ],
                    
                },
                {
                    "heading": "Energy (Wh / kWh) — “Power Over Time”",
                    "paragraphs": [
                        "Energy is the total amount of electricity used or stored over a period of time ."
                    ],
                    "images": [
                        {
                            "src": "images/energy wh,kwh.png",
                            "alt": "images/energy wh,kwh.png",
                        },
                    ],
                    "paragraphs_footer": [
                        "**Summary:**",
                        "",
                        "Understanding the relationship between voltage, current, resistance, power, and energy is essential for correctly sizing systems, selecting equipment, troubleshooting faults, and ensuring safe operation.",
                        "",
                        "<strong>Remember:</strong>",
                        "",
                        "**Power (kW) = what is happening right now**",
                        "",
                        "**Energy (kWh) = what happens over time**",
                        "",
                        "The summary below provides a quick-reference guide to the key electrical terms.",
                    ],
                    "subsections": [
                        {
                            "images": [
                                {
                                    "src": "images/Electrical Fundamental.png",
                                    "alt": "images/Electrical Fundamental.png",
                                },
                            ],
                        },
                    ],
                        
                    
                    
                },
            ],
        },
        {
            "title": "2.3 AC vs DC in Practice",
            "paragraphs": [
                "This section explains what AC and DC do in the system, why they behave differently, and what that means for wiring, protection and fault finding.",
                "In every system, you’re dealing with two completely different electrical environments:",
            ],
            "subsections": [

                {
                    "heading": "",
                    "paragraphs": [
                        "<strong>🔌 AC (Alternating Current):</strong>Household power and comes from Eskom or generator.",
                    ],
                },
                {
                    "heading": "",
                    "paragraphs": [
                        "<strong>🔋 DC (Direct Current):</strong>Comes from solar panels and batteries.",
                    ],
                },
                {
                    "heading": "🔋 DC (Direct Current) — “High Current, High Consequence”",
                    "paragraphs": [
                        "DC flows in one direction. Simple in theory… but in practice, it demands respect.",
                        "<u>In our systems, DC is used for:</u>",
                    ],
                    "bullets": [
                        "PV strings feeding the inverter",
                        "Battery charge and discharge",
                        "High-current battery cables",
                        "DC breakers and isolators",
                    ],
                    "subsections": [
                        {
                            "paragraph": ["<u>Here’s the important part, DC does not forgive mistakes.</u>"],
                            "bullets": [
                                "Polarity matters — reverse it and you can damage equipment instantly.",
                                "DC arcs don’t “let go” easily like AC does. If something sparks, it can keep sparking.",
                                "High battery currents mean heat becomes a real issue if cables or lugs are undersized.",
                                "Small mistakes (loose lug, wrong torque, bad crimp) show up quickly under load.",
                            ],
                            "subsections": [
                                {
                                    "heading": "",
                                    "paragraphs": [
                                        
                                    ],
                                
                                    
                                    "images": [
                                        {
                                            "src": "images/if a system randomly shuts down.png",
                                            "alt": "image of if a system randomly shuts down.png",
                                        },
                                    ],
                                },
                                {
                                    "heading": "🔌 AC (Alternating Current) — Where Compliance and Stability Matter",
                                    "paragraphs": [
                                        "AC changes direction 50 times per second (50 Hz). That constant switching is what allows it to travel long distances efficiently and power homes safely."
                                        "<br><u>On your installs, AC is used for:</u>",
                                    ],
                                    "bullets": [
                                        "Inverter output to essential loads",
                                        "Grid input",
                                        "Generator connection (where applicable)",
                                        
                                    ],

                                },
                                {
                                    "heading": "Key Principle",
                                    "paragraphs": [
                                        "For the same amount of power, increasing the system voltage reduces the amount of current flowing through the system.",
                                        "This is one of the main reasons why modern residential systems commonly use 48V battery architectures, while larger commercial and industrial systems increasingly use high-voltage (HV) battery systems."
                                    ]
                                },
                                {
                                    "heading": "Understanding the Different System Voltages",
                                    "paragraphs": [
                                        "Different voltage architectures are used for different applications. The choice of system voltage depends on factors such as the amount of power required, the size of the installation, installation cost, scalability, and overall system efficiency.",
                                        "As energy demands increase, systems generally move from lower voltages to higher voltages to reduce current, improve efficiency, and simplify installation."
                                    ],
                                    "paragraphs_after": [
                                         "<u>AC brings a different set of considerations:</u>",

                                    ],
                                    "bullets": [
                                            "The inverter must match the grid’s voltage and frequency before connecting.",
                                            "Neutral and earth must be handled correctly — this is where many nuisance trips start.",
                                            "Earth leakage placement matters.",
                                            "Protection must comply with SANS wiring standards."
                                    ],
                                    "images": [
                                            {
                                                "src": "images/if customers complain.png",
                                                "alt": "image of if customers complain.png",
                                            },
                                ],
                                },
                                {
                                    "heading": "The Inverter — The Electrical Traffic Controller",
                                    "paragraphs": [
                                        "The inverter is one of the most important components in any battery and solar system. While many people think its only job is to convert DC electricity into AC electricity, it actually performs a much more important role.",
                                        "",
                                        "The inverter sits between two completely different electrical environments:",
                                        "",
                                        "<br><strong>On the DC side, it receives electricity generated by the solar panels and stored in the batteries.</strong>",
                                        "<br><strong>On the AC side, it supplies electricity to the loads and interacts with the utility grid.</strong>",
                                    ],
                                    "paragraphs_after": [
                                           "The inverter continuously monitors the system and makes intelligent decisions about how energy should flow. It controls:" 
                                    ],
                                    "bullets_after":[
                                            "Where power is supplied from ",
                                            "When batteries should charge or discharge ",
                                            "When to prioritise solar, battery, or grid power ",
                                            "How energy is distributed to the loads ",
                                            "When to activate protection functions to keep the system safe"
                                    ],
                                    "paragraphs_footer":[
                                       "Think of the inverter as a traffic controller standing at a busy intersection. It constantly decides where electricity should come from, where it should go, and how to keep everything moving safely ",
                                       "and efficiently. Without the inverter managing these energy pathways, the different parts of the system would not be able to work together effectively."      
                                    ]

                                },
                                { "heading": "What This Looks Like in Real Life",
                                    "images": [
                                        {
                                            "src": "images/AC,DC ROLE.png",
                                            "alt": "image of AC,DC ROLE.png",
                                        },
                                    ], 

                                },
                              
                               
                               
                               
                            ],
                    },   
                    ],


                    
                },
                
              
                {
                    "heading": "What You Should Be Checking on Site",
                    "paragraphs": [
                        "When you’re troubleshooting, think in two halves.  If you can mentally separate AC and DC while",
                        "diagnosing a fault, your troubleshooting becomes much faster.", 
                    ],
                    "subsections": [
                        {
                            "heading": "DC is where you deal with heat, polarity, voltage drop and high current - DC Side Checks:",
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
                            "heading": "AC is where you deal with compliance, synchronisation, bonding and protection rules - AC Side Checks:",
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
                                {
                                    "src": "images/Think like an Installer.png",
                                    "alt": "images/Think like an Installer.png",
                                },
                            ],
                        },
                    ],
                },
            ],
        },
        {
            "title": "2.4 Understanding Battery System Voltage Architectures",
            "paragraphs": [
                "As energy systems become larger and more powerful, selecting the correct system voltage ",
                "becomes one of the most important design decisions an installer will make. The operating voltage ",
                "of a system influences its performance, efficiency, safety, and scalability. ",
                "Understanding why different voltage architectures are used will help you design better systems, select the correct equipment, and troubleshoot installations more effectively.",
                "System voltage directly affects:",
            ],
            "bullets": [
                    "current flow ",
                "cable size ",
                "heat generation ",
                "efficiency ",
                "inverter compatibility ",
                "battery configuration ",
                "system cost ",
                "installation complexity ",
            ],
            "paragraphs_after": [
                "Understanding why systems operate at different voltages is an important step towards thinking like a professional installer.",
                
            ],
            "subsections": [
                {
                    "heading": "What Does “System Voltage” Mean?",
                    "paragraphs": [
                        "System voltage refers to the normal operating voltage of the battery and inverter system. It ",
                        "determines how electricity is transferred between the batteries, inverter, and other system components",
                        "Common system voltages include:"
                    ],
                    "bullets": [
                        "12V ",
                        "24V ",
                        "48V ",
                        "High-voltage (HV) battery systems ",
                    ],
                    "paragraphs_after": [
                        "The inverter and battery must always operate at compatible voltages for the system to function safely and correctly.",
                        "Think of voltage as the electrical pressure that pushes electricity through a circuit.  The higher the voltage, the less current is required to deliver the same amount of power.",
                        "This principle is one of the key reasons why modern battery systems increasingly operate at higher voltages.",
                    ],
                },
                {
                    "heading": "Why Current Matters So Much in Battery Systems",
                    "paragraphs": [
                        "While voltage is important, current is often the biggest challenge in battery installations. Most ",
                        "installation problems are not caused by voltage itself, but by excessive current flowing through cables, connectors, and electrical equipment.",
                        "High current can result in:",
                    ],
                    "bullets": [
                        "heat generation ",
                        "voltage drop ",
                        "cable losses ",
                        "overheated terminals ",
                        "breaker stress ",
                        "increased fire risk "
                    ],

                    "paragraphs_after": [
                        "This is why installers must understand the relationship between:",
                    ],
                    "bullets_after": [
                        "Voltage",
                       
                        "Current",
                        "Power"
                    ],
                    "subsections": [
                        { "heading": "The Relationship Between Voltage, Current, and Power",
                            "paragraphs": [
                                "These three electrical concepts are directly connected. When designing a battery system, changing one of these values affects the others.",
                                "The relationship is shown by the following formula:Where:",
                            ],
                            "bullets": [
                                    "P = Power (Watts) ",
                                    "V = Voltage (Volts) ",
                                    "I = Current (Amps) "
                            ],
                            "paragraphs_after": [
                                "This formula tells us that power is equal to voltage multiplied by current.",
                                "However, for installers, the most important lesson is not the formula itself—it is understanding what happens when the system voltage changes."
                            ],

                        },
                        {
                            "heading": "Why Higher Voltage Means Lower Current",
                            "paragraphs": [
                                "Imagine two systems that both need to deliver exactly the same amount of power (5 kW). ",
                                "",
                                "The only difference is their operating voltage. ",
                                "The comparison below demonstrates how increasing the system voltage dramatically reduces the amount of current required to deliver the same power."
                            ],
                            "images": [
                                {
                                    "src": "images/why Higher voltage chages everything.png",
                                    "alt": "why Higher voltage chages everything.png"
                                },
                            ],
                        },
                        {
                            "heading": "",
                            "paragraphs": [
                                "What Does This Comparison Show?",
                                "",
                                "Both systems produce exactly the same amount of power—5 kW. ",
                                "",
                                "However, because the operating voltages are different, the amount of current flowing through the system is very different.",

                            ],
                            "bullets":[
                                "A <strong>48V system requires</strong> approximately <strong>104A</strong> of current to deliver 5 kW. ",
                                "A <strong>400V system requires</strong> only <strong>12.5A</strong> of current to deliver the same 5 kW. ",
                            ],
                            "paragraphs_after": [
                                "Although the power delivered is identical, the higher-voltage system requires significantly less current.",
                                "This reduction in current has several important advantages for installers:"
                            ],
                            "bullets_after":[
                                "Smaller cable sizes ",
                                "Less heat generation ",
                                "Reduced voltage drop ",
                                "Improved system efficiency ",
                                "Easier installation ",
                                "Better scalability "
                            ],
                            "paragraphs_footer":[
                                "This simple comparison illustrates one of the most important principles in battery and energy storage system design:"
                            ],
                        },
                        { "heading": "For the same amount of power, increasing the system voltage reduces the amount of current flowing through the system.",
                            "paragraphs":[
                                "This is one of the main reasons why modern residential systems commonly use 48V battery architectures, while larger commercial and industrial systems increasingly use high-voltage (HV) battery systems.",
                                "",
                                "",
                                "<strong>Understanding the Different System Voltages</strong>",
                                "Now that you understand why increasing the system voltage reduces current, let's look at how this principle is applied in real-world energy storage systems.",
                                "",
                                "",
                                "Different voltage architectures are used for different applications. The choice of system voltage depends on factors such as the amount of power required, the size of the installation, installation cost, scalability, and overall system efficiency.",
                                "",
                                "As energy demands increase, systems generally move from lower voltages to higher voltages to reduce current, improve efficiency, and simplify installation.",
                                "",
                                "The following sections introduce the four most common battery system voltage architectures and explain where each is typically used, together with their advantages and limitations."
                            ],

                        },
                        { "heading":"12V Systems – Small Backup Applications",
                         "paragraphs":[
                             "Although 12V systems are simple and cost-effective, they become less practical as power requirements increase because the current rises significantly. ",
                             "",
                             "This means larger cables, heavier protection devices, and greater installation challenges.",
                         ],
                         "images":[
                             {
                                 "src":"images/12v system-small backup.png",
                                 "alt": "image of a 12v system small backup",
                             },
                         ],

                        },
                        { "heading":"24V Systems – Medium Backup Systems",
                            "paragraphs":[
                                "Moving from 12V to 24V immediately reduces the current required for the same power output. This makes cable sizing more manageable and improves overall system efficiency.",
                                "",
                                "While 24V systems are still used in some residential and light commercial applications, most modern lithium systems have progressed to 48V architectures."
                            ],
                            "images":[
                                {
                                    "src":"images/24v system-medium backup systems.png",
                                    "alt":"image of a 24v system medium backup"
                                },
                            ],

                        },
                         { "heading":"48V Systems – The Modern Residential Standard",
                            "paragraphs":[
                                "Today, 48V has become the preferred voltage architecture for most residential and light commercial lithium battery systems.",
                                                        "",
                                "It provides an excellent balance between safety, efficiency, manageable current levels, installation practicality, and future expansion, making it the standard for most modern hybrid energy systems."
                        ],
                        "images":[
                            {
                            "src":"images/48v systems-the modern residential.png",
                            "alt":"image of a 48 system medium backup"
                            },
                        ],
                        
                    },
                     { "heading":"High Voltage (HV) Systems – Large Commercial Installations",
                        "paragraphs":[
                            "As energy requirements continue to increase, even 48V systems become impractical due to the very high currents required.",
                                                                            "",
                            "High Voltage (HV) battery systems solve this by operating at much higher voltages, dramatically reducing current and making large commercial and industrial energy storage systems more efficient and scalable.",
                                                    "",
                            "Because of the higher voltages involved, these systems require specialised equipment, additional protection measures, and experienced installers."
                        ],
                        "images":[
                                {
                                    "src":"images/High voltage (HV).png",
                                    "alt":"image of a High Voltage(HV) system medium backup"
                                },
                       ],
                                            
                    },
                    { "heading":"What This Means for Installers",
                        "paragraphs":[
                            "Understanding system voltage architecture is about much more than knowing the difference between 12V, 24V, 48V and high-voltage (HV) systems. ",
                            "",
                            "As an installer, the operating voltage influences almost every design and installation decision you make.",
                            "",
                            "",
                            "<br><u>System voltage directly affects:</u>"
                        ],
                        "bullets":[
                            "Cable sizing ",
                            "Breaker and fuse selection ",
                            "Inverter compatibility "
                            "Battery configuration ",
                            "Installation layout ",
                            "Voltage drop ",
                            "Heat generation ",
                            "System efficiency ",
                            "Future scalability "
                        ],
                        "paragraphs_after":[
                             "As energy demands have increased, the industry has steadily moved towards higher-voltage systems because they deliver the same amount of power with significantly lower current. This allows installers to design systems that are more efficient, easier to install, more scalable, and better suited to modern residential and commercial energy requirements.",
                             "",
                             "Understanding these principles will help you select the correct system architecture, design safer installations, and explain to customers why different applications require different voltage systems.",
                             "",
                             "Remember: Choosing the correct system voltage is not simply about selecting a battery—it is about designing an energy system that is safe, efficient, reliable, and capable of meeting the customer's current and future energy needs."
                        ],
                        "images":[
                            {
                                "src":"images/higher voltage does not mean.png",
                                "alt": "image of higher voltage does not mean more dangerous only"
                            },
                        ],
                    },
                    {"heading": "Series & Parallel Connections Explained",
                        "paragraphs":[
                            "One battery is often not enough to meet the voltage or energy requirements of a solar or backup system. As systems become larger, multiple batteries are connected together to create a battery bank that can deliver the required voltage, storage capacity, and runtime.",
                            "",
                            "Depending on the system requirements, batteries are connected in either series or parallel.",
                            "",
                            "The type of connection determines whether the system gains:"
                        ],
                        "bullets":[
                            "Higher voltage ",
                            "More energy storage ",
                            "Longer backup time ",
                            "Greater current capability "
                        ],
                        "paragraphs_after":[
                            "",
                            "Understanding the difference between these two connection methods is essential for correctly designing, installing, and expanding battery systems."
                        ],
                    },
                    { "heading":"Remember: There are only two ways to connect batteries together—series or parallel. Each changes the electrical characteristics of the battery bank in a different way.",
                       "paragraphs":[
                           "<br><strong>Series Connection – Voltage Adds,Capacity in Ah stays the same!</strong>,",
                            "<br><span style='color:red;'><strong> E.g. A 12V 100Ah battery bank made by connecting four 3.2V 100Ah cells in series.</strong></span>",
                           "<br>A series connection is used when the system requires a higher operating voltage.",
                           "<br>In a series connection, the batteries are connected:"
                       ],
                      
                       "bullets":[
                           "positive to negative ",
                           "like a chain "
                       ],
                       "paragraphs_after":[
                           "The voltage increases, but the storage capacity (Ah) stays the same.",
                           "Think of it like adding more pressure to a water pipe. The pressure increases, allowing the system to operate at a higher voltage, while the amount of stored energy in each battery (Ah) remains unchanged.",
                           "",
                           "Series connections are commonly used when:"
                       ],
                       "bullets_after":[
                           "the inverter requires a higher DC voltage (24V, 48V, etc.) ",
                           "lower current is required ",
                           "improved system efficiency is desired"
                       ],
                       "images":[
                           {
                               "src":"images/SERIES CONNECTION.png",
                               "alt": "image of the series Connection"
                           },
                       ],
                       "paragraphs_footer":[
                           "After studying the diagram, notice that every additional battery increases the system voltage, while the battery capacity remains the same.",
                           "This allows installers to build battery banks that meet the voltage requirements of different inverter systems without changing the individual battery capacity.",
                           "",
                           "<strong>Parallel Connection – Capacity Adds, Voltage Stays the Same</strong>",
                           "<br> <span style='color:red;'><strong>E.g. 2x48V 100Ah batteries in parallel = 48V 200Ah = 9.6KWH</strong></span>",
                           "A parallel connection is used when the system already operates at the correct voltage but requires additional energy storage and longer backup time.",
                           "In a parallel connection, all positives connect together and all negatives connect together.",
                           "The voltage stays the same, but the storage capacity increases.",
                           "Imagine two water tanks feeding the same house. The water pressure stays the same, but: .",


                          
                           
                           
                           "After reviewing the diagram, notice that adding batteries in parallel increases the total battery capacity (Ah) and available runtime, while the operating voltage remains unchanged.",
                           "",
                           
                           "Imagine you have the same equipment: a small inverter and two identical 12V batteries.",
                           
                           "Using the same two batteries, you can build two completely different battery banks.",   
                       ],
                       "bullets_footer":[
                         " there is now twice as much water available",
                         "the house can run longer before the tanks are empty"  
                       ],
                    },
                    { "heading":"",
                       "paragraphs":[
                            "Battery systems work in much the same way.",
                            "Parallel connections are commonly used when:",

                       ],
                       "bullets":[
                         "longer backup time is required",
                         "additional battery capacity is needed",
                         "the inverter already operates at the correct battery voltage", 
                       ],
                       "images":[
                           {
                              "src": "images/Parallel connection in battery.png",
                              "alt":  "image of parallel connection",

                           },
                       ],
                       "paragraphs_footer":[
                           "After reviewing the diagram, notice that adding batteries in parallel increases the total battery capacity (Ah) and available runtime, while the operating voltage remains unchanged.",
                           ""
                       ],
                        },

                        { "heading":"",

                       "images":[
                           {
                             "src":"images/TIP WHEN CONNECTING BATTERIES ALWAYS FOLLOW PRODUCT RULES.png",
                              "alt":"image of always follow product rules",   
                           },
                          
                       ],
                    },
                    { "heading":"Real-World Example – One Setup, Two Ways",
                      "paragraphs":[
                          "Understanding the theory behind series and parallel connections is important, but professional installers must also know when to use each configuration in practice.",

                          "Imagine you have the same equipment:",
                          ""
                      ],
                      "bullets":[
                          "A small inverter ",
                          "Two identical 12V batteries ",   
                      ],
                       "paragraphs_after":[
                           "Although the equipment is exactly the same, the way you connect the batteries completely changes how the system operates.",
                           "",
                           "The following example demonstrates how choosing either a series or parallel connection produces two very different battery systems, each designed for a different purpose."    
                       ],
                       "images":[
                           {
                             "src":"images/ONE SETUP,TWO WAYS.png",
                             "alt": "image of one setup, two ways",
                           },
                       ],
                       "paragraphs_footer":[
                           "Using the same two batteries, you can build two completely different battery banks.",
                           ""
                           "<strong>Option 1 – Series Connection</strong>",
                           "Connecting the batteries in <strong>series</strong> increases the battery bank voltage from <strong>12V to 24V</strong>, while the battery capacity (Ah) remains the same.",
                            "This configuration is used when: the inverter requires a higher DC voltage, lower current is preferred, or larger loads need to be supplied efficiently.",
                       ],
                       "bullets_footer":[
                            "The inverter requires a higher DC voltage",
                            "lower current is preferred",
                            "larger loads need to be supplied efficiently"
                       ],
                    },
                    { "heading":"Option 2 – Parallel Connection",
                      "paragraphs":[
                          "Connecting the batteries in <strong>parallel</strong> keeps the battery bank at <strong>12V</strong>, but doubles the available battery capacity.",
                         "This configuration is used when:"
                      ],
                      "bullets":[
                          "longer backup time is required",
                          "more stored energy is needed",
                          "the inverter already operates at the correct battery voltage"
                      ],

                    },
                    {"heading":"The Key Lesson",
                     "paragraphs":[
                         "The batteries themselves have not changed.",
                         "The inverter has not changed.",
                         "Only the way the batteries are connected has changed.",
                         "Yet the result is two completely different battery systems.",
                         "This is why installers must never connect batteries based on guesswork or convenience. The correct connection method is always determined by: "
                     ],
                     "bullets":[
                         "the inverter's voltage requirements",
                         "the customer's backup requirements",
                         "the required runtime",
                         "and the overall system design"
                     ],
                     "paragraphs_after":[
                        "<strong>Remember</strong>: A battery bank should always be designed to match both the inverter specifications and the customer's energy requirements—not simply by adding more batteries.",
                     ],

                    },
                    { "heading":"Comparing Series and Parallel Connections",
                      "paragraphs":[
                           "Although both methods connect multiple batteries together, they achieve completely different objectives.",
                           "A<br><strong>series connection</strong> increases the system voltage while maintaining the same battery capacity.",
                           "A <br><strong>parallel connection</strong> increases the battery capacity and available runtime while maintaining the same system voltage.",
                            "Understanding this difference is one of the most important skills for designing battery banks correctly."
                      ],
                      "images":[
                          {
                             "src":"images/series vs parallel.png",
                             "alt":"image of a series vs parallel connections" 
                          },
                      ],
                     

                    },
                    { "heading":"",
                         "paragraphs_after":[
                        "<br>Study the comparison carefully and note the key differences between the two connection methods. ",
                        "As an installer, this information will help you determine the correct battery configuration based on the inverter requirements and the customer's backup needs."   
                    ],
                    "images":[
                        {
                        "src":"images/series and parallel are not better or wor.png",
                        "alt": "image of series and parallel are not better or worse"   
                        },
                    ],
                    },

                    ],
                },
            ],
        },
        {
            "title": "2.5 Electrical Components",
            "paragraphs": [
                "Every electrical system needs to:",
                
                
               
            ],
            "bullets":[
                "move power,",
                "control power",
                "protect equipment",
                "protect people",
                "manage voltage and current",
                "switch things on and off",
                "and communicate between devices"

            ],
            "paragraphs_after":[
                "Electrical components make all this possible.",
                "<br>Without the correct components, electricity would simply flow uncontrolled from the batteries to ",
                "the equipment-which can lead to:"
            ],
            "bullets_after":[
                "overheating",
                "damaged equipment",
                "poor performance",
                "fires",
                "system failures",
                "and serious safety risks"
            ],
            "paragraphs_footer": [
                "A good battery or solar system is not only about the batteries. The cables, lugs, isolators, fuses, breakers, and connections are just as important.",
                "<br>Think of the system like the plumbing in a building:",
            ],
            "bullets_footer": [
                "The battery is the water tank",
                "The cables are the pipes",
                "The isolators and breakers are the valves",
                "The fuses are the emergency safety devices",
                "The lugs and terminations are the joints connecting everything together"
            ],
            "paragraphs_extra": [
                "If any one of these parts is poor quality or installed incorrectly, the whole system can fail.",
                            
            ],
            "subsections":[
                { "heading":"Understanding the Key Electrical Components",
                  "paragraphs": [
                                  
                     "Every electrical component in a battery and solar system has a specific purpose. Some components carry electricity, others control it, while others protect the system and the people using it.",
                     "As an installer, it is essential to understand not only what each component is, but also why it is used, how it works, and the role it plays in ensuring a safe, reliable, and efficient installation.",
                     "<br>The following diagrams introduce the most common electrical components found in battery and solar systems. As you work through each one, pay particular attention to:"
                ],
                "bullets": [
                    "The purpose of the component",
                    "Where it is used in the system",
                    "Why it is important",
                    "What could happen if it is incorrectly selected or installed"
                ],
                "paragraphs_after": [
                        "Although these components may appear simple on their own, together they form the foundation of every safe and reliable energy storage system.",
                               
                ],
                "images":[
                    {
                        "src":"images/Cables carry current.png",
                        "alt":"images of current carry cables"
                    },
                    {
                        "src":"images/Lugs and terminations.png",
                        "alt":"image of lugs and terminations"
                    },
                    {
                        "src":"images/isolators.png",
                        "alt":"image of an isolators"
                    },
                    {
                        "src":"images/isolators.png",
                        "alt":"image of a fuse"
                    },
                    {
                        "src":"images/circuit breaker.png",
                        "alt":"image of a circuit breaker"
                    },
                ],

            },
            { "heading": "A battery system is only as strong as its weakest connection.",
                "paragraphs":[
                    "Even the best battery can fail if:"
                ],
                 "bullets": [
                    "cables are undersized",
                    "lugs are loose",
                    "breakers are incorrect",
                    "fuses are missing",
                    "or isolators are not installed properly."
               ],

                "paragraphs_after": [
                     "Good electrical design is about:",   
                ],
                "bullets_after":[
                    "safety",
                    "reliability",
                    "efficiency, ",
                    "and long equipment life."
                ],
                "images":[
                    {
                        "src":"images/simple summary.module 2.5.png",
                        "alt":"image of a simple summary",
                    },
                ],
               
            },
            ],
            
            
            

          
        },
        {
            "title": "2.6 Earthing & Bonding — The Safety Backbone",
            "paragraphs": [
                "Earthing and bonding are two of the most important safety principles in any battery and solar installation. Although they perform different functions, they work together to protect people, equipment, and property by reducing the risk of electric shock, equipment damage, and fire.",
                "Correct earthing and bonding help protect:",
                
               
            ],
            "bullets":[
                "people",
                " equipment",
                "buildings",
                " batteries",
                "and inverters.",
            ],
            "paragraphs_after":[
                "Without proper earthing and bonding:"
            ],
            "bullets_after":[
                "electric shocks can occur",
                "equipment can become damaged",
                "systems can behave unpredictably",
                "lightning damage can become worse",
                "faults may not trip correctly",
                "and fire risks increase."
            ],
            "paragraphs_footer": [
                "A simple way to understand the difference is:"
                
            ],
            "bullets_footer":[
                "<strong>Earthing</strong> gives dangerous electricity a safe path to the ground",
                "<strong>Bonding</strong> keeps metal parts at the same electrical level so they cannot become dangerous"
            ],
            "paragraphs_extra":[
               "Both are essential for a safe and compliant electrical installation. One does not replace the other—they work together to protect the entire system.",
            ],
            "subsections":[
                {"heading":"Understanding Earthing & Bonding",
                 "paragraphs":[
                     "Although earthing and bonding are closely related, they perform different safety functions within an electrical installation. Understanding the difference is essential for every installer",
                     "<br>The following diagrams explain what earthing is, what bonding is, why each is important, and how they work together to create a safer battery and solar system. ",
                     "<br>As you review each diagram, pay attention to:"
                 ],
                 "bullets":[
                     "the purpose of earthing and bonding, ",
                     "how they protect people and equipment, ",
                     "where they are used within the system, ",
                     "and what can happen if they are omitted or installed incorrectly. "
                 ],
                 "images":[
                     {
                         "src": "images/earthing.png",
                         "alt":"image of Earthing"
                     },
                     {
                         "src":"images/Bonding.png",
                         "alt":"image of Bonding"
                     },
                 ],
                 "paragraphs_footer":[
                     "Although earthing and bonding perform different functions, they are most effective when used together.",
                     
                 ],
                 "bullets_footer":[
                     "<strong>Earthing</strong>provides a safe path for fault current to flow into the ground.",
                     "<strong>Bonding</strong> ensures exposed metal parts remain at the same electrical potential. "
                 ],
                 "paragraphs_extra":[
                     "Together they help protective devices operate correctly, minimise electric shock hazards, reduce the risk of fire, and improve the overall safety of the installation. ",
                     "<br><strong>Remember:</strong> A properly designed battery or solar system is not only efficient—it is also safe. Correct earthing and bonding are fundamental requirements for every professional installation."
                 ],



                },
            ]
        },
        {
            "title": "2.7 Electrical Safety — Non-Negotiable Rules",
            "paragraphs": [
                "Electrical safety is non-negotiable because electricity is invisible, extremely powerful, and can cause serious injury, death, fires, or catastrophic equipment damage in seconds if handled incorrectly.",
                "<br>Unlike many other hazards, you often do not get a warning before something goes wrong. A loose connection, incorrect polarity, missing fuse, poor earthing, or accidental contact with live conductors can instantly create dangerous heat, electric shock, arc flash, or system failure.",
                "<br>In battery and solar systems especially, large amounts of stored energy are always present, even when grid power is off, which means safe isolation, proper PPE, correct tools, testing procedures, and compliant installation practices are absolutely essential.",
                "Good electrical safety is not about slowing the job down, it is about ensuring that everyone goes home safely, equipment remains protected, and systems operate reliably for years to come."
            ],
            "images":[
                {
                    "src":"images/electrical safety.png",
                    "alt":"image of electrical safety"
                },
            ],
        },
        {
            "title": "2.8 Real-World Installer Scenarios (What Can Go Wrong + How to Fix It)",
            "paragraphs": [
                "Up to this point, you have learned the theory behind electrical components, cable sizing, battery connections, and system protection. While understanding the theory is essential, professional installers must also recognise what happens when these principles are not applied correctly.",
                "Many system faults are not caused by defective equipment; they are caused by poor installation practices.",
                "Something as simple as using the wrong cable size, making a poor crimp, or leaving a loose terminal can lead to overheating, nuisance trips, damaged equipment, expensive call-backs, and even serious safety hazards.",
                "The following examples are based on real installation scenarios that installers encounter every day. Each example demonstrates:",
                
                
                
                
            ],
            "bullets":[
                "what went wrong,",
                "why it happened,",
                "what problems it caused,",
                "and how the issue can be prevented or corrected"
            ],
            "paragraphs_after":[
               "As you work through each example, think beyond simply fixing the fault. Ask yourself <strong>why it occurred in the first place</strong> and what could have been done during installation to prevent it.",
               "<br>Remember:",
               "<strong>Most installation problems are preventable.</strong> Good installers do not just fix faults; they install systems correctly the first time.",

            ],
            "images":[
                {
                    "src":"images/incorrect cable size.png",
                    "alt":"image of incorrect cable size.png"
                },
                {
                    "src":"images/swopped-reverse polarity.png",
                    "alt":"image of swopped-reverse polarity.png"
                },
                {
                    "src":"images/poor crimping lug.png",
                    "alt":"image of poor crimping lug.png"
                },
                {
                    "src":"images/no dc isolator installed.png",
                    "alt":"image of no dc isolator installed.png"
                },
                {                                                
                    "src":"images/unequal parallel cables.png",
                    "alt":"image of unequal parallel cables.png"
                }, 
            ],
            "paragraphs_footer":[
                  "Every fault shown in this section has one thing in common: it could have been prevented during installation.",
            ],
            "subsections":[

                { "heading":"It could have been prevented during installation.",
                  "paragraphs":[
                      "Professional installers understand that system reliability is not determined only by the quality of the batteries or inverter—it is determined by the quality of the installation",
                      "<br>A correctly sized cable, a properly crimped lug, a securely tightened connection, and careful attention to detail may seem like small tasks, but together they make the difference between a system that operates reliably for years and one that generates repeated faults and customer complaints.",
                      "<br><strong>Remember:</strong> the best fault is the one that never happens because the installation was done correctly the first time."
                  ],

                },
                
            ],
        },
        {
            "title": "Wrapping Up Module 2",
            "images":[
                {
                  "src":"images/wrapping up module 2.png",
                  "alt":"image of wrapping up module 2"  
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
            "question": "Voltage (V) is best described as:",
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
            "question": "Current (A) refers to:",
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
            "question": "Resistance (Ω) causes:",
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
            "question": "If voltage increases for the same power demand, current will:",
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
            "question": "Why do higher voltage systems improve efficiency?",
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
                "question": "Power (kW) refers to:",
                "options": [
                    "A) Total stored electricity",
                    "B) The rate at which energy is used",
                    "C) The resistance of the system",
                    "D) Battery lifespan"
                ],
                "answer": "B"
            },
            {
                "question": "The formula for power is:",
                "options": [
                  "A) Power = Current ÷ Voltage",
                  "B) Power = Voltage × Current",
                  "C) Power = Energy × Time",
                  "D) Power = Resistance × Current"
                ],
                "answer": "B"
            },
            {
                "question": "Energy (kWh) refers to?",
                "options": [
                    "A) Instantaneous load",
                    "B) Voltage level",
                    "C) Power used over time",
                    "D) Cable size"
                ],
                "answer": "C"
            },
            {
                "question": "If a system runs at 2 kW for 3 hours, how much energy is used?",
                "options": [
                    "A) 2 kWh",
                    "B) 3 kWh",
                    "C) 5 kWh",
                    "D) 6 kWh"
                ],
                "answer": "D"
            },
            {
                "question": "DC (Direct Current) flows:",
                "options": [
                    "A) In both directions",
                    "B) In one direction only",
                    "C) Only through the grid",
                    "D) Only through AC breakers"
                ],
                "answer": "B"
            },
            {
                "question": "One key risk of DC systems is that:",
                "options": [
                  "A) Voltage is always low",
                  "B) DC arcs can sustain and not easily extinguish",
                  "C) Current cannot flow",
                  "D) Polarity does not matter"
                ],
                "answer": "B"
            },
            {
                "question": "AC (Alternating Current) in South Africa operates at:",
                "options": [
                 "A) 110 V / 60 Hz",
                 "B) 48 V DC",
                 "C) 230 V / 50 Hz",
                 "D) 400 V / 25 Hz"
                ],
                "answer": "C"
            },
            {
                "question": "In South Africa, typical household AC supply operates at:",
                "options": [
                 "A) DC side",
                 "B) AC side",
                 "C) PV frame only",
                 "D) Battery enclosure only"
                ],
                "answer": "B"
            },
            {
                "question": "The inverter’s role is best described as:",
                "options": [
                "A) Only converting DC to AC",
                "B) Only storing energy",
                "C) Managing power flow between DC and AC systems",
                "D) Only protecting cables"


                ],
                "answer": "C"
            },
            {
                "question": "In a series connection, what happens?",
                "options": [
                  "A) Voltage stays the same, capacity increases",
                  "B) Voltage increases, capacity stays the same",
                  "C) Voltage decreases, capacity increases",
                  "D) Everything stays the same"
                ],
                "answer": "B"
            },
            {
                "question": "In a parallel connection, what happens?",
                "options": [
                   "A) Voltage increases",
                   "B) Capacity decreases",
                   "C) Voltage stays the same, capacity increases",
                   "D) Power is removed"
                ],
                "answer": "C"
            },
            {
                "question": "Two 48 V batteries connected in series will result in:",
                "options": [
                   "A) 48 V",
                   "B) 96 V",
                   "C) 24 V",
                   "D) 100 Ah"
                ],
                "answer": "B"
            },
            {
                "question": "Why must manufacturers’ rules be followed when connecting batteries?",
                "options": [
                    "A) To improve aesthetics",
                    "B) To avoid warranty issues and system damage",
                    "C) To reduce voltage",
                    "D) To increase resistance"
                ],
                "answer": "B"
            },
            {
                "question": "If a cable is undersized for the current, what is most likely to happen?",
                "options": [
                  "A) Voltage increases",
                  "B) Cable cools down",
                  "C) Heat builds up and voltage drops",
                  "D) Current disappears"
                ],
                "answer": "C"
            },
            {
                "question": "Proper crimping and torque are important because they:",
                "options": [
                    "A) Reduce voltage",
                    "B) Improve cable colour",
                    "C) Prevent resistance and overheating",
                    "D) Increase inverter size"
                ],
                "answer": "C"
            },
            {
                "question": "A DC breaker or fuse is mainly used to:",
                "options": [
                    "A) Increase voltage",
                    "B) Protect cables and equipment",
                    "C) Reduce battery capacity",
                    "D) Control AC frequency"
                ],
                "answer": "B"
            },
            {
                "question": "Where should battery protection devices ideally be installed?",
                "options": [
                   "A) At the DB board only",
                   "B) Close to the battery",
                   "C) On the roof",
                   "D) Inside the inverter only"
                ],
                "answer": "B"
            },
            {
                "question": "Earthing is used to:",
                "options": [
                    "A) Increase system voltage",
                    "B) Store energy",
                    "C) Provide safety and control fault conditions",
                    "D) Reduce inverter size"
                ],
                "answer": "C"
            },
            {
                "question": "One of the most important safety steps before working on a system is to:",
                "options": [
                    "A) Increase load",
                    "B) Turn on all breakers",
                    "C) Isolate and test for dead",
                    "D) Disconnect earth"
                ],
                "answer": "C"
            },
            {
                "question": "In a parallel battery system, unequal cable lengths can cause:",
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
            "bullets": [ 
                        "Explain what a lithium-ion battery is and how it works internally",
                        "Understand how energy is stored and released at the cell level",
                        "Correctly interpret voltage, capacity, power, and energy",
                        "Apply C-rate in real system design",
                        "Understand how SOC, DoD, cycle life, and temperature affect performance",
                        "Identify battery-related problems early",
                        "Make better decisions when selecting and installing batteries",


                        
                        

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
                        "src": "images/COMPARING DEFFERENT TYPES OF BATTERIES.png",
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
                "In practical terms:",
            ],
            "bullets": [
                "Solar panels generate DC energy",
                "The battery stores that DC energy",
                "The inverter controls when the battery charges or discharges",
                "The loads use battery power when solar is not available or when backup is needed",
            ],
            "paragraphs_after": [
                "",
                "A simple way to think about it is this:",
                "The battery is what allows the system to “save power for later.”",
                "Without storage, solar can only help while the sun is shining.",
                "With storage, the system becomes far more flexible, reliable and useful.",
            ],
             "images": [
                    {
                        "src": "images/BATTERY IS NOT THERE JUST TO ADD BACKUP.png",
                        "alt": "images of battery is not there just to add backup",
                    },
                    
            ],    
        },
        {
            "title": "3.4 What Is a Lithium-Ion Battery",
            "paragraphs": [
                "A lithium-ion battery is not just a box that holds power.  It is a controlled energy storage system made up of several parts working together.",
                "",
                "",
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
                        "",
                        "",
                        "",
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
                        "",
                        "",
                        "",
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
                "",
                "",
                "",
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
                     "paragraphs_footer": [
                         "",
                         "",
                         "",
                       "That is what makes lithium systems powerful — but also why settings, communication and installation quality matter so much.",
            ],
                },
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
                    "subsections":[
                        {
                            "heading":"REVOV Cell Configuration",
                              "paragraphs": [
                                 "Every lithium battery starts with individual battery cells. These cells are the basic building blocks ",
                                 "of the battery and determine its voltage, capacity, and overall performance.",
                                 "",
                                 "Each LiFePO₄ (Lithium Iron Phosphate) cell provides a nominal voltage of approximately 3.2 V. To ",
                                 "produce the voltage and energy required by modern inverter systems, REVOV combines multiple cells in carefully engineered configurations.",
                                  "Cells are connected:"
                                            
                            ],
                             "bullets": [
                                "In series to increase voltage",
                                "In parallel to increase the battery capacity and available energy",
                           ],
                           "paragraphs_after": [
                                           
                                "This modular design enables REVOV to manufacture battery systems suitable for a wide range of residential, commercial, and industrial energy storage applications.",
                                
                            ],
                            "paragraphs_before":[
                                    "Examples of REVOV Cell Configuration:",
                            ],
                            "bullets_before": [
                                "<strong>R100 Battery</strong> – 51.2 nominal V, 100 Ah, 5.12 kWh, 16-cell configuration ",     
                                "<strong>R200 Battery</strong> – 51.2 nominal V, 200 Ah, 10.2 kWh, 16-cell configuration. ",    
                                "<strong>E100 Battery</strong> – 51.2 nominal V, 100 Ah, 5.12 kWh, 16-cell configuration.",
                                "<strong>E300 Battery</strong> – 51.2 nominal V, 300 Ah, 15.36 kWh,16-cell configuration."

                             ],
                            "images": [
                                {
                                    "src":"images/Revov cell Configuration.png",
                                    "alt": "image of revov cell configuration.",
                           
                                },
                            ],

                        },
                        {"heading": "Why LiFePO₄?",
                          "paragraphs": [
                            "Not all lithium battery chemistries are the same.",
                            "While several lithium technologies are available, REVOV uses Lithium Iron Phosphate (LiFePO₄) because it offers an excellent combination of safety, reliability, long service life, and performance.",
                            "Compared with traditional lead-acid batteries and other lithium chemistries, LiFePO₄ provides significant advantages for residential, commercial, and industrial energy storage applications.",
                        ],
                        "images": [
                                {
                                  "src": "images/FEATURE,EXPLANATION, BENEFITS....2.png",
                                  "alt": "Comparison of LiFePO₄ and other battery technologies",
                               },
                        ],
                            "paragraphs_after":[
                                "This diagram compares LiFePO₄ with other common battery technologies and highlights why it has become the preferred choice for modern backup and hybrid energy systems.",
                            ],
                             
                        },
                        {  "heading": "Key Advantages of LiFePO₄",
                            "paragraphs":[
                               "LiFePO₄ batteries offer:"
                        ],
                        "bullets": [
                            "Excellent thermal and chemical stability",
                            "Improved safety and reduced fire risk",
                            "Long cycle life and extended service life",
                            "High charging and discharging efficiency",
                            "Consistent performance throughout the battery's life",
                            "Low maintenance requirements",
                            "Reliable operation under frequent cycling",
                        ],
                        "paragraphs_after": [
                            "These characteristics make LiFePO₄ the preferred battery chemistry for demanding backup, hybrid, and energy storage applications.",
                            "Remember: The performance of a battery is determined not only by its capacity, but also by the quality of its cell configuration and the chemistry used. REVOV combines high-quality LiFePO₄ cells with a modular design to deliver battery systems that are safe, reliable, scalable, and built for long-term performance.",
                        ],
                        "notes": [],
                },

             ],
        },
        {
            "title": "3.7 Battery Voltage, Capacity, Power and Energy",
            "paragraphs": [
                "When installers read a battery datasheet, four terms come up again and again:",
            ],
            "bullets": [
                "Voltage",
                "Capacity",
                "Energy",
                "Power",
            ],
            "paragraphs_after": [
                "These values are related, but they do not mean the same thing. And if they are confused, batteries are often sized incorrectly.",
            ],
            "subsections": [
                {
                    "heading": "Battery Voltage (V)",
                    "paragraphs": [
                        "Voltage is the electrical pressure of the battery.  Most REVOV low-voltage batteries operate around 48 V / 51.2 V nominal, which makes them suitable for common residential and commercial inverter systems.",
                        "Why this matters:",
                        " Higher voltage allows the battery to deliver the same power at lower current.",
                        "Lower current means:",
                    ],
                    "bullets": [
                        "Less heat",
                        "Smaller cable requirements",
                        "Lower losses",
                        "Better efficiency",
                    ],
                    "paragraphs_after": [
                        "This links directly to Module 2, where you learned that current is one of the main reasons cables overheat and systems trip under load.",
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
                        "This is the most useful number for system design because it tells you how much backup time or stored energy is actually available."      
                        
                    ],    
                    
                },
                {  "heading": "Formula: ",
                    "paragraphs": [
                        "Energy (kWh) = Voltage (V) × Capacity (Ah) ÷ 1000"
                    ],
                    "images" : [
                        {
                            "src":"images/formula Energy(kwh) =.png",
                            "alt" : "image of formula Energy(kwh).",
                        },
                                        ],
                    "paragraphs_footer": [
                        "This links directly back to Module 1: Energy determines battery sizing and backup duration.",
                    ],
                },
                {
                    "heading": "Battery Power (kW)",
                    "paragraphs": [
                        "Power tells you how fast the battery can deliver that stored energy.  This is not the same as capacity.",
                        "A battery may store a lot of energy, but that does not automatically mean it can supply a very large load all at once.",
                        
                    ],
                    "images": [
                        {
                            "src": "images/a battery may have enough stored energy.png",
                            "alt": "image of a battery may have enough stored energy.",
                        },
                    ],
                    "paragraphs_footer": [
                        "That limit is controlled by the battery’s C-rate, which we cover next."
                    ],
                   
                },
                { "heading":"",
                 "paragraphs": [],
                  "images" : [
                        {
                            "src":"images/so in simple terms energy(kwh) tells.png",
                            "alt" : "image explaining energy (kWh) in simple terms.",
                        },
                    ],

                },
                {
                    "heading": "Understanding Battery Specifications",
                    "paragraphs": [
                        "When selecting or comparing batteries, installers will encounter four key specifications: voltage, capacity, energy, and power.",
                        "Although these terms are often confused, each describes a different aspect of battery performance.",
                        "Understanding what they mean, and how they work together is essential for choosing the correct battery, sizing a system accurately, and explaining battery performance to customers.",
                        "The summary below provides a practical comparison of these four characteristics and highlights why each one is important in real-world battery and solar installations.",
                    ],
                    "images": [
                        {
                            "src": "images/summary below.png"
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
            "image": {
                "src":"images/if battery stores 5kwh and is rated at 1C.png",
                "alt" : "image of if battery stores 5kwh and is rated at 1C.",
            },

            "paragraphs_footer": [
                "So even if two batteries have the same storage capacity, they may not support the same load.",
                "That is a very important installer point. A battery must not only be large enough — it must also be fast enough.",
            ],
            "subsections": [
                {
                    "heading": "Why C-Rate Matters",
                    "paragraphs": [
                        "If battery demand exceeds its C-rate:",
                    ],
                    "bullets": [
                        "The BMS may limit output",
                        "The battery may trip on overcurrent",
                        "SOC may become unstable or inaccurate",
                        "Battery life may reduce",
                        "Warranty may be affected",
                    ],
                    "images": [
                        {
                            "src":"images/Alaways check both energy capcity and power capabilty.png",
                            "alt": "image of capacity check and warnings",
                        }
                    ],
                },
            ],
        },
        {
            "title": "3.9 Key Battery Concepts Installers Must Know",
            "paragraphs": [
                "Now that you understand the main battery ratings—such as voltage, capacity, energy, and power the next step is to understand the key concepts that determine how a battery performs throughout its life.",
                "",
                "",
                "",
                "These concepts explain how the battery is used, how it is monitored, how efficiently it stores and delivers energy, and how long it is likely to last. They are fundamental to correctly designing, installing, commissioning, and troubleshooting modern lithium battery systems.",
                "",
                "As an installer, you will encounter these terms regularly in battery specifications, inverter settings, BMS data, monitoring software, and technical support discussions. Understanding what they ",
                "mean will help you optimise system performance, maximise battery lifespan, and explain battery behaviour confidently to customers.",
                "The following sections introduce five key battery concepts that every installer should understand:",

            ],
            "bullets": [
                "Cycle – How battery lifespan is measured. ",
                "State of Charge (SOC) – The current charge level of the battery as a percentage of its total capacity.",
                "Depth of Discharge (DOD) – The percentage of the battery that has been discharged relative to its total capacity.",
                "Efficiency – How effectively the battery stores and delivers energy.",
                "Battery Management System (BMS) – The system that monitors and manages the battery's performance and safety.",

            ],
            "paragraphs_after": [
                "As you work through each concept, think about how it affects the customer's daily experience, including backup time, battery lifespan, system reliability, and overall performance",
                "Together, these concepts explain why two batteries with the same capacity may perform very differently depending on how they are installed, configured, and operated."
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
                    "paragraphs_footer": [
                        "Although each of these concepts measures a different aspect of battery performance, they are all closely connected.",
                        "The Battery Management System (BMS) continuously monitors the battery's State of Charge (SOC), manages the Depth of Discharge (DoD), tracks charge and discharge cycles, and helps maintain safe and efficient operation throughout the battery's life.",
                        "The summary below provides a quick reference to these key concepts, what they mean, and why they matter in everyday battery and solar installations",
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
                 "",
                 "",
                 "",
                 
            ],
            "subsections": [
                { "heading": "If temperatures rise too high:",
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
            "title": "3.12 Applying Battery Concepts in Real-World Installations",
            "paragraphs": [
                "Understanding battery concepts such as power, capacity, State of Charge (SOC), Depth of Discharge (DoD), efficiency, and the Battery Management System (BMS) is only the first step.",
                "The real challenge is recognising how these concepts affect the performance of a battery system once it has been installed.",
                "Many customer complaints are not caused by faulty batteries. More often, they result from incorrect battery selection, poor system design, incorrect settings, installation errors, or unrealistic customer expectations.",
                "The following examples are based on common situations encountered by installers in the field. Each scenario demonstrates:",

            ],
             "bullets": [
                 "what happened, ",
                 "why it happened, ",
                 "what problems it caused, ",
                 "and how the issue can be prevented or corrected. ",
             ],
             "paragraphs_before": [
                "As you work through each example, think beyond fixing the immediate fault. Ask yourself which battery concept explains the behaviour and what could have been done during system design or installation to prevent the problem.",
                "Remember: A battery that appears to be faulty is often operating exactly as it was designed to. The key is understanding how battery characteristics, system design, inverter settings, and installation quality work together to determine system performance.",
                ""
            ],
            "subsections": [
               { "heading":"Example 1 - Wrong Battery for the Load",
                    "paragraphs": [
                        "This example demonstrates why battery selection involves more than choosing the correct storage capacity (kWh). A battery must also be capable of delivering the required output power (kW) and discharge current (C-rate). Even if a battery stores enough energy, it may not be able to safely supply the power demanded by the connected loads, resulting in BMS protection, inverter alarms, or system shutdowns.",
                    ],
                    "images": [
                                    {
                                        "src":"images/a wrong battery for the load.png",
                                        "alt": "image for what happens if using wrong battery for the load",
                                    },
                ],
               }, 
               {
                    "heading":"Example 2 - State of Charge (SOC) Drops Too Quickly",
                    "paragraphs": [
                        "This example shows that rapid SOC reduction does not automatically indicate a faulty battery. High loads, incorrect inverter settings, poor cable connections, incorrect battery configuration, or inaccurate SOC calibration can all cause the battery percentage to fall faster than expected.",
                    ],
                    "images": [
                        {
                            "src":"images/SOC DROPS TOO FAST.png",
                            "alt": "image for what causes soc to drop fast",
                        }
                    ]
               },
               { "heading":"Example 3 - Battery Never Reaches 100%",
                    "paragraphs": [
                        "This example explains why a battery that never reaches a full charge may gradually develop inaccurate SOC readings and reduced backup performance. In many cases, the cause is not the battery itself, but incorrect charging settings, insufficient PV generation, excessive daytime loads, communication issues, or system configuration.",
                    ],
                    "images": [
                        {
                            "src":"images/BATTERY NEVER REACHES 100%.png",
                            "alt": "image for what makes battery not reach 100%",
                        }
                    ]
               },
               {
                    "heading":"Key Installer Lesson",
                    "paragraphs": [
                        "Every example in this section demonstrates the same principle:",
                    ],
               },
               {
                 "heading": "A battery can only perform as well as the system around it.",
                 "paragraphs": [
                     "Battery performance depends not only on the battery itself, but also on:",
                 ],
                  "bullets": [
                        "Selecting the correct battery for the application",
                        "Matching the battery to the inverter and expected loads",
                        "Applying the correct settings",
                        "Ensuring reliable communication between devices",
                        "Maintaining a high-quality installation",
                ],
                "paragraphs_after": [
                        "Professional installers do not immediately assume the battery is faulty. Instead, they understand how battery concepts such as SOC, DoD, C-rate, efficiency, and the BMS influence system behaviour and use this knowledge to diagnose the root cause of a problem.",
                        "Remember: The best installers do not just replace components - they understand why the system is behaving the way it is and resolve the underlying cause. A well-designed, correctly configured, and professionally installed system delivers reliable performance, maximises battery lifespan, and results in satisfied customers.",
                ],
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
                
            ],
           
        },
        {
            "title": " Wrapping Up Module 3",
            "images": [
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
            "question": "What is the main job of a battery in an energy system?",
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
            "question": "Why do REVOV systems use LiFePO4 battery chemistry?",
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
            "question": "What does a Battery Management System (BMS) do?",
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
            "question": "What is the primary reason for using a lithium battery instead of a lead-acid battery in modern systems?",
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
            "question": "What does the term 'C-rate' describe?",
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
            "question": "What happens to battery life if you discharge it more deeply (higher DoD)?",
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
            "question": "Which of the following is a common reason to avoid charging batteries in very low temperatures?",
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
            "question": "What is SOC?",
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
            "question": "What is DoD?",
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
            "question": "Which value tells you how much stored energy a battery can deliver over time?",
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
            "question": "What term describes the amount of electrical pressure in a battery?",
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
            "question": "What does the BMS do when it detects an unsafe battery temperature?",
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
            "question": "Which of these is not a component usually found inside a battery enclosure?",
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
            "question": "Which best describes why REVOV selects LiFePO4 chemistry?",
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
            "question": "Why is internal resistance important?",
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
            "question": "What is one effect of using a battery at too high a discharge current?",
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
            "question": "Which of the following is true about series connections?",
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
            "question": "Which of the following is true about parallel connections?",
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
            "question": "Which factor is most likely to reduce battery cycle life?",
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
            "question": "What is a safe approach for charging batteries in hot conditions?",
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
            "question": "What does a battery do when there is no solar and the load still needs power?",
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
            "question": "A backup system with no solar includes:",
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
            "question": "A hybrid system typically includes:",
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
            "question": "In a hybrid system, if PV output drops and the load still needs power, the next source is usually the:",
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
            "question": "In a well-designed system, roughly how much of the generated energy is effectively used after typical losses?",
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
                                "src":"images/if the bms is unhappy.png",
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
               
            ],
            "subsections":[
              {
                 "heading": "Think of the BMS as a combination of:",
                 "bullets": [
                     "A doctor (health monitoring)",
                    "A security guard (blocking danger)",
                    "A manager (controlling limits)",
                    "A translator (communicating with the inverter)",
                ],  
              },  
            ]
           
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
                                
                                "src":"images/what the bms monitors.png",
                                "alt": "image of what the bms monitor.png.",
                                },
                                
                                
                                {
                                "src":"images/the bms sees problems before you do.png",
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
                    "paragraphs_footer": [
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
                    "src": "images/the bms will always choose.png",
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
                    "paragraphs_before": [
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
                    "paragraphs_before": [
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

            
            "subsections": [
                {"heading": "The BMS Uses Multiple Factors",
                 "paragraphs": [
                                 
                    "The BMS constantly monitors and calculates:",
                 ],
                  "bullets": [
                    "voltage ",
                    "current flow ",
                    "charging and discharge activity ",
                    "battery temperature ",
                    "cell behaviour ",
                    "historical energy usage ",
                ],
                  "paragraphs_footer": [
                      "It then combines all this information to estimate the remaining battery capacity."
                  ],
                },
                {
                    "heading": "Coulomb Counting – Tracking Energy In and Out",
                    "paragraphs": [
                        "One of the main methods used is called coulomb counting.",
                    ],
                    "paragraphs_after":[
                        "This means the BMS continuously measures:"
                    ],
                    "bullets_after": [
                        "how much energy goes into the battery during charging ",
                        "how much energy leaves during discharge ",
                    ],
                    "paragraphs_before": [
                        "Think of it like tracking money in a bank account:"
                    ],
                    "bullets_before":[
                        "deposits increase the balance ",
                        "withdrawals reduce the balance "
                    ],
                    "paragraphs_under":[
                        "The BMS does something very similar with battery energy."
                    ],
                    "images": [
                        {
                            "src": "images/imagine a 100ah.png",
                            "alt": "image of imagine a 100ah battery.png",
                        },
                    ],
                },
                {
                    "heading": "Why Voltage Alone Cannot Determine SOC",
                    "paragraphs": [
                        "Many people assume battery voltage directly indicates how full the battery is, but lithium batteries behave differently from older battery technologies.",
                        "A lithium battery can maintain a very similar voltage across a large portion of its charge range. ",
                        "This means:"
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
                    "paragraphs_before": [
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
                    "heading": "",
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
                "Understanding what the Battery Management System (BMS) does in theory is only the first step. ",
                "Professional installers must also understand how the BMS behaves in real installations and why it responds the way it does.",
                "",
                "Many installers assume that a warning, alarm or shutdown means the battery has failed. In reality, the opposite is often true. ",
                "",
                "Most BMS warnings and protective actions indicate that the BMS is doing exactly what it was designed to do, protecting the battery from unsafe operating conditions before permanent damage occurs.",
                "",
                "The following examples are based on common situations encountered in the field. Each example ",
                "explains:"
                
                
            ],
            "bullets": [
                "the operating scenario ",
                "how the BMS detects the problem ",
                "why the protection was triggered ",
                "the most likely causes ",
                "what to inspect during fault-finding ",
                "how to resolve the issue correctly. "
            ],
            "paragraphs_before": [
                'As you work through these examples, think like a professional installer. Rather than asking, "Why did the battery shut down?", ask "What condition did the BMS detect that required it to protect the battery?" ',
                "",
                "",
                "Understanding this difference will help you diagnose faults more accurately, reduce unnecessary battery replacements, and build safer, more reliable energy storage systems.",
                ""
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
                
            ],
        },
        {
            "title": "Wrapping Up Module 4",
            "images": [
                {
                    "src": "images/wrapping up module 4.png",
                    "alt": "image of wrapping up module 4.png", 
                },
            ],
            
        },

    ],
}

MODULE_4_ASSESSMENT = {
    "title": "Module 4 Assessment",
    "questions": [
        {
            "question": "The BMS is best described as:",
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
            "question": "Without a BMS, a lithium battery would be:",
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
            "question": "The BMS is responsible for:",
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
            "question": "Which of the following does the BMS monitor?",
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
            "question": "If one cell voltage becomes too high or too low, the BMS will:",
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
            "question": "Why is temperature monitoring important?",
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
            "question": "Internal resistance in a battery can indicate:",
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
            "question": "The BMS protects the battery from:",
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
            "question": "If inverter settings push voltage too high during charging, the BMS will trigger:",
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
            "question": "If the battery is drained too far, the BMS will trigger:",
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
            "question": "The BMS will always prioritise:",
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
            "question": "Cell balancing ensures that:",
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
            "question": "Poor balancing can lead to:",
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
            "question": "When does balancing usually occur?",
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
            "question": "Why is reaching 100% charge important occasionally?",
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
            "question": "Communication between battery and inverter typically uses:",
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
            "question": "If communication is incorrect or missing, one likely issue is:",
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
            "question": "The most accurate method the BMS uses to calculate SOC is:",
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
            "question": "Voltage-based SOC estimation is mainly used:",
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
            "question": "A battery shutting down under load is often:",
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
            "question": "If a battery never reaches 100% SOC over long periods, a likely issue is:",
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
            "question": "High temperatures around the battery can cause:",
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
            "question": "Before resetting a BMS fault, you should:",
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
            "question": "Mixing different battery brands in one system can cause:",
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
            "question": "Exceeding the battery’s C-rate can result in:",
            "options": [
                "A) Higher capacity",
                "B) BMS limiting or shutting down output",
                "C) Increased lifespan",
                "D) Lower current",
            ],
            "answer": "B",
            "explanation": "Exceeding C-rate often causes the BMS to limit or stop output to protect the battery.",
        },
    ]
}

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
            "paragraphs_before": [
                "Poor system design can lead to:"

            ],
            "bullets_before": [
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
                "",
                "The first and most important step in designing any battery or solar system is understanding exactly what the system needs to power. This process is called a load assessment.",
                "A load assessment helps determine:",
            ],
            "bullets": [
                "how much power the system must supply",
                "how long the system must run",
                "which appliances are critical",
                "how large the inverter and battery bank need to be"
            ],
            "paragraphs_before": [
                "Without a proper load assessment, the system may end up:"
            ],
            "bullets_before": [
                "too small and unable to support the required loads ",
                "or unnecessarily oversized and far more expensive than needed"
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
                            "paragraphs_before": [
                                "But during startup: ",
                                
                            ],
                            "bullets_before": [
                                "it may briefly draw 600W or more."
                            ],
                            "paragraphs_footer": [
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
                            "paragraphs_before": [
                                "Excluding unnecessary loads helps:",
                            ],
                            "bullets_before": [
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
                    "paragraphs_before": [
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
            "subsections": [
                 {
                   "heading": "Understanding the Difference Between kW and kWh",
                   "paragraphs": [
                       "This is one of the most important concepts in battery system design.",
                   ],
                 },
                 {
                   "heading": "KW(Kilowatts) =Power",
                   "paragraphs": [
                       "This refers to:",
                   ],
                   "bullets": [
                       "how much power is being used at a specific moment "     
                       
                   ],
                   "paragraphs_after": [
                       "Think of it like:"
                   ],
                   "bullets_after": [
                       "the speed of a vehicle ",
                       "or how hard the engine is working"
                   ],
                 },
                  {
                   "heading": "kWh (Kilowatt-hours) = Energy",
                   "paragraphs": [
                       "This refers to:",
                   ],
                   "bullets": [
                       "how much energy is used over time "     
                       
                   ],
                   "paragraphs_before": [
                       "Think of it like:"
                   ],
                   "bullets_before": [
                       
                       "how much fuel the vehicle uses during the trip"
                   ],
                   "images": [ 
                        {
                            "src": "images/energy usage explained.png",
                            "alt": "",
                        },
                   ],

                 },
                 {
                  "heading": "Simple Formula",
                    "paragraphs": [
                        "Backup energy requirement is calculated as:"
                    ],
                 },
                 {
                  "heading": "Power (kW) × Time (Hours) = Energy Required (kWh)",
                    "paragraphs": [
                        ""
                    ],
                    "images": [
                        {
                            "src": "images/load,runtime,enrgy used.png",
                            "alt": ""
                        },
                         {
                            "src": "images/example system sizing.png",
                            "alt": ""
                        },
                    ],
                 },
                 {
                    "heading": "Why Backup Time Requirements Are So Important",
                    "paragraphs": [
                        "",
                        "Two customers may have exactly the same loads but completely different battery requirements depending on how long they want backup power.",
                        "Customer A – Required backup time of 2 hours for a 1kW load",
                        "Customer B – Required backup time of 10 hours for a 1kW load",
                        "",
                        "Even though the load is identical:"
                    ],
                    "bullets": [
                        "Customer B needs a much larger battery bank "
                    ],
                    "images": [
                        {
                            "src":"images/this is why backup time directly.png",
                            "alt":""
                        },
                    ],
                 },
             ],
            
        },
        {
            "title": "5.5 Step 3 — Select the Correct Battery Size",
            "paragraphs": [
                "Once the load assessment and backup time requirements have been calculated, the next step is selecting the correct battery size.",
                "This is one of the most important parts of system design because the battery determines how much energy the system can store and how long the loads can operate during a power outage.",
                "The battery must be correctly sized to:"
            ],
            "bullets": [
                "support the required loads",
                "provide the required backup time",
                "operate safely within its limits",
                "allow for future expansion where necessary",
                "avoid excessive battery stress"
            ],
            "subsections": [
                {
                    
                    "paragraphs":[
                        "If the battery is too small:",
                    ],
                    "bullets": [
                        "runtime will be shorter than expected",
                        "the battery may discharge too quickly",
                        "the system may shut down prematurely",
                        "battery lifespan may reduce due to excessive cycling"
                    ]
                },
                {
                    
                    "paragraphs":[
                        "If the battery is too large:"
                    ],
                    "bullets": [
                        "system cost increases unnecessarily",
                        "charging times may become longer",
                        "the customer may pay for unused capacity"
                    ]
                },
                {
                    "paragraphs": [
                        "The goal is therefore to select a battery size that is practical, efficient, reliable, and suitable for the customer’s actual needs."
                    ]
                },
                {
                    "heading": "Battery Capacity is Measured in kWh",
                    "paragraphs": [
                        "Battery size is usually measured in:"
                    ],
                    "bullets": [
                        "kilowatt-hours (kWh)"
                    ],
                    "paragraphs_after": [
                        "This represents:"
                    ],
                    "bullets_after": [
                        "how much energy the battery can store"
                    ],
                    "paragraphs_before": [
                        "The larger the kWh rating:"
                    ],
                    "bullets_before": [
                        "the longer the system can run the loads"
                    ],
                    "images" : [
                        {
                            "src" : "images/load assesment requred runtime.png",
                            "alt" : "the image of load assesment",
                        },
                    ],
                },
                {
                    "heading": "Why Additional Capacity is Important",
                    "paragraphs": [
                        "Real-world systems must account for:"
                    ],
                    "bullets": [
                        "inverter losses",
                        "reserve capacity",
                        "surge loads",
                        "battery aging",
                        "temperature effects",
                        "future expansion",
                        "depth of discharge limits"
                    ],
                    "paragraphs_after": [
                        "This means installers usually recommend a slightly larger battery than the minimum calculated requirement."
                    ]
                },
                {
                    "heading": "",
                    "paragraphs": [
                        "Although the calculation shows:"
                    ],
                    "bullets": [
                        "approximately 2kWh required"
                    ],
                    "paragraphs_after": [
                        "An installer may recommend:"
                    ],
                    "bullets_after": [
                        "a 5kWh battery"
                    ],
                    "paragraphs_footer": [
                        "Why?"
                    ],
                    "paragraphs_extra": [
                        "Because the larger battery:"
                    ],
                    "bullets_extra": [
                        "reduces battery stress",
                        "improves runtime stability",
                        "allows for future load growth",
                        "provides reserve capacity",
                        "improves battery lifespan"
                    ]
                },
                {
                    "heading": "Matching Battery Size to Inverter Size",
                    "paragraphs": [
                        "The battery must also be suitable for the inverter’s power requirements.",
                        "A very large inverter connected to a very small battery may:"
                    ],
                    "bullets": [
                        "overload the battery",
                        "exceed discharge limits",
                        "trigger BMS protection events"
                    ],
                    "paragraphs_after": [
                        "The battery and inverter must therefore be correctly matched."
                    ]
                }
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
                    "heading": "",
                    "subsections": [
                        {
                            "paragraphs":[
                                "If the inverter is too small:"
                            ],
                            "bullets": [
                                "it may overload",
                                "trip during operation",
                                "struggle with startup loads",
                                "shut down unexpectedly",
                            ],
                        },
                        {
                             "paragraphs":[
                                "If the inverter is too large:"
                             ],
                            "bullets": [
                                "system cost increases unnecessarily",
                                "efficiency at low loads may reduce",
                                "the battery may not be able to support the inverter properly",
                            ],
                              "paragraphs_footer": [
                                  "The goal is to select an inverter that matches the real power requirements of the system while allowing reasonable operating headroom.",
                    ],
                        },
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
                    "paragraphs_before": [
                        "Unlike battery sizing, which is mainly based on runtime and energy storage (kWh), inverter sizing is mainly based on instantaneous power demand.",
                    ],
                    "images" : [
                        {
                            "src" : "images/example inverter size.png",
                            "alt" : "image of inveter sizing",
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
                                
                            ],
                        },   
                        {
                            "paragraphs":[
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
                            "paragraphs_before": [
                                "But during startup:",
                                
                            ],
                            "bullets_before": [
                                "it may briefly draw 600W or more", 
                            ],
                            "paragraphs_under": [
                                "This is called a surge load or startup current.",
                                "The inverter must be capable of handling these short bursts of power without tripping or shutting down.",
                                ],
                             "images" : [
                                 {
                                   "src" : "images/inverter may be rated.png",
                                   "alt" : "image of inverter may be rated......",
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
                    "heading": "",
                    "subsections": [
                        { 
                            "paragraphs":[
                                "If the solar array is too small:",
                            ],
                            "bullets": [
                                "batteries may not fully recharge",
                                "backup time may reduce",
                                "the system may rely heavily on grid or generator support",
                                "battery lifespan may shorten due to chronic undercharging",
                            ],
                        },
                        {
                             "paragraphs":[
                                  "If the solar array is too large:",
                             ],
                            "bullets": [
                                "equipment limits may be exceeded",
                                "unnecessary costs may increase",
                                "the inverter or charge controller may limit excess production",
                            ],
                        },
                        {  "paragraphs": [
                        "The goal is therefore to design a solar array that provides sufficient energy generation while remaining within the safe operating limits of the system.",
                        ],

                        }
                       
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
                   
                },
                {
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
                            "alt" : "image of solar sizing examples ",
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
                            "alt" : "image:ALTHOUGH THE CALCULATIONS ",
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
                    "paragraphs_before": [
                        "This is why solar design calculations are extremely important.",
                    ],
                    "images": [
                        {
                            "src" : "images/EXAMPLE SOLAR SIZING.png",
                            "alt" : "image of solar sizing examples",
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
            "subsections": [
                {
                    "heading": "What is Voltage Drop?",
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
                {
                    "paragraphs": [
                        "The longer the cable or the higher the current:",
                    ],
                    "bullets": [
                        "the greater the voltage drop becomes."
                    ],
                },
                {
                    "heading": "Effects of Excessive Voltage Drop",
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
                {
                    "heading": "Special Considerations for Battery Systems",
                    "paragraphs": [
                        "In battery systems, this becomes especially important because battery systems often operate at:",
                        "These conditions make proper cable sizing critical for reliable operation.",
                    ],
                    "bullets": [
                        "high current",
                        "relatively low voltage",
                    ],
                    "images": [
                        {
                            "src": "images/EVEN SMALL VOLTAGE LOSSES.png",
                            "alt": "Cable Sizing Illustration",
                        },
                        {
                            "src": "images/EXAMPLE VOLTAGE DROP.png",
                            "alt": "Cable Sizing Illustration",
                        },
                    ],
                },
            ],
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
            "subsections": [
            {
                "heading": "Batteries Perform Best Within Safe Operating Conditions", 
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
            {
                "heading": "Avoid Constant High Stress",
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
                {
                "heading": "Depth of Discharge (DoD) Affects Lifespan", 
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
                {
                    "heading": "Temperature Has a Major Impact",
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
                {
                    "heading": "Proper Charging is Critical",
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
                {
                "heading": "Correct Solar Sizing Improves Battery Health", 
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
                {
                    "heading": "Cable Quality and Voltage Stability Matter",
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
                {
                    "heading": "Communication Improves Long-Term Performance",
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
                    "paragraphs_before": [
                        "Poor communication can reduce overall system performance and battery lifespan.",
                    ],
                    "images": [
                        {
                            "src": "images/EXAMPLE PERFORMANCE AND LONG BATTERY LIFE.png",
                            "alt": "Communication Compatibility Diagram",
                        },
                    ],
                },
               
            ],
        },
        {
            "title": "5.11 Real-World System Design Examples",
            "paragraphs": [
                "Understanding the theory behind system design is important, but seeing how these principles are applied in real-world situations makes the concepts far easier to understand.",
                "Every battery energy storage system is designed around the customer's specific needs. While the design process remains the same, the final system can vary significantly depending on factors ",
                "such as:",

            ],
            "bullets":[
               "the type of application ",
               "the loads that must be powered ",
               "required backup time ",
               "available solar generation ",
               "budget ",
               "installation space ",
               "future expansion requirements. "
            ],
            "paragraphs_after":[
                 "A professional installer does not simply select a battery and inverter. They analyse the customer's energy requirements, calculate the expected loads, determine the required runtime, and then ",
                 "select components that work together safely, efficiently and reliably.",
                 "The following examples demonstrate how the same design principles are applied across a variety of residential, commercial and industrial applications. As you review each example, pay attention ",
                 "to:"
                
            ],
            "bullets_after":[
                "the design goals ",
                "the critical loads being supported ",
                "how the battery, inverter and solar array have been sized ",
                "the expected system performance ",
                "the practical design considerations ",
                "how the system could be expanded in the future. "
            ],
            "paragraphs_before":[
                "These examples are intended to demonstrate the design process rather than provide fixed system ",
                "templates. Every installation is unique, but the engineering principles remain the same."
            ],
            "subsections":[
                {"heading": "Example 1 – Small Home Backup System",
                 "paragraphs":[
                    "This example illustrates a basic residential backup system designed to keep essential household appliances operating during power outages. The emphasis is on simplicity, reliability and cost-",
                    "effective backup for everyday loads.",
                    "As you study this design, notice how the battery capacity, inverter size and solar array are matched to relatively small continuous loads and longer runtime requirements.",  
                 ],
                  "images": [
                                 {
                                     "src": "images/SMALL HOUSE BACKUP.png",
                                     "alt": "Real-World System Design Example",
                                 },
                  ],

                },
                { "heading":"Example 2 – Medium Home Backup System",
                  "paragraphs":[
                      "This example demonstrates a larger residential installation supporting additional household appliances and higher daily energy demand. Compared with the previous example, larger battery ",
                      "storage and inverter capacity are required while maintaining efficient system operation.",
                      "",
                      "",
                      "Observe how increasing the number of appliances affects every major design decision."
                      
                  ],
                  "images": [
                      {
                        "src": "images/MEDIUM HOME BACKUP.png",
                        "alt": "Real-World System Design Example",
                    },
                  ],

                },
                { "heading": "Example 3 – Large Home Backup System",
                  "paragraphs":[
                      "This example shows a whole-home backup solution designed for larger properties with higher energy consumption. Multiple high-power appliances and larger surge loads require careful sizing ",
                      "of the inverter, battery bank and solar array.",
                      "",
                      "Notice how the design balances high performance with future scalability and long-term system reliability."
                  ],
                  "images":[
                      {
                        "src": "images/LARGE HOME BACKUP.png",
                        "alt": "Real-World System Design Example",
                    }, 
                  ],

                },
                { "heading":"Example 4 – Office Backup System",
                  "paragraphs":[
                      "Business continuity is the primary objective of this design. Critical office equipment such as computers, servers, networking equipment, lighting and communication systems are prioritised to ",
                      "minimise downtime during power outages.",
                      "",
                      "Consider how commercial installations often focus on protecting productivity rather than powering every electrical load."
                  ],
                  "images":[
                      {
                        "src": "images/OFFICE BACKUP.png",
                        "alt": "Real-World System Design Example",
                     },
                  ],
                    
                },
                { "heading" :"Example 5 – Restaurant Backup System",
                  "paragraphs":[
                      "Restaurants place greater demands on backup systems because refrigeration, food preparation equipment, lighting and point-of-sale systems are business-critical. Larger continuous and surge ",
                      "loads require careful component selection and appropriate battery capacity.",
                      "",
                      "",
                      "Observe how maintaining operations and protecting refrigerated stock become key design priorities."

                  ],
                  "images":[
                     {
                        "src": "images/RESTURANT BACKUP.png",
                        "alt": "Real-World System Design Example",
                    },  
                  ],

                },
                { "heading":"Example 6 – Commercial BESS Solution",
                  "paragraphs":[
                      "This example introduces a commercial Battery Energy Storage System (BESS) designed for industrial and utility-scale applications. Unlike residential backup systems, these installations may ",
                      "provide peak shaving, demand management, renewable energy integration, grid support and energy arbitrage in addition to backup power.",
                      "",
                      "",
                      "Notice how the scale of the system changes dramatically, but the same fundamental design principles still apply—correct sizing, system protection, efficiency, reliability and future scalability.",
                      ""
                  ],
                  "images":[
                      {
                            "src": "images/COMMERCIAL BESS.png",
                            "alt": "Real-World System Design Example",
                    },
                  ],
                  

                },
                { "heading":"Key Design Lessons",
                  "paragraphs":[
                        "Although these systems vary greatly in size and application, they all follow the same design process:",
                 ],
                 "paragraphs_after":[
                     "1.Understand the customer's operational requirements. ",
                     "2.Identify the critical loads. ",
                     "3.Calculate continuous and surge power demand. ",
                     "4.Determine the required backup duration. ",
                     "5.Size the battery bank to provide sufficient usable energy. ",
                     "6.Select an appropriately rated inverter. ",
                     "7.Size the solar array to recharge the batteries and support ongoing energy needs. ",
                     "8.Design for safety, efficiency, reliability and future expansion. ",
                 ],
                
                 

                },

                {"heading":"",
                  "paragraphs":[
                        "",
                        "",
                        "",
                        "",
                        "",
                        "The difference between a small residential backup system and a large commercial BESS is not the design methodology—it is the scale of the application. Professional installers apply the same ",
                        "engineering principles to every installation, regardless of size.",
                                      "",
                                      "",
                                      "",
                       "Remember: Successful system design is not about installing the biggest battery or the largest inverter. It is about designing a balanced system where every component is correctly matched to ",
                       "the customer's energy requirements, operational goals and future needs."
                                      ],

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

            ],

        },
        { "title": "Wrapping Up Module 5",
           "images":[
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
            "question": "What should determine the design of an energy system before equipment is selected?",
            "options": [
                "A) The equipment currently in stock",
                "B) The customer’s actual load and energy requirements",
                "C) The largest available inverter",
                "D) The number of solar panels that fit on the roof",
            ],
            "answer": "B",
            "explanation": "The system should be designed around the customer's actual load and energy needs before equipment is selected.",
        },
        {
            "question": "Why is a proper load assessment important?",
            "options": [
                "A) It determines the colour of the equipment",
                "B) It identifies how much power and energy the system must supply",
                "C) It removes the need to calculate battery capacity",
                "D) It determines the battery chemistry",
            ],
            "answer": "B",
            "explanation": "A proper load assessment establishes the power and energy the system must supply reliably.",
        },
        {
            "question": "Which two load characteristics are particularly important when sizing an inverter?",
            "options": [
                "A) Daily energy and battery SOC",
                "B) Continuous demand and surge demand",
                "C) Battery voltage and temperature",
                "D) PV voltage and cable length",
            ],
            "answer": "B",
            "explanation": "Continuous demand and surge demand are the critical inverter sizing factors for steady and startup loads.",
        },
        {
            "question": "A customer has essential loads totalling 2 kW that must operate for 4 hours. What is the basic energy requirement before allowances for losses and usable capacity?",
            "options": [
                "A) 2 kWh",
                "B) 4 kWh",
                "C) 6 kWh",
                "D) 8 kWh",
            ],
            "answer": "D",
            "explanation": "Energy = power × time = 2 kW × 4 h = 8 kWh before losses and usable-capacity allowances.",
        },
        {
            "question": "Why should the calculated energy requirement not simply be treated as the final battery size?",
            "options": [
                "A) Real systems must allow for usable capacity, losses and operating margin",
                "B) Batteries always deliver twice their rated capacity",
                "C) Inverter size determines battery capacity",
                "D) Solar panels eliminate battery losses",
            ],
            "answer": "A",
            "explanation": "Final battery sizing must include usable capacity, conversion losses and reserve margin for reliable operation.",
        },
        {
            "question": "A customer wants longer backup time without increasing the essential load. Which part of the system will generally need more capacity?",
            "options": [
                "A) Battery bank",
                "B) Inverter",
                "C) AC isolator",
                "D) DB board",
            ],
            "answer": "A",
            "explanation": "Longer backup time requires greater battery capacity while the essential load remains the same.",
        },
        {
            "question": "What primarily determines the required inverter power rating?",
            "options": [
                "A) Required backup duration",
                "B) Maximum load that may need to be supplied at the same time",
                "C) Number of battery modules",
                "D) Daily PV production only",
            ],
            "answer": "B",
            "explanation": "The inverter should be sized to the maximum simultaneous load it may need to support.",
        },
        {
            "question": "Why must surge loads be considered when selecting an inverter?",
            "options": [
                "A) Some equipment requires significantly more power when starting",
                "B) Surge loads increase battery voltage permanently",
                "C) They determine PV panel orientation",
                "D) They reduce cable resistance",
            ],
            "answer": "A",
            "explanation": "Motors, compressors and pumps often draw a much higher inrush current when starting up.",
        },
        {
            "question": "A system has sufficient battery energy but trips whenever several appliances start together. What should be checked first from a design perspective?",
            "options": [
                "A) Whether the inverter can handle the peak and surge demand",
                "B) Whether the battery enclosure is large enough",
                "C) Whether the solar panels are clean",
                "D) Whether the monitoring platform is online",
            ],
            "answer": "A",
            "explanation": "If a system trips during simultaneous appliance startup, the inverter's peak and surge capability should be reviewed first.",
        },
        {
            "question": "Why are essential and non-essential loads separated during system design?",
            "options": [
                "A) To increase battery voltage",
                "B) To ensure available backup capacity is used for priority loads",
                "C) To increase PV generation",
                "D) To eliminate the need for protection devices",
            ],
            "answer": "B",
            "explanation": "Separating loads ensures backup capacity is reserved for the most important circuits during outages.",
        },
        {
            "question": "Which of the following would generally be the best candidate for a non-essential load during an outage?",
            "options": [
                "A) Alarm system",
                "B) WiFi router",
                "C) Geyser",
                "D) Essential lighting",
            ],
            "answer": "C",
            "explanation": "A geyser is usually a suitable non-essential load because it has a high power draw and is not critical during an outage.",
        },
        {
            "question": "What is the main role of the solar array in a hybrid system?",
            "options": [
                "A) To replace the inverter",
                "B) To generate energy that can support loads and recharge batteries",
                "C) To control battery temperature",
                "D) To provide BMS communication",
            ],
            "answer": "B",
            "explanation": "The solar array generates energy that can support dwelling loads and recharge the battery bank.",
        },
        {
            "question": "What can happen if the PV array is too small for the customer’s energy requirements?",
            "options": [
                "A) The batteries may not recharge adequately between discharge periods",
                "B) Battery voltage automatically increases",
                "C) The inverter becomes larger",
                "D) The battery gains additional capacity",
            ],
            "answer": "A",
            "explanation": "An undersized PV array can prevent the battery from recharging properly between discharge periods.",
        },
        {
            "question": "When sizing the PV array, which combination should be considered?",
            "options": [
                "A) Energy consumption, available solar production and battery recharge requirements",
                "B) Only the battery brand",
                "C) Only the inverter output rating",
                "D) Only the number of available roof panels",
            ],
            "answer": "A",
            "explanation": "PV sizing should account for consumption, solar production and required battery recharge.",
        },
        {
            "question": "Why must the battery and inverter be correctly matched?",
            "options": [
                "A) Their voltage, power capability and operating requirements must be compatible",
                "B) They must always have the same physical dimensions",
                "C) They must always be manufactured by the same company",
                "D) The inverter determines battery chemistry",
            ],
            "answer": "A",
            "explanation": "The battery and inverter must be compatible in voltage, power capability and operating characteristics.",
        },
        {
            "question": "A battery bank has enough kWh for the required runtime but cannot safely supply the required load. What design factor may have been overlooked?",
            "options": [
                "A) Battery power/C-rate capability",
                "B) Solar panel colour",
                "C) AC frequency only",
                "D) Battery enclosure size",
            ],
            "answer": "A",
            "explanation": "A battery may have sufficient energy but still be unable to provide the required power if its C-rate capability is inadequate.",
        },
        {
            "question": "Why is cable sizing part of system design rather than only an installation consideration?",
            "options": [
                "A) Cable size affects voltage drop, heat, losses and safe current carrying capacity",
                "B) Larger cables increase battery capacity",
                "C) Cable size determines solar irradiance",
                "D) Cable size changes inverter firmware",
            ],
            "answer": "A",
            "explanation": "Cable sizing is a design issue because it directly affects efficiency, safety and system performance.",
        },
        {
            "question": "Excessive voltage drop in a battery circuit can result in:",
            "options": [
                "A) Improved system efficiency",
                "B) Reduced losses",
                "C) Poor performance, heat and possible system trips",
                "D) Increased battery capacity",
            ],
            "answer": "C",
            "explanation": "Voltage drop can cause poor performance, excessive heat and nuisance trips or shutdowns.",
        },
        {
            "question": "When planning a system for possible future expansion, what should the designer consider?",
            "options": [
                "A) Whether the inverter, battery architecture and installation can accommodate additional capacity",
                "B) Only the current customer load",
                "C) Only available wall space",
                "D) Whether the battery can be discharged to 0%",
            ],
            "answer": "A",
            "explanation": "Future expansion should be planned around inverter, battery and installation headroom.",
        },
        {
            "question": "Why should system components not be sized independently from one another?",
            "options": [
                "A) The battery, inverter, PV, loads and protection must operate as a balanced system",
                "B) Every component must have the same power rating",
                "C) The battery automatically controls all other equipment",
                "D) Component compatibility only matters in off-grid systems",
            ],
            "answer": "A",
            "explanation": "The whole energy system must be balanced so each component supports the others safely and effectively.",
        },
        {
            "question": "A customer increases the number of essential loads after the original system was designed. What should happen?",
            "options": [
                "A) Nothing, because the battery capacity remains unchanged",
                "B) The system requirements should be reassessed",
                "C) Only the solar panels need to be changed",
                "D) The BMS should be disabled",
            ],
            "answer": "B",
            "explanation": "Any increase in required essential loads means the system design must be re-evaluated.",
        },
        {
            "question": "Why should battery lifespan be considered during system design?",
            "options": [
                "A) Operating batteries repeatedly at inappropriate limits can shorten their service life",
                "B) Battery lifespan only depends on its enclosure",
                "C) Larger inverters always extend battery life",
                "D) Battery lifespan is unrelated to system design",
            ],
            "answer": "A",
            "explanation": "Battery life is strongly affected by operating conditions, depth of cycling and design margins.",
        },
        {
            "question": "What is the main difference between designing a residential system and a large commercial/BESS solution according to the module?",
            "options": [
                "A) Commercial systems do not require load assessment",
                "B) The fundamental design methodology remains similar, but the scale and complexity increase",
                "C) Residential systems do not require protection",
                "D) Commercial systems do not use batteries",
            ],
            "answer": "B",
            "explanation": "The basic methodology is the same, but commercial and BESS solutions are larger and more complex.",
        },
        {
            "question": "Which sequence best represents a professional design approach?",
            "options": [
                "A) Select inverter → buy batteries → determine customer requirements",
                "B) Identify requirements and loads → determine energy and power needs → size and match system components",
                "C) Install PV → select cables → ask the customer about backup time",
                "D) Select the largest battery → calculate the loads afterwards",
            ],
            "answer": "B",
            "explanation": "Good design starts by identifying requirements and loads, then calculating energy and power needs before selecting equipment.",
        },
        {
            "question": "What best describes a well-designed energy system?",
            "options": [
                "A) The system with the largest possible battery",
                "B) The system with the largest possible inverter",
                "C) A balanced system in which components are correctly matched to the customer’s requirements",
                "D) A system designed only around maximum solar production",
            ],
            "answer": "C",
            "explanation": "A well-designed system is balanced and matches the customer's real requirements instead of oversizing components unnecessarily.",
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
            "heading": "6.2 Why Site Assessment Matters",
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
            "title": "6.3 Understanding the Customer Requirement",
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
            "title": "6.4 Identifying Essential vs Non-Essential Loads",
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
            "title": "6.5 DB Board Assessment",
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
                    "alt" : "image showing many nuisance tripps and system install",
                },
            ],
        },
        {
            "title": "6.6 Battery & Inverter Placement",
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
            "paragraphs_before": [
                "Inverter placement should also consider:",
            ],
            "bullets_before": [
                "short DC cable lengths",
                "airflow",
                "accessibility",
                "protection from moisture and dust",
                "proximity to the DB board",
            ],
            "images" :[
                {
                    "src" : "images/heat is one of the biggest causes.png",
                    "alt" : "image showing how bad heating can be",
                },
            ],
        },
        {
            "title": "6.7 Roof Assessment (Solar Systems)",
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
            "title": "6.8 Cable Routing & Layout Planning",
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
            "title": "6.9 Environmental & Safety Considerations",
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
                    "alt" : "image of high-quality system poor installation",
                },
                 {
                    "src" : "images/Children pets and.jpg",
                    "alt" : "image of Children,pets",
                },
            ],
        },
        {
            "title": "6.10 Identifying Risks Before Installation",
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
            "heading": "6.11 Installation Sequence",
            "paragraphs": [
                "Professional installers follow a structured installation process.",
                "",
                "",
                "",
                "",
                
            ],
            "paragraphs_after":[
                "Recommended sequence:",
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
                "11. Prepare for commissioning"
            ],
           
             "images" :[
                {
                    "src" : "images/very important installer rule.png",
                    "alt" : "image of very important installer rule",
                },
            ],
        },
        {
            "title": "6.12 REVOV Battery Installation Best Practices",
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
            "title": "6.13 Inverter Installation Best Practices",
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
            "title": "6.14 DC Wiring Fundamentals",
            "paragraphs": [
                "The DC side of the system is one of the highest-risk areas of the installation.",
               
            ],
             "images" :[
                {
                    "src" : "images/battery system operate at.png",
                    "alt" : "image showing battery system operate at high DC voltage",
                },
            ],
            "paragraphs_footer": [
                 "Incorrect DC wiring can cause:",
            ],
            "bullets_footer": [
                "overheating",
                "fire risks",
                "inverter damage",
                "battery damage",
                "BMS trips",
                "serious safety hazards",
            ],
            "paragraphs_extra": [
                "DC wiring best practices include:",
            ],
            "bullets_extra": [
                "correct cable sizing",
                "short cable runs",
                "correct polarity",
                "proper cable protection",
                "secure terminations",
                "correct isolators and breakers",
            ],
            "paragraphs_end": [
                "Always:",
            ],
            "bullets_end": [
                "verify polarity with a meter before connection",
                "inspect cable quality",
                "ensure clean contact surfaces",
            ],
        },
        {
            "title": "6.15 AC Wiring Fundamentals",
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
            "title": "6.16 Cable Termination & Crimping",
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
                    "alt" : "image of a bad crimping",
                },
            ],
            
        },
        {
            "title": "6.17 Earthing & Bonding",
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
            "title": "6.18 Protection Devices & Isolation",
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
                
            ],
            "bullets_extra":[
                "the installation is unsafe.",
            ],
        },
        {
            "title": "SECTION 3 — SYSTEM WIRING & INTEGRATION",
            "heading": "6.20 Understanding Full System Flow",
            "paragraphs": [
                 "Before wiring the system, the installer must understand how energy flows through the installation.",
                
            ],
             "paragraphs_after":[
                "A typical hybrid system includes:",
            ],
            "bullets_after": [
                "solar PV",
                "battery storage",
                "inverter",
                "loads",
                "grid supply",
                "optional generator support",
            ],
           
            "paragraphs_before": [
                "Simplified energy flow:",
                "1. Solar generates DC power",
                "2. Inverter powers loads",
                "3. Excess energy charges batteries",
                "4. Batteries support loads when PV reduces",
                "5. Grid or generator assists when needed",
            ],
           
            "paragraphs_footer": [
                "If the installer understands the energy flow, the wiring process becomes logical and easier to troubleshoot.",
            ],
        },
        {
            "title": "6.21 REVOV Battery Wiring",
            "paragraphs": [
                "Battery wiring must always follow manufacturer recommendations.",
                "Single battery systems are relatively simple.",
                "Parallel battery systems require far more attention.",
                
            ],
            "paragraphs_after":[
               "Important rules for parallel battery systems:",
            ],
            "bullets_after": [
                "same cable lengths",
                "same cable sizes",
                "same battery models",
                "correct communication wiring",
                "balanced load sharing",
            ],
            "paragraphs_footer": [
                "",
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
                
            ],
            "paragraphs_after":[
                "Generators may integrate through:",
            ],
            "bullets_after": [
                "manual changeover systems",
                "automatic transfer switches (ATS)",
            ],
            "paragraphs_before": [
                "Important considerations include:",
            ],
            "bullets_before": [
                "correct switching",
                "synchronization",
                "backfeed prevention",
                "correct generator sizing",
            ],
            "paragraphs_footer": [
                "Grid and generator supplies must never conflict.",
                "Incorrect generator integration can create serious safety risks.",
            ],
        },
        {
            "title": "SECTION 4 — PROFESSIONAL INSTALLATION STANDARDS",
            "heading":"6.26 Clean Installation Standards",
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
            "title": "6.26 Ideal Installation System Examples",
            "paragraphs": [
                "A good installation is not only about making the system work — it is about creating a safe, reliable, efficient, and professional energy solution that will perform well for many years.",
                "The following examples demonstrate what a properly planned and professionally installed REVOV system should look like in real-world applications.",
                "Pay close attention to equipment placement, cable routing, ventilation, protection devices, communication wiring, and overall workmanship, as these small details often make the biggest difference in long-term system performance and reliability.",
            ],
             "images" :[
                {
                    "src" : "images/ideal installation-small system.png",
                    "alt" : "images about ideal installation-small system",
                },
            
                {
                    "src" : "images/ideal installation-medium system.png",
                    "alt" : "images about ideal installation-medium system",
                },
           
                {
                    "src" : "images/ideal installtion -large system.png",
                    "alt" : "images about ideal installtion -large system",
                },
            ],
        },
        {
            "title": "6.27 Common Installation Mistakes",
            "paragraphs": [],
            "images" :[
                {
                    "src" : "images/installer mistake.png",
                    "alt" : "images about common installation mistakes",
                },
            ],
        },
         
        {
            "title": "6.28 Wrapping Up Module 6",
            "paragraphs": [],
            "images" :[
                {
                    "src" : "images/wrapping up module 6.png",
                    "alt" : "images about wrapping up module 6",
                },
            ],
        },
    ],
}

MODULE_6_ASSESSMENT = {
    "title": "Module 6 Assessment",
    "subtitle": "REVOV System Installation, Wiring & Integration",
    "questions": [
        {
            "question": "What should happen before installation work begins on site?",
            "options": [
                "A) The batteries should immediately be switched on",
                "B) A proper site assessment and installation plan should be completed",
                "C) The inverter should be connected to the grid",
                "D) The BMS communication cable should be removed",
            ],
            "answer": "B",
            "explanation": "A proper site assessment and installation plan should be completed before any installation work begins.",
        },
        {
            "question": "Why must the existing DB board be assessed before installation?",
            "options": [
                "A) To determine whether the existing electrical infrastructure is suitable for the planned installation",
                "B) To determine battery chemistry",
                "C) To calculate battery SOC",
                "D) To select the monitoring platform",
            ],
            "answer": "A",
            "explanation": "The existing DB board must be checked to confirm the electrical infrastructure can support the planned installation safely and correctly.",
        },
        {
            "question": "When selecting a location for a battery, which consideration is most important?",
            "options": [
                "A) It must be hidden from view",
                "B) It should be installed in a suitable, safe environment with appropriate ventilation and access",
                "C) It must always be next to a window",
                "D) It should be as far as possible from the inverter",
            ],
            "answer": "B",
            "explanation": "Battery placement must prioritise safety, ventilation, accessibility and suitable environmental conditions.",
        },
        {
            "question": "Why should batteries and inverters generally be positioned to avoid unnecessarily long DC cable runs?",
            "options": [
                "A) To reduce voltage drop and losses",
                "B) To increase battery capacity",
                "C) To increase inverter frequency",
                "D) To improve BMS firmware",
            ],
            "answer": "A",
            "explanation": "Shorter DC cable runs reduce voltage drop, heat and avoid unnecessary power loss.",
        },
        {
            "question": "Before connecting battery cables, the installer must confirm:",
            "options": [
                "A) Solar production",
                "B) Correct polarity",
                "C) Internet speed",
                "D) Customer electricity tariff",
            ],
            "answer": "B",
            "explanation": "Correct polarity must be confirmed before connecting battery cables to avoid damage and safety hazards.",
        },
        {
            "question": "What can happen if battery polarity is reversed?",
            "options": [
                "A) Backup time improves",
                "B) Equipment may be seriously damaged",
                "C) Battery capacity increases",
                "D) The inverter automatically corrects it",
            ],
            "answer": "B",
            "explanation": "Reversed polarity can severely damage equipment and create dangerous conditions.",
        },
        {
            "question": "Why must battery cables be correctly sized for the installation?",
            "options": [
                "A) To carry the required current safely while limiting heat and voltage drop",
                "B) To improve battery SOC calculation",
                "C) To increase PV production",
                "D) To reduce inverter frequency",
            ],
            "answer": "A",
            "explanation": "Correct cable sizing ensures the system can carry required current safely while controlling heat and voltage drop.",
        },
        {
            "question": "A poorly crimped cable lug can cause:",
            "options": [
                "A) Reduced resistance",
                "B) A high-resistance connection, heat and possible failure",
                "C) Increased battery capacity",
                "D) Improved current sharing",
            ],
            "answer": "B",
            "explanation": "A poorly crimped cable lug creates high resistance, heat and possible connection failure.",
        },
        {
            "question": "Why is the correct terminal torque important?",
            "options": [
                "A) Loose or incorrectly tightened connections can cause resistance, heat and failures",
                "B) It determines battery capacity",
                "C) It changes system voltage",
                "D) It controls inverter firmware",
            ],
            "answer": "A",
            "explanation": "Correct terminal torque prevents loose connections, overheating and avoidable equipment failures.",
        },
        {
            "question": "Why should DC protection devices be correctly selected and installed?",
            "options": [
                "A) To increase the system voltage",
                "B) To protect cables and equipment during fault conditions",
                "C) To improve WiFi communication",
                "D) To increase battery energy",
            ],
            "answer": "B",
            "explanation": "DC protection devices are installed to protect the system during faults and abnormal conditions.",
        },
        {
            "question": "What is the purpose of an isolator in an energy system?",
            "options": [
                "A) To increase current",
                "B) To allow a section of the system to be safely isolated",
                "C) To balance battery cells",
                "D) To control battery SOC",
            ],
            "answer": "B",
            "explanation": "An isolator allows a section of the system to be safely isolated for maintenance or emergency conditions.",
        },
        {
            "question": "Why is correct earthing and bonding important during installation?",
            "options": [
                "A) It helps protect people and equipment and allows fault protection to operate correctly",
                "B) It increases battery runtime",
                "C) It increases solar generation",
                "D) It changes inverter power rating",
            ],
            "answer": "A",
            "explanation": "Correct earthing and bonding protect people and equipment and allow fault protection to function correctly.",
        },
        {
            "question": "When routing power and communication cables, good installation practice is to:",
            "options": [
                "A) Route everything together without planning",
                "B) Follow manufacturer requirements and keep wiring neat, protected and appropriately separated",
                "C) Coil excess power cable around the battery",
                "D) Leave cables unsupported for easier maintenance",
            ],
            "answer": "B",
            "explanation": "Good practice is to route, separate and protect cables according to the manufacturer and site requirements.",
        },
        {
            "question": "What is the purpose of the communication connection between the REVOV battery/BMS and inverter?",
            "options": [
                "A) To increase battery voltage",
                "B) To allow operating information and control limits to be exchanged between the battery and inverter",
                "C) To replace the DC power cables",
                "D) To provide AC power to the battery",
            ],
            "answer": "B",
            "explanation": "The communication connection allows the inverter and battery BMS to exchange operating data and control limits.",
        },
        {
            "question": "If the wrong communication port, cable or wiring arrangement is used, the likely result is:",
            "options": [
                "A) Improved charging",
                "B) Communication failure or incorrect system operation",
                "C) Increased battery capacity",
                "D) Higher solar production",
            ],
            "answer": "B",
            "explanation": "Incorrect communication wiring usually results in communication failure or unstable system operation.",
        },
        {
            "question": "In a parallel battery installation, why is balanced cable routing important?",
            "options": [
                "A) To encourage batteries to share current more evenly",
                "B) To increase system voltage",
                "C) To reduce battery capacity",
                "D) To eliminate the BMS",
            ],
            "answer": "A",
            "explanation": "Balanced cable routing helps equalise current sharing between parallel-connected batteries.",
        },
        {
            "question": "Before adding batteries in parallel, the installer should confirm that:",
            "options": [
                "A) The batteries and configuration comply with the manufacturer’s requirements",
                "B) Any battery brand can be added",
                "C) Different battery voltages can be mixed",
                "D) Communication is unnecessary",
            ],
            "answer": "A",
            "explanation": "Parallel battery systems must comply with the manufacturer’s guidelines and configuration rules.",
        },
        {
            "question": "Why should protection devices, isolators and circuits be clearly labelled?",
            "options": [
                "A) For appearance only",
                "B) To make the system safer and easier to operate, maintain and troubleshoot",
                "C) To increase battery lifespan automatically",
                "D) To improve PV generation",
            ],
            "answer": "B",
            "explanation": "Clear labels improve safety, maintenance and fault-finding by making the installation easier to understand.",
        },
        {
            "question": "Before energising a newly installed system, the installer should verify:",
            "options": [
                "A) Polarity, terminations, protection, wiring and overall installation condition",
                "B) Only the battery SOC",
                "C) Only the inverter display",
                "D) Only the solar panels",
            ],
            "answer": "A",
            "explanation": "The installer must confirm polarity, terminations, protection and the overall installation condition before energising.",
        },
        {
            "question": "A system should not be energised when:",
            "options": [
                "A) All required checks have been completed",
                "B) Wiring or polarity has not been verified",
                "C) Protection devices are correctly installed",
                "D) Communication has been correctly connected",
            ],
            "answer": "B",
            "explanation": "A system should not be energised until wiring and polarity verification are complete and confirmed.",
        },
        {
            "question": "During final inspection, a loose battery terminal is found. What is the correct action?",
            "options": [
                "A) Energise the system and see whether it heats up",
                "B) Correct the connection and torque it according to the required specification before energising",
                "C) Reduce the inverter output and leave it loose",
                "D) Cover the terminal with insulation",
            ],
            "answer": "B",
            "explanation": "A loose battery terminal must be corrected and torqued to specification before the system is energised.",
        },
        {
            "question": "Why should cable routes and components remain reasonably accessible after installation?",
            "options": [
                "A) So the system can be safely inspected, maintained and fault-found later",
                "B) So customers can change the wiring themselves",
                "C) To increase battery voltage",
                "D) To avoid using protection devices",
            ],
            "answer": "A",
            "explanation": "Accessible cable routes and components make ongoing inspection, maintenance and fault-finding safer and easier.",
        },
        {
            "question": "What is a sign of a professional installation?",
            "options": [
                "A) Unlabelled wiring hidden wherever possible",
                "B) Neat, secure, protected and clearly identifiable wiring and components",
                "C) Power and communication cables installed randomly",
                "D) Unused cables left inside the enclosure",
            ],
            "answer": "B",
            "explanation": "A professional installation is neat, secure, protected and clearly labelled for safe operation and maintenance.",
        },
        {
            "question": "After the physical installation has been completed, the installer should:",
            "options": [
                "A) Leave the system without testing",
                "B) Test and verify that the installed components and connections operate as intended before handover/commissioning",
                "C) Remove all labels",
                "D) Disconnect the BMS communication",
            ],
            "answer": "B",
            "explanation": "After installation, testing and verification are required before handover and commissioning.",
        },
        {
            "question": "Why does installation quality matter even when all the equipment has been correctly sized?",
            "options": [
                "A) Poor wiring, terminations, placement or integration can still cause faults, poor performance and reduced equipment life",
                "B) Correctly sized equipment cannot develop installation-related faults",
                "C) Installation quality only affects appearance",
                "D) The BMS automatically corrects installation mistakes",
            ],
            "answer": "A",
            "explanation": "Even correctly sized equipment can fail or perform poorly if the installation quality is poor.",
        },
    ],
}

MODULE_7_SYSTEM_CONFIG = {
    "module_title": "MODULE 7 — System Configuration, Communication & Firmware",
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
            "heading": "7.2 Why System Setup Matters",
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
            "paragraphs_before": [
                "But modern lithium systems are intelligent systems. The software, communication and inverter settings now play a major role in how the entire system behaves.",
                "Poor setup can cause:",
            ],
            "bullets_before": [

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
            "images": [
                {
                    "src": "images/not a battery fault.png",
                    "alt": "image about inverter to battery installation issues!",
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
            "paragraphs_before": [
                "The BMS continuously monitors:",
            ],
            "bullets_before": [
                "cell voltage",
                "battery temperature",
                "current flow",
                "SOC",
                "protection limits",
                "cell balancing",
                "battery health",
            ],
            "paragraphs_under": [
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
        
            "heading": "7.4 Before You Start Configuration",
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
            "paragraphs_under": [
                "A system may still \"switch on\" without proper pairing, but it will not behave like a properly integrated lithium system.",
            ],
             "images" : [
                {
                    "src" : "images/signs communication is not working.png",
                    "alt" : "image about signs communication is not working between inverter and battery!",
                },
             ],
        },
        {
            "title": "7.6 Practical Pairing Process — Step by Step",
            "heading": "Step 1 — Confirm Compatibility",
            "paragraphs": [
                
                "Before connecting communication cables, first confirm:",
                "",
                "",
                "✔inverter supports the battery",
                "✔battery supports the inverter",
                "✔correct communication protocol available",
                "✔firmware versions compatible",
                "✔approved battery profile available",
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
            "images": [
                {
                    "src": "images/never assume.png",
                    "alt": "image about never assume compatibility between inverter and battery!",
                },
            ],
            "subsections": [
                {
                    "heading": "Step 2 — Complete the Power Wiring First",
                    "paragraphs": [
                        "Before communication setup:",
                    ],
                    "bullets": [
                        "complete battery DC wiring",
                        "complete inverter wiring",
                        "install isolators and breakers",
                        "verify polarity carefully",
                    ],
                    "paragraphs_before": [
                        "Check:",
                    ],
                    "bullets_before": [
                        "positive to positive",
                        "negative to negative",
                        "correct cable sizing",
                        "correct torque on lugs",
                        "secure terminations",
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
                    ],
                    "images": [
                        {
                            "src": "images/most communication troubleshooting.jpg",
                            "alt": "image about most communication troubleshooting is caused by incorrect wiring or setup!",
                        },
                    ],
                },
                {
                    "heading": "Step 3 — Connect the Communication Cable",
                    "paragraphs": [
                        "The communication cable allows:",
                        "",
                        "",
                        "•	the inverter ",
                        "•	and battery BMS ",
                        "to exchange information continuously.",
                        "",
                        "",
                        "",
                        "Most systems use:",
                    ],
                    "bullets": [
                        "CAN Bus",
                        "or RS485 communication",
                    ],
                    "paragraphs_after": [
                        "The cable normally connects:",
                        "• from the battery communication port",
                        "to:",
                        "• the inverter communication port",
                        "",
                        "What Communication Allows",
                        "Once communication is active, the inverter can receive:",
                    ],
                    "bullets_after": [
                        "SOC",
                        "battery voltage",
                        "current limits",
                        "charge limits",
                        "discharge limits",
                        "battery temperature",
                        "alarms and warnings",
                        "protection instructions",
                    ],
                    "paragraphs_before": [
                        "This allows the inverter to adjust behaviour dynamically based on real-time battery conditions.",
                    ],
                    "images": [
                        {
                            "src": "images/connect the communication cable.png",
                            "alt": "image about connect the communication cable between inverter and battery!",
                        },
                    ],
                },
                {
                    "heading": "Step 4 — Select the Correct Communication Port",
                    "paragraphs": [
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
                },
                {
                    "heading": "Step 5 — Configure Battery Addressing & Master/Slave Setup",
                    "paragraphs": [
                        "In parallel battery systems:",
                    ],
                    "bullets": [
                        "batteries often require addressing",
                        "or DIP switch configuration",
                    ],
                    "paragraphs_after": [
                        "",
                        "",
                        "This allows the batteries to organise communication correctly.",
                        "",
                        "",
                        "Usually:",
                    ],
                        "bullets_after":[
                        " one battery becomes the master battery",
                        "the others become slave batteries",
                        ],
                       "paragraphs_before":[
                            "",

                        "The master battery communicates directly with the inverter.",
                        "The slave batteries communicate through the master battery.",
                        "",
                        "Why Master/Slave Communication Matters",
                        "This helps:",
                       ],
                       
                    
                    "bullets_before": [
                        "coordinate charging",
                        "coordinate discharge behaviour",
                        "balance battery workload",
                        "synchronize protection behaviour",
                        "improve system stability",
                    ],
                },
                {
                    "heading": "Step 6 — Power Up the System in the Correct Sequence",
                    "paragraphs": [
                        "Startup sequence matters.",
                        "",
                        "Many communication problems are caused simply by incorrect startup order.",
                        "",
                        "Typical startup sequence:",
                        "1. Turn on batteries first",
                        "2. Allow BMS startup",
                        "3. Close battery breaker/isolator",
                        "4. Turn on inverter",
                        "5. Allow inverter to detect battery",
                         "",
                         "",
                          "Some systems require:"
                    ],
                    "bullets": [
                        "the battery BMS fully operational before inverter startup",
                    ],
                    "paragraphs_after": [
                        "Otherwise:",
                        "❌ communication may fail",
                        "❌ battery detection may fail",
                        "❌ incorrect startup behaviour may occur",
                        "",
                        
                    ],
                     "images": [
                        {
                            "src": "images/always follow manufacuter.png",
                            "alt": "image about always follow manufacturer instructions for battery type selection!",
                        },
                    ],
                   
                  
                },
                { "heading": "Step 7 — Configure Battery Type in the Inverter",
                    "paragraphs": [
                        "Inside the inverter settings:",
                    ],
                    "bullets": [
                        "select the correct battery type ",
                        "or approved lithium protocol "
                    ],
                    "paragraphs_after": [
                        "Typical options may include:",
                    ],
                    "bullets_after": [
                        "lead-acid",
                        "AGM",
                        "GEL",
                        "lithium",
                        "user-defined",
                        "manufacturer-specific battery profiles",
                    ],
                    "paragraphs_before": [
                        "Always use:",
                        "✔approved lithium profile",
                        "✔supported battery protocol",
                        "where possible.",
                        "",
                        "",
                        "",
                        "Why Correct Battery Selection Matters",
                        "Correct battery selection allows:",
                        "✔ proper communication",
                        "✔ correct charging behaviour",
                        "✔ proper protection logic",
                        "✔ accurate SOC calculation",
                        "✔ correct balancing behaviour"

                    ],
                    
                    "images": [
                        
                        {
                            "src": "images/never gues battery seetings.png",
                            "alt": "",
                        },
                    ],
                },
                {
                    "heading": "Step 8 — Select the Correct Communication Protocol",
                    "paragraphs": [
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

                    ],

                    },
                    {  "heading": "Step 9 — Configure Charge & Discharge Settings",
                        "paragraphs": [
                        "Some systems configure these automatically through communication and other systems require manual configuration.",
                        "",
                        "Important settings include:",
                        "",
                        "These settings directly affect:",
                    ],
                    "bullets": [
                        "battery lifespan",
                        "balancing",
                        "performance",
                        "runtime",
                        "system stability",
                    ],
                    },
                    {  "heading": "Charge Voltage",
                        "paragraphs": [
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
                        ],
                    },
                    {  "heading": "Charge Current",
                        "paragraphs": [
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
                        ],
                    },
                    {  "heading": "Discharge Current",
                        "paragraphs": [
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
                                "src": "images/even with manual settings.png",
                                "alt": "image about even with manual settings, the battery will still limit the current to protect itself!",
                            }
                        ],
                       

                },   
                
            ],
        },
        {
            "title": "7.7 SOC Accuracy, Calibration & Full Charge Synchronisation",
            "paragraphs": [
                "This is one of the most misunderstood areas in lithium systems.",
                "",
                "The BMS calculates SOC using:"
            ],
            "bullets": [
                "voltage",
                "current flow",
                "battery history",
                "balancing information",
                "charge/discharge behaviour"
            ],
            "paragraphs_after": [
                "Over time:"
            ],
            "bullets_after": [
                "small inaccuracies naturally develop"
            ],
            "paragraphs_before": [
                "The battery therefore requires:"
            ],
            "bullets_before": [
                "full charge cycles",
                "balancing opportunities",
                "stable communication",
                "to maintain accurate SOC."
            ],
            "subsections": [
                {
                    "heading": "",
                    "paragraphs": [
                        "Why Full Charge Matters",
                        "The BMS normally performs balancing near full charge.",
                        "",
                        "If the battery NEVER reaches full charge:"
                    ],
                    "bullets": [
                        "❌ balancing may not complete",
                        "❌ SOC drift develops",
                        "❌ runtime estimates become inaccurate",
                        "❌ battery behaviour becomes unstable"
                    ],
                    "images": [
                        {
                            "src": "images/many battery complains.png",
                            "alt": "image about many battery complaints are caused by SOC drift and inaccurate runtime estimates!",
                        },
                    ],
                },
            ],
        },
        {
            "title": "7.8 Operating Modes & System Behaviour",
            "paragraphs": [
                "Operating mode selection dramatically affects how the system behaves.",
                "",
                "",
                "Two identical systems can behave completely differently simply because different operating modes are selected.",  
                
            ],
            "subsections": [
                {
            "heading": "Backup Priority Mode",
            "paragraphs": [
                "In backup mode:",
                ],
            "bullets": [
                "the battery is preserved mainly for outages",
                "grid support may be prioritised",
                "reserve capacity maintained",
                ],
            "paragraphs_after": [
                "Best for:",
                "✔loadshedding backup",
                "✔uptime-focused customers",
                "✔critical load protection",
                ],
               

                },
                {
                    "heading": "Self-Consumption / Hybrid Mode",
                    "paragraphs": [        
                    "In self-consumption mode:",
                    ],
                    "bullets": [
                        "solar powers loads first",
                        "excess solar charges batteries",
                        "batteries discharge later to reduce grid usage",
                    ],
                    "paragraphs_after": [
                        "Best for:",
                        "✔reducing electricity costs",
                        "✔maximising solar usage",
                        "✔hybrid energy management",
                    ],
                  
                },
                {
                    "heading": "Time-of-Use (TOU) Mode",
                     "paragraphs": [
                        "",
                                    
                        "In TOU mode:",
                    ],
                    "bullets": [
                        "Charging and discharging occur according to schedules",
                        "The inverter responds to electricity tariff periods",
                    ],
                    "paragraphs_after": [
                        "Best for:",
                        "✔commercial systems",
                        "✔tariff optimisation",
                        "✔scheduled energy management",

                    ],
                    
                    "images":[
                        {
                           "src" : "images/the wrong operating mode.png",
                            "alt" : "image about the wrong operating mode can cause unexpected behaviour and poor performance!",
                        },
                    ],
                },
                
            ],   
                
        },    
        {
            "title": "7.9 Reserve SOC & Backup Behaviour",
            "paragraphs": [
                "Reserve SOC determines:",
            ],
            "bullets": [
                "how much battery capacity is preserved",
                "how deeply the battery may discharge",
            ],

            "subsections": [
                {
            "heading": "",
            "paragraphs": [
                "If reserve SOC is set to:",
            ],
            "bullets": [
                "20%",
            ],
            "paragraphs_after": [
                "the inverter attempts to preserve:",
            ],
                "bullets_after": [
                "approximately 20% battery capacity",
            ],
            "paragraphs_before": [
                "for:",
            ],
            "bullets_before": [
                "backup reserve",
                "battery protection",
                "emergency operation",
            ],
            "images" : [
                {
                    "src" : "images/reserve soc.png",
                    "alt" : "image showing reserve SOC",
                },
            ],
                },
            ],
            
        },
        {
            "title": "7.10 Grid Charging & Solar Charging Behaviour",
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
            "title": "7.11 Time, Date & Timezone Settings",
            "paragraphs": [
                "This section is extremely important and often overlooked.",
                "",
                "Many inverter functions rely heavily on accurate:",
                 "✔ time",
                 "✔ date",
                 "✔ timezone",
            ],
            
            "paragraphs_after": [
                "❌Incorrect time settings affect:",
                "❌TOU schedules",
                "❌grid charging",
                "❌backup scheduling",
                "❌reporting accuracy",
                "❌operating behaviour",
            ],  
           
            "images" : [
                {
                    "src" : "images/if inverter time is incorrect.png",
                    "alt" :  "image about if inverter time is incorrect, the battery will not charge or discharge at the correct times!",
                },
            ],
        },
        {
            "title": "7.12 Monitoring & Connectivity Setup",
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
            "title": "7.13 Final Configuration Verification",
            "paragraphs": [
                "Before completing setup, verify:",
                "✔communication stable",
                "✔inverter recognises battery correctly",
                "✔SOC stable and accurate",
                "✔charge/discharge limits updating correctly",
                "✔operating mode correct",
                "✔reserve SOC correct",
                "✔charging behaviour stable",
                "✔monitoring online",
                "✔no active alarms present",

            ],
           
        },
        {
            "title": "SECTION 3 — FIRMWARE & COMPATIBILITY",
            "heading": "7.14 What Is Firmware?",
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
            "title": "7.15 Why Firmware Matters",
            "paragraphs": [
                "Outdated or incompatible firmware can cause:",
                "❌ communication failures",
                "❌ incorrect SOC",
                "❌ BMS trips",
                "❌ unstable charging",
                "❌ inverter instability",
                "❌ strange system behaviour",
            ],
           
            "paragraphs_after": [
                "Correct firmware improves:",
            ],
        },
        {
            "title": "7.16 Firmware Compatibility & Version Matching",
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
                    "alt" : "image about firmware version matching between inverter and battery is important for system stability!",
                },
            ],
        },
        {
            "title": "7.17 When to Update Firmware (and When NOT To)",
            "paragraphs": [
                "Good Reasons to Update",
                "known communication issue",
                "manufacturer recommendation",
                "compatibility issue",
                "abnormal system behaviour",
                "new battery/inverter combination",
        ],
         
        },
        {
            "title": "7.18 Safe Firmware Update Process",
            "heading": "Step 1 — Confirm Need",
            "paragraphs": [
                "Identify:",
            ],  
            "bullets": [
                "actual problem",
                "expected improvement",
            ],
            "subsections": [
                {
            "heading": "Step 2 — Check Compatibility",
            "paragraphs":[
                "Verify:",
            ], 
            "bullets": [
                "supported versions",
                "compatibility lists",
                "manufacturer guidance",
            ],
           },
           {"heading": "Step 3 — Prepare System",
              "paragraphs": [
                 "Ensure:",
            ],
               "bullets": [
                  "stable power supply",
                   "correct update tools",
                   "settings backup where possible",
            ],
            },

              {"heading": "Step 4 — Perform Update",
                "paragraphs": [
                    "Use:"
                ],
                "bullets": [
                   "approved process ",
                   "approved software ",
                   "approved cables ",
                ],
                "paragraphs_after": [
                    "NEVER interrupt the process."
                ],

            },
            {"heading":"Step 5 — Verify System",
                "paragraphs": [
                    "After updating:",
                ],
                "bullets": [
                    "check communication",
                    "check charging",
                    "verify SOC",
                    "verify operating mode",
                    "check for faults",
                ],
                "paragraphs_critical": [
                    "Critical Warning",
                    "Interrupting firmware updates may:",
                    "❌corrupt devices",
                    "❌damage communication",
                    "❌require factory recovery",
                ],
               
            },

            ],
           
           
           
        },
        {
            "title": "SECTION 4 — SYSTEM STABILITY & TROUBLESHOOTING",
            "heading": "7.19 Common Setup, Communication & Firmware Problems",
            "subsections": [
            {  "heading":"Communication Problems",
                "paragraphs": [               
                "Symptoms:",
                "❌ frozen SOC",
                "❌ communication alarms",
                "❌ battery not recognised",
                "Possible causes:"

                ],
                "bullets":[
                    "wrong protocol",
                    "bad communication cable",
                    "incorrect firmware",
                    "wrong port",
                    "unsupported battery profile"
                ],

            },
            {  "heading":  "Charging Problems",
                "paragraphs": [              
                "Symptoms:",
            ],
             "bullets": [
                "❌battery never reaches 100%",
                "❌poor runtime",
                "❌balancing issues",
            ],
             "paragraphs_after": [
                "Possible causes:",
            ],
            "bullets_after": [
                "low charge voltage",
                "incorrect battery type",
                "communication failure",
                "insufficient PV",
            ],

            },
            {  "heading": "SOC Problems", 
                "paragraphs": [              
                 "Symptoms:",
            ],
            "bullets": [
                "❌SOC jumps suddenly",
                "❌inaccurate runtime",
                "❌battery switches off unexpectedly",
            ],
            "paragraphs_after": [
                "Possible causes:",
            ],
             "bullets_after": [
                "no full charges",
                "poor balancing",
                "communication issues",
                "SOC drift",
            ],


            },
            {  "heading": "Firmware Problems",
                "paragraphs": [
                    "Symptoms:",
            ],
             "bullets": [
                "❌unstable behaviour",
                "❌random faults",
                "❌intermittent communication",
            ],
            "paragraphs_after": [
                "Possible causes:",
            ],
             "bullets_after": [
                "incompatible versions",
                "failed update",
                "unsupported firmware combinations",
            ],

            },
            

        

            ],     
            
        },
        {
            "title": "7.20 Practical Installer Examples",
            "paragraphs": [
                "By now you have learned how batteries, inverters and the BMS work together as a complete system. ",
                "In practice, however, many service calls begin with a customer reporting that the battery is faulty, the inverter has stopped working, or the system isn't performing as expected.",
                "",
                "In reality, the equipment is often operating exactly as it was designed to. The real cause is frequently incorrect inverter settings, communication problems, firmware mismatches, operating modes, or system configuration errors.",
                    "",
                "The following real-world examples demonstrate how to think like a professional installer. Rather than immediately replacing components, you will learn how to identify the actual root cause by ",
                "understanding how the battery, inverter, BMS and communication system interact.",
                "",
                "",
                 "",
                "As you work through each example, focus on:",
            ],
            "bullets": [
                "the customer's complaint ",
                "what is actually happening inside the system ",
                "why the behaviour occurs ",
                "the checks you should perform before replacing equipment ",
                "the corrective action that resolves the problem. "  
            ],
            "paragraphs_after": [
                "",
                "A good installer does not simply fix symptoms—they identify the underlying cause. Understanding system configuration and communication is often the difference between an unnecessary ",
                "warranty claim and a correctly diagnosed installation issue.",
                "",
                "",
                "",
                "",
                "Remember: Modern lithium battery systems are intelligent systems. When something appears to be 'wrong', it is often the BMS or inverter protecting the battery or responding to the way the ",
                "professional installer."
            ],
            "images"  : [
                {
                    "src" : "images/faulty battery lets look at the real cause.png",
                    "alt" : "images of faulty battery",
                },
                 {
                    "src" : "images/battery never full.png",
                    "alt" : "image of battery never full",
                },
                 {
                    "src" : "images/communication fault.png",
                    "alt" : "image of communication fault",
                },
                 {
                    "src" : "images/bad run time.png",
                    "alt" : "image of bad run time",
                },
                 {
                    "src" : "images/empty battery.png",
                    "alt" : "image of empty battery",
                },
            ],
        },
        {
            "title": "7.21 Installer Rules for Stable Systems",
            "paragraphs": [],
            
            "images"  : [
                {
                    "src" : "images/installer rules for stable.png",
                    "alt" : "image of intaller rules",
                },
       
                
            ],
            
        },
        {
            "title": "Module 7 Wrap Up",
            "heading": "",
            "images": [
                {
                    "src" : "images/wrapping up module 7.png",
                    "alt" : "image of wrapping up module 7",
                },
            ],

     },
        
    ],
}

MODULE_7_ASSESSMENT = {
    "title": "Module 7 Assessment",
    "subtitle": "System Configuration, Communication & Firmware",
    "questions": [
        {
            "question": "Why is correct system configuration important even when the physical installation is correct?",
            "options": [
                "A) Configuration only changes the display appearance",
                "B) Incorrect settings can cause poor charging, unstable operation and battery problems",
                "C) Configuration only affects WiFi",
                "D) Configuration is optional on lithium systems",
            ],
            "answer": "B",
            "explanation": "Correct system configuration is essential because the wrong settings can lead to poor charging, instability and battery issues.",
        },
        {
            "question": "Before configuring an inverter with a REVOV battery, the installer should first confirm:",
            "options": [
                "A) The inverter and battery are compatible",
                "B) The battery enclosure colour",
                "C) The PV panel brand",
                "D) The customer's WiFi password",
            ],
            "answer": "A",
            "explanation": "Compatibility between the inverter and battery must be confirmed before configuration begins.",
        },
        {
            "question": "What is one of the main purposes of communication between the inverter and battery BMS?",
            "options": [
                "A) To increase battery voltage",
                "B) To allow operating information and limits to be exchanged between the devices",
                "C) To replace the battery power cables",
                "D) To provide AC power to the battery",
            ],
            "answer": "B",
            "explanation": "The inverter and BMS communicate so they can exchange operating information and control limits.",
        },
        {
            "question": "CAN and RS485 are primarily used for:",
            "options": [
                "A) Cooling",
                "B) Device communication",
                "C) Earthing",
                "D) DC protection",
            ],
            "answer": "B",
            "explanation": "CAN and RS485 are common communication interfaces used for device data exchange.",
        },
        {
            "question": "Why must the correct communication protocol be selected?",
            "options": [
                "A) Different batteries and inverters may use different communication requirements",
                "B) It increases battery capacity",
                "C) It reduces cable size",
                "D) It changes the system frequency",
            ],
            "answer": "A",
            "explanation": "Different batteries and inverters can require different communication settings and protocols.",
        },
        {
            "question": "If the wrong battery type or protocol is selected in the inverter settings, the system may:",
            "options": [
                "A) Automatically correct itself in every case",
                "B) Develop communication, charging or SOC problems",
                "C) Produce more solar power",
                "D) Increase battery capacity",
            ],
            "answer": "B",
            "explanation": "Incorrect battery type or protocol settings can result in communication, charging and SOC problems.",
        },
        {
            "question": "What does successful battery-to-inverter communication allow the inverter to receive?",
            "options": [
                "A) Battery information such as SOC and operating limits",
                "B) Weather information only",
                "C) Solar panel dimensions",
                "D) Customer electricity tariffs",
            ],
            "answer": "A",
            "explanation": "Battery communication provides the inverter with information such as state of charge and operating limits.",
        },
        {
            "question": "Why is correct charging configuration important?",
            "options": [
                "A) Incorrect charging settings can affect battery performance, lifespan and protection behaviour",
                "B) Charging settings only affect the inverter display",
                "C) All lithium batteries use identical settings",
                "D) The BMS cannot influence charging",
            ],
            "answer": "A",
            "explanation": "Charging configuration influences battery health, performance and how protection systems behave.",
        },
        {
            "question": "Why must discharge limits be configured correctly?",
            "options": [
                "A) To protect the battery from inappropriate operating conditions",
                "B) To increase inverter frequency",
                "C) To improve internet connectivity",
                "D) To increase PV voltage",
            ],
            "answer": "A",
            "explanation": "Correct discharge limits protect the battery from operating outside safe and appropriate limits.",
        },
        {
            "question": "A system repeatedly discharges further than intended. Which area should be checked?",
            "options": [
                "A) Battery and inverter discharge/SOC settings",
                "B) Solar panel mounting bolts only",
                "C) AC cable colour",
                "D) Battery enclosure ventilation only",
            ],
            "answer": "A",
            "explanation": "Repeated excessive discharge often points to incorrect battery or inverter discharge and SOC settings.",
        },
        {
            "question": "What is battery addressing used for in a multi-battery system?",
            "options": [
                "A) To identify individual batteries within the communication network",
                "B) To increase battery voltage",
                "C) To determine cable size",
                "D) To control AC frequency",
            ],
            "answer": "A",
            "explanation": "Battery addressing identifies each battery in a multi-battery network so communication can be managed correctly.",
        },
        {
            "question": "DIP switches may be used to:",
            "options": [
                "A) Configure battery addressing or communication settings",
                "B) Increase battery capacity",
                "C) Replace protection devices",
                "D) Change battery chemistry",
            ],
            "answer": "A",
            "explanation": "DIP switches are often used to configure addressing and communication settings.",
        },
        {
            "question": "Why must the installer follow the manufacturer’s addressing sequence?",
            "options": [
                "A) Incorrect addressing can prevent batteries from communicating correctly",
                "B) Addressing only affects appearance",
                "C) It changes battery kWh",
                "D) Addressing is optional",
            ],
            "answer": "A",
            "explanation": "Following the proper addressing sequence is critical to correct multi-battery communication.",
        },
        {
            "question": "If communication is lost between the inverter and BMS, one likely symptom is:",
            "options": [
                "A) Incorrect SOC information or abnormal charging behaviour",
                "B) Increased solar irradiance",
                "C) Larger battery capacity",
                "D) Lower cable resistance",
            ],
            "answer": "A",
            "explanation": "Lost communication often results in incorrect SOC readings and abnormal charging behaviour.",
        },
        {
            "question": "What should an installer check first when a communication fault occurs?",
            "options": [
                "A) Communication cable, port, protocol and configuration",
                "B) Replace the battery immediately",
                "C) Increase inverter voltage",
                "D) Disconnect the earth conductor",
            ],
            "answer": "A",
            "explanation": "The first check should be the communication cable, port, protocol and configuration.",
        },
        {
            "question": "Why should communication cables be installed carefully?",
            "options": [
                "A) Damaged, incorrectly wired or incorrectly connected cables can cause communication failure",
                "B) They carry all battery power",
                "C) They determine the battery's energy capacity",
                "D) They replace the DC breaker",
            ],
            "answer": "A",
            "explanation": "Communication cables must be installed carefully because damage or poor wiring can cause communication faults.",
        },
        {
            "question": "What is firmware?",
            "options": [
                "A) Software embedded in devices that controls how they operate",
                "B) A type of DC cable",
                "C) A battery mounting bracket",
                "D) A protection fuse",
            ],
            "answer": "A",
            "explanation": "Firmware is embedded software that controls how the device operates.",
        },
        {
            "question": "Why can firmware compatibility matter between batteries and inverters?",
            "options": [
                "A) Different firmware versions can affect communication and system behaviour",
                "B) Firmware changes battery chemistry",
                "C) Firmware determines cable length",
                "D) Firmware eliminates the need for a BMS",
            ],
            "answer": "A",
            "explanation": "Firmware compatibility matters because mismatched versions can affect communication and system behaviour.",
        },
        {
            "question": "When should an installer consider a firmware update?",
            "options": [
                "A) When recommended or required to resolve compatibility, functionality or known system issues",
                "B) Every time the battery reaches 50% SOC",
                "C) Whenever solar production drops",
                "D) Before every installation regardless of manufacturer guidance",
            ],
            "answer": "A",
            "explanation": "Firmware should only be updated when it is recommended or required to address a compatibility or functionality issue.",
        },
        {
            "question": "Before updating firmware, the installer should:",
            "options": [
                "A) Confirm the correct firmware and follow the approved procedure",
                "B) Use any firmware available online",
                "C) Disconnect all safety devices",
                "D) Increase inverter output to maximum",
            ],
            "answer": "A",
            "explanation": "A firmware update should only be performed using the correct version and approved procedure.",
        },
        {
            "question": "Why should firmware updates not be performed casually?",
            "options": [
                "A) Incorrect firmware or an interrupted update can cause system problems",
                "B) Firmware cannot affect system operation",
                "C) Firmware only changes display colours",
                "D) Firmware automatically increases battery capacity",
            ],
            "answer": "A",
            "explanation": "Firmware updates must be done cautiously because incorrect or interrupted updates can cause faults.",
        },
        {
            "question": "A battery shows 100% SOC but discharges unexpectedly quickly. Which of the following could be investigated?",
            "options": [
                "A) Communication and SOC configuration/calibration",
                "B) Roof pitch only",
                "C) AC breaker colour",
                "D) Battery mounting height only",
            ],
            "answer": "A",
            "explanation": "Unexpectedly fast discharge with a 100% SOC display may point to communication or configuration issues.",
        },
        {
            "question": "Before commissioning, the installer should verify:",
            "options": [
                "A) Battery/inverter compatibility, communication and key operating settings",
                "B) Only that the inverter switches on",
                "C) Only PV output",
                "D) Only the battery voltage",
            ],
            "answer": "A",
            "explanation": "Commissioning checks must include compatibility, communication and critical operating settings.",
        },
        {
            "question": "Incorrect configuration can potentially affect:",
            "options": [
                "A) Performance, reliability, battery life and warranty",
                "B) Only the display language",
                "C) Only WiFi speed",
                "D) Only solar panel output",
            ],
            "answer": "A",
            "explanation": "Incorrect configuration can detrimentally affect performance, reliability, battery life and even warranty.",
        },
        {
            "question": "What best describes a correctly configured lithium system?",
            "options": [
                "A) The battery, BMS and inverter communicate correctly and operate within appropriate limits",
                "B) The inverter operates without any battery communication",
                "C) All settings are left at factory defaults regardless of battery type",
                "D) Protection functions are disabled to avoid trips",
            ],
            "answer": "A",
            "explanation": "A properly configured lithium system has coordinated communication and safe operating limits across the battery, BMS and inverter.",
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
            "heading":"8.2 Why Monitoring Matters",
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
            "paragraphs_before": [
                "Monitoring allows installers to:",
                "✔understand system behaviour",
                "✔identify developing problems early",
                "✔diagnose faults faster",
                "✔optimise performance",
                "✔improve customer support",
                "✔reduce unnecessary call-outs",
                "",
                "",
                "",
                 "Without monitoring:"
            ],
            "bullets_before": [
                "installers often guess",
                "faults become harder to diagnose",
                "customer complaints increase",
                "hidden problems develop unnoticed",
            ],
            "paragraphs_under": [
                "Good monitoring changes troubleshooting from:",
                "❌ reacting to failures",
                "to:",
                "✔ proactively managing system health",
            ],
            "images" :    [
                {
                    "src"  : "images/think like a professional.png",
                    "alt"  : "image of think like a professional",
                },
            ],
        },
        {
            "title": "8.3 What Monitoring Actually Shows You",
            "paragraphs": [
                "Monitoring allows installers to see how the system behaves in real-world operation.",
                "",
            ],
            "paragraphs_after": [
                "Depending on the inverter and battery platform, monitoring may show:",
                "✔battery SOC",
                "✔battery voltage",
                "✔battery current",
                "✔charging behaviour",
                "✔discharge behaviour",
                "✔PV production",
                "✔grid usage",
                "✔load consumption",
                "✔battery temperature",
                "✔alarms and warnings",
                "✔fault history",
                "✔historical trends",
            ],
           
            "paragraphs_before": [
                "This information becomes extremely valuable during:",
            ],
            "bullets_before": [
                "troubleshooting",
                "optimisation",
                "maintenance",
                "customer support",
            ],
             "images" :    [
                {
                    "src"  : "images/monitoring data alone is not.png",
                    "alt"  : "image of monitoring data alone is not Enough",
                },
            ],
        },
        {
            "title": "8.3.1 Why Smart Monitoring Matters in Modern REVOV Systems",
            "paragraphs": [
                "Modern REVOV Batteries systems are designed as intelligent lithium systems with integrated communication and monitoring capabilities.",
                "",
                
            ],
            "paragraphs_after":[
                    "Depending on the system design, REVOV systems may support:",
            ],
            "bullets_after": [
                "CAN Bus communication",
                "RS485 communication",
                "Bluetooth monitoring",
                "inverter monitoring platforms",
                "cloud monitoring portals",
                "remote monitoring apps",
            ],
            "paragraphs_before": [
                "This allows installers and users to monitor:",
                "✔ battery behaviour",
                "✔ charging activity",
                "✔ balancing behaviour",
                "✔ faults and warnings",
                "✔ battery health",
                "✔ system performance trends",
                "in real time."
            ],
        },
        {
            "title": "8.4 Understanding Daily System Behaviour",
            "paragraphs": [
                "One of the most important troubleshooting skills is understanding what a system should normally do throughout a typical day.",
                "A healthy system follows predictable daily behaviour patterns.",
                "",
                
                "",
                
                
            ],
             "images" :    [
                    {
                    "src"  : "images/daily stytem behaviuo.png",
                    "alt"  : "image of daily system behaviour",
                    },
            ],
            "subsections":[
                { "heading":"Why Understanding Daily Behaviour Matters",
                   "paragraphs":[
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
                             
            ],
            
        },
        {
            "title": "8.5 What \"Normal\" Looks Like",
            "paragraphs": [
                "A healthy lithium system should normally show:",
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
                "✔Examples of Normal Behaviour",
                "✔SOC decreasing at night",
                "✔lower winter solar production",
                "✔battery charging slower during cloudy weather",
                "✔increased grid usage during poor solar conditions",
                "These are not faults.",
            ], 
        },
        {
            "title": "SECTION 2 — MONITORING-LED TROUBLESHOOTING",
            "heading": "8.6 Using Monitoring to Diagnose Problems",
            "paragraphs": [
                "Monitoring should always be the installer's first troubleshooting tool.",
                "",
                "Before:",
                "❌replacing equipment",
                "❌changing settings randomly",
                "❌disconnecting components",
            ],
           
            "paragraphs_after": [
                "first:",
                "✔ review system behaviour",
                "✔ check historical trends",
                "✔ analyse charging behaviour",
                "✔ review fault history",
            ],
            
            "paragraphs_before": [
                "Good monitoring often reveals:",
            ],
            "bullets_before": [
                "the actual cause quickly",
            ],
             "images" :    [
                {
                    "src"  : "images/using monitoring to diag.png",
                    "alt"  : "image of using monitoring to diagonose",
                },
            ],
        },
        {
            "title": "8.7 The Installer Mindset — Stop Guessing, Start Diagnosing",
            "paragraphs": [
                "Professional troubleshooting follows logic.",
                "✔follows evidence",
                "✔checks data first",
                "✔isolates sections logically",
                "✔verifies before acting",
            ],
            
             "images" :    [
                {
                    "src"  : "images/most system failure are.png",
                    "alt"  : "image of most system failure are not caused by the battery",
                },
            ],
        },
        {
            "title": "8.8 Break the System Into Sections",
            "paragraphs": [
                "Professional installers divide systems into logical sections during troubleshooting.",
                "",
                "This prevents confusion and unnecessary part replacement.",
            ],
              "images" :    [
                {
                    "src"  : "images/trouble shooting logic flow.png",
                    "alt"  : "image of trouble shooting logic flow",
                },
            ],
        },
        {
            "title": "8.9 The 5-Step Troubleshooting Flow",
            "paragraphs": [
                "Professional troubleshooting should always follow a structured process.",
            ],
              "images" :    [
                {
                    "src"  : "images/5-step troubleshotting.png",
                    "alt"  : "image of 5-step troubleshotting",
                },
            ],
        },
        {
            "title": "SECTION 3 — PRACTICAL FAULT FINDING",
            
            "heading": "8.10 Using Symptoms to Read the System",
            "paragraphs": [
                "The following practical troubleshooting guides are designed to help you think systematically when diagnosing faults. Each guide focuses on a specific group of common problems and follows the ",
                "same logical process:"
            ],
            "bullets":[
                "Identify the fault or symptom observed by the customer or installer. ",
                "Consider the most likely causes before making assumptions. ",
                "Perform the recommended checks in a logical order, starting with the simplest and most common causes. ",
                "Confirm the root cause before replacing any equipment or changing system settings. ",
                "Apply the appropriate corrective action and verify that the system operates normally. ",

            ],
            "paragraphs_after": [
                "As you work through these examples, pay attention to the relationship between the symptom and the underlying cause. You will notice that many different faults can produce similar symptoms, ",
                "while one incorrect setting or installation error can lead to multiple system alarms.",
                "",
                "Developing a logical troubleshooting approach will save time, reduce unnecessary warranty claims, improve first-time fix rates, and build customer confidence. The goal is not simply to clear ",
                "alarms—it is to understand why the alarm occurred and ensure the problem does not happen again.",
                "",
                "Remember: The best troubleshooters don't guess—they observe, measure, verify, and confirm. ",
                "Always follow a logical diagnostic process, eliminate the simple causes first, and let the evidence guide your decisions."
            ],
            "images" :    [
                {
                    "src"  : "images/charging and soc faults.png",
                    "alt"  : "image of charging and soc faults",
                },
                  {
                    "src"  : "images/load and run time.png",
                    "alt"  : "image of load and run time",
                },
                 {
                    "src"  : "images/communication and firmware fault.png",
                    "alt"  : "image of communication and firmware fault",
                },
                 {
                    "src"  : "images/installation and electrical faults.png",
                    "alt"  : "image of installation and electrical faults",
                },
                 {
                    "src"  : "images/behavior and logic problems.png",
                    "alt"  : "image of behavior and logic problems",
                },
                 {
                    "src"  : "images/bms and protection faults.png",
                    "alt"  : "image of bms and protection faults",
                },
                 {
                    "src"  : "images/pv and solar problems.png",
                    "alt"  : "image of pv and solar problems",
                },
                 {
                    "src"  : "images/firmware update problems.png",
                    "alt"  : "image of firmware update problems",
                },
                 {
                    "src"  : "images/parallel system problem.png",
                    "alt"  : "image of parallel system problem",
                },
                 {
                    "src"  : "images/environmental problems.png",
                    "alt"  : "image of environmental problems",
                },
                 {
                    "src"  : "images/environmental problems.png",
                    "alt"  : "image of environmental problems",
                },
                 {
                    "src"  : "images/monitoring problems and pos.png",
                    "alt"  : "image of monitoring problems and possible causes",
                },
                 {
                    "src"  : "images/mechanical and installation problems.png",
                    "alt"  : "image of mechanical and installation problems",
                },
            ],
        },
        {
            "title": "SECTION 4 — MAINTENANCE & OPTIMISATION",
            "heading": "8.13 Routine Maintenance",
            "paragraphs": [
                "Even high-quality systems require periodic inspection.",
                "",
               
            ],
            "paragraphs_after": [
                "Routine maintenance should include:",
                "✔cable inspections",
                "✔checking lugs and torque",
                "✔ventilation inspection",
                "✔dust removal",
                "✔checking for overheating",
                "✔monitoring review",
                "✔firmware review",
                "✔communication verification",
            ],
            "subsections":[
                { "heading":"Why Maintenance Matters",  
                  "paragraphs": [
                      "Small problems become large problems if ignored.",
                            "",
                     "Routine inspections help identify:",
             ],
              "paragraphs_after": [
                    "✔ loose connections",
                    "✔ overheating",
                    "✔ abnormal behaviour",
                    "✔ declining performance",
                    "✔ before major failures occur.",
            ],

            },
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
                "✔maintain proper ventilation",
                "✔allow periodic full charges",
                "✔maintain stable communication",
                "✔avoid excessive discharge",
                "✔use correct operating modes",
                "✔avoid excessive heat",
            ],
           
            "images"  : [
                {
                  "src"  : "images/bms can only balance.png",
                  "alt"  : "image of BMS balancing capabilities",
                },
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
                "✔Optimisation Examples",
                "✔adjusting reserve SOC",
                "✔improving operating modes",
                "✔changing charging schedules",
                "✔reducing unnecessary grid usage",
                "✔improving solar utilisation",
            ],
        },
        {
            "title": "8.16 Seasonal Changes & Customer Behaviour",
            "paragraphs": [
                "System behaviour changes throughout the year.",
                "",
                "Winter may cause:",
                "❄lower solar production",
                "❄increased battery cycling",
                "❄more grid support",
                "summer may cause:",
                "☀ higher solar production",
                "☀ earlier full charging"
            ],  
            "paragraphs_after": [
                "Customer Behaviour Also Matters",
                "Customers may:"
            ],
            
            "paragraphs_before": [
                "Customer Behaviour Also Matters",
                "Customers may:",
            ],
            "bullets_before": [
                "add appliances",
                "change usage patterns",
                "increase nighttime loads",
            ],
            "paragraphs_footer": [
                "Monitoring helps installers identify these changes.",
            ],
        },
        {
            "title": "8.17 Remote Monitoring & Proactive Support",
            "paragraphs": [
                "Professional installers increasingly use remote monitoring before visiting site.",
                "",
                "Remote monitoring allows:",
                "reviewing fault history",
                "analysing charging behaviour",
                "checking system trends",
                "identifying abnormal patterns",
                "reducing unnecessary call-outs",
            ],
            
             
        },
        { "title": "Wrapping Up Module 8",
            "paragraphs": [],
             "images"  : [
                {
                   "src"  : "images/wrapping up module 8.png",
                    "alt"  :  "image of wrapping up module 8",
                },
            ],


        },
    ],
}

MODULE_8_ASSESSMENT = {
    "title": "Module 8 Assessment",
    "subtitle": "Monitoring, Optimisation, Troubleshooting & Fault Finding",
    "questions": [
        {
            "question": "What is one of the main purposes of system monitoring?",
            "options": [
                "A) To increase battery capacity",
                "B) To understand system behaviour and identify developing problems",
                "C) To replace protection devices",
                "D) To increase inverter power",
            ],
            "answer": "B",
            "explanation": "Monitoring helps installers understand system behaviour and detect issues before they become major problems.",
        },
        {
            "question": "Monitoring data can help an installer identify:",
            "options": [
                "A) Only battery colour",
                "B) Charging, discharging, loads, alarms and system trends",
                "C) Only PV panel dimensions",
                "D) Only customer electricity tariffs",
            ],
            "answer": "B",
            "explanation": "Monitoring data reveals charging, discharging, loads, alarms and broader system trends.",
        },
        {
            "question": "Why is historical monitoring data useful?",
            "options": [
                "A) It allows the installer to see patterns and compare system behaviour over time",
                "B) It increases battery voltage",
                "C) It replaces site inspections completely",
                "D) It automatically repairs faults",
            ],
            "answer": "A",
            "explanation": "Historical data shows trends and changes in normal behaviour over time, helping diagnose faults.",
        },
        {
            "question": "What is an early warning sign of possible system trouble?",
            "options": [
                "A) Repeated alarms or unusual changes in normal operating behaviour",
                "B) Consistent normal operation",
                "C) Correct charging behaviour",
                "D) Stable battery temperature",
            ],
            "answer": "A",
            "explanation": "Repeated alarms or abnormal behaviour are early signs that deeper investigation is needed.",
        },
        {
            "question": "What should an installer establish before deciding that a system is faulty?",
            "options": [
                "A) What normal operation looks like for that system",
                "B) The colour of the inverter",
                "C) The customer's preferred battery brand",
                "D) The installer who originally sold the system",
            ],
            "answer": "A",
            "explanation": "Normal operating behaviour must be understood before labelling a system as faulty.",
        },
        {
            "question": "When a customer reports that 'the battery is not lasting,' the first step should be to:",
            "options": [
                "A) Replace the battery immediately",
                "B) Understand the loads, usage pattern and actual system behaviour",
                "C) Increase all inverter settings",
                "D) Disable battery protection",
            ],
            "answer": "B",
            "explanation": "The first step is to understand loads, usage patterns and actual battery behaviour before changing hardware or settings.",
        },
        {
            "question": "What is the best approach to troubleshooting?",
            "options": [
                "A) Change several settings at once",
                "B) Follow a logical and systematic process",
                "C) Replace components until the problem disappears",
                "D) Assume the battery is faulty",
            ],
            "answer": "B",
            "explanation": "Systematic troubleshooting eliminates guesswork and identifies the true root cause.",
        },
        {
            "question": "Why should a system be broken into logical sections during fault finding?",
            "options": [
                "A) It helps isolate where the problem is occurring",
                "B) It increases inverter output",
                "C) It improves solar irradiance",
                "D) It increases battery SOC",
            ],
            "answer": "A",
            "explanation": "Breaking the system into sections narrows the fault to the specific area where it occurs.",
        },
        {
            "question": "Which logical areas might be checked during troubleshooting?",
            "options": [
                "A) Battery, inverter, PV, grid, loads and communication",
                "B) Only the battery",
                "C) Only the solar panels",
                "D) Only the customer DB",
            ],
            "answer": "A",
            "explanation": "Troubleshooting should consider all relevant system sections, not just one component.",
        },
        {
            "question": "Why should installers check alarms and event logs before replacing equipment?",
            "options": [
                "A) Logs may show when the problem occurred and what triggered it",
                "B) Logs increase battery capacity",
                "C) Logs reset the BMS automatically",
                "D) Logs eliminate the need for testing",
            ],
            "answer": "A",
            "explanation": "Alarm logs can reveal exactly when a fault occurred and what triggered it.",
        },
        {
            "question": "Frequent inverter overload alarms generally suggest:",
            "options": [
                "A) Excessive load demand or an operating/design issue",
                "B) Improved system efficiency",
                "C) Increased battery capacity",
                "D) Better PV production",
            ],
            "answer": "A",
            "explanation": "Frequent overload alarms usually show the system is under too much demand or poorly matched to the load.",
        },
        {
            "question": "If battery SOC drops sharply whenever a large load starts, an installer should investigate:",
            "options": [
                "A) Load demand, voltage behaviour and battery/system capability",
                "B) Only WiFi strength",
                "C) PV panel colour",
                "D) Battery mounting height",
            ],
            "answer": "A",
            "explanation": "A sudden SOC drop under load often points to demand, voltage or battery capability issues.",
        },
        {
            "question": "If the battery does not appear to charge properly, useful checks include:",
            "options": [
                "A) Available charging source, system behaviour, communication and relevant settings",
                "B) Only the customer's electricity account",
                "C) Only battery enclosure colour",
                "D) Only cable labels",
            ],
            "answer": "A",
            "explanation": "Charging issues require checks of source availability, communication, settings and operating behaviour.",
        },
        {
            "question": "Why is battery temperature important when monitoring a system?",
            "options": [
                "A) Excessive temperature can affect performance and cause protective action",
                "B) High temperature always improves performance",
                "C) Temperature only affects solar panels",
                "D) Temperature has no effect on lithium systems",
            ],
            "answer": "A",
            "explanation": "Temperature directly affects battery performance and may trigger protection actions.",
        },
        {
            "question": "What could repeated high-temperature warnings indicate?",
            "options": [
                "A) Poor installation environment, ventilation or excessive operating stress",
                "B) Improved battery efficiency",
                "C) Increased battery energy",
                "D) Correct system optimisation",
            ],
            "answer": "A",
            "explanation": "Repeated high-temperature warnings often indicate poor ventilation, heat stress or installation issues.",
        },
        {
            "question": "Why are thermal inspections useful during maintenance?",
            "options": [
                "A) They can help identify hot spots and abnormal connections",
                "B) They measure battery SOC",
                "C) They update firmware",
                "D) They increase inverter power",
            ],
            "answer": "A",
            "explanation": "Thermal inspections reveal abnormal heat patterns that often signal loose or failing connections.",
        },
        {
            "question": "Routine inspection of cables and terminals can help identify:",
            "options": [
                "A) Loose, damaged or overheating connections before they cause failure",
                "B) Only inverter software faults",
                "C) Solar irradiance",
                "D) Customer load preferences",
            ],
            "answer": "A",
            "explanation": "Routine inspections detect loose or damaged connections before they escalate into a failure.",
        },
        {
            "question": "What is preventative maintenance intended to achieve?",
            "options": [
                "A) Identify developing problems before they become major failures",
                "B) Increase the number of call-outs",
                "C) Disable system protection",
                "D) Replace equipment regardless of condition",
            ],
            "answer": "A",
            "explanation": "Preventative maintenance aims to find developing issues early and avoid larger failures.",
        },
        {
            "question": "What is one advantage of remote monitoring?",
            "options": [
                "A) Faults and abnormal system behaviour may be identified without immediately attending site",
                "B) It eliminates all future site visits",
                "C) It increases battery capacity",
                "D) It replaces installation testing",
            ],
            "answer": "A",
            "explanation": "Remote monitoring allows faults and abnormal behaviour to be seen before, or without, a site visit.",
        },
        {
            "question": "Why should an installer compare current monitoring data with historical trends?",
            "options": [
                "A) Changes from previous normal behaviour can help identify developing issues",
                "B) Historical information is irrelevant",
                "C) Trends increase system voltage",
                "D) Historical data changes battery chemistry",
            ],
            "answer": "A",
            "explanation": "Comparing current data to historical trends highlights gradual changes from the normal operating pattern.",
        },
        {
            "question": "Seasonal changes may affect:",
            "options": [
                "A) PV production, charging patterns and customer energy use",
                "B) Battery chemistry",
                "C) Cable resistance permanently",
                "D) Inverter physical size",
            ],
            "answer": "A",
            "explanation": "Seasonal shifts affect solar generation, charging behaviour and customer consumption patterns.",
        },
        {
            "question": "A system that performed well in summer provides less battery charge in winter. What should the installer consider before assuming a fault?",
            "options": [
                "A) Seasonal changes in solar production and customer usage",
                "B) Replace the battery immediately",
                "C) Disable the BMS",
                "D) Increase the inverter rating",
            ],
            "answer": "A",
            "explanation": "Lower winter charge is often a result of seasonal solar and usage conditions, not necessarily a fault.",
        },
        {
            "question": "What does system optimisation mean?",
            "options": [
                "A) Adjusting operation appropriately to improve efficiency, performance and battery life",
                "B) Increasing every setting to maximum",
                "C) Removing operating limits",
                "D) Increasing the number of connected loads",
            ],
            "answer": "A",
            "explanation": "Optimisation means tuning system settings to improve efficiency, performance and battery lifespan safely.",
        },
        {
            "question": "Why should an installer avoid making multiple changes at the same time during troubleshooting?",
            "options": [
                "A) It becomes difficult to determine which change affected the problem",
                "B) The battery capacity will double",
                "C) The inverter will always fail",
                "D) Monitoring data stops permanently",
            ],
            "answer": "A",
            "explanation": "Making one change at a time preserves a clear cause-and-effect trail during troubleshooting.",
        },
        {
            "question": "What is the goal of professional fault finding?",
            "options": [
                "A) To identify the root cause and correct it rather than simply treating the symptom",
                "B) To replace the battery first",
                "C) To reset alarms without investigation",
                "D) To increase inverter settings until the fault disappears",
            ],
            "answer": "A",
            "explanation": "Professional fault finding looks for the root cause and fixes the actual issue rather than masking it.",
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
                
            ],
            "paragraphs_after": ["The company was founded with a clear purpose: ",],
            "subsections":[
                { "heading":"to help people and businesses take control of their energy future.",
                     "paragraphs":[
                         "From the beginning, REVOV focused on energy storage systems designed for real-world African conditions — systems capable of handling unstable grids, demanding environments, and the growing need for dependable backup and solar energy storage solutions.",
                  
                     ],

                },
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
            "paragraphs_footer": [
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
            "paragraphs_footer": [
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
            "paragraphs_footer": [
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
            "paragraphs_footer": [
                "The goal is not simply to create installers who can connect equipment. The goal is to help develop installers who can design, commission, troubleshoot, and support reliable energy systems professionally.",
            ],
        },
        {
            "title": "9.6 The REVOV Philosophy",
            "paragraphs": [
                "At its core, REVOV is built around a simple idea: Reliable energy creates progress.",
                
            ],
            "subsections":[
                {
                    "heading": "Reliable energy allows:",
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
                "paragraphs_footer": [
                    "REVOV is not only part of the backup power industry. It is part of the transition toward smarter, more independent energy systems across South Africa and beyond.",
                        ],


                },
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
            "paragraphs_footer": [
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
            "images":[
                 {
                     "src" : "images/installer design guid.png",
                    "alt" : "image of a installation guid for the installers",
                },
            ],
            "subsections":[
                { "heading": "Installer Guide: Reading Battery Specification Sheets",
                        "paragraphs":[
                            "A battery specification sheet is one of the most important documents an installer will use. It contains the technical information needed to correctly size, configure, install and commission a ",
                            "battery system safely and within the manufacturer's requirements.",
                            "",
                            "Many installation problems occur because important specifications such as voltage, current limits, temperature ranges or communication requirements are overlooked or misunderstood. Learning ",

                            "how to interpret a specification sheet is therefore an essential skill for every installer.",
                            "",
                            "The following guide uses a REVOV battery as an example to explain the purpose of each specification, what it means in practical terms, and why it matters during system design and installation. ",
                            "",
                            "Although the values may differ between manufacturers and battery models, the principles for reading and interpreting a specification sheet remain the same.",
                            "",
                            "As you work through this guide, focus on understanding not only what each specification is, but also how it influences equipment selection, system configuration, battery performance, safety, and long-term reliability.",
                            "",
                            "",
                            "Remember: A specification sheet is more than a list of numbers—it is the manufacturer's guide to installing and operating the battery correctly. Learning to interpret it properly is one of the most valuable skills an installer can develop.",
                        ],
                          "images" : [
                                       
                                          {
                                           "src" : "images/how to read revov batter.png",
                                            "alt" : "image of how to read revov spec sheets.",
                                        },  
                                       
                    ],

                },
                {"heading": "Product Fault-Finding & Quick Reference Guides",
                    "paragraphs":[
                        "Every battery system has its own operating characteristics, recommended settings, alarm codes and troubleshooting procedures. While the fault-finding process follows the same logical ",
                        "approach, the specific values, operating limits and diagnostic information will vary between products.",
                        "",
                        "",
                        "The following quick reference guides have been developed to provide installers with practical, product-specific troubleshooting resources that can be used during commissioning, maintenance, servicing and fault finding. ",
                        "",
                        "Each guide summarises the most common symptoms, likely causes, recommended checks and corrective actions for a particular battery or energy storage product.",
                        "",
                        "These guides are intended as quick field references to help installers diagnose problems efficiently before consulting the manufacturer's detailed service documentation where required. As ",
                        "new products are introduced or existing models are updated, these guides can easily be added, replaced or removed without affecting the rest of the training material.",
                        "",

                    ],
                    "paragraphs_after":[
                        "When using these guides, always follow a structured troubleshooting process:"
                    ],
                    "bullets_after":[
                        "Identify the symptom. ",
                        "Confirm the actual root cause. ",
                        "Perform the recommended checks. ",
                        "Apply the appropriate corrective action. ",
                        "Verify that the fault has been resolved before returning the system to service. ",
                    ],
                    "paragraphs_before":[
                            "Remember: Quick reference guides support the troubleshooting process—they do not replace the manufacturer's installation manuals, service documentation or safety procedures. Always confirm ",
                            "your findings before replacing components or making configuration changes."
                    ],
                    "images":[
                        {
                            "src": "images/Revov E100 FAULT.png",
                            "alt": "IMAGE OF REVOV E100 FAULT FINDING GUIDE",
                        },
                         {
                            "src": "images/E300 fault.png",
                            "alt": "IMAGE OF REVOV E300 FAULT FINDING GUIDE",
                        },
                        {
                            "src": "images/cfe 61.44 fault.png",
                            "alt": "IMAGE OF REVOV CFE 61.44 FAULT FINDING GUIDE",
                        },
                        {
                            "src": "images/energy core fault.png",
                            "alt": "IMAGE OF REVOV ENERGY CORE FAULT FINDING GUIDE",
                        },
                    ],
                     
                  
                

                 },
            ],
           
        },
    ],
}

class CellChemistry(Enum):
    """Battery cell chemistry identifiers"""
    LI_ION = "LI_ION"
    LIFEPO4 = "LIFEPO4"
    LI_POLYMER = "LI_POLYMER"
    NCA = "NCA"
    NCM = "NCM"

@dataclass
class CellSpecifications:
    """Minimal cell specification model used by the interactive tools."""
    nominal_voltage_v: float
    capacity_mah: float
    chemistry: CellChemistry
    min_voltage_v: float
    max_voltage_v: float

    def energy_wh(self) -> float:
        """Return the nominal stored energy in watt-hours."""
        return self.nominal_voltage_v * (self.capacity_mah / 1000.0)

    def voltage_range(self) -> float:
        """Return the usable voltage window from min to max."""
        return max(0.0, self.max_voltage_v - self.min_voltage_v)

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

