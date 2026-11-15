# -*- coding: utf-8 -*-
"""
Created on Sat Aug 29 23:03:08 2026

@author: Russell
"""

# -*- coding: utf-8 -*-

"""
License plate detection and recognition.
"""

import cv2

from ultralytics import YOLO
from hezar.models import Model


class PlateRecognizer:

    # =====================================================
    # Initialization
    # =====================================================

    def __init__(
            self,
            detector_path,
            ocr_path,
            plate_class_id=30
        ):

        # Load the license plate detector.
        self.detector = YOLO(
            detector_path
        )

        # Load the Persian OCR model.
        self.ocr = Model.load(
            ocr_path
        )

        # Store the class ID representing
        # the complete license plate.
        self.plate_class_id = plate_class_id


    # =====================================================
    # Recognize license plate
    # =====================================================

    def recognize(self, vehicle_crop):

        # Check whether the vehicle crop is valid.
        if (
            vehicle_crop is None
            or vehicle_crop.size == 0
        ):

            return None


        # Run license plate detection
        # inside this vehicle crop only.
        results = self.detector.predict(
            source=vehicle_crop,
            conf=0.5,
            verbose=False
        )


        # Get the result for this vehicle.
        result = results[0]


        # Check whether any objects were detected.
        if result.boxes is None:

            return None


        # Store possible plate detections.
        plate_detections = []


        # Process all detections.
        for box in result.boxes:

            # Get class ID.
            class_id = int(
                box.cls[0]
            )


            # Ignore classes other than
            # the complete license plate.
            if class_id != self.plate_class_id:

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


            # Store the detection.
            plate_detections.append(
                (
                    confidence,
                    x1,
                    y1,
                    x2,
                    y2
                )
            )


        # No complete license plate found.
        if not plate_detections:

            return None


        # Select the detection with
        # the highest confidence.
        plate_detections.sort(
            reverse=True
        )

        confidence, x1, y1, x2, y2 = (
            plate_detections[0]
        )


        # Make sure coordinates are inside
        # the vehicle crop.
        height, width = vehicle_crop.shape[:2]

        x1 = max(0, min(x1, width))
        x2 = max(0, min(x2, width))

        y1 = max(0, min(y1, height))
        y2 = max(0, min(y2, height))


        # Check whether the bounding box is valid.
        if x2 <= x1 or y2 <= y1:

            return None


        # Crop the license plate.
        plate_crop = vehicle_crop[
            y1:y2,
            x1:x2
        ]


        # Check whether the crop is valid.
        if plate_crop.size == 0:

            return None


        # Run OCR on the detected plate.
        ocr_result = self.ocr.predict(
            plate_crop
        )


        # Check OCR output.
        if not ocr_result:

            return None


        # Extract recognized text.
        plate_text = ocr_result[0].text


        # Return the recognized plate.
        return plate_text