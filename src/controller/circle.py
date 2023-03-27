import sys
import cv2 as cv
import numpy as np

DEFAULT_WIDTH = 640

def circle_detection(frame, return_image=False, width=DEFAULT_WIDTH):
    """
    Detects circles in the given frame.
    Args:
        frame (numpy.ndarray): The frame to detect circles in.
        return_image (bool): Whether to return the processed image with the circles drawn on it.

    Returns:
        list of circles (x, y, radius) if return_image is False 
        else (list of circles, processed image)
    """
    # Resize image to so width is 320, keep aspect ratio
    height = int(frame.shape[0] * width / frame.shape[1])
    src = cv.resize(frame, (width, height))
    
    gray = cv.cvtColor(src, cv.COLOR_BGR2GRAY)
    
    # Increase kernel size make it more robust against noise
    # gray = cv.medianBlur(gray, 5)
    gray = cv.medianBlur(gray, 7)
    
    
    rows = gray.shape[0]
    circles = cv.HoughCircles(gray, cv.HOUGH_GRADIENT, 1, rows / 8,
                               param1=100, param2=30,
                               minRadius=1, maxRadius=100)


    # Return list circles
    if circles is not None:
        circles = np.uint16(np.around(circles))
        for i in circles[0, :]:
            center = (i[0], i[1])
            # circle center
            cv.circle(src, center, 1, (0, 100, 100), 3)
            # circle outline
            radius = i[2]
            cv.circle(src, center, radius, (255, 0, 255), 3)
    
    
    #cv.imshow("detected circles", src)
    #cv.waitKey(0)
    if return_image:
        return circles, src
    
    if circles is not None:
        return circles[0, :]
    return []


def circle_green_detection(src):

    # Convert the image to HSV color space
    hsv_image = cv.cvtColor(src, cv.COLOR_BGR2HSV)

    # Define the range of green color in HSV
    lower_green = np.array([21, 28, 0])
    upper_green = np.array([71, 255, 113])

    # Create a binary mask using the green color range
    green_mask = cv.inRange(hsv_image, lower_green, upper_green)

    # Perform some morphological operations to reduce noise
    kernel = np.ones((5, 5), np.uint8)
    green_mask = cv.morphologyEx(green_mask, cv.MORPH_OPEN, kernel)
    green_mask = cv.morphologyEx(green_mask, cv.MORPH_CLOSE, kernel)
    # show the green mask
    #cv.imshow("green mask", green_mask)
    rows = green_mask.shape[0]
    
    find_circle = True
    find_ellep = False

    if find_circle==True:
        circles = cv.HoughCircles(green_mask, cv.HOUGH_GRADIENT, 1, rows / 8,
                                param1=100, param2=30,
                                minRadius=1, maxRadius=100)

        # Return list circles
        if circles is not None:
            circles = np.uint16(np.around(circles))
            for i in circles[0, :]:
                center = (i[0], i[1])
                # circle center
                cv.circle(src, center, 1, (0, 100, 100), 3)
                # circle outline
                radius = i[2]
                cv.circle(src, center, radius, (255, 0, 255), 3)

        #cv.imshow("detected circles", src)
        #cv.waitKey(0)

        if circles is not None:
            return circles[0, :]
        
    if find_ellep == True: 
        # find elipse
        contours, hierarchy = cv.findContours(green_mask, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
        for cnt in contours:
            area = cv.contourArea(cnt)
            if area > 100:
                ellipse = cv.fitEllipse(cnt)
                center = (int(ellipse[0][0]), int(ellipse[0][1]))
                #cv.circle(src, center, 1, (0, 100, 100), 3)
                #cv.ellipse(src, ellipse, (0, 255, 0), 2)
        
       #cv.imshow("detected circles", src)
        #cv.waitKey(0)
        if ellipse is not None:
            return ellipse


    return []

def main(argv):
    
    default_file = 'IMG_2338_2.jpg'
    filename = argv[0] if len(argv) > 0 else default_file
    # Loads an image
    src = cv.imread(filename, cv.IMREAD_COLOR)
    # Check if image is loaded fine
    if src is None:
        print ('Error opening image!')
        print ('Usage: hough_circle.py [image_name -- default ' + default_file + '] \n')
        return -1
    
    circles = circle_green_detection(src)
    print(circles)

if __name__ == "__main__":
    main(sys.argv[1:])