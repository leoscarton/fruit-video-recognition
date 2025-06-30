from PySide6.QtCore import Qt, QTimer
from PySide6.QtWidgets import QMainWindow, QPushButton, QLineEdit, QWidget, QVBoxLayout, QHBoxLayout, QStackedLayout, QMessageBox
from PySide6.QtGui import QPalette, QColor, QImage, QPixmap
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

        # Variables to store video file name and FrameAnalysis() object
        self.video_file = None
        self.frame_capture = None

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
        self.play_button.setStyleSheet("""
        background-color: #000000;
        color: #FFFFFF
        """)
        self.play_button.clicked.connect(self.play_video)

        self.pause_button = QPushButton('Pause', self)
        self.pause_button.setStyleSheet("""
        background-color: #000000;
        color: #FFFFFF
        """)
        self.pause_button.clicked.connect(self.pause_video)

        self.is_paused = False
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.play_video)

        self.restart_button = QPushButton('Restart', self)
        self.restart_button.setStyleSheet("""
        background-color: #000000;
        color: #FFFFFF
        """)
        self.restart_button.clicked.connect(self.restart_video)

        self.video_display = EmptyWindow()
        self.fruits_display = EmptyWindow()

        video_layout = QHBoxLayout()
        video_layout.addWidget(self.video_display)
        video_layout.addWidget(self.fruits_display)

        video_button_layout = QHBoxLayout()
        video_button_layout.addWidget(self.play_button)
        video_button_layout.addWidget(self.pause_button)
        video_button_layout.addWidget(self.restart_button)

        layout = QVBoxLayout()

        layout.addLayout(video_layout)
        layout.addLayout(video_button_layout)
        layout.addWidget(self.file_entry)
        layout.addWidget(self.file_button)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

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

                    self.set_button_color(video_in=True)

                    return self.frame_capture
                else:
                    raise AssertionError("Video file could not be opened or is empty.")
            except AssertionError as e:
                msg = QMessageBox(self)
                msg.setIcon(QMessageBox.Warning)
                msg.setWindowTitle("Error")
                msg.setText(str(e))
                msg.exec()

                self.set_button_color(video_in=False)

                return None
        else:
            msg = QMessageBox(self)
            msg.setIcon(QMessageBox.Warning)
            msg.setWindowTitle("Input Error")
            msg.setText("Please enter a video file name.")
            msg.exec()
            return None

    def play_video(self):
        self.is_paused = False
        self.timer.start(1000 // 60)  # Assuming 30 FPS, adjust as needed
        if not self.is_paused and self.frame_capture:
            frame = self.frame_capture.return_frame()
            if frame is None:
                self.timer.stop()
                return
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            h, w, ch = frame_rgb.shape
            bytes_per_line = ch * w
            q_img = QImage(frame_rgb.data, w, h, bytes_per_line, QImage.Format_RGB888)
            # Display q_img in your QLabel or widget

    def pause_video(self):
        pass

    def restart_video(self):
        pass

    def set_button_color(self, video_in:False):
        if video_in:
            self.play_button.setStyleSheet("""
            background-color: #FFFFFF;
            color: #262626
            """)
            self.pause_button.setStyleSheet("""
            background-color: #FFFFFF;
            color: #262626
            """)
            self.restart_button.setStyleSheet("""
            background-color: #FFFFFF;
            color: #262626
            """)
        else:
            self.play_button.setStyleSheet("""
            background-color: #000000;
            color: #FFFFFF
            """)
            self.pause_button.setStyleSheet("""
            background-color: #000000;
            color: #FFFFFF
            """)
            self.restart_button.setStyleSheet("""
            background-color: #000000;
            color: #FFFFFF
            """)

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