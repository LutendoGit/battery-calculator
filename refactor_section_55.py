#!/usr/bin/env python3
"""Refactor section 5.5 with expanded subsections"""

# Read the file
with open('modules/lithium_education.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Find the 5.5 section
section_55_start = content.find('"title": "5.5 Step 3 — Select the Correct Battery Size"')
if section_55_start == -1:
    print("Could not find 5.5 section")
    exit(1)

# Find the opening brace before section 5.5
brace_start = content.rfind('{', 0, section_55_start)

# Find the closing brace of the 5.5 section (find the next section 5.6)
section_56_start = content.find('"title": "5.6 Step 4 — Select the Correct Inverter Size"', section_55_start)

# Find where 5.5 ends (before 5.6 opening brace)
old_section_end = content.rfind('},\n        {', section_55_start, section_56_start) + 2

print(f"Section 5.5 found at position {section_55_start}")

# New section 5.5 with expanded subsections
new_section_55 = '''        {
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
        },'''

# Replace the section
new_content = content[:brace_start] + new_section_55 + content[old_section_end:]

# Write back
with open('modules/lithium_education.py', 'w', encoding='utf-8') as f:
    f.write(new_content)

print("Section 5.5 refactored successfully!")
