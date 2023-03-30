from StepperMotor import StepperMotor

PI = 3.1415926
WHEEL_DIAMETER_IN_CM = 11.3 # D
ROUND_PER_MINUTE = 60 # TODO How many rounds can motor do in 1 minute
STEP_PER_REVOLUTION = 3600 # TODO Check set up How many step for 1 round rotation
ONE_ROUND_IN_DEGREE = 360 
STEP_ANGLE = ONE_ROUND_IN_DEGREE / STEP_PER_REVOLUTION
WHEELBASE_IN_CM = 30

class JetsonRobotMovement():
    """ Controls the movement of the robot using the Nvidia Jetson Nano GPIO pins.
    left_motor_pins: step_pins, dir_pins
    Args:
        RobotMovement (_type_): _description_
    """
    def __init__(self, left_motor_pins, right_motor_pins):
        self.left_motor = StepperMotor(*left_motor_pins, rpm=ROUND_PER_MINUTE, 
                                       step_per_revolution=STEP_PER_REVOLUTION)
        self.right_motor = StepperMotor(*right_motor_pins, rpm=ROUND_PER_MINUTE,
                                        step_per_revolution=STEP_PER_REVOLUTION)
        self.square_degree_distance = 300
        self.square_degree_steps = int(self.square_degree_distance / (3.1416 * 10 / 200) / 1.8)
        
    def distance_in_cm_to_steps(self, distance_in_cm):
        # Number of revolutions 
        numRevolution = distance_in_cm / (WHEEL_DIAMETER_IN_CM * PI)
        steps = numRevolution * STEP_PER_REVOLUTION
        return int(steps)

    def move_forward(self, distance_in_cm):
        # Calculate the number of steps to move forward the specified distance in centimeter
        # TODO Fix this formula
        # steps = int(distance_in_cm / (PI * WHEEL_DIAMETER_IN_CM / STEP_PER_REVOLUTION) / STEP_ANGLE)
        steps = self.distance_in_cm_to_steps(distance_in_cm)

        # Move both wheels forward by the specified number of steps
        for _ in range(steps):
            self.left_motor.move_steps(1, 'CW')
            self.right_motor.move_steps(1, 'CW')

    def move_backward(self, distance):
        # Calculate the number of steps to move forward the specified distance
        # (assuming a wheel diameter of 10cm and a step angle of 1.8 degrees)
        # steps = int(distance / (3.1416 * 10 / 200) / 1.8)
        steps = self.distance_in_cm_to_steps(distance)
        
        # Move both wheels forward by the specified number of steps
        for _ in range(steps):
            self.left_motor.move_steps(1, 'CCW')
            self.right_motor.move_steps(1, 'CCW')

    def step_left(self, angle=None):

        # workaround
        if not angle:
            for _ in range(self.square_degree_steps):
                self.left_motor.move_steps(1, 'CCW')
                self.right_motor.move_steps(1, 'CW')
            return

        # Calculate the number of steps to turn left by the specified angle
        # (assuming a wheelbase of 20cm and a step angle of 1.8 degrees)
        # wheelbase is distance 
        steps = int((PI * WHEELBASE_IN_CM / ONE_ROUND_IN_DEGREE) * angle / (PI * WHEEL_DIAMETER_IN_CM / STEP_PER_REVOLUTION) / STEP_ANGLE)

        # Move the left wheel backward and the right wheel forward by the specified number of steps
        for _ in range(steps):
            self.left_motor.move_steps(1, 'CCW')
            self.right_motor.move_steps(1, 'CW')

    def step_right(self, angle=None):

        # workaround
        if not angle:
            for _ in range(self.square_degree_steps):
                self.left_motor.move_steps(1, 'CW')
                self.right_motor.move_steps(1, 'CCW')
            return

        # Calculate the number of steps to turn right by the specified angle
        # (assuming a wheelbase of 20cm and a step angle of 1.8 degrees)
        steps = int((PI * WHEELBASE_IN_CM / ONE_ROUND_IN_DEGREE) * angle / (PI * WHEEL_DIAMETER_IN_CM / STEP_PER_REVOLUTION) / STEP_ANGLE)
        # steps = int((3.1416 * 20 / 360) * angle / (3.1416 * 10 / 200) / 1.8)

        # Move the right wheel backward and the left wheel forward by the specified number of steps
        for _ in range(steps):
            self.left_motor.move_steps(1, 'CW')
            self.right_motor.move_steps(1, 'CCW')
        
    def stop(self):
        self.left_motor.stop()
        self.right_motor.stop()