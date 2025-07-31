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

if not os.path.exists(FAST_DIR):
    os.makedirs(FAST_DIR)
if not os.path.exists(CROPPED_DIR):
    os.makedirs(CROPPED_DIR)

def take_fast_photos(count=5, interval=0.2):
    photos = []
    cap = cv2.VideoCapture(0)
    for i in range(count):
        ret, frame = cap.read()
        if ret:
            filename = os.path.join(FAST_DIR, f"fast_{i+1}.jpg")
            cv2.imwrite(filename, frame)
            photos.append(filename)
        time.sleep(interval)
    cap.release()
    return photos

def crop_moving_objects(background_path, photo_path, output_path):
    bg = cv2.imread(background_path, cv2.IMREAD_GRAYSCALE)
    frame = cv2.imread(photo_path)
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Boyut eşitleme
    if bg.shape != gray_frame.shape:
        gray_frame = cv2.resize(gray_frame, (bg.shape[1], bg.shape[0]))
        frame = cv2.resize(frame, (bg.shape[1], bg.shape[0]))

    diff = cv2.absdiff(bg, gray_frame)
    blur = cv2.GaussianBlur(diff, (5, 5), 0)
    _, thresh = cv2.threshold(blur, 25, 255, cv2.THRESH_BINARY)

    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if contours:
        # En büyük hareketli nesneyi al
        largest_contour = max(contours, key=cv2.contourArea)
        x, y, w, h = cv2.boundingRect(largest_contour)
        cropped = frame[y:y+h, x:x+w]
        cv2.imwrite(output_path, cropped)

def main(prev_photo, current_photo):
    # 20 saniyelik sayaç başlat
    start_time = time.time()
    
    # 5 hızlı fotoğraf çek
    fast_photos = take_fast_photos()

    # Crop edilmiş fotoğraflar oluştur
    cropped_photos = []
    for i, photo in enumerate(fast_photos):
        cropped_filename = os.path.join(CROPPED_DIR, f"cropped_{i+1}.jpg")
        crop_moving_objects(prev_photo, photo, cropped_filename)
        cropped_photos.append(cropped_filename)

    # Klasör adı (N fotoğrafının çekildiği zaman)
    timestamp = datetime.datetime.now().strftime("%H_%M_%S")
    output_folder = os.path.join("event_results", f"event_{timestamp}")
    os.makedirs(output_folder, exist_ok=True)

    # N-1, N ve crop edilmiş fotoğrafları klasöre kopyala
    shutil.copy(prev_photo, os.path.join(output_folder, os.path.basename(prev_photo)))
    shutil.copy(current_photo, os.path.join(output_folder, os.path.basename(current_photo)))
    for crop_file in cropped_photos:
        shutil.copy(crop_file, os.path.join(output_folder, os.path.basename(crop_file)))

    # Fast fotoğrafları ve crop fotoğraflarını sil
    for f in fast_photos + cropped_photos:
        if os.path.exists(f):
            os.remove(f)

    # 20 saniye dolana kadar bekle
    while time.time() - start_time < 20:
        time.sleep(0.5)

    print(output_folder)

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("")
        sys.exit(0)
    prev_photo = sys.argv[1]
    current_photo = sys.argv[2]
    main(prev_photo, current_photo)
