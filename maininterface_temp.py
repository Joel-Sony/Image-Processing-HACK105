import sys
import subprocess
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton, QLabel

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Image Recognition Options")
        self.setGeometry(100, 100, 400, 200)

        # Central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # Label
        label = QLabel("Choose Image Recognition Type", self)
        label.setStyleSheet("font-size: 16px;")
        layout.addWidget(label)

        # Face Recognition button
        face_btn = QPushButton("Face Recognition", self)
        face_btn.setStyleSheet("font-size: 14px; padding: 10px;")
        face_btn.clicked.connect(self.run_face_recognition)
        layout.addWidget(face_btn)

        # Object Recognition button
        object_btn = QPushButton("Object Recognition", self)
        object_btn.setStyleSheet("font-size: 14px; padding: 10px;")
        object_btn.clicked.connect(self.run_object_recognition)
        layout.addWidget(object_btn)

        # Text Recognition button
        text_btn = QPushButton("Text Recognition", self)
        text_btn.setStyleSheet("font-size: 14px; padding: 10px;")
        text_btn.clicked.connect(self.run_text_recognition)
        layout.addWidget(text_btn)

    def run_face_recognition(self):
        # Launch the face_recognition.py file using the same interpreter.
        subprocess.call([sys.executable, "imgsomething.py"])

    def run_object_recognition(self):
        # Launch the object_recognition.py file (implement this file similarly)
        subprocess.call([sys.executable, "object_recognition.py"])

    def run_text_recognition(self):
        # Launch the text_recognition.py file (implement this file similarly)
        subprocess.call([sys.executable, "text_recognition.py"])

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
