import time
from abc import ABC, abstractmethod

class RobotMovement(ABC):
    @abstractmethod
    def moveForward(self, leftSpeed, rightSpeed):
        pass

    @abstractmethod
    def moveBackward(self, leftSpeed, rightSpeed):
        pass

    @abstractmethod
    def turnLeft(self, speed):
        pass

    @abstractmethod
    def turnRight(self, speed):
        pass

    @abstractmethod
    def stop(self):
        pass
    
    @abstractmethod
    def setLeftSpeed(self, speed):
        pass
    
    @abstractmethod
    def setRightSpeed(self, speed):
        pass
    
    @abstractmethod
    def setSpeed(self, speed):
        pass

class DummyRobot(RobotMovement):
    def moveForward(self, leftSpeed, rightSpeed):
        print("Move forward")

    def moveBackward(self, leftSpeed, rightSpeed):
        print("Move backward")

    def turnLeft(self, speed):
        print("Turn left")

    def turnRight(self, speed):
        print("Turn right")

    def stop(self):
        print("Stop")

    def setLeftSpeed(self, speed):
        print("Set left speed")

    def setRightSpeed(self, speed):
        print("Set right speed")

    def setSpeed(self, speed):
        print("Set speed")




