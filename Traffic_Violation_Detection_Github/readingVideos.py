# -*- coding: utf-8 -*-
"""
Created on Sun Aug  9 16:56:44 2026

@author: Russell
"""

import cv2
import os

video_path = "videos/road.mp4"

# print("Working Directory:")
# print(os.getcwd())

# print("\nVideo path:")
# print(os.path.abspath(video_path))

# print("\nDoes file exist?")
# print(os.path.exists(video_path), "\n")

cap = cv2.VideoCapture(video_path)

if not cap.isOpened():
    print("خطا: ویدیو بارگذاری نشد.")
    exit()
else:
    print("ویدیو با موفقیت باز شد.")
    
    while True:
        ret, frame = cap.read()
        
        if not ret:
            break
        
        cv2.imshow("Video Frames", frame)
        
        key = cv2.waitKey(30)
        
        if key == ord("q"):
            break
        
    
    # if ret:
    #     print("Frame was seccussfully red")
    #     print("Frame Shape:", frame.shape)
    # else:
    #     print("Error in reading frame")
    
# while True:
#     ret, frame = cap.read()
#     if not ret:
#         break
#     cv2.imshow("Video", frame)
#     if cv2.waitKey(25) & 0xFF == ord('q'):
#         break

cap.release()
cv2.destroyAllWindows()