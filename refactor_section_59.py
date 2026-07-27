#!/usr/bin/env python3
"""
Refactor section 5.9 "Voltage Drop and Cable Sizing" with hierarchical subsections
"""

# Read the file
with open(r'modules\lithium_education.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Find and replace section 5.9
old_section = '''        {
            "title": "5.9 Step 7 — Voltage Drop and Cable Sizing",
            "paragraphs": [
                "Correct cable sizing is a critical part of system design because cables are responsible for safely carrying power between the batteries, inverter, solar panels, and loads.",
                "Even the best inverter and battery system can perform poorly if the cables are undersized or installed incorrectly.",
                "Cables may seem simple, but they directly affect system safety, efficiency, voltage stability, charging performance, inverter operation and battery lifespan.",
            ],
            "bullets": [
                "Incorrect cable sizing is one of the most common causes of overheating, inverter faults, poor charging, voltage instability, nuisance tripping, damaged terminals and fire risks.",
            ],
            "paragraphs_after": [
                "Voltage drop is the reduction in voltage that occurs as electricity travels through a cable. As current flows through a cable, the cable creates resistance, resistance causes energy loss, and some voltage is lost along the cable.",
                "The longer the cable or the higher the current, the greater the voltage drop becomes.",
                "Excessive voltage drop can cause poor inverter performance, incorrect charging behaviour, low battery voltage alarms, reduced efficiency, excessive heat and unstable system operation.",
                "In battery systems, this becomes especially important because battery systems often operate at high current and relatively low voltage.",
            ],
        },'''

new_section = '''        {
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
                },
            },
        },'''

# Replace the section
if old_section in content:
    content = content.replace(old_section, new_section)
    with open(r'modules\lithium_education.py', 'w', encoding='utf-8') as f:
        f.write(content)
    print("Section 5.9 refactored successfully!")
else:
    print("ERROR: Could not find section 5.9 to replace!")
    exit(1)
