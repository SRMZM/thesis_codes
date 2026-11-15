# -*- coding: utf-8 -*-
"""
Created on Mon Aug 24 18:35:06 2026

@author: Russell
"""
"""
Test for IntersectionAnalyzer
"""

from intersection_analyzer import IntersectionAnalyzer


# =========================================================
# 1. Create a test intersection polygon
# =========================================================

polygon = [
    (300, 200),   # North-West
    (700, 200),   # North-East
    (700, 500),   # South-East
    (300, 500)    # South-West
]


# =========================================================
# 2. Create the analyzer
# =========================================================

analyzer = IntersectionAnalyzer(
    polygon
)


# =========================================================
# 3. Create a test trajectory
# =========================================================

trajectory = [

    # Outside the intersection.
    (500, 100),

    # Still outside.
    (500, 150),

    # Moving toward the North side.
    (500, 180),

    # Inside the intersection.
    (500, 230),

    # Moving toward the West side.
    (450, 280),
    (400, 330),
    (350, 380),

    # Outside through the West side.
    (280, 420)
]


# =========================================================
# 4. Analyze the trajectory
# =========================================================

result = analyzer.analyze(
    trajectory
)


# =========================================================
# 5. Print the result
# =========================================================

# =========================================================
# 5. Print the result
# =========================================================

print()
print("========================================")
print("Intersection Analysis Result")
print("========================================")

if result is None:

    print("No complete intersection event was detected.")

else:

    print(
        "Entry Side:",
        result["entry_side"]
    )

    print(
        "Entry Point:",
        result["entry_point"]
    )

    print(
        "Entry Index:",
        result["entry_index"]
    )

    print(
        "Exit Side:",
        result["exit_side"]
    )

    print(
        "Exit Point:",
        result["exit_point"]
    )

    print(
        "Exit Index:",
        result["exit_index"]
    )

print("========================================")


# =========================================================
# TEST 2
# North -> South
# =========================================================

trajectory_2 = [

    # Outside the intersection.
    (500, 100),

    # Moving toward the North side.
    (500, 150),
    (500, 180),

    # Inside the intersection.
    (500, 230),
    (500, 300),
    (500, 400),

    # Moving toward the South side.
    (500, 480),

    # Outside through the South side.
    (500, 550)
]


result_2 = analyzer.analyze(
    trajectory_2
)


print()
print("========================================")
print("TEST 2: North -> South")
print("========================================")

if result_2 is None:

    print("No complete intersection event was detected.")

else:

    print(
        "Entry Side:",
        result_2["entry_side"]
    )

    print(
        "Entry Point:",
        result_2["entry_point"]
    )

    print(
        "Exit Side:",
        result_2["exit_side"]
    )

    print(
        "Exit Point:",
        result_2["exit_point"]
    )
    
    
# =========================================================
# TEST 3
# East -> North
# =========================================================

trajectory_3 = [

    # Outside the intersection.
    (800, 400),

    # Moving toward the East side.
    (750, 380),
    (720, 350),

    # Inside the intersection.
    (650, 320),
    (580, 280),
    (520, 240),

    # Moving toward the North side.
    (450, 210),

    # Outside through the North side.
    (450, 150)
]


result_3 = analyzer.analyze(
    trajectory_3
)


print()
print("========================================")
print("TEST 3: East -> North")
print("========================================")

if result_3 is None:

    print("No complete intersection event was detected.")

else:

    print(
        "Entry Side:",
        result_3["entry_side"]
    )

    print(
        "Entry Point:",
        result_3["entry_point"]
    )

    print(
        "Exit Side:",
        result_3["exit_side"]
    )

    print(
        "Exit Point:",
        result_3["exit_point"]
    )
    
    
# =========================================================
# TEST 4
# Vehicle never enters the intersection
# =========================================================

trajectory_4 = [

    # Vehicle moves above the intersection.
    (100, 100),
    (200, 120),
    (300, 130),
    (400, 140),
    (500, 150),
    (600, 160),
    (700, 170)
]


result_4 = analyzer.analyze(
    trajectory_4
)


print()
print("========================================")
print("TEST 4: Never enters intersection")
print("========================================")

if result_4 is None:

    print(
        "PASS: No intersection event detected."
    )

else:

    print(
        "FAIL: An intersection event was detected."
    )

    print(result_4)
    
    
# =========================================================
# TEST 5
# Vehicle enters but does not exit yet
# =========================================================

trajectory_5 = [

    # Outside the intersection.
    (500, 100),
    (500, 150),
    (500, 180),

    # Vehicle enters the intersection.
    (500, 220),
    (500, 300),
    (500, 400)
]


result_5 = analyzer.analyze(
    trajectory_5
)


print()
print("========================================")
print("TEST 5: Enters but does not exit")
print("========================================")

if result_5 is None:

    print(
        "PASS: No complete event yet."
    )

else:

    print(
        "FAIL: A complete event was detected."
    )

    print(result_5)