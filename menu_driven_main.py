import os
os.environ['KIVY_NO_CONSOLELOG'] = '1'
import kivy
import sys
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
import subprocess
import ast
from kivy.core.window import Window
from kivy.uix.scrollview import ScrollView
from kivy.clock import Clock
from kivy.base import EventLoop
from kivy.uix.popup import Popup  # Add Popup for file chooser
from textToImage import imagetotext
from kivy.uix.filechooser import FileChooserListView
import tkinter as tk
from tkinter import filedialog,Toplevel,Label
import tkinter.font as tkFont
    
class MainMenu(GridLayout):
    def __init__(self, **kwargs):
        super(MainMenu, self).__init__(**kwargs)
        self.cols = 1
        

        # Object Recognition Button
        self.obj_recog_btn = Button(text="Object Recognition", size_hint_y=None, height=70,
                                    background_normal='', background_color=(0.2, 0.6, 0.8, 1),
                                    color=(0, 0, 0, 1), border=(20, 20, 20, 20))
        self.obj_recog_btn.bind(on_press=self.launch_object_recognition)
        self.add_widget(self.obj_recog_btn)

        # Text Recognition Button
        self.text_recog_btn = Button(text="Text Recognition", size_hint_y=None, height=70,
                                     background_normal='', background_color=(0.2, 0.6, 0.8, 1),
                                     color=(0, 0, 0, 1), border=(20, 20, 20, 20))
        self.text_recog_btn.bind(on_press=self.launch_text_recognition)
        self.add_widget(self.text_recog_btn)

        # Face Recognition Button
        self.face_recog_btn = Button(text="Face Recognition", size_hint_y=None, height=70,
                                     background_normal='', background_color=(0.2, 0.6, 0.8, 1),
                                     color=(0, 0, 0, 1), border=(20, 20, 20, 20))
        self.face_recog_btn.bind(on_press=self.launch_face_recognition)
        self.add_widget(self.face_recog_btn)

        # Exit Button
        self.exit_btn = Button(text="Exit", size_hint_y=None, height=70,
                               background_normal='', background_color=(1, 0.3, 0.3, 1),
                               color=(0, 0, 0, 1), border=(20, 20, 20, 20))
        self.exit_btn.bind(on_press=self.exit_program)
        self.add_widget(self.exit_btn)

    def launch_object_recognition(self, instance):
        print("Launching Object Recognition...")
        subprocess.call(["python", "main.py"])
    def select_file(self):
        """Opens a file dialog to let the user select an image."""
        root = tk.Tk()
        root.withdraw()
        return filedialog.askopenfilename(
            title="Select an image file",
            filetypes=[("Image Files", "*.jpg *.jpeg *.png")]
        )
    def launch_text_recognition(self, instance):
        print("Launching Text Recognition...")
        selected_file = self.select_file()  # Get the selected file
        if selected_file:  # Check if a file was selected
            self.on_file_selection([selected_file])  # Pass the selected file as a list to match the expected argument format

    def on_file_selection(self, selected_file):
        if selected_file:
            result = imagetotext(selected_file)  # Pass selected image
            print("TEXT EXTRACTED:")
            result = " ".join(result)
            print(result)

            # Create a new Tkinter window to display the result
            root = tk.Tk()
            root.withdraw()  # Hide the main window

            # Create a new top-level window for displaying the result
            top = Toplevel()
            top.title("Extracted Text")
            top.configure(bg='#2C3E50')  # Set a dark background color for the window
            top.geometry('600x400')  # Set the window size

            # Set custom font
            custom_font = tkFont.Font(family="Helvetica", size=14, weight="bold")

            # Create a label with the extracted text
            label = Label(top, text=f"Extracted Text:\n\n{result}", wraplength=550,
                          bg='#34495E', fg='white', padx=20, pady=20)  # Colors and padding
            label.configure(font=custom_font)  # Apply the custom font
            label.pack(padx=20, pady=20)

            top.mainloop()  # Start the Tkinter event loop  

    def launch_face_recognition(self, instance):
        print("Launching Face Recognition...")
        subprocess.call(["python", "face_recognition_main.py"])
        print("Image has been added to the Gallery")

    def exit_program(self, instance):
        print("Exiting program...")
        App.get_running_app().stop()  # This stops the Kivy application
        Window.close()
        Clock.schedule_once(lambda dt: sys.exit(0), 0)  # Force exit after stopping the app


class MainMenuApp(App):
    def build(self):
        Window.size = (500, 220)
        Window.clearcolor = (1, 1, 1, 1)
        return MainMenu()

if __name__ == "__main__":
    MainMenuApp().run()




