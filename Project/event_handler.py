import sys
import os
import cv2
import time
import datetime
import numpy as np
import shutil

PHOTO_DIR = "photos"
FAST_DIR = "fast_photos"
CROPPED_DIR = "cropped_photos"

os.makedirs(FAST_DIR, exist_ok=True)
os.makedirs(CROPPED_DIR, exist_ok=True)

def extract_frames(video_path, timestamps):
    cap = cv2.VideoCapture(video_path)
    # Zorunlu çözünürlük ayarı: 1920x1080
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
    fps = cap.get(cv2.CAP_PROP_FPS)
    frames = []
    for ts in timestamps:
        cap.set(cv2.CAP_PROP_POS_MSEC, ts * 1000)
        ret, frame = cap.read()
        if ret:
            # Çerçeveyi her ihtimale karşı yeniden boyutlandır
            frame = cv2.resize(frame, (1920, 1080))
            filename = os.path.join(FAST_DIR, f"fast_{int(ts*10):02d}.jpg")
            cv2.imwrite(filename, frame)
            frames.append(filename)
    cap.release()
    return frames

def crop_moving_objects(background_path, photo_path, output_path):
    bg = cv2.imread(background_path, cv2.IMREAD_GRAYSCALE)
    frame = cv2.imread(photo_path)

    # Fotoğraf ve video kareleri aynı çözünürlükte olduğundan, resize ihtiyacı azaldı.
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Çözünürlük farkı varsa yeniden boyutlandır
    if bg.shape != gray_frame.shape:
        gray_frame = cv2.resize(gray_frame, (bg.shape[1], bg.shape[0]))
        frame = cv2.resize(frame, (bg.shape[1], bg.shape[0]))

    diff = cv2.absdiff(bg, gray_frame)
    blur = cv2.GaussianBlur(diff, (5, 5), 0)
    _, thresh = cv2.threshold(blur, 25, 255, cv2.THRESH_BINARY)

    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    mask = np.zeros_like(frame)

    if contours:
        largest_contour = max(contours, key=cv2.contourArea)
        x, y, w, h = cv2.boundingRect(largest_contour)
        mask[y:y+h, x:x+w] = frame[y:y+h, x:x+w]
    cv2.imwrite(output_path, mask)

def main(prev_photo, current_photo, video_path):
    start_time = time.time()
    timestamps = [i * 0.5 for i in range(10)]  # 0.0, 0.5, ... 4.5

    # Kare yakalama
    frames = extract_frames(video_path, timestamps)

    # Cropped fotoğraflar
    cropped_photos = []
    for frame in frames:
        crop_file = os.path.join(CROPPED_DIR, f"cropped_{os.path.basename(frame)}")
        crop_moving_objects(prev_photo, frame, crop_file)
        cropped_photos.append(crop_file)

    # Sonuç klasörü
    timestamp = datetime.datetime.now().strftime("%H_%M_%S")
    output_folder = os.path.join("event_results", f"event_{timestamp}")
    os.makedirs(output_folder, exist_ok=True)

    shutil.copy(prev_photo, os.path.join(output_folder, os.path.basename(prev_photo)))
    shutil.copy(current_photo, os.path.join(output_folder, os.path.basename(current_photo)))
    for crop_file in cropped_photos:
        shutil.copy(crop_file, os.path.join(output_folder, os.path.basename(crop_file)))

    # Geçici dosyaları sil
    for f in frames + cropped_photos:
        if os.path.exists(f):
            os.remove(f)

    # 20 saniye bekleme
    while time.time() - start_time < 20:
        time.sleep(0.5)

    print(output_folder)

if __name__ == "__main__":
    if len(sys.argv) < 4:
        sys.exit(0)
    prev_photo = sys.argv[1]
    current_photo = sys.argv[2]
    video_path = sys.argv[3]
    main(prev_photo, current_photo, video_path)
