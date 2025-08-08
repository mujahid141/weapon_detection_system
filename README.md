# 🔫 Weapon Detection System (Django + YOLOv8)

A **real-time weapon detection system** built with **Django** and **Ultralytics YOLOv8**.  
This project can detect:
- **Weapons** (custom fine-tuned YOLOv8n model)
- **Persons** (YOLOv8n pretrained)
- **Human Pose** (YOLOv8n-pose for activity classification like shooting or threatening)

The system supports **live video streaming** and **detection statistics** via Django views.

---

## 🚀 Features
- **Weapon Detection** → Uses a custom-trained YOLOv8n model.
- **Person Detection** → Identifies people in the video feed.
- **Pose Estimation** → Detects human posture and classifies as `shooting`, `threatening`, or `normal`.
- **Real-time Streaming** → Supports HLS or direct MJPEG streaming.
- **Live Stats API** → Returns detection counts & pose labels as JSON for frontend display.

---

## 📂 Project Structure

weapon_detection_system/
│
├── detection_app/ # Main Django app for detection
│ ├── views.py # Detection logic & streaming endpoints
│ ├── models.py # (Optional) Django models if used
│ ├── templates/ # HTML templates for frontend
│ └── static/ # CSS/JS/Images
│
├── weapon_model/ # YOLO model files
│ ├── yolov8n.pt # Person detection
│ ├── yolov8n-pose.pt # Pose estimation
│ └── yolov8n_weapon_best.pt# Custom fine-tuned weapon detection
│
├── requirements.txt # Python dependencies
├── manage.py
└── README.md # This file



---

## 🛠️ Installation

### 1️⃣ Clone the Repository
### bash
git clone https://github.com/mujahid141/weapon-detection-system.git
cd weapon-detection-system


python -m venv env
## 🛠️ Installation
## windows
env\Scripts\activate

## Linux/Mac
source env/bin/activate

## 🛠️ Installation Dependencies

pip install -r requirements.txt



## Configuration
Place your YOLO model files (yolov8n.pt, yolov8n-pose.pt, yolov8n_weapon_best.pt) in the weapon_model/ folder.

Update paths in views.py if needed:

python
Copy
Edit
self.weapon_model = YOLO('weapon_model/yolov8n_weapon_best.pt')
self.person_model = YOLO('weapon_model/yolov8n.pt')
self.pose_model   = YOLO('weapon_model/yolov8n-pose.pt')


## System FLow

RTSP Camera / Video File
        ↓
      FFmpeg
        ↓
     YOLOv8 Models
 (Weapon, Person, Pose)
        ↓
   Django Backend
 (Video Processing + Stats)
        ↓
   HTML/CSS/JS Frontend
 (Live Stream + Graphs)



## Contributing
Pull requests are welcome!
For major changes, please open an issue first to discuss what you would like to change.