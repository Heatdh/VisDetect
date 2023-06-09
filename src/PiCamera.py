import cv2
from src.AbstractCamera import AbstractCamera

class PiCamera(AbstractCamera):
    def __init__(self, camera_index=0):
        self.video = cv2.VideoCapture(self.gstreamer_pipeline(flip_method=2), cv2.CAP_GSTREAMER)
        if not self.video.isOpened():
            raise Exception("Camera is not opened")

    def __del__(self):
        self.video.release()

    def read(self):
        success, image = self.video.read()
        return success, image

        """ 
    gstreamer_pipeline returns a GStreamer pipeline for capturing from the CSI camera
    Flip the image by setting the flip_method (most common values: 0 and 2)
    display_width and display_height determine the size of each camera pane in the window on the screen
    Default 1920x1080 displayd in a 1/4 size window
    """
    def gstreamer_pipeline(
        self,
        sensor_id=0,
        capture_width=1920,
        capture_height=1080,
        display_width=960,
        display_height=540,
        framerate=30,
        flip_method=0,
    ):
        return (
            "nvarguscamerasrc sensor-id=%d !"
            "video/x-raw(memory:NVMM), width=(int)%d, height=(int)%d, framerate=(fraction)%d/1 ! "
            "nvvidconv flip-method=%d ! "
            "video/x-raw, width=(int)%d, height=(int)%d, format=(string)BGRx ! "
            "videoconvert ! "
            "video/x-raw, format=(string)BGR ! appsink"
            % (
                sensor_id,
                capture_width,
                capture_height,
                framerate,
                flip_method,
                display_width,
                display_height,
            )
        )