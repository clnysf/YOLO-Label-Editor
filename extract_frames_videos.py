import cv2
import os

VIDEO_PATH = "videos/ornek2.mp4"
OUTPUT_DIR = "new_frames"
FRAME_INTERVAL = 10

os.makedirs(OUTPUT_DIR, exist_ok=True)

cap = cv2.VideoCapture(VIDEO_PATH)
frame_id = 0
saved_id = 0

while True:
    ret, frame = cap.read()
    if not ret:
        break

    if frame_id % FRAME_INTERVAL == 0:
        filename = os.path.join(OUTPUT_DIR, f"ornek2frames_{saved_id:05d}.jpg")
        cv2.imwrite(filename, frame)
        saved_id += 1

    frame_id += 1

cap.release()
print(f"{saved_id} frame kaydedildi.")