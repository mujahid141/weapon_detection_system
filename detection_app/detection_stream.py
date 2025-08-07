import cv2
from ultralytics import YOLO

class DetectionStream:
    def __init__(self, video_path):
        self.cap = cv2.VideoCapture(video_path)
        self.model = YOLO('../weapon_model/yolov8n_weapon_best.pt')  # Load YOLOv8 model
        self.running = False
        self.stats = {"detections": 0}

    def start(self):
        self.running = True

    def get_frame(self):
        if not self.running:
            return None

        ret, frame = self.cap.read()
        if not ret:
            self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            return None

        # Run detection
        results = self.model(frame)[0]

        # Draw bounding boxes
        for box in results.boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            conf = float(box.conf[0])
            cls = int(box.cls[0])
            label = f"{self.model.names[cls]} {conf:.2f}"

            # Draw rectangle and label
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(frame, label, (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)

        self.stats["detections"] = len(results.boxes)

        return frame

    def get_stats(self):
        return self.stats
