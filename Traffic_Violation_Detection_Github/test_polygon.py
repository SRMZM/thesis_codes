# -*- coding: utf-8 -*-
"""
Created on Mon Aug 17 10:47:48 2026

@author: Russell
"""

import cv2
import json
import numpy as np

def load_polygon(filename):

    # Open the JSON file for reading.
    with open(filename, "r") as file:

        # Read the JSON data.
        data = json.load(file)

    # Get the polygon points.
    polygon = data["polygon"]

    # Convert the points into the format
    # required by OpenCV.
    polygon = [tuple(point) for point in polygon]

    return polygon


def is_inside_polygon(point, polygon):

    # Convert polygon to a NumPy array.
    polygon_array = np.array(
        polygon,
        dtype=np.int32
    )

    # Check the position of the point.
    result = cv2.pointPolygonTest(
        polygon_array,
        point,
        False
    )

    # Return True if the point is inside
    # or exactly on the polygon boundary.
    return result >= 0


# Test functions
# =============================================================================
# test_points = [
#     (900, 500),
#     (300, 300),
#     (650, 350)
# ]
# 
# polygon = load_polygon(
#     "intersection_polygon.json"
#     )
# 
# for point in test_points:
#     
#     result = is_inside_polygon(
#         point,
#         polygon
#     )
#     
#     print(result)
# =============================================================================
