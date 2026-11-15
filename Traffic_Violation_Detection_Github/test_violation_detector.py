# -*- coding: utf-8 -*-
"""
Created on Tue Aug 25 17:11:27 2026

@author: Russell
"""

# -*- coding: utf-8 -*-
"""
Tests for ViolationDetector
"""

from test_polygon import load_polygon

from violation_detector import (
    load_forbidden_boundaries,
    ViolationDetector
)


# =========================================================
# Load polygon
# =========================================================

polygon = load_polygon(
    "intersection_polygon.json"
)


# =========================================================
# Load forbidden boundaries
# =========================================================

forbidden_boundaries = load_forbidden_boundaries(
    "forbidden_boundaries.json"
)


# =========================================================
# Create violation detector
# =========================================================

detector = ViolationDetector(
    polygon,
    forbidden_boundaries
)



def run_test(
    test_name,
    entry_side,
    entry_point,
    expected
):

    # Run the violation detector.
    result = detector.is_entry_forbidden(
        entry_side,
        entry_point
    )

    # Check whether the result is correct.
    if result == expected:

        status = "PASS"

    else:

        status = "FAIL"

    # Display the test result.
    print()
    print("========================================")
    print(test_name)
    print("========================================")

    print(
        "Entry Side:",
        entry_side
    )

    print(
        "Entry Point:",
        entry_point
    )

    print(
        "Expected:",
        expected
    )

    print(
        "Actual:",
        result
    )

    print(
        "Result:",
        status
    )
    
    

def point_between(
    p1,
    p2,
    ratio
):

    # Calculate the X coordinate.
    x = (
        p1[0]
        + ratio * (p2[0] - p1[0])
    )

    # Calculate the Y coordinate.
    y = (
        p1[1]
        + ratio * (p2[1] - p1[1])
    )

    # Return the generated point.
    return (
        int(x),
        int(y)
    )



p0 = polygon[0]
p1 = polygon[1]
p2 = polygon[2]
p3 = polygon[3]

north_boundary = tuple(
    forbidden_boundaries["north"]
)


north_forbidden_point = point_between(
    p0,
    north_boundary,
    0.5
)

run_test(
    "TEST 1 - North - Forbidden Side",
    "north",
    north_forbidden_point,
    True
)

north_allowed_point = point_between(
    north_boundary,
    p1,
    0.5
)

run_test(
    "TEST 2 - North - Allowed Side",
    "north",
    north_allowed_point,
    False
)


east_boundary = tuple(
    forbidden_boundaries["east"]
)

east_forbidden_point = point_between(
    p1,
    east_boundary,
    0.5
)

run_test(
    "TEST 3 - East - Forbidden Side",
    "east",
    east_forbidden_point,
    True
)

east_allowed_point = point_between(
    east_boundary,
    p2,
    0.5
)

run_test(
    "TEST 4 - East - Allowed Side",
    "east",
    east_allowed_point,
    False
)

south_boundary = tuple(
    forbidden_boundaries["south"]
)

south_forbidden_point = point_between(
    p2,
    south_boundary,
    0.5
)

run_test(
    "TEST 5 - South - Forbidden Side",
    "south",
    south_forbidden_point,
    True
)

south_allowed_point = point_between(
    south_boundary,
    p3,
    0.5
)

run_test(
    "TEST 6 - South - Allowed Side",
    "south",
    south_allowed_point,
    False
)

west_boundary = tuple(
    forbidden_boundaries["west"]
)

west_forbidden_point = point_between(
    p3,
    west_boundary,
    0.5
)

run_test(
    "TEST 7 - West - Forbidden Side",
    "west",
    west_forbidden_point,
    True
)

west_allowed_point = point_between(
    west_boundary,
    p0,
    0.5
)

run_test(
    "TEST 8 - West - Allowed Side",
    "west",
    west_allowed_point,
    False
)













