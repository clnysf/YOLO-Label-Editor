from ultralytics import YOLO
import os
import cv2

MODEL_PATH = "yolov8n.pt" # Kullanılacak model
IMAGE_DIR = "new_frames"
LABEL_DIR = "new_labels"

CONF_THRESHOLD = 0.45

os.makedirs(LABEL_DIR, exist_ok=True)

print("Label klasörü:", os.path.abspath(LABEL_DIR))

model = YOLO(MODEL_PATH)

saved_files = 0

for img_name in sorted(os.listdir(IMAGE_DIR)):
    if not img_name.lower().endswith((".jpg", ".png", ".jpeg","webp")):
        continue

    img_path = os.path.join(IMAGE_DIR, img_name)
    img = cv2.imread(img_path)

    if img is None:
        print(f"[HATA] Resim okunamadı: {img_name}")
        continue

    h, w = img.shape[:2]

    results = model(img_path, conf=CONF_THRESHOLD)[0]

    print(f"{img_name} -> {len(results.boxes)} nesne bulundu.")

    label_name = os.path.splitext(img_name)[0] + ".txt"
    label_path = os.path.join(LABEL_DIR, label_name)

    with open(label_path, "w") as f:
        for box in results.boxes:
            cls = int(box.cls[0])
            x1, y1, x2, y2 = box.xyxy[0].tolist()

            x_center = ((x1 + x2) / 2) / w
            y_center = ((y1 + y2) / 2) / h
            box_width = (x2 - x1) / w
            box_height = (y2 - y1) / h

            f.write(
                f"{cls} {x_center:.6f} {y_center:.6f} {box_width:.6f} {box_height:.6f}\n"
            )

    print(f"Kaydedildi: {label_path}")
    saved_files += 1

print(f"\nToplam {saved_files} adet label dosyası oluşturuldu.")