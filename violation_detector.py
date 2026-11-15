"""
Created on Tue Aug 25 16:52:42 2026

@author: Russell
"""

# -*- coding: utf-8 -*-
"""
Violation Detector

This module loads forbidden boundaries
and determines whether a vehicle entered
the intersection through a forbidden part.
"""

import json


def load_forbidden_boundaries(filename):
    """
    Load forbidden boundaries from a JSON file.
    """

    # Open the JSON file.
    with open(
        filename,
        "r",
        encoding="utf-8"
    ) as file:

        # Convert JSON data into a Python object.
        forbidden_boundaries = json.load(file)

    # Return the loaded boundaries.
    return forbidden_boundaries


class ViolationDetector:

    def __init__(
        self,
        polygon,
        forbidden_boundaries
    ):

        # Store the intersection polygon.
        self.polygon = polygon

        # Store the forbidden boundary points.
        self.forbidden_boundaries = (
            forbidden_boundaries
        )

        # Define polygon sides according to
        # the fixed polygon point order.
        #
        # P0 -> P1 = North
        # P1 -> P2 = East
        # P2 -> P3 = South
        # P3 -> P0 = West

        self.sides = {

            "north": (
                self.polygon[0],
                self.polygon[1]
            ),

            "east": (
                self.polygon[1],
                self.polygon[2]
            ),

            "south": (
                self.polygon[2],
                self.polygon[3]
            ),

            "west": (
                self.polygon[3],
                self.polygon[0]
            )
        }


    def _is_between(
        self,
        point,
        p1,
        p2
    ):

        # Check whether the point lies between
        # p1 and p2 in the X direction.
        x_between = (
            min(p1[0], p2[0])
            <= point[0]
            <= max(p1[0], p2[0])
        )

        # Check whether the point lies between
        # p1 and p2 in the Y direction.
        y_between = (
            min(p1[1], p2[1])
            <= point[1]
            <= max(p1[1], p2[1])
        )

        # Return True only if both conditions
        # are satisfied.
        return x_between and y_between


    def is_entry_forbidden(
        self,
        entry_side,
        entry_point
    ):

        # Get the two vertices of the entry side.
        side_start, side_end = self.sides[
            entry_side
        ]

        # Get the forbidden boundary point
        # belonging to this side.
        boundary_point = (
            self.forbidden_boundaries[
                entry_side
            ]
        )

        # The part between the first vertex
        # and the forbidden boundary is forbidden.
        forbidden_side = self._is_between(
            entry_point,
            side_start,
            boundary_point
        )

        # Return the final result.
        return forbidden_side
    

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