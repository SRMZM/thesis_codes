# -*- coding: utf-8 -*-
"""
Created on Sun Aug 30 11:12:32 2026

@author: Russell
"""

# -*- coding: utf-8 -*-

"""
Test PlateRecognizer.
"""

import cv2

from plate_recognizer import PlateRecognizer


# =========================================================
# Create PlateRecognizer
# =========================================================

recognizer = PlateRecognizer(
    detector_path=(
        "models/persian_plate_detector/best.pt"
    ),

    ocr_path=(
        "models/persian_plate_ocr"
    )
)


# =========================================================
# Load vehicle image
# =========================================================

image = cv2.imread(
    "test_detector_and_ocr_2.jfif"
)


# Check image.
if image is None:

    print(
        "Error: Could not load image."
    )

    exit()


# =========================================================
# Run recognition
# =========================================================

plate_text = recognizer.recognize(
    image
)


# =========================================================
# Display result
# =========================================================

print(
    "Recognized plate:"
)

print(
    plate_text
)