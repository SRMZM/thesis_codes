# -*- coding: utf-8 -*-
"""
Created on Tue Aug 11 16:26:47 2026

@author: Russell
"""

import cv2
from ultralytics import YOLO

model = YOLO("yolo11n.pt")

video_path = "videos/crossroad.mov"

cap = cv2.VideoCapture(video_path)

if not cap.isOpened():
    print("ویدیو بارگذاری نشد.")
    exit()

print("Video is seccussfully opened")

while True:
    ret, frame = cap.read()
    
    if not ret: 
        print("Video finishes")
        break
    
    results = model.predict(
        source = frame,
        conf = .4,
        verbose = False
        )
    
    result = results[0]
    
    boxes = result.boxes
    
    for box in boxes:
        
        x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
        
        class_id = int(box.cls[0])
        
        confidence = float(box.conf[0])
        
        class_name = model.names[class_id]
        
        cx = int((x1 + x2) / 2)
        cy = int((y1 + y2) / 2)
        
        print(
            f"{class_name} | "
            f"confidence = {confidence:.2f} | "
            f"center = ({cx}, {cy})"
            )   
        
        cv2.rectangle(
            frame,
            (int(x1), int(y1)),
            (int(x2), int(y2)),
            (0, 255, 0),
            2
            )
        
        cv2.circle(
            frame,
            (cx, cy),
            5,
            (0, 0, 255),
            -1
            )
        
        label = f"{class_name} {confidence:.2f}"
        
        cv2.putText(
            frame, 
            label, 
            (int(x1), int(y1) - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (0, 255, 0),
            2
            )
    
    
    #annotiated_frame = results[0].plot()
    
    cv2.namedWindow("YOLO Vehicle Detection", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("YOLO Vehicle Detection", 800, 600)
    
    cv2.imshow("YOLO Vehicle Detection", frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
cap.release()
cv2.destroyAllWindows()
        
    
    