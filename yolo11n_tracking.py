# -*- coding: utf-8 -*-
"""
Created on Thu Aug 13 14:11:03 2026

@author: Russell
"""

import cv2
from ultralytics import YOLO

model = YOLO("yolo11n.pt")

#Vehicle classes that are relavent to the project
Vehicle_classes = {
    "car", 
    "motorcycle",
    "bus",
    "truck"
    }

video_path = "videos/road.mp4"

cap = cv2.VideoCapture(video_path)

if not cap.isOpened():
    print("Video is not opened.")
    exit()
    
print("Video is successfully opened.")

track_history = {}

while True:
    ret, frame = cap.read()
    
    if not ret:
        print("Video finishes.")
        break
    
    results = model.track(
        source = frame,
        persist = True,
        conf = .4,
        verbose = False
        )
    
    result = results[0]
    
    boxes = result.boxes
    
    if boxes.id is not None:
        
        for box, track_id in zip(boxes, boxes.id):
            
            class_id = int(box.cls[0])
            
            class_name = model.names[class_id]
            
            if class_name not in Vehicle_classes:
                continue
            
            x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
            
            track_id = int(track_id.item())
            
            confidence = float(box.conf[0])
            
            cx = int((x1 + x2) / 2)
            cy = int((y1 + y2) / 2)
            
            if track_id not in track_history:
                track_history[track_id] = []
                
            track_history[track_id].append((cx, cy))
            
            print(
                f"ID = {track_id} | "
                f"{class_name} | "
                f"confidence = {confidence:.2f} |"
                f"center = ({cx}, {cy})"
                )
            
            cv2.rectangle(
                frame,
                (int(x1), int(y1)),
                (int(x2), int(y2)),
                (0, 255, 0),
                2
            )
            # Draw the bounding box.


            cv2.circle(
                frame,
                (cx, cy),
                5,
                (0, 0, 255),
                -1
            )
            # Draw the center point.


            label = f"ID: {track_id} | {class_name} {confidence:.2f}"
            # Create a label containing the tracking ID
            # and the object class.


            cv2.putText(
                frame,
                label,
                (int(x1), int(y1) - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (0, 255, 0),
                2
            )
            # Draw the label above the bounding box.
            
            points = track_history[track_id]
            
            for i in range(1, len(points)):
                
                cv2.line(
                    frame,
                    points[i-1],
                    points[i],
                    (255, 0, 0),
                    2
                    )
            # Draw trajectory

        #annotiated_frame = result[0].plot()
        
        cv2.imshow("YOLO tracking + Trajectory", frame)
        
        if(cv2.waitKey(1) & 0xFF == ord("q")):
            break
        
cap.release()
cv2.destroyAllWindows()
