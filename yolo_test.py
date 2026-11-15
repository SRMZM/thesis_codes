# -*- coding: utf-8 -*-
"""
Created on Mon Aug 10 18:57:14 2026

@author: Russell
"""

from ultralytics import YOLO

model = YOLO("yolo11n.pt");

results = model("videos/road.mp4")

print("Detecetion completed.")