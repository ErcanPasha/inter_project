import cv2
import os
import shutil
from datetime import datetime

class Detector:
    def __init__(self, 
                 output_dir="Detections",
                 cfg_path="yolov4-tiny.cfg",
                 weights_path="yolov4-tiny.weights",
                 names_path="coco.names"):
        self.output_dir = output_dir
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # Load class names
        with open(names_path, "r") as f:
            self.classes = [line.strip() for line in f.readlines()]

        # Load YOLO model
        self.net = cv2.dnn.readNetFromDarknet(cfg_path, weights_path)
        self.net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
        self.net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)

        self.layer_names = self.net.getLayerNames()
        self.output_layers = [self.layer_names[i - 1] for i in self.net.getUnconnectedOutLayers()]

    def count_people(self, image_path):
        """Count number of people in a single image using YOLOv4-tiny"""
        image = cv2.imread(image_path)
        if image is None:
            print(f"Warning: Failed to read image: {image_path}")
            return 0

        (H, W) = image.shape[:2]
        blob = cv2.dnn.blobFromImage(image, 1/255.0, (416, 416), swapRB=True, crop=False)
        self.net.setInput(blob)
        layer_outputs = self.net.forward(self.output_layers)

        count = 0
        for output in layer_outputs:
            for detection in output:
                scores = detection[5:]
                class_id = int(scores.argmax())
                confidence = scores[class_id]
                if self.classes[class_id] == "person" and confidence > 0.65:
                    count += 1
        return count

    def run(self, images):
        """
        images: [n_frame, n_minus_1_frame, case_photo]
        Returns:
            {
                "event_dir": <folder path>,
                "txt_path": <txt file path>,
                "zip_path": <zip file path>,
                "counts": {"n-1": int, "n": int, "case_photo": int},
                "timestamp": <event timestamp>
            }
        """
        if len(images) < 3:
            print("Warning: Detector requires [n, n-1, case_photo].")
            return None

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        event_dir = os.path.join(self.output_dir, f"event_{timestamp}")
        os.makedirs(event_dir)

        # Count people
        counts = {
            "n-1": self.count_people(images[1]),
            "n": self.count_people(images[0]),
            "case_photo": self.count_people(images[2])
        }

        # Save counts to txt
        txt_path = os.path.join(event_dir, "counts.txt")
        with open(txt_path, "w") as f:
            for label, count in counts.items():
                f.write(f"{label}: {count}\n")

        # Copy related images
        for img_path in images:
            if img_path:
                shutil.copy(img_path, event_dir)

        # Zip event folder
        zip_path = shutil.make_archive(event_dir, 'zip', event_dir)
        print(f"Detection results saved: {zip_path}")

        return {
            "event_dir": event_dir,
            "txt_path": txt_path,
            "zip_path": zip_path,
            "counts": counts,
            "timestamp": timestamp
        }
