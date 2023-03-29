import Jetson.GPIO as GPIO

from JetsonRobotMovement import JetsonRobotMovement

LEFT_STEP_PIN=36
LEFT_DIR_PIN=38
RIGHT_STEP_PIN=35
RIGHT_DIR_PIN=37

GPIO.setmode(GPIO.BOARD)

robotMovement = JetsonRobotMovement([LEFT_STEP_PIN, LEFT_DIR_PIN], [RIGHT_STEP_PIN, RIGHT_DIR_PIN])
print("move forward")
robotMovement.move_forward(1000)
print("step_left")
robotMovement.step_left(90)
print("step_right")
robotMovement.step_right(90)

GPIO.cleanup()