import time
import board
import busio

# Import the PCA9685 module. Available in the bundle and here:
#   https://github.com/adafruit/Adafruit_CircuitPython_PCA9685
from adafruit_motor import servo
from adafruit_pca9685 import PCA9685

class NozzleControl:
    def __init__(self, leftNozzleChannel:int, rightNozzleChannel:int):
        # pin 28, 27
        self.i2c = busio.I2C(board.SCL_1, board.SDA_1)
        self.pca = PCA9685(self.i2c)
        self.pca.frequency = 50
        self.leftServo = servo.Servo(self.pca.channels[leftNozzleChannel], actuation_range=180)
        self.rightServo = servo.Servo(self.pca.channels[rightNozzleChannel], actuation_range=180)
        self.leftServo.angle = 0
        self.rightServo.angle = 0
        time.sleep(0.5)
        self.DELAY_IN_SECOND=0.8
        self.sprayAngle = 40
    
    def __del__(self):
        self.pca.deinit()

    def sprayLeft(self):
        self.leftServo.angle = self.sprayAngle
        time.sleep(self.DELAY_IN_SECOND)
        self.leftServo.angle = 0
        time.sleep(self.DELAY_IN_SECOND)

    def sprayRight(self):
        self.rightServo.angle = self.sprayAngle
        time.sleep(self.DELAY_IN_SECOND)
        self.rightServo.angle = 0
        time.sleep(self.DELAY_IN_SECOND)

    def sprayBoth(self):
        self.leftServo.angle = self.sprayAngle
        self.rightServo.angle = self.sprayAngle
        time.sleep(self.DELAY_IN_SECOND)
        self.leftServo.angle = 0
        self.rightServo.angle = 0
        time.sleep(self.DELAY_IN_SECOND)