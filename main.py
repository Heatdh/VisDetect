import cv2 as cv
import numpy as np
from queue import Queue
from threading import Thread
from flask import Flask, render_template, Response
import time
from threading import Thread


from src.VisualDetector import VisualDetector
from src.DecisionMaker import DecisionMaker
app = Flask(__name__)

def gen(queue):
    while True:
        if not queue.empty():
            frame = queue.get()
            ret, jpeg = cv.imencode('.jpg', frame)
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n')
        else:
            time.sleep(0.01)

@app.route('/video_feed')
def video_feed():
    return Response(gen(app.queue),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

def run_web_server(queue):
    app.queue = queue
    app.run()



if __name__ == "__main__":
    cap = cv.VideoCapture(0)
    queue = Queue() 
    vision_detector = VisualDetector()
    control = DecisionMaker()
    t = Thread(target=run_web_server, args=(queue,))
    t.start()
    while True:
        ret, frame = cap.read()
        width = 320
        height = int(frame.shape[0] * width / frame.shape[1])
        dim = (width, height)
        frame = cv.resize(frame, dim, interpolation=cv.INTER_AREA)

        if not ret:
            break

        circle_data = vision_detector.detect_circles_blob(frame)
        frame_with_keypoints = cv.drawKeypoints(frame, [data[0] for data in circle_data], np.array([]), (0, 0, 255),
                                                cv.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

        h = frame.shape[0] // 2

        cv.line(frame_with_keypoints, (0, h), (frame.shape[1], h), (255, 0, 0), 2)
        cv.line(frame_with_keypoints, (frame.shape[1]//2, 0), (frame.shape[1]//2, frame.shape[0]), (255, 0, 0), 2)

        intersection_points = vision_detector.intersection_with_horizontal_line(circle_data, h)

        green_circle_coordinates = vision_detector.label_green_circles(frame_with_keypoints, circle_data)
        green_circle_intersections = vision_detector.intersection_green_horizontal(green_circle_coordinates, h)
        green_intersection = len(green_circle_intersections) > 0
        intersection_side = None

        if green_intersection:
            for point in green_circle_intersections:
                cv.circle(frame_with_keypoints, (int(point[0]), int(point[1])), 3, (255, 0, 0), -1)
                if point[0] > frame.shape[1] // 2:
                    intersection_side = 'right'
                else:
                    intersection_side = 'left'

        control.update_control(green_circle_coordinates, green_intersection, intersection_side)

        cv.putText(frame_with_keypoints, f"Stop: {control.stop}, Move: {control.move}", (10, 100), cv.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1)
        cv.putText(frame_with_keypoints, f"Spray Right: {control.spray_right}, Spray Left: {control.spray_left}", (10, 120), cv.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1)
        cv.putText(frame_with_keypoints, f"Green circles: {len(green_circle_coordinates)}", (10, 50), cv.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1)
        queue.put(frame_with_keypoints)
        cv.imshow('Robot Controller', frame_with_keypoints)

        if cv.waitKey(1) & 0xFF == ord('q'):
            break
        
    cap.release()
    cv.destroyAllWindows()
