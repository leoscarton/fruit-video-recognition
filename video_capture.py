import cv2

# videos_teste/IMG_0612.MOV

class FrameAnalysis():
    def __init__(self):
        #self.video_file = None
        self.supported_types = ['.avi', '.mp4', '.mov']
        uppercase_types = [type.upper() for type in self.supported_types]
        self.supported_types.extend(uppercase_types)
        self.video_capture = None
        self.fps = 60

    def test_video_capture(self):
        assert self.video_capture, 'No video to capture'
        ret, _ = self.video_capture.read()
        if not ret:
            return False
        else:
            return True

    def insert_video_file(self, file:str):
        assert file[-4:] in self.supported_types, 'File type not supported'
        self.video_capture = cv2.VideoCapture(file)
        self.fps = self.video_capture.get(cv2.CAP_PROP_FPS)
        if not self.fps or self.fps <= 0:
            self.fps = 60

    def get_fps(self):
        assert self.video_capture, 'No video to capture'
        return self.fps
    
    def return_frame(self):
        assert self.video_capture, 'No video to capture'
        ret, frame = self.video_capture.read()
        if not ret:
            return None
        else:
            return frame