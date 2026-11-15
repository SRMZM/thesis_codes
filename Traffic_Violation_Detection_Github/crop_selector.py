# -*- coding: utf-8 -*-
"""
Created on Mon Aug 31 16:18:16 2026

@author: Russell
"""

# -*- coding: utf-8 -*-
"""
Crop Region Selector

This program allows the user to select a rectangular
region of interest (ROI) from the first frame of a video.

The intersection polygon is also displayed to help
the user select an appropriate crop region.

The selected crop coordinates are saved to a JSON file.
"""

import cv2
import json
import numpy as np

from test_polygon import load_polygon


# =========================================================
# Load crop region
# =========================================================

def load_crop_region(filename):

    # Open the crop region JSON file.
    with open(
        filename,
        "r",
        encoding="utf-8"
    ) as file:

        crop_region = json.load(file)

    return crop_region


# =========================================================
# Configuration
# =========================================================

video_path = "videos/Takhti_3.asf"

output_file = "crop_region.json"

polygon_file = "intersection_polygon.json"

window_name = "Crop Region Selector"


# =========================================================
# Global variables
# =========================================================

points = []



# =========================================================
# Mouse callback
# =========================================================

def mouse_callback(event, x, y, flags, param):

    global points

    # Check whether the left mouse button was clicked.
    if event == cv2.EVENT_LBUTTONDOWN:

        # Allow only two points.
        if len(points) < 2:

            points.append((x, y))


# =========================================================
# Save crop region
# =========================================================

def save_crop_region(points, filename):

    # Make sure exactly two points exist.
    if len(points) != 2:

        print(
            "Error: Two points must be selected."
        )

        return


    # Get the two selected points.
    x1, y1 = points[0]
    x2, y2 = points[1]


    # Make sure x1 is the left coordinate.
    left = min(x1, x2)

    # Make sure y1 is the top coordinate.
    top = min(y1, y2)

    # Make sure x2 is the right coordinate.
    right = max(x1, x2)

    # Make sure y2 is the bottom coordinate.
    bottom = max(y1, y2)


    # Create the crop data.
    crop_data = {

        "x1": left,
        "y1": top,

        "x2": right,
        "y2": bottom,

        # Offset used to convert cropped coordinates
        # back to original frame coordinates.
        "x_offset": left,
        "y_offset": top
    }


    # Save the data to JSON.
    with open(
        filename,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            crop_data,
            file,
            indent=4
        )


    # Print the saved values.
    print(
        "\nCrop region saved successfully."
    )

    print(f"x1 = {left}")
    print(f"y1 = {top}")
    print(f"x2 = {right}")
    print(f"y2 = {bottom}")

    print(f"x_offset = {left}")
    print(f"y_offset = {top}")


# =========================================================
# Main
# =========================================================

cap = cv2.VideoCapture(
    video_path
)


# Check whether the video was opened successfully.
if not cap.isOpened():

    print(
        "Error: Could not open the video."
    )

    exit()


# Read the first frame.
ret, frame = cap.read()


# Check whether the frame was read successfully.
if not ret:

    print(
        "Error: Could not read the first frame."
    )

    cap.release()

    exit()


# Release the video.
cap.release()


# =========================================================
# Load intersection polygon
# =========================================================

try:

    polygon = load_polygon(
        polygon_file
    )

except Exception as e:

    print(
        f"Error: Could not load polygon: {e}"
    )

    exit()


# Convert polygon to NumPy array.
polygon_array = np.array(
    polygon,
    dtype=np.int32
)


# =========================================================
# Create window
# =========================================================

cv2.namedWindow(
    window_name,
    cv2.WINDOW_NORMAL
)


# Set the mouse callback.
cv2.setMouseCallback(
    window_name,
    mouse_callback
)


# =========================================================
# Display loop
# =========================================================

while True:

    # Create a copy of the original frame.
    display_frame = frame.copy()


    # -----------------------------------------------------
    # Draw intersection polygon.
    # -----------------------------------------------------

    cv2.polylines(
        display_frame,
        [polygon_array],
        True,
        (255, 0, 255),
        3
    )


    # -----------------------------------------------------
    # Draw the first selected point.
    # -----------------------------------------------------

    if len(points) >= 1:

        cv2.circle(
            display_frame,
            points[0],
            6,
            (0, 0, 255),
            -1
        )


    # -----------------------------------------------------
    # Draw the second selected point.
    # -----------------------------------------------------

    if len(points) >= 2:

        cv2.circle(
            display_frame,
            points[1],
            6,
            (0, 0, 255),
            -1
        )


        # Get the two points.
        x1, y1 = points[0]
        x2, y2 = points[1]


        # Calculate rectangle boundaries.
        left = min(x1, x2)
        top = min(y1, y2)

        right = max(x1, x2)
        bottom = max(y1, y2)


        # Draw the crop rectangle.
        cv2.rectangle(
            display_frame,
            (left, top),
            (right, bottom),
            (0, 255, 0),
            3
        )


        # Create coordinate label.
        coordinate_text = (
            f"x1={left}, y1={top}, "
            f"x2={right}, y2={bottom}"
        )


        # Display coordinates.
        cv2.putText(
            display_frame,
            coordinate_text,
            (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0, 255, 255),
            2
        )


    # -----------------------------------------------------
    # Display instructions.
    # -----------------------------------------------------

    cv2.putText(
        display_frame,
        "Click two corners | ENTER: Save | R: Reset | Q: Quit",
        (20, display_frame.shape[0] - 20),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.6,
        (255, 255, 255),
        2
    )


    # -----------------------------------------------------
    # Display the frame.
    # -----------------------------------------------------

    cv2.imshow(
        window_name,
        display_frame
    )


    # Read keyboard input.
    key = cv2.waitKey(1) & 0xFF


    # -----------------------------------------------------
    # Reset
    # -----------------------------------------------------

    if key == ord("r"):

        points.clear()

        print(
            "Selection reset."
        )


    # -----------------------------------------------------
    # Save with Enter
    # -----------------------------------------------------

    elif key == 13:

        if len(points) == 2:

            save_crop_region(
                points,
                output_file
            )
            
            break

        else:

            print(
                "Please select exactly two points "
                "before saving."
            )


    # -----------------------------------------------------
    # ESC → Cancel
    # -----------------------------------------------------

    elif key == 27:

        print("Selection cancelled.")

        points.clear()

        break


# =========================================================
# Clean up
# =========================================================

cv2.destroyAllWindows()
