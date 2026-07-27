from pathlib import Path

path = Path('modules/lithium_education.py')
text = path.read_text(encoding='utf-8')
old = '\n}\n\n\nclass CapacityAndDOD:'
if old not in text:
    raise SystemExit('Marker not found in lithium_education.py')
new_content = '''
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
        },
        {
            "title": "5.3 Step 1 — Load Assessment: Understanding What Must Be Powered",
            "paragraphs": [
                "The first and most important step in designing any battery or solar system is understanding exactly what the system needs to power. This process is called a load assessment.",
                "A load assessment helps determine:",
            ],
            "bullets": [
                "how much power the system must supply",
                "how long the system must run",
                "which appliances are critical",
                "how large the inverter and battery bank need to be",
            ],
            "paragraphs_after": [
                "Without a proper load assessment, the system may end up:",
            ],
            "bullets_after": [
                "too small and unable to support the required loads",
                "or unnecessarily oversized and far more expensive than needed",
            ],
            "numbered": [
                "1. Power Requirement (Instant Demand) - This is the total power the system must supply at a specific moment.",
                "2. Energy Requirement (Runtime) - This determines how long the system must supply power.",
            ],
            "paragraphs_extra": [
                "A load is anything that consumes electrical power.",
                "Examples include lights, TV, Wi-Fi routers, fridges, computers, kettles, pumps, air conditioners, and machinery.",
                "Every load uses a certain amount of power, usually measured in watts (W) or kilowatts (kW).",
                "If the system is not designed around the actual loads: the inverter may overload, the batteries may drain too quickly, runtime may be much shorter than expected, and equipment may trip or shut down.",
                "A proper load assessment ensures the system is designed realistically for the customer’s needs.",
            ],
            "bullets_extra": [
                "critical loads",
                "non-essential loads",
            ],
        },
        {
            "title": "5.4 Step 2 — Calculate Backup Time Requirements (kWh)",
            "paragraphs": [
                "Once the loads have been identified, the next step is to determine how long the customer wants those loads to operate during a power outage. This is called the backup time requirement and is one of the most important factors when sizing a battery system.",
                "The backup time requirement determines how much energy storage is needed, how large the battery bank must be, and how long the system can support the required loads.",
                "While inverter sizing is mainly based on power (kW), battery sizing is mainly based on energy storage capacity, usually measured in kilowatt-hours (kWh).",
                "Understanding the Difference Between kW and kWh is one of the most important concepts in battery system design.",
            ],
            "bullets": [
                "kW (Kilowatts) = Power; how much power is being used at a specific moment",
                "kWh (Kilowatt-hours) = Energy; how much energy is used over time",
            ],
            "paragraphs_after": [
                "Backup energy requirement is calculated as: Power (kW) × Time (Hours) = Energy Required (kWh)",
                "Two customers may have exactly the same loads but completely different battery requirements depending on how long they want backup power.",
                "Customer A – Required backup time of 2 hours for a 1 kW load.",
                "Customer B – Required backup time of 10 hours for a 1 kW load.",
                "Even though the load is identical, Customer B needs a much larger battery bank.",
            ],
        },
        {
            "title": "5.5 Step 3 — Select the Correct Battery Size",
            "paragraphs": [
                "Once the load assessment and backup time requirements have been calculated, the next step is selecting the correct battery size.",
                "This is one of the most important parts of system design because the battery determines how much energy the system can store and how long the loads can operate during a power outage.",
                "The battery must be correctly sized to support the required loads, provide the required backup time, operate safely within its limits, allow for future expansion where necessary, and avoid excessive battery stress.",
            ],
            "bullets": [
                "If the battery is too small: runtime will be shorter than expected, the battery may discharge too quickly, the system may shut down prematurely, battery lifespan may reduce due to excessive cycling.",
                "If the battery is too large: system cost increases unnecessarily, charging times may become longer, the customer may pay for unused capacity.",
            ],
            "paragraphs_after": [
                "Battery Capacity is Measured in kWh. Battery size is usually measured in kilowatt-hours (kWh). This represents how much energy the battery can store. The larger the kWh rating, the longer the system can run the loads.",
                "Real-world systems must account for inverter losses, reserve capacity, surge loads, battery aging, temperature effects, future expansion and depth of discharge limits.",
                "This means installers usually recommend a slightly larger battery than the minimum calculated requirement.",
                "Although the calculation shows approximately 2 kWh required, an installer may recommend a 5 kWh battery because the larger battery reduces battery stress, improves runtime stability, allows for future load growth, provides reserve capacity and improves battery lifespan.",
            ],
            "bullets_after": [
                "The battery must also be suitable for the inverter’s power requirements.",
                "A very large inverter connected to a very small battery may overload the battery, exceed discharge limits and trigger BMS protection events.",
                "The battery and inverter must therefore be correctly matched.",
            ],
        },
        {
            "title": "5.6 Step 4 — Select the Correct Inverter Size",
            "paragraphs": [
                "Once the battery size has been determined, the next step is selecting the correct inverter size.",
                "The inverter is one of the most important components in the system because it converts the battery’s DC power into usable AC power for appliances and electrical equipment.",
                "The inverter must be correctly sized to safely handle the required loads, support startup surges, operate efficiently, communicate correctly with the battery, and provide stable system performance.",
            ],
            "bullets": [
                "If the inverter is too small: it may overload, trip during operation, struggle with startup loads, and shut down unexpectedly.",
                "If the inverter is too large: system cost increases unnecessarily, efficiency at low loads may reduce, the battery may not be able to support the inverter properly.",
            ],
            "paragraphs_after": [
                "Understanding Inverter Size: Inverter size is usually measured in watts (W) or kilowatts (kW). This refers to how much power the inverter can supply at a specific moment.",
                "Unlike battery sizing, which is mainly based on runtime and energy storage (kWh), inverter sizing is mainly based on instantaneous power demand.",
            ],
            "bullets_after": [
                "Continuous Rating - the power the inverter can safely supply continuously during normal operation.",
                "Surge Rating - the extra power available for short startup bursts from appliances like fridges, pumps, compressors, air conditioners and power tools.",
            ],
            "paragraphs_extra": [
                "A fridge may normally use 150 W but during startup it may briefly draw 600 W or more. This is called a surge load or startup current.",
                "The inverter must be capable of handling these short bursts of power without tripping or shutting down.",
                "The inverter and battery must work together correctly. A very large inverter connected to a very small battery may exceed the battery’s discharge limits, trigger BMS protection events, cause voltage drops and reduce battery lifespan.",
                "The inverter must also match the battery bank voltage. For example, a 48 V inverter requires a 48 V battery bank and a 24 V inverter requires a 24 V battery bank.",
                "Modern lithium systems also rely heavily on communication between the inverter and the battery BMS. Compatible communication improves charging accuracy, protection, SOC accuracy and system stability.",
            ],
        },
        {
            "title": "5.7 Step 5 — Size the Solar PV Array",
            "paragraphs": [
                "Once the battery and inverter have been selected, the next step is sizing the solar PV array. The solar array is responsible for generating the energy that powers the loads and recharges the batteries.",
                "Correct solar sizing is extremely important because the solar panels must generate enough energy to supply daytime loads, recharge the batteries, compensate for system losses, and support reliable system operation throughout the year.",
            ],
            "bullets": [
                "If the solar array is too small: batteries may not fully recharge, backup time may reduce, the system may rely heavily on grid or generator support, battery lifespan may shorten due to chronic undercharging.",
                "If the solar array is too large: equipment limits may be exceeded, unnecessary costs may increase, the inverter or charge controller may limit excess production.",
            ],
            "paragraphs_after": [
                "Solar panels are usually rated in watts (W) or kilowatts peak (kWp). This rating indicates the maximum power the panel can produce under ideal test conditions.",
                "Solar Array Sizing Starts with Energy Usage. The first step in PV sizing is understanding how much energy the system uses per day. This is usually measured in kWh per day.",
                "The solar array must generate enough energy to run the daytime loads, recharge the battery for nighttime use, and compensate for system losses.",
            ],
            "bullets_after": [
                "Peak Sun Hours (PSH) represent the average number of hours per day during which the solar panels produce near-rated output.",
                "Losses from inverter efficiency, temperature, cable losses, panel mismatch, dirt and dust, charging losses, shading and weather variation must be considered.",
                "Good system design typically oversizes the array slightly to ensure reliable performance.",
            ],
            "paragraphs_extra": [
                "Panel Orientation and Tilt Matter. Solar production is heavily affected by roof direction, tilt angle and shading. Poor panel placement can significantly reduce performance.",
                "Series and Parallel PV Design: series PV connection increases voltage while parallel PV connection increases current. The PV array must be designed within inverter limits, MPPT voltage ranges, current limits and safety requirements.",
                "Matching the PV Array to the Inverter is critical. The solar array must remain within the inverter’s maximum PV voltage, maximum PV current and MPPT operating range.",
            ],
        },
        {
            "title": "5.8 Step 6 — Check Inverter-to-Battery Compatibility",
            "paragraphs": [
                "Once the battery, inverter, and solar array have been selected, it is critical to ensure that the inverter and battery are fully compatible with each other.",
                "This is one of the most important parts of system design because even high-quality equipment may not operate correctly if the devices are not properly matched.",
                "Many installation problems are not caused by faulty equipment, but rather by compatibility issues between the inverter and battery.",
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
                "Modern lithium batteries are intelligent systems controlled by a BMS. The inverter and BMS constantly exchange information to ensure the battery operates safely and efficiently.",
                "The inverter relies on the battery BMS to provide information such as battery state of charge (SOC), charge and discharge limits, battery temperature, alarms and warnings, and battery protection status.",
                "If the inverter cannot properly communicate with the BMS, charging may become inaccurate, battery protection may reduce, runtime estimates may be incorrect, nuisance faults may occur, and battery lifespan may shorten.",
            ],
            "bullets_after": [
                "The first requirement is ensuring the inverter and battery operate at the same system voltage.",
                "Modern lithium systems rely heavily on CAN Bus, RS485 or Modbus for communication.",
                "The battery must also be capable of safely supplying the current the inverter requires.",
                "A large inverter connected to a very small battery may cause BMS overcurrent protection events, voltage drops, system shutdowns and excessive battery stress.",
            ],
        },
        {
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
        },
        {
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
        },
        {
            "title": "5.11 Real-World System Design Examples",
            "paragraphs": [
                "Understanding the theory behind system design is important, but seeing how these principles are applied in real-world situations makes the concepts far easier to understand.",
                "Every installation is different, and factors such as load requirements, backup time expectations, budget, available space, and future expansion all influence the final system design.",
                "The following examples demonstrate how system sizing and component selection may differ depending on the application, while highlighting the practical thinking and decision-making that goes into designing safe, reliable, and efficient battery and solar systems.",
            ],
        },
        {
            "title": "5.12 Common Mistakes Installers Must Avoid",
            "paragraphs": [
                "Good system design is about avoiding common mistakes before installation.",
                "Mistakes can include ignoring startup loads, undersizing cables, mismatching inverter and battery voltage, and failing to plan for future expansion.",
                "A careful design process helps prevent nuisance trips, overheating, incorrect charging, shortened battery life, communication faults, overloaded components, unstable system behaviour and safety risks.",
            ],
        },
    ],
}

MODULE_5_ASSESSMENT = {
    "title": "Module 5 Assessment",
    "questions": [
        {
            "question": "1. What is the first step in designing a battery and solar system?",
            "options": [
                "A) Choosing the inverter brand",
                "B) Performing a load assessment",
                "C) Installing the battery",
                "D) Selecting panel colour",
            ],
            "answer": "B",
            "explanation": "The first step is to perform a load assessment to understand what the system must power.",
        },
        {
            "question": "2. A load assessment helps determine:",
            "options": [
                "A) Which colour panels to use",
                "B) how much power is needed and how long the loads must run",
                "C) the GPS location of the system",
                "D) the battery cell chemistry",
            ],
            "answer": "B",
            "explanation": "A load assessment determines power demand and runtime requirements.",
        },
        {
            "question": "3. Which of these is considered a load?",
            "options": [
                "A) A solar panel",
                "B) A fridge",
                "C) The inverter casing",
                "D) The roof structure",
            ],
            "answer": "B",
            "explanation": "A load is anything that consumes electrical power, such as a fridge.",
        },
        {
            "question": "4. Critical loads are:",
            "options": [
                "A) Items the customer wants to keep running during outages",
                "B) Appliances that are always off",
                "C) Only the solar panels",
                "D) Only decorative lights",
            ],
            "answer": "A",
            "explanation": "Critical loads are the important appliances the customer wants to keep powered during outages.",
        },
        {
            "question": "5. Why is it important to exclude non-essential loads from backup design?",
            "options": [
                "A) To increase system cost",
                "B) To improve runtime and reduce battery stress",
                "C) To reduce solar output",
                "D) To avoid using the inverter",
            ],
            "answer": "B",
            "explanation": "Excluding non-essential loads helps reduce cost, improve runtime and reduce battery stress.",
        },
        {
            "question": "6. A fridge may draw 150 W normally, but during startup it may draw:",
            "options": [
                "A) 50 W",
                "B) 600 W or more",
                "C) 1500 W constantly",
                "D) No power at all",
            ],
            "answer": "B",
            "explanation": "Some appliances like fridges draw extra power during startup.",
        },
        {
            "question": "7. Backup energy requirement is calculated as:",
            "options": [
                "A) Power (kW) × Time (hours)",
                "B) Voltage × Current",
                "C) Frequency × Resistance",
                "D) Battery capacity ÷ time",
            ],
            "answer": "A",
            "explanation": "Backup energy required equals power multiplied by runtime.",
        },
        {
            "question": "8. If a system has a 1 kW load and needs 4 hours of backup, the energy needed is:",
            "options": [
                "A) 1 kWh",
                "B) 4 kWh",
                "C) 0.25 kWh",
                "D) 40 kWh",
            ],
            "answer": "B",
            "explanation": "Energy = 1 kW × 4 hours = 4 kWh.",
        },
        {
            "question": "9. Battery size is usually measured in:",
            "options": [
                "A) Volts",
                "B) Kilowatt-hours",
                "C) Hertz",
                "D) Amperes",
            ],
            "answer": "B",
            "explanation": "Battery capacity is usually measured in kilowatt-hours (kWh).",
        },
        {
            "question": "10. The inverter size is mainly based on:",
            "options": [
                "A) Energy storage",
                "B) Instantaneous power demand",
                "C) Battery chemistry",
                "D) Roof tilt",
            ],
            "answer": "B",
            "explanation": "Inverter sizing is based on the power the system must supply at a given moment.",
        },
        {
            "question": "11. Most inverters provide two ratings: continuous power and:",
            "options": [
                "A) Voltage rating",
                "B) Surge rating",
                "C) Colour rating",
                "D) Panel rating",
            ],
            "answer": "B",
            "explanation": "Most inverters have a surge rating for short startup bursts.",
        },
        {
            "question": "12. The battery and inverter must match in:",
            "options": [
                "A) Colour",
                "B) Voltage",
                "C) Cable length",
                "D) Roof position",
            ],
            "answer": "B",
            "explanation": "The inverter and battery must operate at the same system voltage.",
        },
        {
            "question": "13. A solar array must be sized to do more than just run daytime loads because it must also:",
            "options": [
                "A) Look attractive on the roof",
                "B) Recharge the batteries",
                "C) Replace the inverter",
                "D) Reduce load demand",
            ],
            "answer": "B",
            "explanation": "The solar array must also recharge batteries and compensate for losses.",
        },
        {
            "question": "14. Peak Sun Hours are used to estimate:",
            "options": [
                "A) How long the inverter will last",
                "B) The average equivalent hours of full-power solar output per day",
                "C) The battery voltage",
                "D) The cable size",
            ],
            "answer": "B",
            "explanation": "Peak Sun Hours estimate the usable full-power sunlight per day.",
        },
        {
            "question": "15. Which of these is a common source of solar system losses?",
            "options": [
                "A) Inverter efficiency",
                "B) Roof colour",
                "C) Battery brand",
                "D) Load importance",
            ],
            "answer": "A",
            "explanation": "Inverter efficiency is a common source of solar system losses.",
        },
        {
            "question": "16. Undersized cables can cause:",
            "options": [
                "A) Higher efficiency",
                "B) Voltage drop and overheating",
                "C) More sunshine",
                "D) Lower battery voltage rating",
            ],
            "answer": "B",
            "explanation": "Undersized cables cause voltage drop and overheating.",
        },
        {
            "question": "17. Voltage drop happens because:",
            "options": [
                "A) The cable is too short",
                "B) Cable resistance causes energy loss as current flows",
                "C) The battery is oversized",
                "D) The inverter is off",
            ],
            "answer": "B",
            "explanation": "Voltage drop is caused by resistance in the cable as current flows.",
        },
        {
            "question": "18. A key compatibility issue between inverter and battery is:",
            "options": [
                "A) Same physical size",
                "B) Communication protocol compatibility",
                "C) Same colour",
                "D) Same roof position",
            ],
            "answer": "B",
            "explanation": "Communication compatibility between inverter and BMS is essential.",
        },
        {
            "question": "19. Poor system design often causes:",
            "options": [
                "A) Nuisance tripping and instability",
                "B) More sunshine",
                "C) Lower battery capacity",
                "D) Higher roof temperature",
            ],
            "answer": "A",
            "explanation": "Poor system design often causes nuisance tripping and unstable behaviour.",
        },
        {
            "question": "20. A system should consider future expansion because:",
            "options": [
                "A) Future loads may increase",
                "B) Batteries will always shrink",
                "C) Solar panels never age",
                "D) Inverters become lighter",
            ],
            "answer": "A",
            "explanation": "Good design considers future appliances, batteries and solar expansion.",
        },
        {
            "question": "21. Installers usually recommend a larger battery than the minimum to:",
            "options": [
                "A) Reduce battery stress and improve lifespan",
                "B) Increase panel voltage",
                "C) Lower inverter size",
                "D) Avoid using a BMS",
            ],
            "answer": "A",
            "explanation": "A larger battery reduces stress, improves runtime stability and allows headroom.",
        },
        {
            "question": "22. If an inverter is much larger than the battery, the likely problem is:",
            "options": [
                "A) Better battery life",
                "B) Excessive battery stress and possible protection trips",
                "C) More sunshine",
                "D) Smaller cable size",
            ],
            "answer": "B",
            "explanation": "A very large inverter with a small battery can demand too much current and trigger protection.",
        },
        {
            "question": "23. Proper system design improves battery life by:",
            "options": [
                "A) Avoiding constant high stress and deep cycling",
                "B) Using the smallest possible battery",
                "C) Removing the inverter",
                "D) Increasing panel tilt",
            ],
            "answer": "A",
            "explanation": "Good design avoids constant high stress and deep discharge to preserve battery life.",
        },
        {
            "question": "24. Real-world system design examples are useful because they:",
            "options": [
                "A) Show how theory applies in practice",
                "B) Replace the need for calculations",
                "C) Avoid using load assessments",
                "D) Make the system more expensive",
            ],
            "answer": "A",
            "explanation": "Examples help illustrate how design principles are applied in real installations.",
        },
        {
            "question": "25. One common installer mistake is failing to account for:",
            "options": [
                "A) Startup surges and cable sizing",
                "B) Solar panel colour",
                "C) Roof angle",
                "D) Battery brand logo",
            ],
            "answer": "A",
            "explanation": "Failing to account for startup surges and correct cable sizing is a common mistake.",
        },
    ],
}

class CapacityAndDOD:'''
text = text.replace(old, new_content)
path.write_text(text, encoding='utf-8')
print('MODULE_5 inserted successfully')
