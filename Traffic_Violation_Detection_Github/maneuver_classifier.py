# -*- coding: utf-8 -*-
"""
Created on Thu Aug 13 17:00:07 2026

@author: Russell
"""

import math


def calculate_heading(point1, point2):
    
    x1, y1 = point1
    x2, y2 = point2
    
    dx = x2 - x1
    dy = y2 - y1
    
    angle = math.atan2(dx, dy)
    angle = math.degrees(angle)
    
    return angle

# def angle_difference(angle1, angle2):
    
#     difference = abs(angle2 - angle1)
    
#     if difference > 180:
#         difference = 360 - difference
        
#     return difference

def signed_angle_difference(angle1, angle2):
    
    difference = angle2 - angle1
    
    if difference > 180:
        difference -= 360
        
    elif difference < -180:
        difference += 360
        
    return difference

def classify_maneuver(trajectory):
    
    if len(trajectory) < 10 :
        return "UNKNOWN"
    
    n = len(trajectory)
    
    segment_size = max(3, int(n * 0.3))
    
    start_points = trajectory[:segment_size]
    
    end_points = trajectory[-segment_size:]
    
    start_heading = calculate_heading(
        start_points[0], 
        start_points[-1]
        )
    
    end_heading = calculate_heading(
        end_points[0],
        end_points[-1]
        )
    
    turn_angle = signed_angle_difference(
        start_heading,
        end_heading
        )
    
    absolute_angle = abs(turn_angle)
    
    if absolute_angle < 15:
        return "STRAIGHT"
    
    elif 60 <= absolute_angle <= 120:
        
        if turn_angle > 0:
            return "RIGHT_TURN"
        else:
            return "LEFT_TURN"
    
    elif 150 <= absolute_angle:
        return "U_TURN"
    
    else:
        return "LANE_CHANGE_OR_KNOWN"
    

# =============================================================================
#Test Cases for the classifier
#
# straight_trajectory = [
#     (500, 700),
#     (500, 680),
#     (500, 660),
#     (500, 640),
#     (500, 620),
#     (500, 600),
#     (500, 580),
#     (500, 560),
#     (500, 540),
#     (500, 520),
# ]
# 
# result = classify_maneuver(straight_trajectory)
# print(result)
#     
# right_turn_trajectory = [
#     (500, 700),
#     (500, 680),
#     (500, 660),
#     (500, 640),
#     (500, 620),
#     (500, 600),
#     (500, 580),
#     (520, 580),
#     (540, 580),
#     (560, 580),
#     (580, 580),
#     (600, 580),
# ]
#     
# result = classify_maneuver(right_turn_trajectory)
# print(result)  
#     
# left_turn_trajectory = [
#     (500, 700),
#     (500, 680),
#     (500, 660),
#     (500, 640),
#     (500, 620),
#     (500, 600),
#     (480, 600),
#     (460, 600),
#     (440, 600),
#     (420, 600),
#     (400, 600),
# ]
# 
# result = classify_maneuver(left_turn_trajectory)
# print(result)
# 
# u_turn_trajectory = [
#     (500, 700),
#     (500, 680),
#     (500, 660),
#     (500, 640),
#     (500, 620),
#     (500, 600),
#     (480, 580),
#     (460, 570),
#     (440, 580),
#     (430, 600),
#     (430, 620),
#     (430, 640),
#     (430, 660),
# ]
# 
# result = classify_maneuver(u_turn_trajectory)
# print(result)
# 
# lane_change_trajectory = [
#     (500, 700),
#     (505, 680),
#     (510, 660),
#     (515, 640),
#     (520, 620),
#     (525, 600),
#     (535, 580),
#     (545, 560),
#     (555, 540),
#     (565, 520),
#     (575, 500),
# ]
# 
# result = classify_maneuver(lane_change_trajectory)
# print(result)
# 
# 
#     
# =============================================================================
