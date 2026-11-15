# -*- coding: utf-8 -*-
"""
Created on Thu Aug 13 17:40:00 2026

@author: Russell
"""

import cv2
import numpy as np
from maneuver_classifier import calculate_heading


# -----------------------------------------
# 1. Define the trajectories
# -----------------------------------------

straight_trajectory = [
    (500, 500),
    (500, 480),
    (500, 460),
    (500, 440),
    (500, 420),
    (500, 400),
    (500, 380),
    (500, 360),
    (500, 340),
    (500, 320),
]


right_turn_trajectory = [
    (500, 500),
    (500, 480),
    (500, 460),
    (500, 440),
    (500, 420),
    (500, 400),
    (520, 380),
    (540, 380),
    (560, 380),
    (580, 380),
    (600, 380),
]


left_turn_trajectory = [
    (500, 500),
    (500, 480),
    (500, 460),
    (500, 440),
    (500, 420),
    (500, 400),
    (480, 380),
    (460, 380),
    (440, 380),
    (420, 380),
    (400, 380),
]


u_turn_trajectory = [
    (500, 500),
    (500, 480),
    (500, 460),
    (500, 440),
    (500, 420),
    (500, 400),
    (480, 380),
    (460, 370),
    (440, 380),
    (430, 400),
    (430, 420),
    (430, 440),
    (430, 460),
]


lane_change_trajectory = [
    (500, 500),
    (505, 480),
    (510, 460),
    (515, 440),
    (520, 420),
    (525, 400),
    (535, 380),
    (545, 360),
    (555, 340),
    (565, 320),
    (575, 300),
]


# -----------------------------------------
# 2. Create a blank image
# -----------------------------------------

# Create a white image with:
# height = 800 pixels
# width  = 1000 pixels
# channels = 3 (BGR)
image = np.ones((800, 1000, 3), dtype = np.uint8) * 255


# -----------------------------------------
# 3. Draw the trajectories
# -----------------------------------------

trajectories = [
    # ("STRAIGHT", straight_trajectory),
    # ("RIGHT TURN", right_turn_trajectory),
    # ("LEFT TURN", left_turn_trajectory),
    ("U-TURN", u_turn_trajectory),
    # ("LANE CHANGE", lane_change_trajectory)
]


for name, points in trajectories:

    # Draw every point.
    for point in points:

        cv2.circle(
            image,
            point,
            4,
            (0, 0, 255),
            -1
        )


    # Connect consecutive points.
    for i in range(1, len(points)):

        cv2.line(
            image,
            points[i - 1],
            points[i],
            (255, 0, 0),
            2
        )

        heading = calculate_heading(
            points[i - 1],
            points[i]
            )
    
        cv2.putText(
            image,
            f"{heading:.1f}",
            points[i],
            cv2.FONT_HERSHEY_SIMPLEX,
            0.4,
            (0, 0, 0),
            5
            )

    # Write the name of the trajectory.
    end_point = points[-1]

    cv2.putText(
        image,
        name,
        end_point,
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (0, 255, 0),
        2
    )


# -----------------------------------------
# 4. Display the image
# -----------------------------------------

cv2.imshow("Synthetic Trajectories", image)


# Wait until a key is pressed.
cv2.waitKey(0)


# Close the window.
cv2.destroyAllWindows()