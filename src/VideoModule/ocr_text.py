import cv2
from paddleocr import PaddleOCR
import paddle
import numpy as np
from extract_yt_link import video_url
print(paddle.device.get_device())
# Load GPU-based OCR model
ocr = PaddleOCR(use_angle_cls=True, lang='en')

# Simulate your OpenCV video pipeline
cap = cv2.VideoCapture(video_url)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Convert BGR (OpenCV) to RGB (OCR expects RGB)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # PaddleOCR works with image paths or numpy arrays
    result = ocr.ocr(rgb_frame, cls=True)

    # Optional: Draw results on frame
    for line in result[0]:
        text = line[1][0]
        box = np.array(line[0]).astype(np.int32)
        cv2.polylines(frame, [box], True, (0, 255, 0), 2)
        cv2.putText(frame, text, tuple(box[0]), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 1)

    # Show frame (or save to video)
    cv2.imshow('OCR Output', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()