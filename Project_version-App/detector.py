import cv2
from datetime import datetime

class Detector:
    """
    - Yalnızca sayım yapar: iki kare (N ve N-1) arasındaki 'person' nesnelerini sayar.
    - Dosya/klasör/zip üretmez; yalnızca sonuç ve meta döndürür.
    - Hata toleranslı: Görsel okunamazsa 0 sayar ve meta.warnings içine not düşer.
    """

    def __init__(
        self,
        cfg_path="yolov4-tiny.cfg",
        weights_path="yolov4-tiny.weights",
        names_path="coco.names",
        confidence_threshold=0.65,
        input_size=(416, 416)
    ):
        self.conf_threshold = float(confidence_threshold)
        self.input_size = tuple(input_size)

        # Sınıf adları
        with open(names_path, "r") as f:
            self.classes = [line.strip() for line in f.readlines()]

        # YOLO model
        self.net = cv2.dnn.readNetFromDarknet(cfg_path, weights_path)
        self.net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
        self.net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)

        self.layer_names = self.net.getLayerNames()
        self.output_layers = [self.layer_names[i - 1] for i in self.net.getUnconnectedOutLayers()]

        # Model adı meta için
        self.model_name = "yolov4-tiny"

    def _count_people_in_image(self, image_path, warnings):
        """Tek görselde kişi sayar; okunamazsa 0 ve warnings'e not ekler."""
        image = cv2.imread(image_path)
        if image is None:
            warnings.append(f"failed_to_read:{image_path}")
            return 0

        blob = cv2.dnn.blobFromImage(
            image, 1/255.0, self.input_size, swapRB=True, crop=False
        )
        self.net.setInput(blob)
        layer_outputs = self.net.forward(self.output_layers)

        count = 0
        for output in layer_outputs:
            for detection in output:
                scores = detection[5:]
                class_id = int(scores.argmax())
                confidence = float(scores[class_id])
                if self.classes[class_id] == "person" and confidence > self.conf_threshold:
                    count += 1
        return count

    def run(self, n_path, n_1_path):
        """
        Girdi: n_path (son kare), n_1_path (bir önceki kare)
        Çıktı:
            {
              "people_n": int,
              "people_n_1": int,
              "delta": int,
              "meta": {
                  "model": "yolov4-tiny",
                  "confidence_threshold": 0.65,
                  "ts_process": "YYYY-mm-ddTHH:MM:SSZ",
                  "warnings": [ ... ]   # opsiyonel
              }
            }
        """
        warnings = []

        people_n_1 = self._count_people_in_image(n_1_path, warnings)
        people_n   = self._count_people_in_image(n_path, warnings)
        delta = int(people_n - people_n_1)

        meta = {
            "model": self.model_name,
            "confidence_threshold": self.conf_threshold,
            "ts_process": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
        }
        if warnings:
            meta["warnings"] = warnings  # UI'da göstermek zorunda değilsin; teşhis için tutulur.

        return {
            "people_n": int(people_n),
            "people_n_1": int(people_n_1),
            "delta": delta,
            "meta": meta
        }
