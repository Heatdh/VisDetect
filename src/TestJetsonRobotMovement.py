import Jetson.GPIO as GPIO
import board
import time

from JetsonRobotMovement import JetsonRobotMovement

LEFT_STEP_PIN=str(board.D16)
LEFT_DIR_PIN=str(board.D20)
RIGHT_STEP_PIN=str(board.D19)
RIGHT_DIR_PIN=str(board.D26)
ENABLE_PIN=str(board.D4)

GPIO.setmode(GPIO.TEGRA_SOC)

robotMovement = JetsonRobotMovement(ENABLE_PIN, [LEFT_STEP_PIN, LEFT_DIR_PIN], [RIGHT_STEP_PIN, RIGHT_DIR_PIN])

DISTANCE = 10
ANGLE = 0

print("move forward")
robotMovement.move_forward(DISTANCE)

time.sleep(1)

print("move backward")
robotMovement.move_backward(DISTANCE)

time.sleep(1)

print("step_left")
robotMovement.step_left(ANGLE)

time.sleep(1)

print("step_right")
robotMovement.step_right(ANGLE)

GPIO.cleanup()