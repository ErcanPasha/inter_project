import argparse
import os
import glob
import time
from detector import Detector

IMG_EXTS = (".jpg", ".jpeg", ".png", ".bmp")

def iter_images(paths):
    for p in paths:
        if os.path.isdir(p):
            for ext in IMG_EXTS:
                for f in sorted(glob.glob(os.path.join(p, f"*{ext}"))):
                    yield f
        elif os.path.isfile(p) and p.lower().endswith(IMG_EXTS):
            yield p
        else:
            print(f"[skip] Not an image or directory: {p}")


def main():
    ap = argparse.ArgumentParser(
        description="Manual person detector using YOLOv4-tiny (counts only)."
    )
    ap.add_argument(
        "inputs",
        nargs="+",
        help="Image files and/or directories to process",
    )
    ap.add_argument("--cfg", default="yolov4-tiny.cfg", help="Path to YOLO cfg file")
    ap.add_argument(
        "--weights", default="yolov4-tiny.weights", help="Path to YOLO weights file"
    )
    ap.add_argument(
        "--names", default="coco.names", help="Path to class names (COCO)"
    )
    ap.add_argument(
        "--benchmark", action="store_true", help="Show per-image inference time"
    )
    args = ap.parse_args()

    det = Detector(
        cfg_path=args.cfg, weights_path=args.weights, names_path=args.names
    )

    processed = 0
    total_people = 0

    for img_path in iter_images(args.inputs):
        processed += 1
        t0 = time.time()
        cnt = det.count_people(img_path)
        elapsed = (time.time() - t0) * 1000.0
        total_people += cnt
        if args.benchmark:
            print(f"{img_path}: {cnt} person(s)\t{elapsed:.1f} ms")
        else:
            print(f"{img_path}: {cnt} person(s)")

    print(f"-- Done. Processed {processed} image(s). Total people counted: {total_people}.")


if __name__ == "__main__":
    main()
