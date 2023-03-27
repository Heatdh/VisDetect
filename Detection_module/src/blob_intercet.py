import cv2 as cv
import numpy as np

def detect_circles_blob(frame):
    params = cv.SimpleBlobDetector_Params()

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

    circle_data = []
    for keypoint in keypoints:
        x, y = int(keypoint.pt[0]), int(keypoint.pt[1])
        radius = int(keypoint.size / 2)

        # Get the bounding box of the circle
        x1, y1 = x - radius, y - radius
        x2, y2 = x + radius, y + radius

        # Clip the bounding box to the image dimensions
        x1, y1 = max(x1, 0), max(y1, 0)
        x2, y2 = min(x2, frame.shape[1]), min(y2, frame.shape[0])

        # Get the circle's region of interest (ROI)
        roi = frame[y1:y2, x1:x2]

        # Calculate the average color within the ROI
        avg_color = np.mean(roi, axis=(0, 1))

        circle_data.append((keypoint, avg_color))

    return circle_data

cap = cv.VideoCapture(0)

while True:
    ret, frame = cap.read()
    width = 320
    height = int(frame.shape[0] * width / frame.shape[1])
    dim = (width, height)
    frame = cv.resize(frame, dim, interpolation=cv.INTER_AREA)

    if not ret:
        break

    circle_data = detect_circles_blob(frame)
    frame_with_keypoints = cv.drawKeypoints(frame, [data[0] for data in circle_data], np.array([]), (0, 0, 255),
                                            cv.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

    for keypoint, avg_color in circle_data:
        print(f"Circle at ({int(keypoint.pt[0])}, {int(keypoint.pt[1])}) has color {avg_color}")

    cv.imshow('Robot Controller', frame_with_keypoints)

    if cv.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv.destroyAllWindows()