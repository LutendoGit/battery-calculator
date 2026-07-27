#!/usr/bin/env python3
"""
Refactor section 5.10 "Designing for Performance and Long Battery Life" with hierarchical subsections
"""

# Read the file
with open(r'modules\lithium_education.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Find and replace section 5.10
old_section = '''        {
            "title": "5.10 Step 8 — Designing for Performance and Long Battery Life",
            "paragraphs": [
                "A good battery system should not only work today — it should continue operating safely, efficiently, and reliably for many years.",
                "This is why proper system design must always consider long-term battery performance and lifespan, not just whether the system can power the loads immediately after installation.",
                "Lithium batteries are a major investment, and the way the system is designed has a direct impact on battery lifespan, system reliability, charging performance, efficiency, operating temperature and long-term stability.",
            ],
            "bullets": [
                "A poorly designed system may still function initially, but excessive stress, incorrect settings, or poor operating conditions can significantly shorten battery life over time.",
                "Batteries perform best within safe operating conditions. The BMS continuously protects the battery against overcharging, deep discharge, excessive current, overheating and unsafe operating conditions.",
                "However, good system design aims to avoid these conditions altogether rather than relying on the BMS to constantly intervene.",
            ],
            "paragraphs_after": [
                "Batteries last longer when they are not constantly pushed to their limits. A system designed too tightly may cause deep daily discharges, high charging current, excessive discharge current, frequent protection events and increased operating temperatures.",
                "Depth of Discharge (DoD) affects lifespan. Although lithium batteries support deep discharge, constantly operating at maximum depth of discharge increases stress on the cells.",
                "Temperature has a major impact. Battery temperature significantly affects performance, charging behaviour and lifespan. Excessive heat is one of the biggest causes of accelerated battery aging.",
                "Proper charging is critical. Incorrect charge voltage, charge current, float settings or inverter configuration can reduce battery lifespan, prevent balancing, cause inaccurate SOC and trigger BMS alarms.",
                "Correct solar sizing improves battery health. A solar array that is too small may leave batteries partially charged for long periods, prevent balancing, reduce SOC accuracy and increase cycling stress.",
            ],
        },'''

new_section = '''        {
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
                },
            },
        },'''

# Replace the section
if old_section in content:
    content = content.replace(old_section, new_section)
    with open(r'modules\lithium_education.py', 'w', encoding='utf-8') as f:
        f.write(content)
    print("Section 5.10 refactored successfully!")
else:
    print("ERROR: Could not find section 5.10 to replace!")
    exit(1)
