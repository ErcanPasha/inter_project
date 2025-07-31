import os
import time
import subprocess
import datetime
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
    # Fotoğraf çekimi 1920x1080 çözünürlükte
    result = subprocess.run(["libcamera-jpeg", "-o", filename, "--width", "1920", "--height", "1080"])
    if result.returncode != 0:
        print(f"[WARN] Kamera görüntü yakalayamadı: {filename}")

def record_video(video_h264, duration=5):
    # Video çekimi 1920x1080 çözünürlükte
    result = subprocess.run([
        "libcamera-vid", "-t", str(duration * 1000),
        "-o", video_h264, "--width", "1920", "--height", "1080"
    ])
    if result.returncode != 0:
        print(f"[WARN] Video yakalanamadı: {video_h264}")

def convert_h264_to_mp4(h264_path, mp4_path):
    # ffmpeg dönüşümü
    result = subprocess.run(["ffmpeg", "-y", "-i", h264_path, "-c", "copy", mp4_path])
    if result.returncode != 0:
        print(f"[WARN] MP4 dönüşümü başarısız: {h264_path}")

def send_to_thingsboard(message):
    payload = {"alert": message}
    client.publish(TOPIC, json.dumps(payload), 1)

def upload_to_drive(folder_path):
    cmd = ["rclone", "copy", folder_path, f"{RCLONE_REMOTE}:intern-images/{os.path.basename(folder_path)}"]
    subprocess.run(cmd)

def clear_file(filepath):
    try:
        if filepath and os.path.exists(filepath):
            os.remove(filepath)
    except Exception as e:
        print(f"[WARN] Dosya silinemedi: {filepath}, Hata: {e}")

# ---------- Ana Döngü ----------
def main():
    img_counter = 0
    prev_photo = None

    while True:
        img_counter += 1
        current_photo = os.path.join(PHOTO_DIR, f"img_{img_counter}.jpg")
        take_photo(current_photo)

        if prev_photo and os.path.exists(prev_photo):
            result = subprocess.run(
                ["python3", "change_detector.py", prev_photo, current_photo],
                stdout=subprocess.PIPE, text=True
            )
            diff_flag = result.stdout.strip()

            if diff_flag == "1":
                print("[INFO] Değişim algılandı, video kaydı başlatılıyor...")
                video_h264 = os.path.join(PHOTO_DIR, f"vid_{img_counter}.h264")
                video_mp4 = os.path.join(PHOTO_DIR, f"vid_{img_counter}.mp4")

                # Video çekimi ve mp4 dönüşümü
                record_video(video_h264)
                convert_h264_to_mp4(video_h264, video_mp4)

                # Event handler çağrısı (3 argüman: prev, current, video)
                result_event = subprocess.run(
                    ["python3", "event_handler.py", prev_photo, current_photo, video_mp4],
                    stdout=subprocess.PIPE, text=True
                )
                output_folder = result_event.stdout.strip()

                # Klasör yeniden adlandırma (saat_dakika_saniye)
                timestamp = datetime.datetime.now().strftime("%H_%M_%S")
                final_folder = f"{output_folder}_{timestamp}"
                shutil.move(output_folder, final_folder)

                # Drive'a yükle
                upload_to_drive(final_folder)

                # ThingsBoard'a mesaj
                send_to_thingsboard(f"Yeni değişim: {os.path.basename(final_folder)}")

                # Temizlik
                clear_file(video_h264)
                clear_file(video_mp4)

            clear_file(prev_photo)

        prev_photo = current_photo
        time.sleep(5)

if __name__ == "__main__":
    main()
