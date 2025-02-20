import cv2
import numpy as np
import tkinter as tk
from tkinter import filedialog

def select_file():
    # Hide the main Tkinter window and open file dialog
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(
        title="Select an image file",
        filetypes=[("Image Files", "*.jpg *.jpeg *.png")]
    )
    return file_path

# --- Step 1: Let the user select two images ---
print("Select the first image:")
image_path1 = select_file()
if not image_path1:
    print("No file selected for the first image.")
    exit()

print("Select the second image:")
image_path2 = select_file()
if not image_path2:
    print("No file selected for the second image.")
    exit()

# --- Step 2: Load images using OpenCV ---
image1 = cv2.imread(image_path1)
image2 = cv2.imread(image_path2)
if image1 is None or image2 is None:
    print("Error loading images.")
    exit()

# --- Step 3: Face Detection using OpenCV DNN ---
# Paths for face detection model (download these files beforehand)
detector_prototxt = "./deploy.prototxt"  # Caffe deploy file for face detection
detector_model = "res10_300x300_ssd_iter_140000.caffemodel"  # Pre-trained weights

# Create the face detector
face_detector = cv2.dnn.readNetFromCaffe(detector_prototxt, detector_model)

def get_face_embedding(image, detector, embedder):
    (h, w) = image.shape[:2]
    # Resize and create blob for face detection
    resized = cv2.resize(image, (300, 300))
    print("Resized image shape:", resized.shape)  # Debug
    blob = cv2.dnn.blobFromImage(resized, 1.0, (300, 300), (104.0, 177.0, 123.0))
    print("Blob shape:", blob.shape)  # Should be (1, 3, 300, 300)
    
    # Set input and run forward pass
    detector.setInput(blob)
    detections = detector.forward()
    print("Detections shape:", detections.shape)  # Debug

    if detections.shape[2] > 0:
        # Get the index of the detection with the highest confidence
        i = np.argmax(detections[0, 0, :, 2])
        confidence = detections[0, 0, i, 2]
        if confidence < 0.5:
            return None, None  # Confidence too low
        # Compute face bounding box
        box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
        (startX, startY, endX, endY) = box.astype("int")
        face = image[startY:endY, startX:endX]
        # Preprocess face for embedding extraction
        face_blob = cv2.dnn.blobFromImage(face, 1.0/255, (96, 96), (0, 0, 0), swapRB=True, crop=False)
        embedder.setInput(face_blob)
        vec = embedder.forward()
        return vec.flatten(), (startX, startY, endX, endY)
    else:
        return None, None

# --- Step 4: Load face embedding model (OpenFace) ---
# Download "openface_nn4.small2.v1.t7" and place it in the same directory.
embedder_model = "./openface.nn4.small2.v1.t7"
embedder = cv2.dnn.readNetFromTorch(embedder_model)

# Extract face embeddings for both images
embedding1, box1 = get_face_embedding(image1, face_detector, embedder)
embedding2, box2 = get_face_embedding(image2, face_detector, embedder)

if embedding1 is None:
    print("No face detected in the first image.")
    exit()
if embedding2 is None:
    print("No face detected in the second image.")
    exit()

# --- Step 5: Compare the face embeddings ---
def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

similarity = cosine_similarity(embedding1, embedding2)
print("Cosine similarity:", similarity)

# Choose a threshold (for cosine similarity, values closer to 1 indicate a higher match)
match = similarity > 0.5  # Adjust this threshold as needed

# --- Step 6: Display the Results ---
# Draw bounding boxes on the original images
if box1 is not None:
    (startX, startY, endX, endY) = box1
    cv2.rectangle(image1, (startX, startY), (endX, endY), (0, 255, 0), 2)
if box2 is not None:
    (startX, startY, endX, endY) = box2
    cv2.rectangle(image2, (startX, startY), (endX, endY), (0, 255, 0), 2)

# --- Resize images to a common height before concatenation ---
(h1, w1) = image1.shape[:2]
(h2, w2) = image2.shape[:2]
common_height = min(h1, h2)

new_width1 = int(w1 * common_height / h1)
new_width2 = int(w2 * common_height / h2)

resized_image1 = cv2.resize(image1, (new_width1, common_height))
resized_image2 = cv2.resize(image2, (new_width2, common_height))

# Concatenate images side-by-side for display
combined = np.hstack((resized_image1, resized_image2))
result_text = "FACE MATCHED" if match else "FACE DOESNT MATCH"
cv2.putText(combined, result_text, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 255), 3)

cv2.imshow("Face Comparison", combined)
cv2.waitKey(0)
cv2.destroyAllWindows()
