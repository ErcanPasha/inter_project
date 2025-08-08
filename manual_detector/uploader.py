import os
import shutil
import subprocess
import paho.mqtt.client as mqtt
import json
import time

class Uploader:
    def __init__(self,
                 broker="mqtt.thingsboard.cloud",
                 port=1883,
                 access_token="aQ3eNcaKthG279lMKJMp",
                 topic="v1/devices/me/telemetry",
                 rclone_remote="drivepi"):
        self.broker = broker
        self.port = port
        self.access_token = access_token
        self.topic = topic
        self.rclone_remote = rclone_remote
        self.payload_sequence = 0

        # MQTT setup
        self.client = mqtt.Client()
        self.client.username_pw_set(self.access_token)
        self.client.connect(self.broker, self.port, 60)

    def _read_counts_from_txt(self, event_dir):
        """Read counts.txt file and return dictionary of counts"""
        counts_path = os.path.join(event_dir, "counts.txt")
        counts = {}
        if not os.path.exists(counts_path):
            print(f"Warning: counts.txt not found in {event_dir}")
            return counts

        with open(counts_path, "r") as f:
            for line in f:
                try:
                    label, value = line.strip().split(":")
                    counts[label.strip()] = int(value.strip())
                except ValueError:
                    print(f"Warning: Invalid line in counts.txt -> {line}")
        return counts

    def _create_zip(self, folder_path):
        """Zip a folder and return zip path"""
        zip_path = shutil.make_archive(folder_path, 'zip', folder_path)
        return zip_path

    def _send_payload(self, timestamp, counts):
        """Send payload to ThingsBoard"""
        self.payload_sequence += 1

        payload = {
            "Folder Name": f"event_{timestamp}",
            "Payload Sequence Number": self.payload_sequence
        }
        # Add counts info to payload
        for label, count in counts.items():
            payload[f"{label} Person"] = count

        self.client.publish(self.topic, json.dumps(payload))
        print(f"Payload sent to ThingsBoard: {payload}")

    def _upload_to_drive(self, zip_path):
        """Upload zip file to Google Drive using rclone into daily folder"""
        date_folder = time.strftime("%Y-%m-%d")
        remote_path = f"{self.rclone_remote}:events/{date_folder}"
        try:
            subprocess.run(["rclone", "copy", zip_path, remote_path], check=True)
            print(f"Uploaded to Google Drive: {zip_path} -> {remote_path}")
        except subprocess.CalledProcessError as e:
            print(f"Error uploading {zip_path}: {e}")

    def upload_event(self, detector_event_dir, last12_dir, timestamp):
        """
        detector_event_dir: Detector output folder (with counts.txt and photos)
        last12_dir: Folder with last 12 images
        timestamp: event timestamp string
        """
        print("Uploader started...")

        # 1. Read counts from detector counts.txt
        counts = self._read_counts_from_txt(detector_event_dir)
        if not counts:
            print("Warning: No counts found, aborting upload.")
            return False

        # 2. Send payload to ThingsBoard
        self._send_payload(timestamp, counts)

        # 3. Zip and upload both folders
        zip_detector = self._create_zip(detector_event_dir)
        zip_last12 = self._create_zip(last12_dir)

        self._upload_to_drive(zip_detector)
        self._upload_to_drive(zip_last12)

        print("Uploader finished successfully.")
        return True
