import os
import time
import subprocess
import datetime
import cv2
import paho.mqtt.client as mqtt
import json
import shutil

# ---------- Konfigürasyon ----------
PHOTO_DIR = "photos"
if not os.path.exists(PHOTO_DIR):
    os.makedirs(PHOTO_DIR)

BROKER = "mqtt.thingsboard.cloud"
PORT = 1883
ACCESS_TOKEN = "aQ3eNcaKthG279lMKJMp"
TOPIC = "v1/devices/me/telemetry"
RCLONE_REMOTE = "drivepi"

# ---------- MQTT Bağlantısı ----------
client = mqtt.Client()
client.username_pw_set(ACCESS_TOKEN)
client.connect(BROKER, PORT, 60)

# ---------- Yardımcı Fonksiyonlar ----------
def take_photo(filename):
    cap = cv2.VideoCapture(0)
    time.sleep(0.1)  # Kameranın oturması için kısa bekleme
    ret, frame = cap.read()
    if ret:
        cv2.imwrite(filename, frame)
    cap.release()

def send_to_thingsboard(message):
    payload = {"alert": message}
    client.publish(TOPIC, json.dumps(payload), 1)

def upload_to_drive(folder_path):
    cmd = ["rclone", "copy", folder_path, f"{RCLONE_REMOTE}:intern-images/{os.path.basename(folder_path)}"]
    subprocess.run(cmd)

def clear_file(filepath):
    try:
        if os.path.exists(filepath):
            os.remove(filepath)
    except Exception as e:
        print(f"[WARN] Dosya silinemedi: {filepath}, Hata: {e}")

# ---------- Ana Döngü ----------
def main():
    img_counter = 0
    prev_photo = None

    while True:
        # 1) Fotoğraf çek
        img_counter += 1
        current_photo = os.path.join(PHOTO_DIR, f"img_{img_counter}.jpg")
        take_photo(current_photo)

        # 2) Önceki fotoğraf varsa değişim kontrolü
        if prev_photo is not None:
            result = subprocess.run(
                ["python3", "change_detector.py", prev_photo, current_photo],
                stdout=subprocess.PIPE, text=True
            )
            diff_flag = result.stdout.strip()

            # 3) Değişim varsa event handler çalıştır
            if diff_flag == "1":
                print("[INFO] Değişim algılandı, event handler başlatılıyor...")

                # Event handler çalıştır (N-1 ve N gönder)
                result_event = subprocess.run(
                    ["python3", "event_handler.py", prev_photo, current_photo],
                    stdout=subprocess.PIPE, text=True
                )
                output_folder = result_event.stdout.strip()

                # 4) Drive'a yükle
                upload_to_drive(output_folder)

                # 5) ThingsBoard'a mesaj gönder
                send_to_thingsboard(f"Yeni bir değişim tespit edildi. Klasör adı: {os.path.basename(output_folder)}")

        # 4) Önceki (N-1) fotoğrafı sil, böylece gereksiz birikim olmaz
        if prev_photo is not None:
            clear_file(prev_photo)

        # 5) Yeni fotoğrafı bir sonraki karşılaştırma için sakla
        prev_photo = current_photo

        # 6) Döngü arası bekleme
        time.sleep(5)

if __name__ == "__main__":
    main()
