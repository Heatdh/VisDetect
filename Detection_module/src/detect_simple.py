import cv2
import numpy as np

def find_green_circles(image):
    # Convert the image to HSV color space
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Define the range of green color in HSV
    lower_green = np.array([35, 43, 46])
    upper_green = np.array([77, 255, 255])

    # Create a binary mask using the green color range
    green_mask = cv2.inRange(hsv_image, lower_green, upper_green)

    # Perform some morphological operations to reduce noise
    kernel = np.ones((5, 5), np.uint8)
    green_mask = cv2.morphologyEx(green_mask, cv2.MORPH_OPEN, kernel)
    green_mask = cv2.morphologyEx(green_mask, cv2.MORPH_CLOSE, kernel)

    # Detect circles using HoughCircles
    circles = cv2.HoughCircles(green_mask, cv2.HOUGH_GRADIENT, 1, 20,
                                param1=50, param2=30, minRadius=0, maxRadius=0)

    return circles

def main():
    # Capture video from webcam
    cap = cv2.VideoCapture(0)

    while True:
        # Read a frame from the webcam
        ret, frame = cap.read()

        if not ret:
            break

        # Find green circles in the frame
        circles = find_green_circles(frame)
        print(circles)
        if circles is not None:
            circles = np.uint16(np.around(circles))
            for i in circles[0, :]:
                # Draw the circle and its center
                cv2.circle(frame, (i[0], i[1]), i[2], (0, 255, 0), 2)
                cv2.circle(frame, (i[0], i[1]), 2, (0, 0, 255), 3)

                # Print the center coordinates
                print(f"Center: ({i[0]}, {i[1]})")

        # Show the frame
        cv2.imshow('Green Circles Detection', frame)

        # Exit the loop when 'q' key is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
