import cv2
import time
from collections import deque
import os
from change_detector import ChangeDetector
from detector import Detector 

class CameraManager:
    def __init__(self, save_dir="Images", buffer_size=12, interval=5):
        self.save_dir = save_dir
        self.buffer_size = buffer_size
        self.interval = interval
        self.frame_buffer = deque(maxlen=buffer_size)

        # Değişim ve insan tespiti sınıfları//Detection classes
        self.change_detector = ChangeDetector()
        self.detector = Detector()

        # Kayıt klasörü yoksa oluştur//Creating folder
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)

        # Kamera başlatma
        self.camera = cv2.VideoCapture(0)   # 0 = default camera

    def capture_frame(self):
        """Tek kare yakala ve buffer’a ekle"""
        ret, frame = self.camera.read()
        if not ret:
            print("Capturing failed!")
            return None

        timestamp = int(time.time())
        filename = os.path.join(self.save_dir, f"frame_{timestamp}.jpg")
        cv2.imwrite(filename, frame)

        # Buffer’a ekle (12 kareden fazlasını otomatik siler)
        self.frame_buffer.append(filename)
        return filename

    def capture_series(self, count=3):
        """Değişim tespit edilirse seri fotoğraf çekimi"""
        series_paths = []
        for i in range(count):
            path = self.capture_frame()
            if path:
                series_paths.append(path)
            time.sleep(0.2)  # Seri çekim için kısa bekleme
        return series_paths

    def run_loop(self):
        """Sürekli fotoğraf çekme, değişim kontrolü ve insan tespiti//Continuous photography, change detection and human detection"""
        try:
            while True:
                image_path = self.capture_frame()
                if image_path:
                    print(f"New frame taken: {image_path}")

                    # En az iki kare varsa değişim kontrolü yap
                    if len(self.frame_buffer) >= 2:
                        latest_frame = self.frame_buffer[-1]
                        previous_frame = self.frame_buffer[-2]
                        change = self.change_detector.detect_change(
                            [latest_frame, previous_frame]
                        )
                    else:
                        change = False

                    if change:
                        print("Change detected, starting burst...")
                        series = self.capture_series()

                        # n ve n-1 kareleri + seri kareler → detector.py'ye gönderim
                        all_images = [latest_frame, previous_frame] + series
                        result = self.detector.run(all_images)
                        print(f"Detector result: {result}")

                time.sleep(self.interval)
        except KeyboardInterrupt:
            print("Loop Stopped.")
        finally:
            self.camera.release()
            cv2.destroyAllWindows()
