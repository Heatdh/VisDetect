from abc import ABC, abstractmethod

class AbstractCamera(ABC):
    """ Abstract cemera class. It have a process_frame method with callback function.
    """
    def __init__(self) -> None:
        super().__init__()
        
    def process_frame(self, callback):
        """ Process frame and call callback function.
        """
        pass
    
    def get_frame(self):
        """ Get frame from camera.
        """
        pass
        
    