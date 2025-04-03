import cv2
import easyocr
from extract_yt_link import video_url
import time

#vanakkam da maple
reader = easyocr.Reader(['en'])

cap = cv2.VideoCapture(video_url)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    start_time = time.time()
    results = reader.readtext(frame)
    end_time = time.time()
    print("Time Taken: ",end_time-start_time)

    for (bbox, text, prob) in results:
        (top_left, top_right, bottom_right, bottom_left) = bbox
        top_left = tuple(map(int, top_left))
        bottom_right = tuple(map(int, bottom_right))

        cv2.rectangle(frame, top_left, bottom_right, (0, 255, 0), 2)
        cv2.putText(frame, text, top_left, cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)


    # cv2.imshow("Text Detection", frame)
    if cv2.waitKey(1) & 0xFF == ord("q"):  # Press 'q' to quit
        break


cap.release()
cv2.destroyAllWindows()
