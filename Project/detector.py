import cv2
import os
import shutil
from datetime import datetime

class Detector:
    def __init__(self, output_dir="Detections",
                 cfg_path="yolov4-tiny.cfg",
                 weights_path="yolov4-tiny.weights",
                 names_path="coco.names"):
        self.output_dir = output_dir
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # COCO class names
        with open(names_path, "r") as f:
            self.classes = [line.strip() for line in f.readlines()]

        # YOLOv4-tiny model yükleme
        self.net = cv2.dnn.readNetFromDarknet(cfg_path, weights_path)
        self.net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
        self.net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)

        self.layer_names = self.net.getLayerNames()
        self.output_layers = [self.layer_names[i - 1] for i in self.net.getUnconnectedOutLayers()]

    def count_people(self, image_path):
        image = cv2.imread(image_path)
        if image is None:
            print(f"Image could not be read: {image_path}")
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
                if self.classes[class_id] == "person" and confidence > 0.5:
                    count += 1
        return count

    def run(self, images):
        """
        images: [n_frame, n_minus_1_frame, fast_1, fast_2 ...]
        1) İnsan sayısı tespiti//Detection of people number
        2) Zaman damgalı klasör oluşturma//Creating a timestamped folder
        3) Txt dosyası oluşturma//Creating folder txt
        """
        if len(images) < 2:
            print("Not Enough Images")
            return None

        # Zaman damgalı klasör ismi//Named timestamp folder
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        event_dir = os.path.join(self.output_dir, f"event_{timestamp}")
        os.makedirs(event_dir)

        # Txt dosyası için sonuç listesi//Result list for Txt folder
        counts = []
        labels = []

        # n-1 → images[1], n → images[0], others fast_x
        labels.append("n-1")
        counts.append(self.count_people(images[1]))

        labels.append("n")
        counts.append(self.count_people(images[0]))

        for i, fast_img in enumerate(images[2:], start=1):
            labels.append(f"fast_{i}")
            counts.append(self.count_people(fast_img))

        # Txt oluşturma//creating
        txt_path = os.path.join(event_dir, "counts.txt")
        with open(txt_path, "w") as f:
            for label, count in zip(labels, counts):
                f.write(f"{label}: {count}\n")

        # Fotoğrafları klasöre kopyala//Photo copy to folder
        for img_path in images:
            shutil.copy(img_path, event_dir)

        return {
            "event_dir": event_dir,
            "txt_path": txt_path,
            "counts": dict(zip(labels, counts)),
            "timestamp": timestamp
        }
