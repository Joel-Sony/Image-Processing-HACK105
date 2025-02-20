import customtkinter as ctk
import cv2
import numpy as np
import torch
from tkinter import filedialog
from ultralytics import YOLO
from threading import Thread

# Load YOLOv8 model
model = YOLO("yolov8n.pt")

# Global variables
cap = None
running = False


def detect_objects(frame):
    """Run YOLO object detection on a frame."""
    results = model(frame)
    for box in results[0].boxes:
        x1, y1, x2, y2 = map(int, box.xyxy[0])  # Bounding box
        confidence = float(box.conf[0])  # Confidence
        class_name = model.names[int(box.cls[0])]  # Class name
        
        # Draw bounding box & label
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 3)
        cv2.putText(frame, f"{class_name} {confidence:.2f}", (x1, y1 - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
    return frame


def process_video(video_path):
    """Process a selected video file."""
    global running
    running = True
    cap = cv2.VideoCapture(video_path)
    
    while cap.isOpened() and running:
        ret, frame = cap.read()
        if not ret:
            break
        
        frame = detect_objects(frame)
        cv2.imshow("YOLOv8 Object Detection", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


def process_webcam():
    """Process real-time object detection using webcam."""
    global cap, running
    running = True
    cap = cv2.VideoCapture(0)  # 0 = default webcam
    
    while cap.isOpened() and running:
        ret, frame = cap.read()
        if not ret:
            break
        
        frame = detect_objects(frame)
        cv2.imshow("YOLOv8 Real-Time Detection", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


def select_video():
    """Open file dialog to select a video and process it."""
    file_path = filedialog.askopenfilename(filetypes=[("Video files", "*.mp4;*.avi;*.mov")])
    if file_path:
        Thread(target=process_video, args=(file_path,)).start()


def start_webcam():
    """Start webcam-based object detection."""
    Thread(target=process_webcam).start()


def stop_detection():
    """Stop any running detection."""
    global running
    running = False


# CustomTkinter GUI
app = ctk.CTk()
app.title("Object Detection GUI")
app.geometry("300x245")
custom_font = ctk.CTkFont(family="Helvetica", size=18, weight="bold")

btn_video = ctk.CTkButton(app,fg_color ="#3498DB",text="Select Video", command=select_video, width=250, height=50,font = custom_font)
btn_video.pack(pady=15)

btn_webcam = ctk.CTkButton(app,fg_color ="#3498DB", text="Use Webcam", command=start_webcam, width=250, height=50,font = custom_font)
btn_webcam.pack(pady=15)

btn_stop = ctk.CTkButton(app,fg_color ="#E74C3C", text="Stop Detection", command=stop_detection, width=250, height=50,font = custom_font)
btn_stop.pack(pady=15)

app.mainloop()
