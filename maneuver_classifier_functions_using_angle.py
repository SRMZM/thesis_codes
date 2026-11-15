# -*- coding: utf-8 -*-
"""
Created on Tue Aug 18 18:16:29 2026

@author: Russell
"""

import math


# =========================================================
# 1. Calculate the heading angle of a moving object
# =========================================================

def calculate_heading(point1, point2):

    # Extract coordinates of the first point.
    x1, y1 = point1

    # Extract coordinates of the second point.
    x2, y2 = point2

    # Calculate movement in X direction.
    dx = x2 - x1

    # Calculate movement in Y direction.
    dy = y2 - y1

    # Calculate the angle in radians.
    angle = math.atan2(dy, dx)

    # Convert radians to degrees.
    angle = math.degrees(angle)

    return angle


# =========================================================
# 2. Calculate signed difference between two angles
# =========================================================

def signed_angle_difference(angle1, angle2):

    # Calculate the difference between the two angles.
    difference = angle2 - angle1

    # Keep the result inside the range [-180, 180].
    if difference > 180:
        difference -= 360

    elif difference < -180:
        difference += 360

    return difference


# =========================================================
# 3. Classify the vehicle maneuver
# =========================================================

def classify_maneuver(trajectory):

    # We need enough points to make a reliable decision.
    if len(trajectory) < 10:
        return "UNKNOWN"


    # Get the number of trajectory points.
    n = len(trajectory)


    # Use 30% of the trajectory for the initial
    # and final heading calculations.
    segment_size = max(3, int(n * 0.3))


    # Get the beginning part of the trajectory.
    start_points = trajectory[:segment_size]


    # Get the ending part of the trajectory.
    end_points = trajectory[-segment_size:]


    # Calculate the initial heading.
    start_heading = calculate_heading(
        start_points[0],
        start_points[-1]
    )


    # Calculate the final heading.
    end_heading = calculate_heading(
        end_points[0],
        end_points[-1]
    )


    # Calculate the signed change in heading.
    turn_angle = signed_angle_difference(
        start_heading,
        end_heading
    )


    # Calculate the absolute angle.
    absolute_angle = abs(turn_angle)


    # -----------------------------------------
    # Straight movement
    # -----------------------------------------

    if absolute_angle < 15:
        return "STRAIGHT"


    # -----------------------------------------
    # Approximately 90-degree turn
    # -----------------------------------------

    elif 60 <= absolute_angle <= 120:

        # Positive angle means right turn
        # under our current image-coordinate convention.
        if turn_angle > 0:
            return "RIGHT_TURN"

        # Negative angle means left turn.
        else:
            return "LEFT_TURN"


    # -----------------------------------------
    # Approximately 180-degree turn
    # -----------------------------------------

    elif absolute_angle >= 150:
        return "U_TURN"


    # -----------------------------------------
    # Other movements
    # -----------------------------------------

    else:
        return "LANE_CHANGE_OR_UNKNOWN"

# =========================================================
# Calculate stable maneuver (not instant maneuver)
# =========================================================

def get_stable_maneuver(maneuvers):

    # If there are no predictions, return UNKNOWN.
    if not maneuvers:
        return "UNKNOWN"

    # Count how many times each maneuver appears.
    counts = {}

    for maneuver in maneuvers:

        if maneuver not in counts:
            counts[maneuver] = 0

        counts[maneuver] += 1

    # Find the maneuver with the highest count.
    stable_maneuver = max(
        counts,
        key=counts.get
    )

    return stable_maneuver

