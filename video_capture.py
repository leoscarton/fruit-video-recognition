import cv2
import os

# videos_teste/IMG_0612.MOV

# FrameAnalysis class handles video file input and frame capture
class FrameAnalysis():
    def __init__(self):
        #self.video_file = None

        # List of supported video file types
        # It includes both lowercase and uppercase extensions
        self.supported_types = ['.avi', '.mp4', '.mov']
        uppercase_types = [type.upper() for type in self.supported_types]
        self.supported_types.extend(uppercase_types)
        # Initialize video capture object
        # It will be set when a video file is inserted
        self.video_capture = None
        # Default frames per second (fps) value
        # It will be updated when a video file is inserted (?)
        self.fps = 60

    # Method to check if the video capture is working
    # It reads a frame from the video capture object
    def test_video_capture(self):
        assert self.video_capture, 'No video to capture'
        ret, _ = self.video_capture.read()
        if not ret:
            return False
        else:
            return True

    # Method to insert a video file into the video capture object
    # It checks if the file type is supported
    def insert_video_file(self, file:str):
        # Check if the file type is supported
        # If not, it raises an error
        #ext = os.path.splitext(file)[1].lower()
        ext = os.path.splitext(file)[1]
        if ext not in [e for e in self.supported_types]:
            raise ValueError('File type not supported')

        #assert file[-4:] in self.supported_types, 'File type not supported'
        
        # Open the video file using OpenCV
        # It sets the video capture object to the opened file
        self.video_capture = cv2.VideoCapture(file)

        # Gets the frames per second (fps) of the video
        # If the fps is not available or less than or equal to 0, it sets to 60
        self.fps = self.video_capture.get(cv2.CAP_PROP_FPS)
        if not self.fps or self.fps <= 0:
            self.fps = 60

    # Method to get the frames per second (fps) of the video capture object
    # It asserts that the video capture object is not None
    def get_fps(self):
        #assert self.video_capture, 'No video to capture'
        if not self.video_capture:
            raise ValueError('No video to capture')
        else:
            return self.fps
    
    # Method to return the current frame from the video capture object
    # It reads a frame from the video capture object
    def return_frame(self):
        #assert self.video_capture, 'No video to capture'

        if not self.video_capture:
            raise ValueError('No video to capture')
        else:
            ret, frame = self.video_capture.read()
            if not ret:
                return None
            else:
                return frame