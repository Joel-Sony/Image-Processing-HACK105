import cv2
import numpy as np

# Model paths (update these paths if needed)
DETECTOR_PROTO = "./deploy.prototxt"  # Caffe deploy file for face detection
DETECTOR_MODEL = "res10_300x300_ssd_iter_140000.caffemodel"  # Detector weights
EMBEDDER_MODEL = "./openface.nn4.small2.v1.t7"  # Face embedding model

# Load models globally
face_detector = cv2.dnn.readNetFromCaffe(DETECTOR_PROTO, DETECTOR_MODEL)
embedder = cv2.dnn.readNetFromTorch(EMBEDDER_MODEL)

def get_face_embedding(image_path):
    """
    Loads an image, detects the largest face, and returns its embedding vector.
    Returns None if no valid face is detected.
    """
    image = cv2.imread(image_path)
    if image is None:
        return None
    (h, w) = image.shape[:2]
    # Resize to 300x300 for detection
    resized = cv2.resize(image, (300, 300))
    blob = cv2.dnn.blobFromImage(resized, 1.0, (300, 300), (104.0, 177.0, 123.0))
    face_detector.setInput(blob)
    detections = face_detector.forward()
    if detections.shape[2] > 0:
        # Use the detection with highest confidence
        i = np.argmax(detections[0, 0, :, 2])
        confidence = detections[0, 0, i, 2]
        if confidence < 0.5:
            return None
        box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
        (startX, startY, endX, endY) = box.astype("int")
        face = image[startY:endY, startX:endX]
        if face.size == 0:
            return None
        face_blob = cv2.dnn.blobFromImage(face, 1.0/255, (96, 96), (0, 0, 0), swapRB=True, crop=False)
        embedder.setInput(face_blob)
        vec = embedder.forward()
        return vec.flatten()
    else:
        return None

def check_face_match(image_path1, image_path2, threshold=0.5):
    """
    Compares two images and returns True if they are of the same person, else False.
    """
    embedding1 = get_face_embedding(image_path1)
    embedding2 = get_face_embedding(image_path2)
    if embedding1 is None or embedding2 is None:
        return False
    similarity = np.dot(embedding1, embedding2) / (np.linalg.norm(embedding1) * np.linalg.norm(embedding2))
    # Return True if similarity is above the threshold (i.e. faces match)
    return similarity > threshold

if __name__ == "__main__":
    # For testing: prompt user to select two images and print the result.
    import tkinter as tk
    from tkinter import filedialog

    def select_file():
        root = tk.Tk()
        root.withdraw()
        return filedialog.askopenfilename(
            title="Select an image file",
            filetypes=[("Image Files", "*.jpg *.jpeg *.png")]
        )

    print("Select the first image:")
    img1 = select_file()
    print("Select the second image:")
    img2 = select_file()
    result = check_face_match(img1, img2, threshold=0.5)
    print("Faces match:" if result else "Faces do not match")
