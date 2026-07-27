#!/usr/bin/env python3
"""Refactor section 5.3 with expanded subsections"""

import json

# Read the file
with open('modules/lithium_education.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Find MODULE_5_ENERGY_SYSTEM_DESIGN
start_idx = content.find('MODULE_5_ENERGY_SYSTEM_DESIGN = {')
if start_idx == -1:
    print("Could not find MODULE_5_ENERGY_SYSTEM_DESIGN")
    exit(1)

# Find the 5.3 section
section_53_start = content.find('"title": "5.3 Step 1 — Load Assessment: Understanding What Must Be Powered"', start_idx)
if section_53_start == -1:
    print("Could not find 5.3 section")
    exit(1)

# Find the closing brace of the 5.3 section (find the next section 5.4)
section_54_start = content.find('"title": "5.4 Step 2 — Calculate Backup Time Requirements (kWh)"', section_53_start)

# Find the opening brace before section 5.3
brace_start = content.rfind('{', 0, section_53_start)

# The old section ends at the comma before 5.4
old_section_end = content.rfind('},\n        {', section_53_start, section_54_start) + 2  # Include the },

print(f"Section 5.3 found at position {section_53_start}")
print(f"Old section: {content[brace_start:old_section_end][:200]}...")

# New section 5.3 with expanded subsections
new_section_53 = '''        {
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
                },
            ],
            "images": [
                {
                    "src":"images/Appliance ,power.png",
                    "alt":"Load Assessment"
                }
            ],
        },'''

# Replace the section
new_content = content[:brace_start] + new_section_53 + content[old_section_end:]

# Write back
with open('modules/lithium_education.py', 'w', encoding='utf-8') as f:
    f.write(new_content)

print("Section 5.3 refactored successfully!")
