import cv2

prototxt_path = "MobileNetSSD_deploy.prototxt.txt"  # adjust name if needed
model_path = "MobileNetSSD_deploy.caffemodel"

try:
    net = cv2.dnn.readNetFromCaffe(prototxt_path, model_path)
    print("Model loaded successfully.")
except Exception as e:
    print("Error loading model:", e)
    exit()
