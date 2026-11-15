"""
Created on Wed Aug 26 15:29:10 2026

@author: Russell
"""

# -*- coding: utf-8 -*-
"""
Movement Classifier

This module determines the type of vehicle
movement from its entry side and exit side.
"""


def classify_movement(
    entry_side,
    exit_side
):

    # Define the fixed order of intersection sides.
    sides = [
        "north",
        "east",
        "south",
        "west"
    ]

    # Find the index of the entry side.
    entry_index = sides.index(
        entry_side
    )

    # Find the index of the exit side.
    exit_index = sides.index(
        exit_side
    )

    # Calculate the relative movement.
    difference = (
        exit_index - entry_index
    ) % 4

    # Same entry and exit side means U-turn.
    if difference == 0:

        return "U-TURN"

    # One side clockwise means left turn.
    elif difference == 1:

        return "LEFT TURN"

    # Two sides apart means going straight.
    elif difference == 2:

        return "STRAIGHT"

    # Three sides clockwise is a right turn.
    elif difference == 3:

        return "RIGHT TURN"
    
    