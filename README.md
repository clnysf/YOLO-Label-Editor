# YOLO Label Editor

YOLO formatında sınırlayıcı kutu (bounding box) etiketleri oluşturmak ve düzenlemek için geliştirilmiş OpenCV tabanlı bir etiketleme aracıdır.

## Dosyalar

### `opencv_label_editor.py`
YOLO formatında etiketleme yapmak ve mevcut etiketleri düzenlemek için kullanılan program.

**Klavye Kısayolları**
- **Q** : Programı kapatır.
- **S** : Yapılan değişiklikleri kaydeder.
- **A** : Önceki görsele geçer.
- **D** : Sonraki görsele geçer.
- **Z** : Son işlemi geri alır.
- **Y** : Geri alınan işlemi tekrar uygular.
- **0-3** : Etiket sınıfını seçer.

---

### `extract_frames_videos.py`
Belirlenen aralıklarla videodan frame çıkararak yeni bir klasöre kaydeder.

---

### `extract_frames_folders.py`
Bir klasördeki görsellerden belirlenen aralıklarla seçim yaparak yeni bir klasöre kopyalar.

---

### `auto_label.py`
Eğitilmiş bir YOLO modeli kullanarak görseller için otomatik olarak YOLO formatında etiket dosyaları oluşturur.