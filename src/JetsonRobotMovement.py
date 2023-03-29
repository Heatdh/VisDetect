from src.StepperMotor import StepperMotor

class JetsonRobotMovement():
    """ Controls the movement of the robot using the Nvidia Jetson Nano GPIO pins.

    Args:
        RobotMovement (_type_): _description_
    """
    def __init__(self, left_motor_pins, right_motor_pins):
        self.left_motor = StepperMotor(*left_motor_pins)
        self.right_motor = StepperMotor(*right_motor_pins)

    def move_forward(self, distance):
        # Calculate the number of steps to move forward the specified distance
        # (assuming a wheel diameter of 10cm and a step angle of 1.8 degrees)
        steps = int(distance / (3.1416 * 10 / 200) / 1.8)

        # Move both wheels forward by the specified number of steps
        self.left_motor.move_steps(steps, 'CW')
        self.right_motor.move_steps(steps, 'CW')

    def step_left(self, angle):
        # Calculate the number of steps to turn left by the specified angle
        # (assuming a wheelbase of 20cm and a step angle of 1.8 degrees)
        steps = int((3.1416 * 20 / 360) * angle / (3.1416 * 10 / 200) / 1.8)

        # Move the left wheel backward and the right wheel forward by the specified number of steps
        self.left_motor.move_steps(steps, 'CCW')
        self.right_motor.move_steps(steps, 'CW')

    def step_right(self, angle):
        # Calculate the number of steps to turn right by the specified angle
        # (assuming a wheelbase of 20cm and a step angle of 1.8 degrees)
        steps = int((3.1416 * 20 / 360) * angle / (3.1416 * 10 / 200) / 1.8)

        # Move the right wheel backward and the left wheel forward by the specified number of steps
        self.right_motor.move_steps(steps, 'CCW')
        self.left_motor.move_steps(steps, 'CW')
        
    def stop(self):
        self.left_motor.stop()
        self.right_motor.stop()