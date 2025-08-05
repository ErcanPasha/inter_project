import cv2
import numpy as np

class ChangeDetector:
    def __init__(self, diff_threshold=50000):
        # Fark eşik değeri: ne kadar değişiklikte tetikleme olsun
        self.diff_threshold = diff_threshold

    def detect_change(self, images):
        """
        Kendisine gelen iki fotoğrafı karşılaştırır//Comparing two photos come from camera_manager (n ve n-1).
        images: [n_frame_path, n_minus_1_frame_path]
        True: değişim var//change, False: değişim yok//no change
        """
        if len(images) != 2:
            print("Karşılaştırma için iki görüntü yolu gerekli.")
            return False

        img1 = cv2.imread(images[0])
        img2 = cv2.imread(images[1])

        if img1 is None or img2 is None:
            print("Fotoğraf(lar) yüklenemedi.")
            return False

        # Gri ton ve blur ile küçük gürültüleri azalt
        gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
        gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
        gray1 = cv2.GaussianBlur(gray1, (21, 21), 0)
        gray2 = cv2.GaussianBlur(gray2, (21, 21), 0)

        # Fark ve threshold
        diff = cv2.absdiff(gray1, gray2)
        _, thresh = cv2.threshold(diff, 25, 255, cv2.THRESH_BINARY)
        change_score = np.sum(thresh)

        return change_score > self.diff_threshold
