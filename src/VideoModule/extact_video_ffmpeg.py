from extract_yt_link import video_url
import cv2
from ultralytics import YOLO
# import pytesseract
import subprocess
import numpy as np
import json
from detect_object import object_detect

model = YOLO("yolov8n.pt")

def process_video(video_url):
    """Read and process video frames in real-time."""
    cap = cv2.VideoCapture(video_url)  # Open video stream

    if not cap.isOpened():
        print("Error: Couldn't open video stream.")
        return

    while True:
        ret, frame = cap.read()
        if not ret:
            break  # Stop if video ends or error occurs

        object_detect(frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()


# def get_video_resolution(video_url):
#     cmd = [
#         "ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
#         "stream=width,height", "-of", "json", video_url
#     ]
#     result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
#
#     if result.returncode != 0:
#         print("❌ Error getting video resolution")
#         return None, None
#
#     info = json.loads(result.stdout)
#     if "streams" in info and len(info["streams"]) > 0:
#         width = info["streams"][0]["width"]
#         height = info["streams"][0]["height"]
#         return width, height
#
#     return None, None
#
#
# def process_video(video_url):
#     # FFmpeg command to pipe video frames to OpenCV
#     command = [
#         "ffmpeg", "-i", video_url, "-f", "rawvideo", "-pix_fmt", "bgr24", "-"
#     ]
#
#     process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, bufsize=10 ** 8)
#
#     # Video Properties
#     width, height = get_video_resolution(video_url)
#     frame_size = width * height * 3  # Each pixel has 3 channels (BGR)
#
#     while True:
#         raw_frame = process.stdout.read(frame_size)  # Read frame from FFmpeg
#
#         if not raw_frame:
#             break  # Exit when video ends
#
#         # Convert raw bytes to a NumPy array
#         frame = np.frombuffer(raw_frame, np.uint8).reshape((height, width, 3))
#
#         if frame is None:
#             break
#
#         cv2.imshow("Live Video Stream", frame)
#
#         # Press 'q' to exit
#         if cv2.waitKey(1) & 0xFF == ord('q'):
#             break
#
#     process.stdout.close()
#     process.wait()
#     cv2.destroyAllWindows()


print("Processing video stream...")
process_video(video_url)
