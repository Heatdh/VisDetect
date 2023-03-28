import cv2 as cv
import numpy as np


def control_system(green_circle_intersections, vertical_line_x, circle_data, green_circle_coordinates):
    stop = False
    move = False
    spray_right = False
    spray_left = False

    if len(circle_data) > 0:
        move = True
        stop = False

    if len(green_circle_coordinates) == 0:
        move = True
        stop = False

    if len(circle_data) == 0:
        stop = True
        move = False

    if len(green_circle_intersections) > 0:
        stop = True
        move = False

        for point in green_circle_intersections:
            if point[0] > vertical_line_x:
                spray_right = True
                break
            elif point[0] < vertical_line_x:
                spray_left = True
                break

    return stop, move, spray_right, spray_left



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

def label_green_circles(frame, circle_data, hue_range=(30, 90), min_saturation=80, min_value=80):
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




def intersection_with_horizontal_line(circle_data, h):
    intersection_points = []
    for keypoint, _ in circle_data:
        x, y = int(keypoint.pt[0]), int(keypoint.pt[1])
        radius = int(keypoint.size / 2)
        
        if abs(h - y) <= radius:
            dx = np.sqrt(radius ** 2 - (h - y) ** 2)
            intersection_points.append((x - dx, h))
            intersection_points.append((x + dx, h))

    return intersection_points

def intersection_green_horizontal(circle_data, h):
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
   


if __name__ == "__main__":
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
            #print(f"Circle at ({int(keypoint.pt[0])}, {int(keypoint.pt[1])}) has color {avg_color}")
            pass

        # Define the horizontal line's height (e.g., half of the frame height)
        h = frame.shape[0] // 2

        # Draw the horizontal line
        cv.line(frame_with_keypoints, (0, h), (frame.shape[1], h), (255, 0, 0), 2)
        # draw vertical line 
        cv.line(frame_with_keypoints, (frame.shape[1]//2, 0), (frame.shape[1]//2, frame.shape[0]), (255, 0, 0), 2)

        # Find the intersection points between the circles and the horizontal line
        intersection_points = intersection_with_horizontal_line(circle_data, h)

        green_circle_coordinates = label_green_circles(frame_with_keypoints, circle_data)

        # Print the coordinates of the green circles
        for coord in green_circle_coordinates:
            print(f"Green circle at {coord}")
        print(f"in each frame there are {len(green_circle_coordinates)} green circles")
        cv.putText(frame_with_keypoints, f"Green circles: {len(green_circle_coordinates)}", (10, 50), cv.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1)

        green_circle_intersections = intersection_green_horizontal(green_circle_coordinates, h)
        print(f"green circle intersections {green_circle_intersections}")

        vertical_line_x = frame.shape[1] // 2

        stop, move, spray_right, spray_left = control_system(green_circle_intersections, vertical_line_x, circle_data, green_circle_coordinates)
        print(f"Control Signals: Stop: {stop}, Move: {move}, Spray Right: {spray_right}, Spray Left: {spray_left}")
        cv.putText(frame_with_keypoints, f"Stop: {stop}, Move: {move}", (10, 90), cv.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1)
        cv.putText(frame_with_keypoints, f"Spray Right: {spray_right}, Spray Left: {spray_left}", (10, 110), cv.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1)

        

        #label_green_circles(frame_with_keypoints, circle_data)
        cv.imshow('Robot Controller', frame_with_keypoints)

        if cv.waitKey(1) & 0xFF == ord('q'):
            break
        
    cap.release()
    cv.destroyAllWindows()
