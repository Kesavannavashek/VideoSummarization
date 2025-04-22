# import cv2
# import numpy as np
# import paddle
# from paddleocr import PaddleOCR
from extract_yt_link import get_video_info_with_subs
#
# print(paddle.device.get_device())
video_url = "https://youtu.be/ldYLYRNaucM?si=ximNENy042FR06sR"
_,_,url = get_video_info_with_subs(video_url)
# print("url",url)
# # Initialize OCR with CPU
# # ocr = PaddleOCR(use_angle_cls=True, lang='en', use_gpu=Truffe)
# use_gpu = paddle.is_compiled_with_cuda() and paddle.device.get_device().startswith('gpu')
#
# ocr = PaddleOCR(
#     det_model_dir='en_PP-OCRv4_det',
#     rec_model_dir='en_PP-OCRv4_rec',
#     cls_model_dir='ch_ppocr_mobile_v2.0_cls',
#     use_angle_cls=True,
#     lang='en',
#     use_gpu=use_gpu,
#     precision='fp16' if use_gpu else 'fp32'
# )
#
# FRAME_SIZE = 3
# # Open video capture from URL or file
# cap = cv2.VideoCapture(url)
# frame_c = 0
# while cap.isOpened():
#     ret, frame = cap.read()
#     if not ret:
#         break
#
#     if frame_c % FRAME_SIZE == 0:
#         # Convert BGR to RGB
#         rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#
#         # Perform OCR
#         result = ocr.ocr(rgb_frame, cls=True)
#
#         # Safely handle result
#         if result and result[0]:
#             for line in result[0]:
#                 text = line[1][0]
#                 box = np.array(line[0]).astype(np.int32)
#                 print(f"- {text}")
#                 cv2.polylines(frame, [box], True, (0, 255, 0), 2)
#                 cv2.putText(frame, text, tuple(box[0]), cv2.FONT_HERSHEY_SIMPLEX,
#                             0.6, (255, 0, 0), 1)
#         else:
#             print("No text detected in this frame.")
#
#         # Show output
#         cv2.imshow('OCR Output', frame)
#         if cv2.waitKey(1) & 0xFF == ord('q'):
#             break
#     frame_c += 1
#
# cap.release()
# cv2.destroyAllWindows()

import cv2
import numpy as np
from paddleocr import PaddleOCR

# Load OCR model (auto-detect GPU support)
ocr = PaddleOCR(use_angle_cls=True, use_gpu=True)

# Your video URL or path
cap = cv2.VideoCapture(url)

prev_frame = None
prev_text = ""
frame_interval = 10  # OCR every N frames
frame_count = 0

def histogram_diff(img1, img2):
    hist1 = cv2.calcHist([img1], [0], None, [256], [0,256])
    hist2 = cv2.calcHist([img2], [0], None, [256], [0,256])
    return cv2.compareHist(hist1, hist2, cv2.HISTCMP_BHATTACHARYYA)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Run OCR if it's the first frame, a keyframe, or at interval
    if prev_frame is None or histogram_diff(prev_frame, gray) > 0.3 or frame_count % frame_interval == 0:
        result = ocr.ocr(frame, cls=True)
        if result and result[0]:
            try:
                curr_text = " ".join([line[1][0] for line in result[0]])
                if prev_text.strip() != curr_text.strip():
                    timestamp = cap.get(cv2.CAP_PROP_POS_MSEC) / 1000  # Time in seconds
                    print(f"\n[KEY FRAME OCR] @ {timestamp:.2f}s:")
                    print(curr_text)
                    prev_text = curr_text
                    prev_frame = gray
            except Exception as e:
                print("OCR Error:", e)

    frame_count += 1
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
