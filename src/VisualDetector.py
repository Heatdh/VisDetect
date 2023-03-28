import cv2 as cv
import numpy as np

class VisualDetector:
    def __init__(self):
        pass

    def detect_circles_blob(self,frame):
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

    def label_green_circles(self, frame, circle_data, hue_range=(30, 90), min_saturation=80, min_value=80):
        green_circle_coordinates = []

        hsv_frame = cv.cvtColor(frame, cv.COLOR_BGR2HSV)

        for keypoint, _ in circle_data:
            x, y = int(keypoint.pt[0]), int(keypoint.pt[1])
            hsv_color = hsv_frame[y, x]

            if hue_range[0] <= hsv_color[0] <= hue_range[1] and hsv_color[1] >= min_saturation and hsv_color[2] >= min_value:
                radius = int(keypoint.size / 2)
                cv.circle(frame, (x, y), radius, (0, 255, 0), 2)
                green_circle_coordinates.append((x, y, radius))
                
        return green_circle_coordinates




    def intersection_with_horizontal_line(self,circle_data, h):
        intersection_points = []
        for keypoint, _ in circle_data:
            x, y = int(keypoint.pt[0]), int(keypoint.pt[1])
            radius = int(keypoint.size / 2)
            
            if abs(h - y) <= radius:
                dx = np.sqrt(radius ** 2 - (h - y) ** 2)
                intersection_points.append((x - dx, h))
                intersection_points.append((x + dx, h))

        return intersection_points

    def intersection_green_horizontal(self,circle_data, h):
        print(circle_data)
        intersection_points = []
        for keypoint in circle_data:
            x, y = int(keypoint[0]), int(keypoint[1])
            radius = keypoint[2]
            
            if abs(h - y) <= radius:
                dx = np.sqrt(radius ** 2 - (h - y) ** 2)
                intersection_points.append((x - dx, h))
                intersection_points.append((x + dx, h))

        return intersection_points
   


    

