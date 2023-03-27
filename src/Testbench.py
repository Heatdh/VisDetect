import cv2
from controller.circle import *
import numpy as np
import time

import cv2 as cv
import numpy as np


class ExponentialMovingAverage:
    def __init__(self, alpha=0.1):
        self.alpha = alpha
        self.value = None

    def update(self, value):
        if self.value is None:
            self.value = value
        else:
            self.value = self.alpha * value + (1 - self.alpha) * self.value

    def get_value(self):
        return self.value


cap = cv.VideoCapture(0)

while True:
    ret, frame = cap.read()
    width = 320
    height = int(frame.shape[0] * width / frame.shape[1])
    dim = (width, height)
    frame = cv.resize(frame, dim, interpolation=cv.INTER_AREA)
    if not ret:
        break

    all_circles = circle_detection(frame)
    goal_circles = circle_green_detection(frame)

    cv.line(frame, (0, int(height/2)), (width, int(height/2)), (0, 0, 0), 2)
    cv.line(frame, (int(width/2), 0), (int(width/2), height), (255, 0, 0), 2)

    for circle in all_circles:
        
        cv.circle(frame, (circle[0], circle[1]), circle[2], (0, 255, 0), 2)
        cv.circle(frame, (circle[0], circle[1]), 2, (0, 0, 255), 3)

    for circle in all_circles:
        dist_to_horizontal_line = abs(circle[1] - int(height/2))

        if dist_to_horizontal_line <= circle[2]:
            print("True")
        else:
            print("False")

    cv.imshow('Robot Controller', frame)

    if cv.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv.destroyAllWindows()