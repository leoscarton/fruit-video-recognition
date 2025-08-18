from PySide6.QtCore import Qt, QTimer
from PySide6.QtWidgets import QMainWindow, QPushButton, QLineEdit, QWidget, QVBoxLayout, QHBoxLayout, QStackedLayout, QMessageBox, QLabel
from PySide6.QtGui import QPalette, QColor, QImage, QPixmap
from video_capture import FrameAnalysis
import cv2

# Class to create an empty window with a black background as a placeholder
class EmptyWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor('black'))

class FruitCountWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Fruit Count')
        self.setGeometry(0, 0, 400, 400)
        self.setStyleSheet("""
            background-color: #1e1e1e;
            color: #FFFFFF;
            border: 1px solid #FFFFFF;
            border-radius: 4px;
        """)
        self.setMinimumWidth(220)
        self.setMaximumWidth(280)

        # Label to display the text provided by fruit_cv_model.py
        # It will be updated with the detected fruit counts
        self.label = QLabel(self)
        self.label.setStyleSheet("color: #FFFFFF;")
        self.label.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        self.label.setWordWrap(True)
        self.label.setContentsMargins(8, 8, 8, 8)

        layout = QVBoxLayout(self)
        layout.addWidget(self.label)
        self.setLayout(layout)

    def set_text(self, text: str):
        # Replace the displayed text (call from fruit_cv_model.py)
        self.label.setText(text)

    def append_text(self, text: str):
        # Append text to current content
        current = self.label.text()
        if current:
            self.label.setText(current + "\n" + text)
        else:
            self.label.setText(text)

    def clear(self):
        # Clear the displayed text
        self.label.clear()

# Class to display the video frames
class VideoDisplayWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Initializing window dimensions
        self.setGeometry(0, 0, 400, 400)

        
        self.label = QLabel(self)
        self.label.setAlignment(Qt.AlignCenter)
        layout = QVBoxLayout(self)
        layout.addWidget(self.label)
        self.setLayout(layout)

    # Method to set the image in the label
    def set_image(self, q_img):
        pixmap = QPixmap.fromImage(q_img)
        scaled_pixmap = pixmap.scaled(
            self.label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation
        )
        self.label.setPixmap(scaled_pixmap)

# Main window class to handle video playback, fruit detection and user interaction
class VideoWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        # Setting the window title and dimensions
        self.setWindowTitle('Fruit Video Recognition by Leonardo Scarton - Video')
        self.setGeometry(100, 100, 900, 500)

        # Setting the background color and text color
        self.setStyleSheet("""
            background-color: #262626;
            color: #FFFFFF;
            """)

        # Variables to store video file name and FrameAnalysis() object
        self.video_file = None
        self.frame_capture = None

        # Layout to input a video file

        # Line to type video file name
        self.file_entry = QLineEdit(self)
        self.file_entry.setPlaceholderText('Example.avi')
        self.file_entry.setStyleSheet("""
        background-color: #FFFFFF;
        color: #262626
        """)

        # Button to set the video file
        # When clicked, it will set the video file and start the FrameAnalysis
        self.file_button = QPushButton('Enter video', self)
        self.file_button.clicked.connect(self.set_video_file)
        self.file_button.setStyleSheet("""
        background-color: #FFFFFF;
        color: #262626
        """)

        # Buttons to control video playback
        # Play, Pause, and Restart buttons
        # Play button will start the video playback
        self.play_button = QPushButton('Play', self)
        self.play_button.setStyleSheet("""
        background-color: #000000;
        color: #FFFFFF
        """)
        self.play_button.clicked.connect(self.play_video)

        # Pause button will pause the video playback
        # It will also stop the timer that updates the video frame
        self.pause_button = QPushButton('Pause', self)
        self.pause_button.setStyleSheet("""
        background-color: #000000;
        color: #FFFFFF
        """)
        self.pause_button.clicked.connect(self.pause_video)

        self.is_paused = True
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)

        # Restart button will restart the video playback
        # It will reset the FrameAnalysis object and start the video from the beginning
        self.restart_button = QPushButton('Restart', self)
        self.restart_button.setStyleSheet("""
        background-color: #000000;
        color: #FFFFFF
        """)
        self.restart_button.clicked.connect(self.restart_video)

        # Creating the video display and fruits display subwindows
        # Video display will show the video frames
        self.video_display = VideoDisplayWindow()
        # Fruits display will show the detected fruits (currently an empty window as placeholder)
        self.fruits_display = FruitCountWindow()

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

    # Method to set the video file and start the FrameAnalysis
    def set_video_file(self):
        if len(self.file_entry.text()) > 0:
            # Get the video file name from the entry field
            self.video_file = self.file_entry.text()
            # Create a FrameAnalysis object to handle video processing
            self.frame_capture = FrameAnalysis()
            try:
                # Attempts to insert the video file into the FrameAnalysis object
                self.frame_capture.insert_video_file(self.video_file)
                # Clear the file entry field after setting the video file
                self.file_entry.setText('')
                # Test if the video file can be opened and is not empty
                if self.frame_capture.test_video_capture():
                    msg = QMessageBox(self)
                    msg.setIcon(QMessageBox.Information)
                    msg.setWindowTitle("Success")
                    msg.setText(f"Video file '{self.video_file}' loaded successfully.")
                    msg.exec()

                    # Set the button colors to indicate a valid video file
                    self.set_button_color(video_in=True)
                else:
                    # Raise an error if the video file could not be opened or is empty
                    raise AssertionError("Video file could not be opened or is empty.")
            except AssertionError as e:
                # Show an error message if the video file could not be opened
                msg = QMessageBox(self)
                msg.setIcon(QMessageBox.Warning)
                msg.setWindowTitle("Error")
                msg.setText(str(e))
                msg.exec()

                # Reset the FrameAnalysis object and button colors
                self.set_button_color(video_in=False)
        else:
            # Show an error message if the video file name is empty
            msg = QMessageBox(self)
            msg.setIcon(QMessageBox.Warning)
            msg.setWindowTitle("Input Error")
            msg.setText("Please enter a video file name.")
            msg.exec()

    # Method to play the video
    # It starts the timer that updates the video frame at the specified FPS
    def play_video(self):
        self.is_paused = False
        if not self.timer.isActive():
            fps = self.frame_capture.get_fps()
            self.timer.start(1000 // fps)
        self.start_fruit_count()

    # Method to update the video frame
    # It retrieves the current frame from the FrameAnalysis object and updates the video display
    def update_frame(self):
        if self.is_paused or not self.frame_capture:
            return        
        frame = self.frame_capture.return_frame()
        if frame is None:
        #    self.timer.stop()
            return
        # Convert the frame from BGR to RGB format for display
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        # Create a QImage from the frame data
        # Get the dimensions of the frame
        h, w, ch = frame_rgb.shape
        # Calculate the bytes per line for the QImage
        bytes_per_line = ch * w
        # Create a QImage from the frame data
        q_img = QImage(frame_rgb.data, w, h, bytes_per_line, QImage.Format_RGB888)
        # Set the QImage in the video display
        self.video_display.set_image(q_img)

    # Method to pause the video playback
    # It stops the timer that updates the video frame
    def pause_video(self):
        self.is_paused = True
        self.timer.stop()
        pass

    # Method to restart the video playback
    # It resets the FrameAnalysis object and starts the video from the beginning
    # Currently not implemented
    def restart_video(self):
        pass

    # Method to set the button colors based on whether a video file is loaded
    # If a video file is loaded, the buttons will have a white background and dark text
    # If not, the buttons will have a black background and white text
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

    def start_fruit_count(self):
        if not self.is_paused and self.frame_capture:
            self.fruits_display.set_text(text="In this frame, there are:")
    
    def refresh_fruit_count(self):
        if not self.is_paused and self.frame_capture:
            pass

# Class to create the initial window with a start button
# When the start button is clicked, it will open the VideoWindow
class StartWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        # Setting the window title and dimensions
        self.setWindowTitle('Fruit Video Recognition by Leonardo Scarton')
        self.setGeometry(100, 100, 400, 200)
        
        # Setting the background color and text color
        self.setStyleSheet("""
            background-color: #262626;
            color: #FFFFFF;
            """)
        
        # Creating the start button
        # When clicked, it will open the VideoWindow
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

    # Method to handle the start button click
    # It creates an instance of VideoWindow and shows it
    def start_clicked(self):
        self.video_window = VideoWindow()
        self.video_window.show()
        self.hide()