from extract_yt_link import video_url
import cv2
from ultralytics import YOLO
import pytesseract
import subprocess
import numpy as np
import json
from detect_object import object_detect

model = YOLO("yolov8n.pt")

def process_video(video_url):
    cap = cv2.VideoCapture(video_url)

    if not cap.isOpened():
        print("Error: Couldn't open video stream.")
        return

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        object_detect(frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()

print("Processing video stream...")
process_video(video_url)
