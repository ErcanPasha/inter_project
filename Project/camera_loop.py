import os
import time
import subprocess
import json
import paho.mqtt.client as mqtt

# MQTT - ThingsBoard bağlantısı
ACCESS_TOKEN = "fLXRg0k8ZDHC79DGntyh"  # cihaz token'ı
broker = "mqtt.thingsboard.cloud"
port = 1883
topic = "v1/devices/me/telemetry"

# MQTT istemcisi
client = mqtt.Client()
client.username_pw_set(ACCESS_TOKEN)
client.connect(broker, port, 60)
client.loop_start()

# Görsel klasörü
image_dir = "Images"
os.makedirs(image_dir, exist_ok=True)

# Başlangıç
print("Fotoğraf döngüsü başlatılıyor...")
cycle = 1
max_cycles = 10

while cycle <= max_cycles:
    filename = f"img_{cycle}.jpg"
    filepath = os.path.join(image_dir, filename)

    # 1. Fotoğraf çekimi (libcamera-jpeg)
    print(f"[{cycle}] Fotoğraf çekiliyor: {filename}")
    try:
        subprocess.run(["libcamera-jpeg", "-o", filepath], check=True)
    except subprocess.CalledProcessError:
        print("Fotoğraf çekilemedi!")
        continue

    # 2. Karşılaştırma yapılacaksa
    if cycle > 1:
        last_img = os.path.join(image_dir, f"img_{cycle - 1}.jpg")
        current_img = filepath

        # compare_images.py çağrısı
        try:
            result = subprocess.check_output(
                ["python3", "compare_images.py", last_img, current_img],
                stderr=subprocess.DEVNULL
            ).decode().strip()
        except Exception as e:
            print("Karşılaştırma hatası:", e)
            result = "Error"

        print(f"[{cycle}] Sonuç: {result}")

        # Payload oluştur
        payload = {
            "cycle": cycle,
            "comparison_result": result
        }

        # Eğer "Change" varsa ek bilgi ekle
        if result == "Change":
            payload["note"] = "Görüntüde değişim var, upload yapılacak"

        client.publish(topic, json.dumps(payload), qos=1)

        # Eski fotoğrafları temizle (yalnızca son iki kalır)
        try:
            old_img = os.path.join(image_dir, f"img_{cycle - 2}.jpg")
            if os.path.exists(old_img):
                os.remove(old_img)
        except Exception as e:
            print("Temizleme hatası:", e)

    else:
        print(f"[{cycle}] İlk görsel çekildi, karşılaştırma yapılmadı.")

    cycle += 1
    time.sleep(5)

# MQTT bağlantı kapat
client.loop_stop()
client.disconnect()
print("Fotoğraf döngüsü tamamlandı.")
