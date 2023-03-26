import cv2 
import numpy as np
import os


def detect_green_circle(img):
    h_circle = cv2.HoughCircles(img, cv2.HOUGH_GRADIENT, 1, 20, param1=50, param2=30, minRadius=0, maxRadius=0)
    if h_circle is not None:
        h_circle = np.uint16(np.around(h_circle))
        for i in h_circle[0, :]:
            cv2.circle(img, (i[0], i[1]), i[2], (0, 255, 0), 2)
            cv2.circle(img, (i[0], i[1]), 2, (0, 0, 255), 3)
    return img



def detect_green(img):
    #hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    # onlt
    lower_green = np.array([35, 43, 46])
    upper_green = np.array([77, 255, 255])
    #shape detection circles as well
   

    #mask = cv2.inRange(hsv, lower_green, upper_green)
    img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    img_hsv_blur = cv2.medianBlur(img_hsv, 15)
    mask = cv2.inRange(img_hsv_blur, lower_green, upper_green)
    mask = cv2.erode(mask, None, iterations=2) # 3x3 kernel used
    mask = cv2.dilate(mask, None, iterations=2)
    

    output = cv2.bitwise_and(img, img, mask=mask)

    return output


def get_center_mask(mask):
    moments = cv2.moments(mask)
    if moments["m00"] != 0:
        cx = int(moments["m10"] / moments["m00"])
        cy = int(moments["m01"] / moments["m00"])
    else:
        cx, cy = 0, 0
    return cx, cy



def capture_video():
    cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        mask = detect_green(frame)
        #circle = detect_green_circle(frame)
        #cx, cy = get_center_mask(mask)
        cv2.imshow("frame", frame)
        cv2.imshow("mask", mask)
        #print(cx, cy)
        #cv2.circle(mask, (cx, cy), 20, (0, 0, 255), -1)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    #capture_video()
    capture_video()

