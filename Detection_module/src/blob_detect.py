import cv2 as cv
import numpy as np

def detect_circles_blob(frame):
    params = cv.SimpleBlobDetector_Params()

    # Change these parameters based on the properties of the circles in your images
    params.filterByArea = True
    params.minArea = 100
    params.maxArea = 10000

    params.filterByCircularity = True
    params.minCircularity = 0.7

    params.filterByConvexity = True
    params.minConvexity = 0.7

    params.filterByInertia = True
    params.minInertiaRatio = 0.5

    detector = cv.SimpleBlobDetector_create(params)
    keypoints = detector.detect(frame)

    return keypoints

cap = cv.VideoCapture(0)

while True:
    ret, frame = cap.read()
    width = 320
    height = int(frame.shape[0] * width / frame.shape[1])
    dim = (width, height)
    frame = cv.resize(frame, dim, interpolation=cv.INTER_AREA)

    if not ret:
        break

    keypoints = detect_circles_blob(frame)

    frame_with_keypoints = cv.drawKeypoints(frame, keypoints, np.array([]), (0, 0, 255),
                                            cv.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

    cv.imshow('Robot Controller', frame_with_keypoints)

    if cv.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv.destroyAllWindows()