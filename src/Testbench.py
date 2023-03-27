import cv2
from controller.circle import *
import numpy as np
import time

if __name__ == """__main__""":
    # Initialize webcam to capture video
    cap = cv2.VideoCapture(0)
 
    while True:
        # Read frame from video stream 10 fps
        ret, frame = cap.read()
        width = 320
        height = int(frame.shape[0] * width / frame.shape[1])
        dim = (width, height)
        frame = cv2.resize(frame, dim, interpolation = cv2.INTER_AREA)
        frame = cv2.GaussianBlur(frame, (5, 5), 0)
        if not ret:
            break
        # line in the middle horizontal

        all_circles = circle_detection(frame)
        goal_circles = circle_green_detection(frame)

        # horizontal black line
        cv2.line(frame, (0, int(height/2)), (width, int(height/2)), (0, 0, 0), 2)
        # vertical blue line
        cv2.line(frame, (int(width/2), 0), (int(width/2), height), (255, 0, 0), 2)
        
        for circle in all_circles:
            cv2.circle(frame, (circle[0], circle[1]), circle[2], (0, 255, 0), 2)
            cv2.circle(frame, (circle[0], circle[1]), 2, (0, 0, 255), 3)

        # check if the line intersects with a circle

       # print("goal_circles: ", goal_circles)

        for circle in all_circles:
            # Calculate distance between circle center and horizontal line
            dist_to_horizontal_line = abs(circle[1] - int(height/2))
            
            # Check if circle intersects horizontal line
            if dist_to_horizontal_line <= circle[2]:
                print("True")
            else:
                print("False")
        
        
        
        cv2.imshow('Robot Controller', frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()

