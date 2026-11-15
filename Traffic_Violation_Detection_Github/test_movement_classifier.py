"""
Created on Wed Aug 26 15:37:59 2026

@author: Russell
"""

# -*- coding: utf-8 -*-
"""
Tests for movement_classifier.py
"""

from movement_classifier import classify_movement


def run_test(
    test_name,
    entry_side,
    exit_side,
    expected
):

    # Classify the movement.
    result = classify_movement(
        entry_side,
        exit_side
    )

    # Compare the result with the expected value.
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
        "Entry:",
        entry_side
    )

    print(
        "Exit:",
        exit_side
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


# =========================================================
# North
# =========================================================

run_test(
    "Test 1",
    "north",
    "north",
    "U-TURN"
)

run_test(
    "Test 2",
    "north",
    "east",
    "LEFT TURN"
)

run_test(
    "Test 3",
    "north",
    "south",
    "STRAIGHT"
)

run_test(
    "Test 4",
    "north",
    "west",
    "RIGHT TURN"
)


# =========================================================
# East
# =========================================================

run_test(
    "Test 5",
    "east",
    "east",
    "U-TURN"
)

run_test(
    "Test 6",
    "east",
    "south",
    "LEFT TURN"
)

run_test(
    "Test 7",
    "east",
    "west",
    "STRAIGHT"
)

run_test(
    "Test 8",
    "east",
    "north",
    "RIGHT TURN"
)


# =========================================================
# South
# =========================================================

run_test(
    "Test 9",
    "south",
    "south",
    "U-TURN"
)

run_test(
    "Test 10",
    "south",
    "west",
    "LEFT TURN"
)

run_test(
    "Test 11",
    "south",
    "north",
    "STRAIGHT"
)

run_test(
    "Test 12",
    "south",
    "east",
    "RIGHT TURN"
)


# =========================================================
# West
# =========================================================

run_test(
    "Test 13",
    "west",
    "west",
    "U-TURN"
)

run_test(
    "Test 14",
    "west",
    "north",
    "LEFT TURN"
)

run_test(
    "Test 15",
    "west",
    "east",
    "STRAIGHT"
)

run_test(
    "Test 16",
    "west",
    "south",
    "RIGHT TURN"
)