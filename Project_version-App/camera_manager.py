import subprocess
import time
from collections import deque
import os
from detector import Detector
from local_writer import LocalWriter

class CameraManager:
    """
    - Her 10 sn'de bir kare yakalar (libcamera-jpeg).
    - Diskte ve RAM'de son 30 kareyi tutar (≈ 5 dakika).
    - Her yeni karede, elde en az 2 kare varsa (N ve N-1) Detector ile insan sayımı yapar.
    - JSON sözleşmesine uygun bir payload üretir ve LocalWriter ile:
        * latest_info.json dosyasına ATOMİK olarak yazar,
        * history/ YYYY-MM-DD.ndjson dosyasına tek satır ekler (append_history).
    - Statik erişim için kareleri `Images/frames` altında toplar.
    """

    def __init__(
        self,
        device_id="pi-01",
        frames_dir="Images/frames",
        buffer_size=30,          # last 30 frames
        interval=10,             # 10 sec
        latest_json_path="latest_info.json",
        history_dir="history"
    ):
        self.device_id = device_id
        self.frames_dir = frames_dir
        self.buffer_size = buffer_size
        self.interval = interval
        self.latest_json_path = latest_json_path
        self.history_dir = history_dir

        os.makedirs(self.frames_dir, exist_ok=True)
        os.makedirs(self.history_dir, exist_ok=True)

        self.frame_buffer = deque(maxlen=self.buffer_size)
        self.detector = Detector()
        self.writer = LocalWriter()

    def _capture_frame(self):
        """libcamera-jpeg ile tek kare yakalar ve dosya yolunu döndürür; hata varsa None."""
        timestamp_str = time.strftime("%Y%m%d_%H%M%S")
        filename = os.path.join(self.frames_dir, f"frame_{timestamp_str}.jpg")
        cmd = ["libcamera-jpeg", "-o", filename, "-n"]

        result = subprocess.run(cmd, capture_output=True)
        if result.returncode != 0:
            print("Warning: frame capture failed!")
            return None

        # RAM buffer’a ekle
        self.frame_buffer.append(filename)

        # Diskte de yalnızca son N kareyi koru
        self._trim_disk_frames()

        return filename

    def _trim_disk_frames(self):
        """frames_dir içinde 'frame_*.jpg' dosyalarını tarihe göre sıralayıp yalnızca son N'yi bırakır."""
        all_frames = sorted(
            [f for f in os.listdir(self.frames_dir) if f.startswith("frame_") and f.endswith(".jpg")]
        )
        extra = len(all_frames) - self.buffer_size
        if extra > 0:
            for old in all_frames[:extra]:
                try:
                    os.remove(os.path.join(self.frames_dir, old))
                except Exception as e:
                    print(f"Warning: failed to remove old frame {old}: {e}")

    def _build_payload(self, n_path, n_1_path, counts_meta):
        """Sabit JSON sözleşmesine uygun payload üretir."""
        # Göreli yollar (web tarafı için daha kullanışlı)
        n_rel = os.path.relpath(n_path)
        p_rel = os.path.relpath(n_1_path)

        payload = {
            "device": self.device_id,
            "ts": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),  # ISO-8601 UTC
            "images": {
                "n_path": n_rel,
                "n_1_path": p_rel
            },
            "result": {
                "people_n": counts_meta["people_n"],
                "people_n_1": counts_meta["people_n_1"],
                "delta": counts_meta["delta"]
            },
            "meta": counts_meta.get("meta", {})
        }
        # Şema sürümü meta içinde yoksa ekleyelim
        payload["meta"].setdefault("schema_version", 1)
        return payload

    def run_loop(self):
        try:
            while True:
                path = self._capture_frame()
                if path:
                    print(f"Captured: {path}")

                    # En az 2 kare olduğunda sayım yap
                    if len(self.frame_buffer) >= 2:
                        n_path = self.frame_buffer[-1]
                        n_1_path = self.frame_buffer[-2]

                        counts_meta = self.detector.run(n_path, n_1_path)
                        if counts_meta is None:
                            print("Warning: detector returned None; skipping write.")
                        else:
                            payload = self._build_payload(n_path, n_1_path, counts_meta)

                            # 1) latest_info.json ATOMİK yazım
                            ok_latest = self.writer.write_latest(payload, self.latest_json_path)
                            # 2) history/ YYYY-MM-DD.ndjson append
                            ok_hist = self.writer.append_history(payload, self.history_dir)

                            if not ok_latest or not ok_hist:
                                print("Warning: write failed (latest or history).")

                time.sleep(self.interval)

        except KeyboardInterrupt:
            print("Loop stopped by user.")
        finally:
            print("Program terminated.")


# ---- Entry point ----
if __name__ == "__main__":
    cam = CameraManager()
    cam.run_loop()
