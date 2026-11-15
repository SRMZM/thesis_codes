"""
Created on Wed Aug 26 16:26:29 2026

@author: Russell
"""

# -*- coding: utf-8 -*-
"""
Tests for final_decision.py
"""

from final_decision import determine_violation


def run_test(
    test_name,
    movement,
    entry_forbidden,
    expected
):

    # Determine the final result.
    result = determine_violation(
        movement,
        entry_forbidden
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
        "Movement:",
        movement
    )

    print(
        "Entry Forbidden:",
        entry_forbidden
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
# LEFT TURN
# =========================================================

run_test(
    "Test 1 - Illegal Left Turn",
    "LEFT TURN",
    True,
    "ILLEGAL LEFT TURN"
)

run_test(
    "Test 2 - Legal Left Turn",
    "LEFT TURN",
    False,
    "LEGAL LEFT TURN"
)

# =========================================================
# U-TURN
# =========================================================

run_test(
    "Test 3 - Illegal U-Turn",
    "U-TURN",
    True,
    "ILLEGAL U-TURN"
)

run_test(
    "Test 4 - Legal U-Turn",
    "U-TURN",
    False,
    "LEGAL U-TURN"
)

# =========================================================
# RIGHT TURN
# =========================================================

run_test(
    "Test 5 - Right Turn From Forbidden Entry",
    "RIGHT TURN",
    True,
    "RIGHT TURN"
)

run_test(
    "Test 6 - Right Turn From Allowed Entry",
    "RIGHT TURN",
    False,
    "RIGHT TURN"
)

# =========================================================
# STRAIGHT
# =========================================================

run_test(
    "Test 7 - Straight From Forbidden Entry",
    "STRAIGHT",
    True,
    "STRAIGHT"
)

run_test(
    "Test 8 - Straight From Allowed Entry",
    "STRAIGHT",
    False,
    "STRAIGHT"
)

# =========================================================
# ANALYZING
# =========================================================

run_test(
    "Test 9 - Analyzing",
    "ANALYZING",
    False,
    "ANALYZING"
)

run_test(
    "Test 10 - Unknown Movement",
    "UNKNOWN",
    False,
    "ANALYZING"
)