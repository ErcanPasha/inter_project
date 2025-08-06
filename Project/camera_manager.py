import subprocess
import time
from collections import deque
import os
import shutil
from change_detector import ChangeDetector
from detector import Detector
from uploader import Uploader

class CameraManager:
    def __init__(self, save_dir="Images", buffer_size=12, interval=5):
        self.save_dir = save_dir
        self.buffer_size = buffer_size
        self.interval = interval
        self.frame_buffer = deque(maxlen=buffer_size)

        self.change_detector = ChangeDetector()
        self.detector = Detector()
        self.uploader = Uploader()

        # Create save directory if not exists
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)

    def capture_frame(self, is_case_photo=False):
        """Capture a single frame using libcamera-jpeg and add it to buffer"""
        timestamp_str = time.strftime("%Y%m%d_%H%M%S")
        if is_case_photo:
            filename = os.path.join(self.save_dir, f"case_photo_{timestamp_str}.jpg")
        else:
            filename = os.path.join(self.save_dir, f"frame_{timestamp_str}.jpg")

        cmd = ["libcamera-jpeg", "-o", filename, "-n"]
        result = subprocess.run(cmd, capture_output=True)

        if result.returncode != 0:
            print(f"Warning: Capturing failed for {'case photo' if is_case_photo else 'frame'}!")
            return None

        if not is_case_photo:
            self.frame_buffer.append(filename)

            # Ensure only last N photos exist on disk
            existing_files = sorted(
                [f for f in os.listdir(self.save_dir) if f.startswith("frame_") and f.endswith(".jpg")]
            )
            extra_files = len(existing_files) - self.buffer_size
            if extra_files > 0:
                for old_file in existing_files[:extra_files]:
                    os.remove(os.path.join(self.save_dir, old_file))
                    print(f"Old photo removed: {old_file}")

        return filename

    def save_last_12(self):
        """Save the last 12 buffered frames into a timestamped folder"""
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        event_dir = os.path.join(self.save_dir, f"event_{timestamp}")
        os.makedirs(event_dir)

        for img_path in list(self.frame_buffer):
            shutil.copy(img_path, event_dir)

        print(f"Last 12 frames copied to folder: {event_dir}")
        return event_dir

    def run_loop(self):
        """Main loop for continuous capture, change detection, detection and uploading"""
        try:
            while True:
                image_path = self.capture_frame()
                if image_path:
                    print(f"New frame captured: {image_path}")

                    if len(self.frame_buffer) >= 2:
                        latest_frame = self.frame_buffer[-1]
                        previous_frame = self.frame_buffer[-2]
                        change = self.change_detector.detect_change(
                            [latest_frame, previous_frame]
                        )
                    else:
                        change = False

                    if change:
                        print("Change detected, starting event process...")

                        # Cooldown start
                        start_cooldown = time.time()

                        # Save last 12 images to folder
                        last12_dir = self.save_last_12()

                        # Capture case photo
                        case_photo = self.capture_frame(is_case_photo=True)
                        if case_photo:
                            print(f"Case photo captured: {case_photo}")
                        else:
                            print("Warning: Case photo could not be captured!")

                        # Run detector (n, n-1, case_photo)
                        print(f"Detector input images:\n n-1={previous_frame}\n n={latest_frame}\n case_photo={case_photo}")
                        detector_result = self.detector.run(
                            [latest_frame, previous_frame, case_photo]
                        )

                        if detector_result:
                            # Upload detector results and last 12 images
                            self.uploader.upload_event(
                                detector_event_dir=detector_result["event_dir"],
                                last12_dir=last12_dir,
                                timestamp=detector_result["timestamp"]
                            )

                        # Cooldown period (10 seconds total)
                        elapsed = time.time() - start_cooldown
                        if elapsed < 10:
                            wait_time = 10 - elapsed
                            print(f"Cooldown active, waiting {wait_time:.2f} seconds...")
                            time.sleep(wait_time)

                time.sleep(self.interval)

        except KeyboardInterrupt:
            print("Loop stopped by user.")
        finally:
            print("Program terminated.")


# ---- Entry point ----
if __name__ == "__main__":
    cam = CameraManager()
    cam.run_loop()
