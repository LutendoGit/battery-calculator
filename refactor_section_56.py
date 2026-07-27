#!/usr/bin/env python3
"""Refactor section 5.6 with expanded subsections"""

# Read the file
with open('modules/lithium_education.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Find the 5.6 section
section_56_start = content.find('"title": "5.6 Step 4 — Select the Correct Inverter Size"')
if section_56_start == -1:
    print("Could not find 5.6 section")
    exit(1)

# Find the opening brace before section 5.6
brace_start = content.rfind('{', 0, section_56_start)

# Find the closing brace of the 5.6 section (find the next section 5.7)
section_57_start = content.find('"title": "5.7 Step 5 — Size the Solar PV Array"', section_56_start)

# Find where 5.6 ends (before 5.7 opening brace)
old_section_end = content.rfind('},\n        {', section_56_start, section_57_start) + 2

print(f"Section 5.6 found at position {section_56_start}")

# New section 5.6 with expanded subsections
new_section_56 = '''        {
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
                        "Customers often focus only on: \"How many appliances can the inverter run?\"",
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
                },
            ],
        },'''

# Replace the section
new_content = content[:brace_start] + new_section_56 + content[old_section_end:]

# Write back
with open('modules/lithium_education.py', 'w', encoding='utf-8') as f:
    f.write(new_content)

print("Section 5.6 refactored successfully!")
