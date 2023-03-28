import time
import Jetson.GPIO as GPIO
from robot_movement import RobotMovement

class StepperMotor:
    """ Controls a stepper motor using the DRV8825 driver with NEMA 17 stepper motors
        and Nvidia Jetson Nano GPIO pins.
    """
    def __init__(self, step_pin, dir_pin, enable_pin):
        self.step_pin = step_pin
        self.dir_pin = dir_pin
        self.enable_pin = enable_pin
        self.rpm = 60
        self.ms_per_step = 1 / (self.rpm * 200 / 60)
        
        # Set up the GPIO pins for the DRV8825 driver
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.step_pin, GPIO.OUT)
        GPIO.setup(self.dir_pin, GPIO.OUT)
        GPIO.setup(self.enable_pin, GPIO.OUT)

        # Set the direction of rotation
        GPIO.output(self.dir_pin, GPIO.HIGH)  # CW
        # GPIO.output(self.dir_pin, GPIO.LOW)  # CCW

        # Set the step resolution (microstepping)
        GPIO.output(22, GPIO.HIGH)  # MS1
        GPIO.output(24, GPIO.HIGH)  # MS2
        GPIO.output(26, GPIO.HIGH)  # MS3

        # Set the enable pin to high to enable the driver
        GPIO.output(self.enable_pin, GPIO.HIGH)

    def move_steps(self, steps, direction):
        # Set the direction of rotation
        if direction == 'CW':
            GPIO.output(self.dir_pin, GPIO.HIGH)
        elif direction == 'CCW':
            GPIO.output(self.dir_pin, GPIO.LOW)

        # Make the specified number of steps in the specified direction
        for i in range(steps):
            GPIO.output(self.step_pin, GPIO.HIGH)
            time.sleep(self.ms_per_step / 2)
            GPIO.output(self.step_pin, GPIO.LOW)
            time.sleep(self.ms_per_step / 2)

    def stop(self):
        # Disable the driver by setting the enable pin to low
        GPIO.output(self.enable_pin, GPIO.LOW)

