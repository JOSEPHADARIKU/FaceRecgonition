import cv2
import time
import os
from detector.face_detector import FaceDetector
from utils.logger import log
from utils.config import Config
from datetime import datetime
import numpy as np
import threading
import winsound
import tkinter as tk
from tkinter import messagebox

class VideoStream:
    def __init__(self, source=0):
        self.cap = cv2.VideoCapture(source)
        self.detector = FaceDetector()
        self.face_count = 0
        os.makedirs("faces", exist_ok=True)
        os.makedirs("logs", exist_ok=True)
        self.prev_time = time.time()
        self.detection_history = []
        self.sound_enabled = True

    def start(self):
        self.build_gui()

    def run_detection(self):
        while True:
            ret, frame = self.cap.read()
            if not ret:
                log("Failed to grab frame")
                break

            frame = cv2.flip(frame, 1)
            faces = self.detector.detect_faces(frame)

            self.face_count = len(faces)
            self.detection_history.append((datetime.now(), self.face_count))

            for i, (x, y, w, h) in enumerate(faces, start=1):
                cx, cy = x + w // 2, y + h // 2
                if Config.ZONE_ONLY and not self.in_detection_zone(cx, cy):
                    continue
                cv2.rectangle(frame, (x, y), (x + w, y + h), Config.RECT_COLOR, 2)
                cv2.circle(frame, (cx, cy), 3, (255, 0, 0), -1)
                cv2.putText(frame, f"Face {i}", (x, y - 10), Config.FONT, 0.7, Config.TEXT_COLOR, 2)

            fps = self.calculate_fps()
            cv2.putText(frame, f"Total Faces: {self.face_count}", (10, 30), Config.FONT, 0.7, Config.TEXT_COLOR, 2)
            cv2.putText(frame, f"FPS: {fps:.2f}", (10, 60), Config.FONT, 0.7, (0, 255, 255), 2)

            if Config.ZONE_ONLY:
                self.draw_detection_zone(frame)

            cv2.imshow("Face Detection", frame)

            if self.face_count > 0 and self.sound_enabled:
                threading.Thread(target=self.beep_alert).start()

            key = cv2.waitKey(1) & 0xFF
            if key == ord("q"):
                log("Quitting video stream")
                self.save_history()
                break
            elif key == ord("s"):
                self.save_faces(frame, faces)

        self.cap.release()
        cv2.destroyAllWindows()

    def save_faces(self, frame, faces):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        for i, (x, y, w, h) in enumerate(faces, start=1):
            face_img = frame[y:y + h, x:x + w]
            filename = f"faces/face_{timestamp}_{i}.jpg"
            cv2.imwrite(filename, face_img)
            log(f"Saved {filename}")

    def calculate_fps(self):
        current_time = time.time()
        fps = 1 / (current_time - self.prev_time)
        self.prev_time = current_time
        return fps

    def beep_alert(self):
        try:
            winsound.Beep(1000, 100)
        except:
            pass

    def save_history(self):
        with open("logs/history.log", "w") as f:
            for entry_time, count in self.detection_history:
                f.write(f"{entry_time.strftime('%Y-%m-%d %H:%M:%S')} - Faces: {count}\n")
        log("Detection history saved.")

    def build_gui(self):
        window = tk.Tk()
        window.title("Face Detection Control")

        start_btn = tk.Button(window, text="Start Detection", command=lambda: threading.Thread(target=self.run_detection).start())
        start_btn.pack(pady=10)

        sound_btn = tk.Button(window, text="Toggle Sound", command=self.toggle_sound)
        sound_btn.pack(pady=10)

        quit_btn = tk.Button(window, text="Quit", command=window.quit)
        quit_btn.pack(pady=10)

        window.mainloop()

    def toggle_sound(self):
        self.sound_enabled = not self.sound_enabled
        status = "ON" if self.sound_enabled else "OFF"
        messagebox.showinfo("Sound Toggled", f"Beep Sound is now {status}")

    def draw_detection_zone(self, frame):
        h, w = frame.shape[:2]
        x1 = int(w * 0.3)
        y1 = int(h * 0.3)
        x2 = int(w * 0.7)
        y2 = int(h * 0.7)
        cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 255, 0), 2)

    def in_detection_zone(self, cx, cy):
        h = int(self.cap.get(4))
        w = int(self.cap.get(3))
        x1 = int(w * 0.3)
        y1 = int(h * 0.3)
        x2 = int(w * 0.7)
        y2 = int(h * 0.7)
        return x1 <= cx <= x2 and y1 <= cy <= y2