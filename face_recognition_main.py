import os
import shutil
import tkinter as tk
from tkinter import filedialog
from single_person_check_with_all import check_face_match

# ----- Configuration -----
GALLERY_FOLDER = "Gallery"
MATCH_THRESHOLD = 0.5  # Must match the threshold used in check_face_match

def select_file():
    """Opens a file dialog to let the user select an image."""
    root = tk.Tk()
    root.withdraw()
    return filedialog.askopenfilename(
        title="Select an image file",
        filetypes=[("Image Files", "*.jpg *.jpeg *.png")]
    )

def organize_image(new_image_path):
    """
    Organizes the new image into the proper Gallery subfolder based on face matching.
    Uses a representative image (first image found) from each folder for comparison.
    """
    # Create the gallery folder if it doesn't exist
    if not os.path.exists(GALLERY_FOLDER):
        os.makedirs(GALLERY_FOLDER)

    # Get list of existing person folders
    person_folders = [f for f in os.listdir(GALLERY_FOLDER) if os.path.isdir(os.path.join(GALLERY_FOLDER, f))]
    
    matched_folder = None
    # Check each folder for a match
    for folder in person_folders:
        folder_path = os.path.join(GALLERY_FOLDER, folder)
        # Use the first image in the folder as a representative
        folder_images = [f for f in os.listdir(folder_path) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
        if not folder_images:
            continue
        rep_image_path = os.path.join(folder_path, folder_images[0])
        if check_face_match(new_image_path, rep_image_path, threshold=MATCH_THRESHOLD):
            matched_folder = folder_path
            break

    if matched_folder:
        shutil.copy(new_image_path, matched_folder)
        print(f"Image added to existing folder: {matched_folder}")
    else:
        new_folder_name = f"Person {len(person_folders) + 1}"
        new_folder_path = os.path.join(GALLERY_FOLDER, new_folder_name)
        os.makedirs(new_folder_path)
        shutil.copy(new_image_path, new_folder_path)
        print(f"Image added to new folder: {new_folder_path}")

if __name__ == "__main__":
    print("Select a new image to organize into the gallery:")
    new_image_path = select_file()
    if not new_image_path:
        print("No image selected.")
    else:
        organize_image(new_image_path)
