#!/usr/bin/env python3
"""Refactor section 5.4 with expanded subsections"""

# Read the file
with open('modules/lithium_education.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Find the 5.4 section
section_54_start = content.find('"title": "5.4 Step 2 — Calculate Backup Time Requirements (kWh)"')
if section_54_start == -1:
    print("Could not find 5.4 section")
    exit(1)

# Find the opening brace before section 5.4
brace_start = content.rfind('{', 0, section_54_start)

# Find the closing brace of the 5.4 section (find the next section 5.5)
section_55_start = content.find('"title": "5.5 Step 3 — Select the Correct Battery Size"', section_54_start)

# Find where 5.4 ends (before 5.5 opening brace)
old_section_end = content.rfind('},\n        {', section_54_start, section_55_start) + 2

print(f"Section 5.4 found at position {section_54_start}")

# New section 5.4 with expanded subsections
new_section_54 = '''        {
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
                    "subsections": [
                        {
                            "heading": "kW (Kilowatts) = Power",
                            "paragraphs": [
                                "This refers to:",
                            ],
                            "bullets": [
                                "how much power is being used at a specific moment",
                            ],
                            "paragraphs_after": [
                                "Think of it like:",
                            ],
                            "bullets_after": [
                                "the speed of a vehicle",
                                "or how hard the engine is working",
                            ],
                        },
                        {
                            "heading": "kWh (Kilowatt-hours) = Energy",
                            "paragraphs": [
                                "This refers to:",
                            ],
                            "bullets": [
                                "how much energy is used over time",
                            ],
                            "paragraphs_after": [
                                "Think of it like:",
                            ],
                            "bullets_after": [
                                "how much fuel the vehicle uses during the trip",
                            ],
                        },
                    ],
                },
                {
                    "heading": "Simple Formula",
                    "paragraphs": [
                        "Backup energy requirement is calculated as:",
                    ],
                    "bullets": [
                        "Power (kW) × Time (Hours) = Energy Required (kWh)",
                    ],
                },
                {
                    "heading": "Why Backup Time Requirements Are So Important",
                    "paragraphs": [
                        "Two customers may have exactly the same loads but completely different battery requirements depending on how long they want backup power.",
                    ],
                    "subsections": [
                        {
                            "heading": "Example Comparison",
                            "paragraphs": [
                                "Customer A – Required backup time of 2 hours for a 1kW load",
                                "Customer B – Required backup time of 10 hours for a 1kW load",
                                "Even though the load is identical:",
                            ],
                            "bullets": [
                                "Customer B needs a much larger battery bank",
                            ],
                        },
                    ],
                },
            ],
        },'''

# Replace the section
new_content = content[:brace_start] + new_section_54 + content[old_section_end:]

# Write back
with open('modules/lithium_education.py', 'w', encoding='utf-8') as f:
    f.write(new_content)

print("Section 5.4 refactored successfully!")
