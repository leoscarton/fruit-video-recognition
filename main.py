import video_capture
import user_interface
import cv2
import sys
from PySide6.QtWidgets import QApplication

app = QApplication(sys.argv)
video_window = user_interface.VideoWindow()
video_window.show()
app.exec()
