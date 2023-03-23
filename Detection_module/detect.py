import cv2 
import numpy as np
import os




def detect_green(img):
    #hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    lower_green = np.array([35, 43, 46])
    upper_green = np.array([77, 255, 255])
    #mask = cv2.inRange(hsv, lower_green, upper_green)
    img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    img_hsv_blur = cv2.medianBlur(img_hsv, 15)
    mask = cv2.inRange(img_hsv_blur, lower_green, upper_green)
    mask = cv2.erode(mask, None, iterations=2) # 3x3 kernel used
    mask = cv2.dilate(mask, None, iterations=2)

    #y_max, x_max = mask.shape

    # Expand obstacle size by the radius of the thymio
    #dilatation_size = int(thymio_radius*1.2) # add security margin of 20% of thymio's radius
    #kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2 * dilatation_size + 1,2 * dilatation_size + 1))
    #mask_dilated = cv2.dilate(mask, kernel, iterations = 1)

    #contours = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2] # RETR_EXTERNAL to get external contour, CHAIN_APPROX_SIMPLE to get geometrical shape 

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
    capture_video()

