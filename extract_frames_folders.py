import os
import shutil

INPUT_DIR = "klasor_ayirici_frameleri"   
OUTPUT_DIR = "new_frames"                
FRAME_INTERVAL = 10                     

os.makedirs(OUTPUT_DIR, exist_ok=True)

extensions = (".jpg", ".jpeg", ".png", ".bmp", ".webp")

files = sorted(
    [f for f in os.listdir(INPUT_DIR) if f.lower().endswith(extensions)]
)

saved = 1

for i, file in enumerate(files):
    if i % FRAME_INTERVAL == 0:
        src = os.path.join(INPUT_DIR, file)

        ext = os.path.splitext(file)[1]

        new_name = f"frame_{saved:05d}{ext}"

        dst = os.path.join(OUTPUT_DIR, new_name)
        shutil.copy2(src, dst)

        saved += 1

print(f"{saved - 1} frame kaydedildi.")