from enum import Enum


class NozzleControl:
    def __init__(self, leftNozzlePin:int, rightNozzlePin:int):
        self.leftNozzlePin = leftNozzlePin
        self.rightNozzlePin = rightNozzlePin
        pass

    def sprayLeft(self):
        pass

    def sprayRight(self):
        pass