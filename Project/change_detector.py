import sys
import cv2
import numpy as np

def compare_images(image1_path, image2_path, threshold=30):
    # 1) Fotoğrafları oku (gri tonlamalı)
    img1 = cv2.imread(image1_path, cv2.IMREAD_GRAYSCALE)
    img2 = cv2.imread(image2_path, cv2.IMREAD_GRAYSCALE)

    if img1 is None or img2 is None:
        print("0")
        return

    # 2) Fotoğraf boyutlarını eşitle
    if img1.shape != img2.shape:
        img2 = cv2.resize(img2, (img1.shape[1], img1.shape[0]))

    # 3) Farkı al
    diff = cv2.absdiff(img1, img2)

    # 4) Gürültü azaltma (küçük farkları temizlemek için)
    blur = cv2.GaussianBlur(diff, (5, 5), 0)

    # 5) İkili maske (threshold)
    _, thresh_img = cv2.threshold(blur, 25, 255, cv2.THRESH_BINARY)

    # 6) Beyaz piksel sayısı (fark miktarı)
    diff_pixels = np.sum(thresh_img == 255)
    total_pixels = img1.shape[0] * img1.shape[1]
    diff_percentage = (diff_pixels / total_pixels) * 100

    # 7) Threshold kontrolü
    if diff_percentage > threshold:
        print("1")  # değişim var
    else:
        print("0")  # değişim yok

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("0")
        sys.exit(0)

    image1_path = sys.argv[1]
    image2_path = sys.argv[2]
    # Default threshold: 30 (%)
    compare_images(image1_path, image2_path, threshold=30)
