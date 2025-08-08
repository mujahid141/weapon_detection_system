import cv2
from ultralytics import YOLO

class DetectionStream:
    def __init__(self, video_path):
        self.cap = cv2.VideoCapture(video_path)

        # Load models
        self.weapon_model = YOLO('../weapon_model/yolov8n_weapon_best.pt')  # weapon detection
        self.person_model = YOLO('../weapon_model/yolov8n.pt')              # general person detection
        self.pose_model = YOLO('../weapon_model/yolov8n-pose.pt')           # pose estimation

        self.running = False
        self.stats = {
            "weapon_detections": 0,
            "person_detections": 0,
            "pose_detections": 0
        }

    def start(self):
        self.running = True

    def get_frame(self):
        if not self.running:
            return None

        ret, frame = self.cap.read()
        if not ret:
            self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            return None

        # ========== 1. Weapon Detection ==========
        weapon_results = self.weapon_model(frame)[0]
        for box in weapon_results.boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            conf = float(box.conf[0])
            cls = int(box.cls[0])
            label = f"{self.weapon_model.names[cls]} {conf:.2f}"
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)
            cv2.putText(frame, label, (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)

        # ========== 2. Person Detection ==========
        person_results = self.person_model(frame)[0]
        person_count = 0
        for box in person_results.boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            conf = float(box.conf[0])
            cls = int(box.cls[0])
            if self.person_model.names[cls] == 'person':
                person_count += 1
                label = f"Person {conf:.2f}"
                cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 255, 0), 2)
                cv2.putText(frame, label, (x1, y2 + 15),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 1)

        # ========== 3. Pose Detection ==========
        pose_results = self.pose_model(frame)[0]
        pose_labels = []

        if pose_results.keypoints is not None:
            for kp in pose_results.keypoints:
                label = classify_pose(kp)
                pose_labels.append(label)
                cv2.putText(frame, label, (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

        # Update stats (store only serializable types!)
        self.stats["weapon_detections"] = len(weapon_results.boxes)
        self.stats["person_detections"] = person_count
        self.stats["pose_detections"] = len(pose_results.keypoints) if pose_results.keypoints is not None else 0
        self.stats["pose_labels"] = pose_labels

        return frame

    def get_stats(self):
        return self.stats

def classify_pose(keypoints):
    if keypoints is None or len(keypoints.xy[0]) < 17:
        return "unknown"

    # Extract keypoints
    points = keypoints.xy[0]  # shape: (17, 2)
    
    # Indexes of key body parts
    LEFT_WRIST = 9
    RIGHT_WRIST = 10
    LEFT_ELBOW = 7
    RIGHT_ELBOW = 8
    LEFT_SHOULDER = 5
    RIGHT_SHOULDER = 6

    try:
        lw = points[LEFT_WRIST]
        rw = points[RIGHT_WRIST]
        le = points[LEFT_ELBOW]
        re = points[RIGHT_ELBOW]
        ls = points[LEFT_SHOULDER]
        rs = points[RIGHT_SHOULDER]

        # Shooting: One or both hands above shoulders and extended forward
        shooting_condition = (
            (lw[1] < ls[1] and le[1] < ls[1]) or
            (rw[1] < rs[1] and re[1] < rs[1])
        )
        # Threatening: hands up
        threatening_condition = (
            lw[1] < ls[1] and rw[1] < rs[1]
        )

        if shooting_condition:
            return "shooting"
        elif threatening_condition:
            return "threatening"
        else:
            return "normal"
    except:
        return "unknown"
