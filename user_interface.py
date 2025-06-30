from PySide6.QtCore import Qt, QTimer
from PySide6.QtWidgets import QMainWindow, QPushButton, QLineEdit, QWidget, QVBoxLayout, QHBoxLayout, QStackedLayout, QMessageBox, QLabel
from PySide6.QtGui import QPalette, QColor, QImage, QPixmap
from video_capture import FrameAnalysis
import cv2

class EmptyWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor('black'))

class VideoDisplayWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setGeometry(100, 100, 400, 400)
        self.label = QLabel(self)
        self.label.setAlignment(Qt.AlignCenter)
        layout = QVBoxLayout(self)
        layout.addWidget(self.label)
        self.setLayout(layout)

    def set_image(self, q_img):
        pixmap = QPixmap.fromImage(q_img)
        scaled_pixmap = pixmap.scaled(
            self.label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation
        )
        self.label.setPixmap(scaled_pixmap)

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
        self.timer.timeout.connect(self.update_frame)

        self.restart_button = QPushButton('Restart', self)
        self.restart_button.setStyleSheet("""
        background-color: #000000;
        color: #FFFFFF
        """)
        self.restart_button.clicked.connect(self.restart_video)

        self.video_display = VideoDisplayWindow()
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
                else:
                    raise AssertionError("Video file could not be opened or is empty.")
            except AssertionError as e:
                msg = QMessageBox(self)
                msg.setIcon(QMessageBox.Warning)
                msg.setWindowTitle("Error")
                msg.setText(str(e))
                msg.exec()

                self.set_button_color(video_in=False)
        else:
            msg = QMessageBox(self)
            msg.setIcon(QMessageBox.Warning)
            msg.setWindowTitle("Input Error")
            msg.setText("Please enter a video file name.")
            msg.exec()

    def play_video(self):
        self.is_paused = False
        if not self.timer.isActive():
            fps = self.frame_capture.get_fps()
            self.timer.start(1000 // fps)

    def update_frame(self):
        if self.is_paused or not self.frame_capture:
            return        
        frame = self.frame_capture.return_frame()
        if frame is None:
        #    self.timer.stop()
            return
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        h, w, ch = frame_rgb.shape
        bytes_per_line = ch * w
        q_img = QImage(frame_rgb.data, w, h, bytes_per_line, QImage.Format_RGB888)
        self.video_display.set_image(q_img)

    def pause_video(self):
        self.is_paused = True
        self.timer.stop()
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