import cv2

class Camera:
    def __init__(self):
        self.VIDEO_PATH = "C:/Programming/Vogelschreck/video1.mp4"
        self.cap = cv2.VideoCapture(self.VIDEO_PATH)
        
    def get_frame(self):
        ret, frame = self.cap.read()
        return frame
    
    def release(self):
        self.cap.release()