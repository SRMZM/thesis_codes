# -*- coding: utf-8 -*-
"""
Created on Fri Aug 28 15:21:12 2026

@author: Russell
"""



"""
Test Persian license plate recognition.
"""

from hezar.models import Model


# =========================================================
# Load the local OCR model
# =========================================================

model = Model.load(
    "models/persian_plate_ocr"
)


# =========================================================
# Image path
# =========================================================

image_path = "test_plate.jpg"


# =========================================================
# Run OCR
# =========================================================

predictions = model.predict(
    image_path
)


# =========================================================
# Display the result
# =========================================================

print("OCR result:")
print(predictions)













