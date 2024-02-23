import video_capture
import user_interface
import vision_api
import cv2
import sys
from PySide6.QtWidgets import QApplication

caller = vision_api.APICaller()

app = QApplication(sys.argv)
#login_window = user_interface.LoginWindow()
#login_window.show()
video_window = user_interface.VideoWindow()
video_window.show()
app.exec()

'''
while True:
    user_data = login_window.retrieve_user_data()
    caller.set_user_data(user_data)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
'''