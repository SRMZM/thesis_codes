"""
Created on Wed Aug 26 16:24:08 2026

@author: Russell
"""

# -*- coding: utf-8 -*-
"""
Final Violation Decision

This module determines the final traffic violation
based on the vehicle movement and entry status.
"""


def determine_violation(
    movement,
    entry_forbidden
):

    # Check for an illegal left turn.
    if (
        movement == "LEFT TURN"
        and entry_forbidden
    ):

        return "ILLEGAL LEFT TURN"


    # Check for an illegal U-turn.
    if (
        movement == "U-TURN"
        and entry_forbidden
    ):

        return "ILLEGAL U-TURN"


    # A left turn through an allowed entry.
    if movement == "LEFT TURN":

        return "LEGAL LEFT TURN"


    # A U-turn through an allowed entry.
    if movement == "U-TURN":

        return "LEGAL U-TURN"


    # A right turn is not one of
    # the violations defined in this project.
    if movement == "RIGHT TURN":

        return "RIGHT TURN"


    # Straight movement is not one of
    # the violations defined in this project.
    if movement == "STRAIGHT":

        return "STRAIGHT"


    # Return ANALYZING for an unknown or
    # not-yet-stable movement.
    return "ANALYZING"