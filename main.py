#LA
"""
Created on Fri Aug 14 14:23:33 2026

@author: Russell
"""

import cv2
import math
from ultralytics import YOLO
import numpy as np
from test_polygon import load_polygon, is_inside_polygon
from maneuver_classifier_functions_using_angle import calculate_heading, signed_angle_difference, classify_maneuver, get_stable_maneuver
from intersection_analyzer import IntersectionAnalyzer
from violation_detector import (
    load_forbidden_boundaries,
    ViolationDetector,
    determine_violation
)
from movement_classifier import classify_movement
#from final_decision import determine_violation
from plate_recognizer import PlateRecognizer
from violation_record import ViolationRecordManager

# =========================================================
# 4. Load YOLO
# =========================================================

model = YOLO("yolo26n.pt")


# =========================================================
# 5. Open the video
# =========================================================

video_path = "videos/Takhti_1.asf"

cap = cv2.VideoCapture(video_path)


# Check whether the video was opened successfully.
if not cap.isOpened():
    print("Error: Could not open the video.")
    exit()


# =========================================================
# 6. Vehicle classes
# =========================================================

vehicle_classes = {
    "car",
    "motorcycle",
    "bus",
    "truck"
}


# =========================================================
# 7. Store trajectories
# =========================================================

track_history = {}

# =========================================================
# .Store maneuvers
# =========================================================
 
maneuver_history = {}

# =========================================================
# Store intersection events
# =========================================================

intersection_history = {}

# =========================================================
# 
# =========================================================

violation_history = {}

# =========================================================
# Store vehicle movements
# =========================================================

movement_results = {}

# =========================================================
# Store final violation decisions
# =========================================================

final_decisions = {}

# =========================================================
# Store license plates
# =========================================================

plate_history = {}

# =========================================================
# Store entry frame and exit frame when a vehicle comes to polygon
# =========================================================

entry_frame_history = {}

exit_frame_history = {}

# =========================================================
# .Load intersection polygon
# =========================================================

polygon = load_polygon(
    "intersection_polygon.json"
)

# =========================================================
# Load forbidden boundaries
# =========================================================

forbidden_boundaries = load_forbidden_boundaries(
    "forbidden_boundaries.json"
)

# =========================================================
# Create intersection analyzer
# =========================================================

intersection_analyzer = IntersectionAnalyzer(
    polygon
)

# =========================================================
# Create violation detector
# =========================================================

violation_detector = ViolationDetector(
    polygon,
    forbidden_boundaries
)

# =========================================================
# Create plate recognizer
# =========================================================

plate_recognizer = PlateRecognizer(
    detector_path=(
        "models/persian_plate_detector/best.pt"
    ),

    ocr_path=(
        "models/persian_plate_ocr"
    )
)

# =========================================================
# Store complete vehicle records
# =========================================================

record_manager = ViolationRecordManager()


# =========================================================
# 8. Process the video
# =========================================================

frame_number = 0

while True:

    # Read one frame.
    ret, frame = cap.read()


    # Stop when the video ends.
    if not ret:
        break

    frame_number += 1
    
    # Run YOLO tracking.
    results = model.track(
        source=frame,
        persist=True,
        conf=0.5,
        verbose=False
    )


    # Get the result for the current frame.
    result = results[0]


    # Get detected bounding boxes.
    boxes = result.boxes


    # Make sure tracking IDs exist.
    if boxes.id is not None:


        # Process every tracked object.
        for box, track_id in zip(boxes, boxes.id):


            # Get the class ID.
            class_id = int(box.cls[0])


            # Convert class ID to class name.
            class_name = model.names[class_id]


            # Ignore non-vehicle objects.
            if class_name not in vehicle_classes:
                continue


            # Convert track ID to integer.
            track_id = int(track_id.item())


            # Get bounding box coordinates.
            x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()


            # Calculate the center point.
            cx = int((x1 + x2) / 2)
            cy = int((y1 + y2) / 2)
            
            center = (cx, cy)


            # Create a trajectory for a new vehicle.
            if track_id not in track_history:
                track_history[track_id] = []

            
            # Add the current center point.
            track_history[track_id].append((cx, cy))


            # Get this vehicle's trajectory.
            points = track_history[track_id]

            # =========================================================
            # Recognize license plate
            # =========================================================
            
            if track_id not in plate_history:
            
                # Convert vehicle bounding box coordinates
                # to integers.
                vx1 = max(0, int(x1))
                vy1 = max(0, int(y1))
                vx2 = min(frame.shape[1], int(x2))
                vy2 = min(frame.shape[0], int(y2))
            
            
                # Crop this vehicle from the frame.
                vehicle_crop = frame[
                    vy1:vy2,
                    vx1:vx2
                ]
            
            
                # Try to recognize the license plate.
                plate_text = plate_recognizer.recognize(
                    vehicle_crop
                )
            
            
                # Store the result.
                plate_history[track_id] = plate_text
                
                record = record_manager.get_record(
                    track_id
                )
                
                if record is not None:
                
                    record.plate = plate_text
            
            # =========================================
            # Analyze intersection entry and exit
            # =========================================
            
            if track_id not in intersection_history:

                intersection_result = (
                    intersection_analyzer.analyze(points)
                )
            
                if intersection_result is not None:
            
                    # Store the intersection result.
                    intersection_history[track_id] = (
                        intersection_result
                    )
                    
                    # Create a record for this vehicle.
                    record = record_manager.create_record(
                        track_id
                    )
                    
                    # Add the plate which is already recognized to record
                    record.plate = plate_history.get(
                        track_id
                    )
                    
                    record.entry_frame = (
                        entry_frame_history.get(track_id)
                    )
                    
                    record.exit_frame = (
                        exit_frame_history.get(track_id)
                    )
            
                    # Store entry and exit sides.
                    record.entry_side = (
                        intersection_result["entry_side"]
                    )
            
                    record.exit_side = (
                        intersection_result["exit_side"]
                    )
                    
                    # Get the entry side.
                    entry_side = intersection_result[
                        "entry_side"
                    ]
            
                    # Get the entry point.
                    entry_point = intersection_result[
                        "entry_point"
                    ]
                    
                    # Get the exit side.
                    exit_side = intersection_result[
                        "exit_side"
                    ]
            
                    # Determine whether the entry is forbidden.
                    is_forbidden = (
                        violation_detector.is_entry_forbidden(
                            entry_side,
                            entry_point
                        )
                    )
            
                    # Store the violation result.
                    violation_history[track_id] = (
                        is_forbidden
                    )
                    
                    # Classify the vehicle movement.
                    movement = classify_movement(
                        entry_side,
                        exit_side
                    )
                    
                    # Store the movement result.
                    movement_results[track_id] = (
                        movement
                    )
                    
                    record.movement = movement
                    
                    # Determine the final violation decision.
                    final_decision = determine_violation(
                        movement,
                        is_forbidden
                    )
                    
                    # Store the final decision.
                    final_decisions[track_id] = (
                        final_decision
                    )
                    
                    record.violation_type = final_decision

                    record.violation = (
                        final_decision
                        in {
                            "ILLEGAL LEFT TURN",
                            "ILLEGAL U-TURN"
                        }
                    )


            # Draw the bounding box.
            cv2.rectangle(
                frame,
                (int(x1), int(y1)),
                (int(x2), int(y2)),
                (0, 255, 0),
                2
            )


            # Draw the center point.
            cv2.circle(
                frame,
                (cx, cy),
                5,
                (0, 0, 255),
                -1
            )


            # Draw the trajectory.
            for i in range(1, len(points)):

                cv2.line(
                    frame,
                    points[i - 1],
                    points[i],
                    (255, 0, 0),
                    2
                )


            # =========================================
            # Classify the maneuver
            # =========================================

            if len(points) >= 10:

                # Classify the current trajectory.
                current_maneuver = classify_maneuver(points)
            
            
                # Create maneuver history for a new vehicle.
                if track_id not in maneuver_history:
                    maneuver_history[track_id] = []
            
            
                # Store the current prediction.
                maneuver_history[track_id].append(
                    current_maneuver
                )
            
            
                # Keep only the latest 5 predictions.
                if len(maneuver_history[track_id]) > 5:
                    maneuver_history[track_id].pop(0)
            
            
                # Get the most common recent prediction.
                maneuver = get_stable_maneuver(
                    maneuver_history[track_id]
                )
            
            else:
            
                maneuver = "ANALYZING"


            # Create the label.
            label = f"ID: {track_id} | {maneuver}"
            
            # =========================================
            # Create intersection label
            # =========================================
            
            intersection_result = intersection_history.get(
                track_id
            )
            
            if intersection_result is not None:
            
                entry_side = intersection_result[
                    "entry_side"
                ]
            
                exit_side = intersection_result[
                    "exit_side"
                ]
            
                intersection_label = (
                    f"Entry: {entry_side} | "
                    f"Exit: {exit_side}"
                )
            
            else:
            
                intersection_label = "Entry/Exit: ANALYZING"
                
                
            # =========================================
            # Create movement label
            # =========================================
            
            if track_id in movement_results:
            
                movement_label = (
                    f"Movement: {movement_results[track_id]}"
                )
            
            else:
            
                movement_label = "Movement: ANALYZING"
                
                
            # =========================================
            # Create final decision label
            # =========================================
            
            if track_id in final_decisions:
            
                final_decision_label = (
                    f"Decision: {final_decisions[track_id]}"
                )
            
            else:
            
                final_decision_label = (
                    "Decision: ANALYZING"
                )
                
                
            # =========================================
            # Create violation label
            # =========================================
            
            if track_id in violation_history:
            
                if violation_history[track_id]:
            
                    violation_label = "VIOLATION"
            
                else:
            
                    violation_label = "ALLOWED"
            
            else:
            
                violation_label = "Violation: ANALYZING"


            # =========================================================
            # Create license plate label
            # =========================================================
            
            plate_text = plate_history.get(
                track_id
            )
            
            
            if plate_text is not None:
            
                plate_label = (
                    f"Plate: {plate_text}"
                )
            
            else:
            
                plate_label = (
                    "Plate: ANALYZING"
                )
            
            
            # Draw the label.
            cv2.putText(
                frame,
                label,
                (int(x1), int(y1) - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (0, 255, 0),
                2
            )
            
            # cv2.putText(
            #     frame,
            #     intersection_label,
            #     (int(x1), int(y1) - 35),
            #     cv2.FONT_HERSHEY_SIMPLEX,
            #     0.55,
            #     (255, 255, 0),
            #     2
            # )
            
            # cv2.putText(
            #     frame,
            #     violation_label,
            #     (int(x1), int(y1) - 60),
            #     cv2.FONT_HERSHEY_SIMPLEX,
            #     0.55,
            #     (0, 0, 255),
            #     2
            # )
            
            # cv2.putText(
            #     frame,
            #     movement_label,
            #     (int(x1), int(y1) - 35),
            #     cv2.FONT_HERSHEY_SIMPLEX,
            #     0.55,
            #     (255, 255, 0),
            #     2
            # )
            
            cv2.putText(
                frame,
                final_decision_label,
                (int(x1), int(y1) - 35),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.55,
                (0, 0, 255),
                2
            )
            
            # # Draw license plate label.
            # cv2.putText(
            #     frame,
            #     plate_label,
            #     (int(x1), int(y1) - 135),
            #     cv2.FONT_HERSHEY_SIMPLEX,
            #     0.55,
            #     (0, 255, 255),
            #     2
            # )
            
            inside = is_inside_polygon(
                center,
                polygon
            )
            
            if inside:

                status = "IN INTERSECTION"
                
                if track_id not in entry_frame_history:
            
                    entry_frame_history[track_id] = (
                        frame_number
                    )
            
            else:
            
                status = "OUTSIDE"
                
                if (
                    track_id in entry_frame_history
                    and track_id not in exit_frame_history
                ):
            
                    exit_frame_history[track_id] = frame_number
            
                    record = record_manager.get_record(
                        track_id
                    )
            
                    if record is not None:
            
                        record.exit_frame = frame_number
            
            
            # cv2.putText(
            #     frame,
            #     status,
            #     (cx, cy + 25),
            #     cv2.FONT_HERSHEY_SIMPLEX,
            #     0.6,
            #     (0, 255, 255),
            #     2
            # )


    polygon_array = np.array(
        polygon,
        dtype=np.int32
    )
    
    cv2.polylines(
        frame,
        [polygon_array],
        True,
        (255, 0, 255),
        2
    )
    
    # Display the frame.
    
    cv2.namedWindow("Left Turn Violation Detection", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("Left Turn Violation Detection", 800, 600)
    
    cv2.imshow(
        "Left Turn Violation Detection",
        frame
    )


    # Press Q to exit.
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break


# =========================================================
# 9. Clean up
# =========================================================

cap.release()

cv2.destroyAllWindows()

# =========================================================
# Print all vehicle records
# =========================================================

print("\n================ VEHICLE RECORDS ================\n")

for record in record_manager.get_all_records():

    print(record.to_dict())

    print("\n===================================================\n")