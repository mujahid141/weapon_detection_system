import cv2
import threading
import dill  # Required if your models were serialized with dill
from ultralytics import YOLO

# Load two models: one for person detection, one for weapon detection
person_model = YOLO('weapon_model/yolov8n.pt')  # Replace with your person model if needed
weapon_model = YOLO('weapon_model/best.pt')

weapon_names = ['Gun', 'Knife', 'Gernade']

class DetectionStream:
    def __init__(self, rtsp_url):
        self.rtsp_url = rtsp_url
        self.capture = cv2.VideoCapture(rtsp_url)
        self.frame = None
        self.stats = {name: 0 for name in weapon_names}
        self.running = False

    def start(self):
        self.running = True
        thread = threading.Thread(target=self._update, daemon=True)
        thread.start()

    def stop(self):
        self.running = False
        self.capture.release()

    def _update(self):
        while self.running:
            ret, frame = self.capture.read()
            if not ret:
                continue

            # Step 1: Detect people
            person_results = person_model(frame)
            has_person = False

            for box in person_results[0].boxes.cls.tolist():
                label = person_results[0].names[int(box)]
                if label == "person":
                    has_person = True
                    break

            if has_person:
                # Step 2: Save screenshot and run weapon detection
                weapon_results = weapon_model(frame)

                # Draw boxes from weapon detection
                self.frame = weapon_results[0].plot()

                # Count weapon detections
                self.stats = {name: 0 for name in weapon_names}
                for cls_id in weapon_results[0].boxes.cls.tolist():
                    label = weapon_results[0].names[int(cls_id)]
                    if label in self.stats:
                        self.stats[label] += 1
            else:
                # No person detected, just show frame
                self.frame = frame
                self.stats = {name: 0 for name in weapon_names}

    def get_frame(self):
        return self.frame

    def get_stats(self):
        return self.stats
