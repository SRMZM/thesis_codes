# -*- coding: utf-8 -*-
"""
Created on Sat Aug 29 18:03:10 2026

@author: Russell
"""

# -*- coding: utf-8 -*-

"""
Test Persian license plate detection.
"""

import cv2
from ultralytics import YOLO


# =========================================================
# Load the Persian license plate detector
# =========================================================

model = YOLO(
    "models/persian_plate_detector/best.pt"
)


# =========================================================
# Load test image
# =========================================================

image_path = "test_vehicle.jfif"

frame = cv2.imread(image_path)


# Check whether the image was loaded successfully.
if frame is None:

    print("Error: Could not load the test image.")
    exit()


# =========================================================
# Run license plate detection
# =========================================================

results = model.predict(
    source=frame,
    conf=0.5,
    verbose=False
)


# Get the result for the current image.
result = results[0]


# =========================================================
# Process detected plates
# =========================================================

# =========================================================
# Process detected license plates
# =========================================================

if result.boxes is not None:

    print(
        f"Number of detections: "
        f"{len(result.boxes)}"
    )

    for index, box in enumerate(result.boxes):

        # Get the class ID.
        class_id = int(
            box.cls[0]
        )
        
        print(
            class_id,
            f": {model.names[class_id]}"
            )
        # Ignore character detections.
        if class_id != 30:
            continue

        # Get bounding box coordinates.
        x1, y1, x2, y2 = (
            box.xyxy[0]
            .cpu()
            .numpy()
            .astype(int)
        )

        # Get confidence.
        confidence = float(
            box.conf[0]
        )

        print(
            f"License plate: "
            f"confidence={confidence:.3f}, "
            f"box=({x1}, {y1}, {x2}, {y2})"
        )

        # Draw the license plate bounding box.
        cv2.rectangle(
            frame,
            (x1, y1),
            (x2, y2),
            (0, 255, 0),
            2
        )

        # Create the label.
        label = f"Plate: {confidence:.2f}"

        # Draw the label.
        cv2.putText(
            frame,
            label,
            (x1, y1 - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (0, 255, 0),
            2
        )

        print(
            f"Plate detected: "
            f"({x1}, {y1}) - ({x2}, {y2}) "
            f"confidence={confidence:.2f}"
        )


# =========================================================
# Display result
# =========================================================

cv2.imshow(
    "Persian License Plate Detection",
    frame
)
# print(model.names)

cv2.waitKey(0)

cv2.destroyAllWindows()