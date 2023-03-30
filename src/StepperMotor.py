import time
import Jetson.GPIO as GPIO
SECONDS_PER_MINUTE = 60
class StepperMotor:
    """ Controls a stepper motor using the DRV8825 driver with NEMA 17 stepper motors
        and Nvidia Jetson Nano GPIO pins.
    """
    def __init__(self, step_pin, dir_pin, 
                 rpm=1200,
                 step_per_revolution=3200):
        """ Init stepper motor controller

        Args:
            step_pin (_type_): _description_
            dir_pin (_type_): _description_
            rpm (int, optional): Round per minute. Speed of the stepper motor. Defaults to 3600.
        """
        self.step_pin = step_pin
        self.dir_pin = dir_pin
        self.rpm = rpm
        self.step_per_revolution = step_per_revolution
        self.s_per_step = 1 / (self.rpm * self.step_per_revolution / SECONDS_PER_MINUTE)
        
        # Set up the GPIO pins for the DRV8825 driver
        GPIO.setup(self.step_pin, GPIO.OUT)
        GPIO.setup(self.dir_pin, GPIO.OUT)

        # Set the direction of rotation
        GPIO.output(self.dir_pin, GPIO.HIGH)  # CW
        # GPIO.output(self.dir_pin, GPIO.LOW)  # CCW


    def move_steps(self, steps, direction):
        # Set the direction of rotation
        if direction == 'CW':
            GPIO.output(self.dir_pin, GPIO.HIGH)
        elif direction == 'CCW':
            GPIO.output(self.dir_pin, GPIO.LOW)

        # Make the specified number of steps in the specified direction
        for i in range(steps):
            GPIO.output(self.step_pin, GPIO.HIGH)
            time.sleep(self.s_per_step / 2)
            GPIO.output(self.step_pin, GPIO.LOW)
            time.sleep(self.s_per_step / 2)

    def stop(self):
        pass

