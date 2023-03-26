import cv2
from controller.circle import *
import numpy as np
import time

if __name__ == """__main__""":
    # Initialize webcam to capture video
    cap = cv2.VideoCapture(0)
 
    while True:
        # Read frame from video stream
        ret, frame = cap.read()
        width = 320
        height = int(frame.shape[0] * width / frame.shape[1])
        dim = (width, height)
        frame = cv2.resize(frame, dim, interpolation = cv2.INTER_AREA)
        if not ret:
            break
        # line in the middle horizontal

        all_circles = circle_detection(frame)
        goal_circles = circle_green_detection(frame)

        # horizontal black line
        cv2.line(frame, (0, int(height/2)), (width, int(height/2)), (0, 0, 0), 2)
        
        for circle in all_circles:
            cv2.circle(frame, (circle[0], circle[1]), circle[2], (0, 255, 0), 2)
            cv2.circle(frame, (circle[0], circle[1]), 2, (0, 0, 255), 3)


        print("goal_circles: ", goal_circles)
        




        cv2.imshow('Robot Controller', frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()

