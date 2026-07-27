#!/usr/bin/env python3
"""Refactor section 5.8 with expanded subsections"""

# Read the file
with open('modules/lithium_education.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Find the 5.8 section
section_58_start = content.find('"title": "5.8 Step 6 — Check Inverter-to-Battery Compatibility"')
if section_58_start == -1:
    print("Could not find 5.8 section")
    exit(1)

# Find the opening brace before section 5.8
brace_start = content.rfind('{', 0, section_58_start)

# Find the closing brace of the 5.8 section (find the next section 5.9)
section_59_start = content.find('"title": "5.9 Step 7 — Voltage Drop and Cable Sizing"', section_58_start)

# Find where 5.8 ends (before 5.9 opening brace)
old_section_end = content.rfind('},\n        {', section_58_start, section_59_start) + 2

print(f"Section 5.8 found at position {section_58_start}")

# New section 5.8 with expanded subsections
new_section_58 = '''        {
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
                },
            ],
        },'''

# Replace the section
new_content = content[:brace_start] + new_section_58 + content[old_section_end:]

# Write back
with open('modules/lithium_education.py', 'w', encoding='utf-8') as f:
    f.write(new_content)

print("Section 5.8 refactored successfully!")
