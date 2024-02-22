import cv2

class FrameAnalysis():
    def __init__(self):
        #self.video_file = None
        self.supported_types = ['.avi', '.mp4']
        self.video_capture = None

    def insert_video_file(self, file:str):
        assert file[-4:] in self.supported_types, 'File type not supported'
        self.video_capture = cv2.VideoCapture(file)
    
    def return_frame(self):
        assert self.video_capture, 'No video to capture'
        ret, frame = self.video_capture.read()
        if not ret:
            return None
        else:
            return frame
        
    