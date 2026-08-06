import os
import cv2

IMAGE_DIR = "new_frames"
LABEL_DIR = "new_labels"

CLASSES = ["vehicle", "person", "UAP", "UAI"]

images = sorted([
    f for f in os.listdir(IMAGE_DIR)
    if f.lower().endswith((".jpg", ".jpeg", ".png",".webp"))
])

idx = 0
boxes = []

drawing = False
start_x, start_y = 0, 0
current_x, current_y = 0, 0

current_class = 0

redo_stack = []


def get_paths():
    img_name = images[idx]

    img_path = os.path.join(
        IMAGE_DIR,
        img_name
    )

    label_path = os.path.join(
        LABEL_DIR,
        os.path.splitext(img_name)[0] + ".txt"
    )

    return img_path, label_path


def load_boxes():
    global boxes, redo_stack

    boxes = []
    redo_stack = []

    img_path, label_path = get_paths()

    img = cv2.imread(img_path)

    h, w = img.shape[:2]

    if not os.path.exists(label_path):
        return

    with open(label_path, "r") as f:

        for line in f:

            p = line.strip().split()

            if len(p) != 5:
                continue

            cls = int(float(p[0]))

            xc, yc, bw, bh = map(
                float,
                p[1:]
            )

            x1 = int(
                (xc - bw / 2) * w
            )

            y1 = int(
                (yc - bh / 2) * h
            )

            x2 = int(
                (xc + bw / 2) * w
            )

            y2 = int(
                (yc + bh / 2) * h
            )

            boxes.append([
                cls,
                x1,
                y1,
                x2,
                y2
            ])


def save_boxes():

    os.makedirs(
        LABEL_DIR,
        exist_ok=True
    )

    img_path, label_path = get_paths()

    img = cv2.imread(img_path)

    h, w = img.shape[:2]

    with open(label_path, "w") as f:

        for cls, x1, y1, x2, y2 in boxes:

            x1, x2 = sorted([x1, x2])
            y1, y2 = sorted([y1, y2])

            x1 = max(0, min(w, x1))
            x2 = max(0, min(w, x2))

            y1 = max(0, min(h, y1))
            y2 = max(0, min(h, y2))

            bw = (x2 - x1) / w
            bh = (y2 - y1) / h

            if bw <= 0 or bh <= 0:
                continue

            xc = ((x1 + x2) / 2) / w
            yc = ((y1 + y2) / 2) / h

            f.write(
                f"{cls} "
                f"{xc:.6f} "
                f"{yc:.6f} "
                f"{bw:.6f} "
                f"{bh:.6f}\n"
            )

    print(
        "Kaydedildi:",
        label_path
    )


def draw():

    img_path, _ = get_paths()

    img = cv2.imread(img_path)

    # Mevcut kutular
    for cls, x1, y1, x2, y2 in boxes:

        cv2.rectangle(
            img,
            (x1, y1),
            (x2, y2),
            (0, 255, 0),
            2
        )

        cv2.putText(
            img,
            CLASSES[cls],
            (
                x1,
                max(25, y1 - 5)
            ),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0, 255, 0),
            2
        )

    
    if drawing:

        cv2.rectangle(
            img,
            (start_x, start_y),
            (current_x, current_y),
            (0, 255, 255),
            2
        )

        cv2.putText(
            img,
            CLASSES[current_class],
            (
                start_x,
                max(25, start_y - 5)
            ),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0, 255, 255),
            2
        )

    text = (
        f"{idx + 1}/{len(images)} "
        f"| Class: {current_class} "
        f"{CLASSES[current_class]}"
    )

    cv2.putText(
        img,
        text,
        (20, 40),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 0, 255),
        2
    )

    return img


def mouse_callback(
    event,
    x,
    y,
    flags,
    param
):

    global drawing
    global start_x, start_y
    global current_x, current_y
    global boxes
    global redo_stack

    if event == cv2.EVENT_LBUTTONDOWN:

        drawing = True

        start_x = x
        start_y = y

        current_x = x
        current_y = y

    elif event == cv2.EVENT_MOUSEMOVE:

        if drawing:

            current_x = x
            current_y = y

    elif event == cv2.EVENT_LBUTTONUP:

        drawing = False

        current_x = x
        current_y = y

        if (
            abs(x - start_x) > 5
            and
            abs(y - start_y) > 5
        ):

            boxes.append([
                current_class,
                start_x,
                start_y,
                x,
                y
            ])

            
            redo_stack.clear()


if not images:

    raise RuntimeError(
        "new_frames klasöründe görsel yok."
    )


cv2.namedWindow(
    "YOLO Label Editor",
    cv2.WINDOW_NORMAL
)

cv2.setMouseCallback(
    "YOLO Label Editor",
    mouse_callback
)

load_boxes()


while True:

    img = draw()

    cv2.imshow(
        "YOLO Label Editor",
        img
    )

    key = cv2.waitKey(30) & 0xFF


    # Çıkış
    if key == ord("q"):

        save_boxes()
        break


    # Kaydet
    elif key == ord("s"):

        save_boxes()


    # Sonraki görsel
    elif key == ord("d"):

        save_boxes()

        idx = min(
            idx + 1,
            len(images) - 1
        )

        load_boxes()


    # Önceki görsel
    elif key == ord("a"):

        save_boxes()

        idx = max(
            idx - 1,
            0
        )

        load_boxes()


    # GERİ AL
    elif key == ord("z"):

        if boxes:

            removed_box = boxes.pop()

            redo_stack.append(
                removed_box
            )

            print("Geri alındı")


    # İLERİ AL
    elif key == ord("y"):

        if redo_stack:

            restored_box = redo_stack.pop()

            boxes.append(
                restored_box
            )

            print("İleri alındı")


    # Sınıf seçimi
    elif key in [
        ord("0"),
        ord("1"),
        ord("2"),
        ord("3")
    ]:

        current_class = int(
            chr(key)
        )

        print(
            "Seçili sınıf:",
            current_class,
            CLASSES[current_class]
        )


cv2.destroyAllWindows()