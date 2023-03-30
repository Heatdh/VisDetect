import time

from NozzleControl import NozzleControl

nozzleControl = NozzleControl(4, 11)
print("start spraying left")
nozzleControl.sprayLeft()
time.sleep(2)
print("start spraying right")
nozzleControl.sprayRight()
time.sleep(2)
print("start spraying both")
nozzleControl.sprayBoth()
time.sleep(2)
