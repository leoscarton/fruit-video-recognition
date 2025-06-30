from PySide6.QtCore import Qt
from PySide6.QtWidgets import QMainWindow, QPushButton, QLineEdit, QWidget, QVBoxLayout, QHBoxLayout, QStackedLayout, QMessageBox
from PySide6.QtGui import QPalette, QColor
from video_capture import FrameAnalysis
import cv2

'''
class LoginWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Fruit Video Recognition - Login')
        self.setGeometry(100, 100, 400, 200)
        
        self.setStyleSheet("""
            background-color: #262626;
            color: #FFFFFF;
            """)

        self.user_data = None

        # Login layout

        self.email_entry = QLineEdit(self)
        self.email_entry.setPlaceholderText('name@example.com')
        self.email_entry.setStyleSheet("""
        background-color: #FFFFFF;
        color: #262626
        """)

        self.password_entry = QLineEdit(self)
        self.password_entry.setPlaceholderText('Password')
        self.password_entry.setEchoMode(QLineEdit.Password)
        self.password_entry.setStyleSheet("""
        background-color: #FFFFFF;
        color: #262626
        """)


        self.login_button = QPushButton('Login', self)
        self.login_button.setStyleSheet("""
        background-color: #FFFFFF;
        color: #262626
        """)
        self.login_button.clicked.connect(self.store_login)

        self.login_layout = QVBoxLayout()
        self.login_layout.addWidget(self.email_entry)
        self.login_layout.addWidget(self.password_entry)
        self.login_layout.addWidget(self.login_button)

        self.central_widget = QWidget()
        self.central_widget.setLayout(self.login_layout)
        self.setCentralWidget(self.central_widget)

    def store_login(self):
        email = self.email_entry.text()
        password = self.password_entry.text()
        assert (len(email) > 0) and (len(password) > 0), 'Empty email or password'
        self.user_data = (email, password)

    def retrieve_user_data(self):
        if not self.user_data:
            return None
        if not self.user_data[0] or not self.user_data[1]:
            return None
        return self.user_data
'''

class EmptyWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor('black'))

class VideoWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Fruit Video Recognition by Leonardo Scarton - Video')
        self.setGeometry(100, 100, 800, 400)

        self.setStyleSheet("""
            background-color: #262626;
            color: #FFFFFF;
            """)

        # Layout to input a video file

        self.file_entry = QLineEdit(self)
        self.file_entry.setPlaceholderText('Example.avi')
        self.file_entry.setStyleSheet("""
        background-color: #FFFFFF;
        color: #262626
        """)

        self.file_button = QPushButton('Enter video', self)
        self.file_button.clicked.connect(self.set_video_file)
        self.file_button.setStyleSheet("""
        background-color: #FFFFFF;
        color: #262626
        """)

        self.play_button = QPushButton('Play', self)
        self.play_button.clicked.connect(self.play_video)

        self.pause_button = QPushButton('Pause', self)
        self.pause_button.clicked.connect(self.pause_video)

        self.restart_button = QPushButton('Restart', self)
        self.restart_button.clicked.connect(self.restart_video)

        self.video_display = EmptyWindow()
        self.fruits_display = EmptyWindow()

        video_layout = QHBoxLayout()
        video_layout.addWidget(self.video_display)
        video_layout.addWidget(self.fruits_display)

        layout = QVBoxLayout()

        layout.addLayout(video_layout)
        layout.addWidget(self.file_entry)
        layout.addWidget(self.file_button)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

        # Variable to store video file name
        self.video_file = None

    def set_video_file(self):
        if len(self.file_entry.text()) > 0:
            self.video_file = self.file_entry.text()
            self.frame_capture = FrameAnalysis()
            try:
                self.frame_capture.insert_video_file(self.video_file)
                self.file_entry.setText('')
                if self.frame_capture.test_video_capture():
                    msg = QMessageBox(self)
                    msg.setIcon(QMessageBox.Information)
                    msg.setWindowTitle("Success")
                    msg.setText(f"Video file '{self.video_file}' loaded successfully.")
                    msg.exec()
                else:
                    raise AssertionError("Video file could not be opened or is empty.")
            except AssertionError as e:
                msg = QMessageBox(self)
                msg.setIcon(QMessageBox.Warning)
                msg.setWindowTitle("Error")
                msg.setText(str(e))
                msg.exec()
        else:
            msg = QMessageBox(self)
            msg.setIcon(QMessageBox.Warning)
            msg.setWindowTitle("Input Error")
            msg.setText("Please enter a video file name.")
            msg.exec()

    def play_video(self):
        pass

    def pause_video(self):
        pass

    def restart_video(self):
        pass

class StartWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Fruit Video Recognition by Leonardo Scarton')
        self.setGeometry(100, 100, 400, 200)
        
        self.setStyleSheet("""
            background-color: #262626;
            color: #FFFFFF;
            """)
        
        self.start_button = QPushButton('Start', self)
        self.start_button.setStyleSheet("""
        background-color: #FFFFFF;
        color: #262626
        """)
        self.start_button.clicked.connect(self.start_clicked)

        self.start_layout = QVBoxLayout()
        self.start_layout.addWidget(self.start_button)

        self.central_widget = QWidget()
        self.central_widget.setLayout(self.start_layout)
        self.setCentralWidget(self.central_widget)

    def start_clicked(self):
        self.video_window = VideoWindow()
        self.video_window.show()
        self.hide()