import cv2
import numpy as np
from robot_movement import RobotMovement, DummyRobot

# Initialize hardware components
# robot = RobotMovement.RobotMovement()

# Open camera stream
cap = cv2.VideoCapture(0)

# Define the lower and upper threshold for the black color
black_lower = np.array([0, 0, 0], dtype=np.uint8)
black_upper = np.array([50, 50, 50], dtype=np.uint8)

# Clean up
green_lower = np.array([45, 100, 20], dtype=np.uint8)
green_upper = np.array([75, 255, 255], dtype=np.uint8)

def line_following(robot):
    while True:
        # Read frame from camera
        ret, frame = cap.read()
        if not ret:
            break

        # Convert image to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Apply binary threshold to detect black color
        _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

        # Find contours in the binary image
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Process the contours to find the line
        if len(contours) > 0:
            # Find the contour with the largest area
            largest_contour = max(contours, key=cv2.contourArea)

            # Find the centroid of the contour
            M = cv2.moments(largest_contour)
            cx = int(M['m10'] / M['m00'])

            # Determine the robot's movement based on the line position
            if cx < 300:
                # Line is to the right of the robot
                robot.moveForward(80, 100) # move forward with left wheel faster
            elif cx > 340:
                # Line is to the left of the robot
                robot.moveForward(100, 80) # move forward with right wheel faster
            else:
                # Robot is on the line, move straight
                robot.moveForward(100, 100)

        # Display the processed image
        cv2.imshow('Line Follower', thresh)

        # Display the original frame
        cv2.imshow('Original Frame', frame)

        # Wait for a key press
        if cv2.waitKey(1) == 27:
            break

    # Clean up
    cap.release()
    cv2.destroyAllWindows()

def main():
    robot = DummyRobot()
    line_following(robot)

if __name__ == "__main__":
    main()
