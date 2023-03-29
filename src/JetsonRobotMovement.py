from src.StepperMotor import StepperMotor

PI = 3.1415926
WHEEL_DIAMETER_IN_CM = 11.3 # D
ROUND_PER_MINUTE = 60 # TODO How many rounds can motor do in 1 minute
STEP_PER_REVOLUTION = 3600 # TODO Check set up How many step for 1 round rotation
ONE_ROUND_IN_DEGREE = 360 
STEP_ANGLE = ONE_ROUND_IN_DEGREE / STEP_PER_REVOLUTION
WHEELBASE_IN_CM = 30

class JetsonRobotMovement():
    """ Controls the movement of the robot using the Nvidia Jetson Nano GPIO pins.

    Args:
        RobotMovement (_type_): _description_
    """
    def __init__(self, left_motor_pins, right_motor_pins):
        self.left_motor = StepperMotor(*left_motor_pins, rpm=ROUND_PER_MINUTE, 
                                       step_per_revolution=STEP_PER_REVOLUTION)
        self.right_motor = StepperMotor(*right_motor_pins, rpm=ROUND_PER_MINUTE,
                                        step_per_revolution=STEP_PER_REVOLUTION)

    def move_forward(self, distance_in_cm):
        # Calculate the number of steps to move forward the specified distance in centimeter
        steps = int(distance_in_cm / (PI * WHEEL_DIAMETER_IN_CM / STEP_PER_REVOLUTION) / STEP_ANGLE)

        # Move both wheels forward by the specified number of steps
        for i in range(steps):
            self.left_motor.move_steps(1, 'CW')
            self.right_motor.move_steps(1, 'CW')

    def step_left(self, angle):
        # Calculate the number of steps to turn left by the specified angle
        # (assuming a wheelbase of 20cm and a step angle of 1.8 degrees)
        # wheelbase is distance 
        steps = int((PI * WHEELBASE_IN_CM / ONE_ROUND_IN_DEGREE) * angle / (PI * WHEEL_DIAMETER_IN_CM / STEP_PER_REVOLUTION) / STEP_ANGLE)

        # Move the left wheel backward and the right wheel forward by the specified number of steps
        self.left_motor.move_steps(steps, 'CCW')
        self.right_motor.move_steps(steps, 'CW')

    def step_right(self, angle):
        # Calculate the number of steps to turn right by the specified angle
        # (assuming a wheelbase of 20cm and a step angle of 1.8 degrees)
        steps = int((PI * WHEELBASE_IN_CM / ONE_ROUND_IN_DEGREE) * angle / (PI * WHEEL_DIAMETER_IN_CM / STEP_PER_REVOLUTION) / STEP_ANGLE)
        # steps = int((3.1416 * 20 / 360) * angle / (3.1416 * 10 / 200) / 1.8)

        # Move the right wheel backward and the left wheel forward by the specified number of steps
        self.right_motor.move_steps(steps, 'CCW')
        self.left_motor.move_steps(steps, 'CW')
        
    def stop(self):
        self.left_motor.stop()
        self.right_motor.stop()