import cv2

# Generic name while deciding which APi to use
class APICaller():
    def __init__(self):
        self.user_data = None
    
    def set_user_data(self, data:tuple):
        assert isinstance(data[0], str) and isinstance(data[1], str), 'Data type is not string'
        assert len(data) == 2, 'Data is not email and password'
        self.user_data = data