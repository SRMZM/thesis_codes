# -*- coding: utf-8 -*-
"""
Created on Fri Aug 21 15:20:36 2026

@author: Russell
"""

import cv2
import json

from geometry import calculate_segment_intersection


# =========================================================
# Global variables
# =========================================================

# Store the two points selected by the user
# for the current edge.
user_points = []


# Store the calculated intersection point.
intersection_point = None


# Store the polygon points.
polygon_points = []


# Current edge index.
current_edge = 0


# =========================================================
# Polygon edges
# =========================================================

# The polygon points are assumed to be stored
# in clockwise order:
#
# P0 → P1 → P2 → P3
#
# Therefore:
#
# North = P0 → P1
# East  = P1 → P2
# South = P2 → P3
# West  = P3 → P0

edge_names = [
    "NORTH",
    "EAST",
    "SOUTH",
    "WEST"
]


# =========================================================
# Mouse callback
# =========================================================

def mouse_callback(event, x, y, flags, param):

    global intersection_point

    # Check whether the left mouse button was clicked.
    if event == cv2.EVENT_LBUTTONDOWN:

        # We only need two points.
        if len(user_points) < 2:

            # Store the clicked point.
            user_points.append((x, y))

            print(
                f"Point {len(user_points)}: ({x}, {y})"
            )

            # Once two points are selected,
            # calculate their intersection with the edge.
            if len(user_points) == 2:

                # Get the current polygon edge.
                edge_start = polygon_points[current_edge]

                edge_end = polygon_points[
                    (current_edge + 1) % len(polygon_points)
                ]

                # Get the two user-selected points.
                user_start = user_points[0]
                user_end = user_points[1]

                # Calculate the intersection.
                intersection_point = calculate_segment_intersection(
                    edge_start,
                    edge_end,
                    user_start,
                    user_end
                )

                # Check whether an intersection was found.
                if intersection_point is None:

                    print(
                        "No valid intersection found."
                    )

                else:

                    print(
                        f"Intersection: "
                        f"{intersection_point}"
                    )


# =========================================================
# Load polygon from JSON
# =========================================================

def load_polygon(filename):

    # Open the JSON file.
    with open(filename, "r") as file:

        # Read the JSON data.
        data = json.load(file)

    # Convert polygon points to tuples.
    polygon = [
        tuple(point)
        for point in data["polygon"]
    ]

    return polygon


# =========================================================
# Save boundaries to JSON
# =========================================================

def save_boundaries(boundaries, filename):

    # Open the output JSON file.
    with open(filename, "w") as file:

        # Save the boundary points.
        json.dump(
            boundaries,
            file,
            indent=4
        )

    print(
        f"Boundaries saved to: {filename}"
    )


# =========================================================
# Load polygon
# =========================================================

polygon_file = "intersection_polygon.json"

polygon_points = load_polygon(
    polygon_file
)


# =========================================================
# Check polygon
# =========================================================

if len(polygon_points) < 4:

    print(
        "Error: Polygon must contain at least 4 points."
    )

    exit()


# =========================================================
# Create video capture
# =========================================================

video_path = "videos/Takhti_3.asf"

cap = cv2.VideoCapture(video_path)


if not cap.isOpened():

    print(
        "Error: Could not open the video."
    )

    exit()


# =========================================================
# Read first frame
# =========================================================

ret, frame = cap.read()


if not ret:

    print(
        "Error: Could not read video frame."
    )

    cap.release()

    exit()


# Store the original frame.
original_frame = frame.copy()


# =========================================================
# Create window
# =========================================================

window_name = "Forbidden Boundary Selector"

cv2.namedWindow(
    window_name,
    cv2.WINDOW_NORMAL
)


cv2.setMouseCallback(
    window_name,
    mouse_callback
)


# =========================================================
# Main loop
# =========================================================

boundaries = {}


while True:

    # Create a fresh copy of the original frame.
    display_frame = original_frame.copy()


    # -----------------------------------------------------
    # Draw the complete polygon
    # -----------------------------------------------------

    for i in range(len(polygon_points)):

        start = polygon_points[i]

        end = polygon_points[
            (i + 1) % len(polygon_points)
        ]

        cv2.line(
            display_frame,
            start,
            end,
            (255, 0, 0),
            2
        )


    # -----------------------------------------------------
    # Get current edge
    # -----------------------------------------------------

    edge_start = polygon_points[current_edge]

    edge_end = polygon_points[
        (current_edge + 1) % len(polygon_points)
    ]


    # -----------------------------------------------------
    # Highlight current edge
    # -----------------------------------------------------

    cv2.line(
        display_frame,
        edge_start,
        edge_end,
        (0, 255, 255),
        5
    )


    # -----------------------------------------------------
    # Draw polygon points
    # -----------------------------------------------------

    for i, point in enumerate(polygon_points):

        cv2.circle(
            display_frame,
            point,
            6,
            (0, 0, 255),
            -1
        )

        cv2.putText(
            display_frame,
            f"P{i}",
            (
                point[0] + 8,
                point[1] - 8
            ),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (255, 255, 255),
            2
        )


    # -----------------------------------------------------
    # Draw user-selected points
    # -----------------------------------------------------

    for point in user_points:

        cv2.circle(
            display_frame,
            point,
            7,
            (0, 255, 0),
            -1
        )


    # -----------------------------------------------------
    # Draw the line between user points
    # -----------------------------------------------------

    if len(user_points) == 2:

        cv2.line(
            display_frame,
            user_points[0],
            user_points[1],
            (0, 255, 0),
            2
        )


    # -----------------------------------------------------
    # Draw intersection point
    # -----------------------------------------------------

    if intersection_point is not None:

        cv2.circle(
            display_frame,
            intersection_point,
            9,
            (255, 0, 255),
            -1
        )


    # -----------------------------------------------------
    # Display instructions
    # -----------------------------------------------------

    instruction = (
        f"{edge_names[current_edge]}: "
        f"P{current_edge} -> "
        f"P{(current_edge + 1) % len(polygon_points)}"
    )


    cv2.putText(
        display_frame,
        instruction,
        (20, 30),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (0, 255, 0),
        2
    )


    cv2.putText(
        display_frame,
        "Click two points | Enter: Confirm | R: Reset | ESC: Exit",
        (20, 60),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.6,
        (0, 255, 0),
        2
    )


    # -----------------------------------------------------
    # Show frame
    # -----------------------------------------------------

    cv2.imshow(
        window_name,
        display_frame
    )


    # -----------------------------------------------------
    # Keyboard input
    # -----------------------------------------------------

    key = cv2.waitKey(20) & 0xFF


    # =====================================================
    # ENTER → Confirm current boundary
    # =====================================================

    if key == 13:

        # Make sure two points were selected.
        if len(user_points) != 2:

            print(
                "Please select two points first."
            )

            continue


        # Make sure a valid intersection exists.
        if intersection_point is None:

            print(
                "Invalid boundary."
            )

            continue


        # Store the boundary point.
        boundaries[
            edge_names[current_edge].lower()
        ] = list(intersection_point)


        print(
            f"{edge_names[current_edge]} boundary "
            f"saved: {intersection_point}"
        )


        # Move to the next edge.
        current_edge += 1


        # Check whether all four edges are finished.
        if current_edge >= 4:

            print(
                "\nAll boundaries selected."
            )

            save_boundaries(
                boundaries,
                "forbidden_boundaries.json"
            )

            break


        # Reset the points for the next edge.
        user_points.clear()

        intersection_point = None


    # =====================================================
    # R → Reset current edge
    # =====================================================

    elif key == ord("r"):

        user_points.clear()

        intersection_point = None

        print(
            f"{edge_names[current_edge]} reset."
        )


    # =====================================================
    # ESC → Cancel
    # =====================================================

    elif key == 27:

        print(
            "Selection cancelled."
        )

        break


# =========================================================
# Clean up
# =========================================================

cap.release()

cv2.destroyAllWindows()