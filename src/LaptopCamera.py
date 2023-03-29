import cv2
from src.AbstractCamera import AbstractCamera

class LaptopCamera(AbstractCamera):
    def __init__(self, camera_index=0):
        self.video = cv2.VideoCapture(camera_index)

    def __del__(self):
        self.video.release()

    def read(self):
        success, image = self.video.read()
        return success, image