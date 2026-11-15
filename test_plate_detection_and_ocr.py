# -*- coding: utf-8 -*-
"""
Created on Sat Aug 29 22:25:01 2026

@author: Russell
"""

# -*- coding: utf-8 -*-

"""
Test license plate detection and OCR.
"""

import cv2

from ultralytics import YOLO
from hezar.models import Model


# =========================================================
# Load plate detector
# =========================================================

plate_detector = YOLO(
    "models/persian_plate_detector/best.pt"
)


# =========================================================
# Load Persian OCR model
# =========================================================

ocr_model = Model.load(
    "models/persian_plate_ocr"
)


# =========================================================
# Load test image
# =========================================================

image_path = "test_plate.jpg"

image = cv2.imread(
    image_path
)


# Check whether the image was loaded successfully.
if image is None:

    print(
        "Error: Could not load the image."
    )

    exit()


# =========================================================
# Detect license plate
# =========================================================

results = plate_detector.predict(
    source=image,
    conf=0.5,
    verbose=False
)


result = results[0]


# =========================================================
# Find the license plate
# =========================================================

plate_box = None

for box in result.boxes:

    # Get the class ID.
    class_id = int(
        box.cls[0]
    )

    # Class ID 30 represents the
    # complete license plate.
    if class_id != 30:
        continue

    # Get confidence.
    confidence = float(
        box.conf[0]
    )

    # Get bounding box coordinates.
    x1, y1, x2, y2 = (
        box.xyxy[0]
        .cpu()
        .numpy()
        .astype(int)
    )

    plate_box = (
        x1,
        y1,
        x2,
        y2
    )

    print(
        f"License plate detected: "
        f"confidence={confidence:.3f}"
    )

    print(
        f"Bounding box: "
        f"({x1}, {y1}, {x2}, {y2})"
    )

    break


# =========================================================
# Check whether a plate was found
# =========================================================

if plate_box is None:

    print(
        "No license plate detected."
    )

    exit()


# =========================================================
# Crop the license plate
# =========================================================

x1, y1, x2, y2 = plate_box

plate_crop = image[
    y1:y2,
    x1:x2
]


# Check whether the crop is valid.
if plate_crop.size == 0:

    print(
        "Error: License plate crop is empty."
    )

    exit()


# =========================================================
# Save the plate crop
# =========================================================

cv2.imwrite(
    "detected_plate.jpg",
    plate_crop
)


# =========================================================
# Run OCR
# =========================================================

ocr_result = ocr_model.predict(
    "detected_plate.jpg"
)


# =========================================================
# Display OCR result
# =========================================================

print(
    "OCR result:"
)

print(
    ocr_result
)


# =========================================================
# Display the detected plate
# =========================================================

cv2.rectangle(
    image,
    (x1, y1),
    (x2, y2),
    (0, 255, 0),
    2
)

cv2.imshow(
    "Plate Detection + OCR",
    image
)

cv2.waitKey(0)

cv2.destroyAllWindows()