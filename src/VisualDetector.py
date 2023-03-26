from typing import List
from enum import Enum

class Color(Enum):
    BLUE = 0,
    GREEN = 1,
    BLACK = 2

class Action(Enum):
    MOVE_FORWARD = 0,
    STOP = 1

class Target:
    def __init__(self, x, y, color: Color):
        self.x = x
        self.y = y
        self.color = color


class VisualDetector:
    def __init__(self, w, h):
        self.w = w
        self.h = h
        pass

    # get an image, return a list of Target.
    def getTargets(self, img) -> List[Target]:
        pass  

    def getActions(self, targets: List[Target]) -> Action:
        pass