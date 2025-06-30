# 🟢 Face Detection Pro

Welcome to Face Detection Pro, a real-time face detection system built for folks who love clean Python projects — no internet nonsense, no weird installs, no headaches. Just pure offline tech, structured properly, feature-packed, ready to flex your Python skills.

💻 What This Does:
✅ Real-time face detection using your webcam or video files
✅ Uses pure OpenCV — no dlib, no extra system installs needed
✅ Fancy FPS counter to track performance
✅ Snapshots of detected faces saved with timestamps
✅ Sound alert when a face is spotted (toggleable)
✅ Simple GUI window to control detection without touching terminal
✅ Detection zone: Only detect faces inside the center of the frame (optional)
✅ History logs of face counts saved when you quit
✅ Fully offline — no internet, no API keys, no sneaky downloads

📦 Project Structure:
FaceDetectionPro/
├── main.py               # The main entry point
├── detector/
│   ├── face_detector.py  # Handles face detection logic (pure OpenCV)
│   ├── video_stream.py   # Video stream + GUI + detection
├── utils/
│   ├── logger.py         # Handles logging
│   ├── config.py         # Central config for colors/zones
├── faces/                # Snapshots of detected faces saved here
├── logs/                 # System logs & detection history
└── requirements.txt      # Dependencies

🚀 Quick Start:
Install Requirements

pip install -r requirements.txt
Run the Program

python main.py
Use the GUI to start detection, toggle sound, or quit anytime.

🎯 Requirements:
Python 3.7+

OpenCV

Numpy

(Already listed in requirements.txt for easy install)

💡 Why This Exists:
Because face detection projects don't have to be messy. This project started basic, but evolved into a maxed-out, modular, offline-friendly system — no internet, no complex setups, just clean code that works.

✨ Credits:
Big shout to OpenCV and Python for making computer vision easy.

🤘 Final Note:
Use this responsibly. It's for personal projects, learning, or fun offline tools.
Enjoy the project — and welcome to the cool dev squad.

