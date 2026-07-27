#!/usr/bin/env python3
"""Refactor section 5.7 with expanded subsections"""

# Read the file
with open('modules/lithium_education.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Find the 5.7 section
section_57_start = content.find('"title": "5.7 Step 5 — Size the Solar PV Array"')
if section_57_start == -1:
    print("Could not find 5.7 section")
    exit(1)

# Find the opening brace before section 5.7
brace_start = content.rfind('{', 0, section_57_start)

# Find the closing brace of the 5.7 section (find the next section 5.8)
section_58_start = content.find('"title": "5.8 Step 6 — Check Inverter-to-Battery Compatibility"', section_57_start)

# Find where 5.7 ends (before 5.8 opening brace)
old_section_end = content.rfind('},\n        {', section_57_start, section_58_start) + 2

print(f"Section 5.7 found at position {section_57_start}")

# New section 5.7 with expanded subsections
new_section_57 = '''        {
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
                },
            ],
        },'''

# Replace the section
new_content = content[:brace_start] + new_section_57 + content[old_section_end:]

# Write back
with open('modules/lithium_education.py', 'w', encoding='utf-8') as f:
    f.write(new_content)

print("Section 5.7 refactored successfully!")
