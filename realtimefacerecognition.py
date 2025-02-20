import cv2
import numpy as np
import os

prototxt_path = "MobileNetSSD_deploy.prototxt.txt"  # adjust name if needed
model_path = "MobileNetSSD_deploy.caffemodel"

try:
    net = cv2.dnn.readNetFromCaffe(prototxt_path, model_path)
    print("Model loaded successfully.")
except Exception as e:
    print("Error loading model:", e)
    exit()

# (Assuming the model is already loaded as above)

# Initialize Haar Cascade for face detection
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Cannot open webcam")
    exit()

while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to capture frame")
        break

    # Add a label to see that processing is happening
    cv2.putText(frame, "Processing...", (10, 30), cv2.FONT_HERSHEY_SIMPLEX,
                1, (0, 255, 0), 2)
    
    # --- Object Detection ---
    blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)), 0.007843,
                                 (300, 300), 127.5)
    net.setInput(blob)
    detections = net.forward()

    for i in np.arange(0, detections.shape[2]):
        confidence = detections[0, 0, i, 2]
        if confidence > 0.2:  # Confidence threshold
            idx = int(detections[0, 0, i, 1])
            # Draw a bounding box around the detected object
            box = detections[0, 0, i, 3:7] * np.array(
                [frame.shape[1], frame.shape[0], frame.shape[1], frame.shape[0]])
            (startX, startY, endX, endY) = box.astype("int")
            cv2.rectangle(frame, (startX, startY), (endX, endY), (0, 255, 0), 2)
            text = f"Object: {confidence*100:.1f}%"
            cv2.putText(frame, text, (startX, startY - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    # --- Face Detection ---
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
        cv2.putText(frame, "Face", (x, y - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

    # Show the frame
    cv2.imshow("Image Recognition", frame)
    
    # Break loop on 'q' key press
    if cv2.waitKey(1) & 0xFF == ord('q') or cv2.getWindowProperty("Image Recognition", cv2.WND_PROP_VISIBLE) < 1:
        break

cap.release()
cv2.destroyAllWindows()
