"""
Created on Mon Aug 24 18:19:30 2026

@author: Russell
"""

# -*- coding: utf-8 -*-
"""
Intersection Analyzer

This module analyzes a vehicle trajectory and determines:
1. Entry side of the intersection.
2. Exit side of the intersection.
3. Entry and exit points.
4. Entry and exit frame indexes.
"""

from test_polygon import is_inside_polygon
from geometry import calculate_segment_intersection


class IntersectionAnalyzer:

    def __init__(self, polygon):

        # Store the intersection polygon.
        self.polygon = polygon

        # The polygon points are stored in this order:
        # North -> East -> South -> West.
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

    def _find_crossing_side(self, p1, p2):

        # Check the trajectory segment against
        # every polygon side.
        for side_name, side in self.sides.items():

            # Get the two endpoints of the polygon side.
            side_p1 = side[0]
            side_p2 = side[1]

            # Calculate the intersection between
            # the trajectory segment and polygon side.
            intersection = calculate_segment_intersection(
                p1,
                p2,
                side_p1,
                side_p2
            )

            # If an intersection exists,
            # this is the crossing side.
            if intersection is not None:

                return side_name, intersection

        # No polygon side was crossed.
        return None, None

    def analyze(self, trajectory):

        # Return no result if the trajectory
        # contains fewer than two points.
        if len(trajectory) < 2:
            return None

        # Store whether the vehicle has entered
        # the intersection.
        entered = False

        # Store entry information.
        entry_side = None
        entry_point = None
        entry_index = None

        # Store exit information.
        exit_side = None
        exit_point = None
        exit_index = None

        # Get the first trajectory point.
        previous_point = trajectory[0]

        # Determine whether the first point
        # is inside the polygon.
        previous_inside = is_inside_polygon(
            previous_point,
            self.polygon
        )

        # Process every following trajectory point.
        for i in range(1, len(trajectory)):

            # Get the current trajectory point.
            current_point = trajectory[i]

            # Determine whether the current point
            # is inside the polygon.
            current_inside = is_inside_polygon(
                current_point,
                self.polygon
            )

            # -------------------------------------------------
            # Detect entry: OUTSIDE -> INSIDE
            # -------------------------------------------------

            if (
                not previous_inside
                and current_inside
                and not entered
            ):

                # Find the polygon side crossed by
                # the vehicle trajectory.
                side_name, intersection = (
                    self._find_crossing_side(
                        previous_point,
                        current_point
                    )
                )

                # Make sure a crossing side was found.
                if side_name is not None:

                    # Store entry information.
                    entry_side = side_name
                    entry_point = intersection
                    entry_index = i

                    # Mark the vehicle as inside.
                    entered = True

            # -------------------------------------------------
            # Detect exit: INSIDE -> OUTSIDE
            # -------------------------------------------------

            elif (
                previous_inside
                and not current_inside
                and entered
            ):

                # Find the polygon side crossed by
                # the vehicle trajectory.
                side_name, intersection = (
                    self._find_crossing_side(
                        previous_point,
                        current_point
                    )
                )

                # Make sure a crossing side was found.
                if side_name is not None:

                    # Store exit information.
                    exit_side = side_name
                    exit_point = intersection
                    exit_index = i

                    # The complete intersection event
                    # has now been detected.
                    break

            # Update the previous point.
            previous_point = current_point

            # Update the previous inside/outside state.
            previous_inside = current_inside

        # Return no result if a complete
        # entry and exit event was not detected.
        if (
            entry_side is None
            or exit_side is None
        ):
            return None

        # Return the complete intersection event.
        return {

            "entry_side": entry_side,
            "entry_point": entry_point,
            "entry_index": entry_index,

            "exit_side": exit_side,
            "exit_point": exit_point,
            "exit_index": exit_index
        }