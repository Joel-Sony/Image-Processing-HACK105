import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog, Toplevel
import subprocess
from textToImage import imagetotext
import tkinter.font as tkFont
from PIL import Image, ImageTk

class MainMenu(ctk.CTkFrame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.pack(fill='both', expand=True)
        self.configure(fg_color="#2C3E50")  # Background color
        self.grid_columnconfigure(0, weight=1)
        custom_font = ctk.CTkFont(family="Helvetica", size=14, weight="bold")
        # Object Recognition Button
        self.obj_recog_btn = ctk.CTkButton(self, text="Object Recognition",
                                           height=50, command=self.launch_object_recognition,
                                           fg_color="#3498DB", hover_color="#2980B9",font=custom_font)
        self.obj_recog_btn.grid(padx=20, pady=10, sticky='ew')

        # Text Recognition Button
        self.text_recog_btn = ctk.CTkButton(self, text="Text Recognition",
                                            height=50, command=self.launch_text_recognition,
                                            fg_color="#3498DB", hover_color="#2980B9",font=custom_font)
        self.text_recog_btn.grid(padx=20, pady=10, sticky='ew')

        # Face Recognition Button
        self.face_recog_btn = ctk.CTkButton(self, text="Face Recognition",
                                            height=50, command=self.launch_face_recognition,
                                            fg_color="#3498DB", hover_color="#2980B9",font=custom_font)
        self.face_recog_btn.grid(padx=20, pady=10, sticky='ew')

        # Exit Button
        self.exit_btn = ctk.CTkButton(self, text="Exit",
                                      height=50, command=self.exit_program,
                                      fg_color="#E74C3C", hover_color="#C0392B",font=custom_font)
        self.exit_btn.grid(padx=20, pady=10, sticky='ew')

    def launch_object_recognition(self):
        print("Launching Object Recognition...")
        subprocess.call(["python", "main.pyw"])

    def select_file(self):
        root = tk.Tk()
        root.withdraw()
        return filedialog.askopenfilename(title="Select an image file",
                                          filetypes=[('Image Files', '*.jpg *.jpeg *.png')])

    def launch_text_recognition(self):
        print("Launching Text Recognition...")
        selected_file = self.select_file()
        if selected_file:
            self.on_file_selection(selected_file)

    def on_file_selection(self, selected_file):
        if selected_file:
            result = imagetotext([selected_file])
            print("TEXT EXTRACTED:")
            result = " ".join(result)
            print(result)

            # Create a new customtkinter window to display the result
            top = ctk.CTkToplevel()
            top.title("Extracted Text")
            top.configure(fg_color='#2C3E50')
            top.geometry('600x400')

            # Load the image
            image = Image.open(selected_file)
            image = image.resize((300, 300), Image.LANCZOS)
            photo = ImageTk.PhotoImage(image)

            # Create a label to display the image
            image_label = ctk.CTkLabel(top, image=photo, text="")
            image_label.image = photo  # Keep a reference to avoid garbage collection
            image_label.pack(padx=20, pady=10)

            # Set custom font
            custom_font = ctk.CTkFont(family="Helvetica", size=14, weight="bold")

            # Create a label with the extracted text
            text_label = ctk.CTkLabel(top, text=f"Extracted Text:\n\n{result}", wraplength=550,
                                 fg_color='#34495E', text_color='white', padx=20, pady=20, font = custom_font)
            text_label.pack(padx=20, pady=20)

    def launch_face_recognition(self):
        print("Launching Face Recognition...")
        subprocess.call(["python", "face_recognition_main.py"])
        print("Image has been added to the Gallery")

    def exit_program(self):
        print("Exiting program...")
        self.master.quit()
        self.master.destroy()

class MainMenuApp(ctk.CTk):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.geometry("500x290")
        self.title("Image Recognition Application")
        self.configure(fg_color="#1A1A1D")  # Window background

        self.menu_frame = MainMenu(self)
        self.menu_frame.pack(fill='both', expand=True)

if __name__ == "__main__":
    app = MainMenuApp()
    app.mainloop()
