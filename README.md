# PTE_SSDMS – Smart Stop Density Monitoring (Human‑Aware)

> **TL;DR**: Camera captures every **5s**, compares the last two frames, and if the visual change is high **and** at least one **person** is detected (YOLOv4‑tiny), it uploads the last 12 images to Google Drive via **rclone** and sends a structured MQTT payload to **ThingsBoard**.

---

## 1) What is this?
A lightweight IoT pipeline for **public transportation stop density monitoring**. It reduces false alarms by verifying **human presence** after change detection.

**Core scripts**
- **`camera_manager.py`** – Main orchestrator: capture → housekeeping (keep last 12) → trigger flow.
- **`change_detector.py`** – Compares `n` vs `n-1` image; emits a numeric **diff score** (current threshold ≈ **120000**).
- **`detector.py`** – Human verification using **YOLOv4‑tiny**; returns people count.
- **`uploader.py`** – Zips last 12 images and uploads to Google Drive (**rclone**); publishes MQTT to **ThingsBoard**.
- **`manual_detector/`** – **Standalone quick test** for human detection (see below). This folder also contains the **model files** for convenience.

---

## 2) Repository Structure (key parts)
```
Project/
  camera_manager.py
  change_detector.py
  detector.py
  uploader.py
manual_detector/
  manual_detector.py
  detector.py                   # same Detector class interface
  coco.names | yolov4-tiny.cfg | yolov4-tiny.weights
All FlowCharts of All Versions/ # flowchart images for each version
PTE_SSDMS.pdf                   # full technical report
Intern(tr).md                   # Turkish notes/summary
```
> **Note**: If the large model files are not in your clone, see **Model Files** below to download them in 1–2 minutes.

---

## 3) Quick Start
### A) Windows (PowerShell/CMD)
```bat
cd path\to\repo
python -m venv .venv && .venv\Scripts\activate
pip install -r requirements.txt
```

### B) Linux/Raspberry Pi
```bash
cd /path/to/repo
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

> **Dependencies (typical)**: `opencv-python`, `numpy`, `paho-mqtt`, `python-dotenv` (for tokens), plus **rclone** installed system‑wide for Drive upload.

---

## 4) Model Files (YOLOv4‑tiny)
These are **files**, not Python packages:  
- `yolov4-tiny.cfg` (architecture)  
- `yolov4-tiny.weights` (trained weights)  
- `coco.names` (labels; includes `person`)

**Option 1 – Use repo’s copy**: If present, files live in `manual_detector/` and are used in examples below.  
**Option 2 – Download yourself** (recommended for fresh setups):

### Windows (CMD)
```cmd
cd path\to\repo\manual_detector
curl -L -o coco.names https://raw.githubusercontent.com/pjreddie/darknet/master/data/coco.names
curl -L -o yolov4-tiny.cfg https://raw.githubusercontent.com/AlexeyAB/darknet/master/cfg/yolov4-tiny.cfg
curl -L -o yolov4-tiny.weights https://github.com/AlexeyAB/darknet/releases/download/darknet_yolo_v4_pre/yolov4-tiny.weights
```

### Linux/Raspberry Pi
```bash
cd /path/to/repo/manual_detector
curl -L -o coco.names https://raw.githubusercontent.com/pjreddie/darknet/master/data/coco.names
curl -L -o yolov4-tiny.cfg https://github.com/AlexeyAB/darknet/blob/master/cfg/yolov4-tiny.cfg?raw=1
curl -L -o yolov4-tiny.weights https://github.com/AlexeyAB/darknet/releases/download/darknet_yolo_v4_pre/yolov4-tiny.weights
```

> You can also keep them under `./models/` if you prefer.

---

## 5) Manual Quick Test (bypass full pipeline)
Run only the human‑detection step on a single image or a folder.

**Single image**
```bash
cd manual_detector
python manual_detector.py test.jpg --benchmark
```

**Folder (process all images)**
```bash
python manual_detector.py ./Images
```

Output sample: `test.jpg: 1 person(s)   24.7 ms`

---

## 6) Full Pipeline (demo)
1) **Configure tokens** (ThingsBoard, rclone) locally, e.g. with a `.env` file:
```
# .env (example)
TB_HOST=thingsboard.cloud
TB_TOKEN=YOUR_DEVICE_TOKEN
RCLONE_REMOTE=drivepi:
RCLONE_PATH=intern-images
```
2) **Run**
```bash
python Project/camera_manager.py
```
**Flow**: Capture every 5s → keep last 12 → diff > ~120000 → YOLO person check → if ≥1 person → zip last 12 + rclone upload → MQTT to ThingsBoard.

> Note: We **do not** send/preview the last image on ThingsBoard; all images are archived to the configured Cloud destination via rclone.

---

## 7) Dashboard & Screenshots
You can personalize a ThingsBoard dashboard quickly:
- Create an **Entity Alias** pointing to your device.
- Add **Latest values** widgets to display: `Person`, `Folder Name`, `Payload Sequence Number`.
- (Optional) Add a **Timeseries Chart** for `Person` to visualize detections over time.

Suggested screenshots for the repo:
- Repo overview (root folders)
- CMD: model downloads completed (if you install manually)
- `manual_detector.py --benchmark` console output
- Flowchart for the current version
- (Optional) Cloud folder view after an upload

Place images under `docs/img/` and reference them like:
```markdown
![Repo Overview](docs/img/repo.png)
![Manual Benchmark](docs/img/manual_benchmark.png)
![Flowchart](docs/img/flowchart.png)
```

---

## 8) Versions & History
Multiple iterations exist (baseline change‑only → human‑aware).  
You can browse earlier versions through **Git history/commits**.  
Flowchart images for earlier versions are in **All FlowCharts of All Versions**.

---

## 9) Files that must be located locally (not in repo)
- **Model files**: `yolov4-tiny.cfg`, `yolov4-tiny.weights`, `coco.names` (place under `manual_detector/` or `models/`).
- **Secrets**: a local `.env` file with your private values (e.g., `TB_HOST`, `TB_TOKEN`, `RCLONE_REMOTE`, `RCLONE_PATH`). Keep it on your machine; do **not** add it to the repo.

---

## 10) License & Credits
- YOLOv4‑tiny: AlexeyAB/darknet, COCO labels.
- Add your preferred license here (e.g., MIT).
