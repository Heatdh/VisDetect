import Jetson.GPIO as GPIO
import board
import time

from JetsonRobotMovement import JetsonRobotMovement

LEFT_STEP_PIN=str(board.D16)
LEFT_DIR_PIN=str(board.D20)
RIGHT_STEP_PIN=str(board.D19)
RIGHT_DIR_PIN=str(board.D26)

GPIO.setmode(GPIO.TEGRA_SOC)

robotMovement = JetsonRobotMovement([LEFT_STEP_PIN, LEFT_DIR_PIN], [RIGHT_STEP_PIN, RIGHT_DIR_PIN])
print("move forward")
robotMovement.move_forward(1000)

time.sleep(2)

print("step_left")
robotMovement.step_left(90)

time.sleep(2)

print("step_right")
robotMovement.step_right(90)

GPIO.cleanup()