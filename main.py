import cv2 as cv
import numpy as np
from queue import Queue
from threading import Thread
from flask import Flask, render_template, Response
import time
from threading import Thread
import Jetson.GPIO as GPIO
import board


from src.VisualDetector import VisualDetector
from src.DecisionMaker import DecisionMaker
from src.NozzleControl import NozzleControl
from src.LaptopCamera import LaptopCamera
from src.PiCamera import PiCamera


# NOTE: adafruit_blinka already called GPIO.setmode(GPIO.TEGRA_SOC)
# the rest of the software MUST use this pin mode naming.

# define pins here
NOZZLE_LEFT_CHANNEL=4
NOZZLE_RIGHT_CHANNEL=11


app = Flask(__name__)
cap = PiCamera()
nozzleControl = NozzleControl(NOZZLE_LEFT_CHANNEL, NOZZLE_RIGHT_CHANNEL)
lastImage = None

def gen(queue):
    while True:
        frame = None
        if not queue.empty():
            frame = queue.get()
            lastImage = frame
        else:
            frame = lastImage
        ret, jpeg = cv.imencode('.jpg', frame)
        yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n')


@app.route('/video_feed')
def video_feed():
    return Response(gen(app.queue),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

def run_web_server(queue):
    app.queue = queue
    app.run()



if __name__ == "__main__":
    queue = Queue() 
    vision_detector = VisualDetector()
    decisionMaker = DecisionMaker()
    t = Thread(target=run_web_server, args=(queue,))
    t.start()

    try:
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


            ############################# DRAWING ONLY #############################
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

            decisionMaker.update_control(green_circle_coordinates, green_intersection, intersection_side)
            ############################# END DRAWING ONLY #############################


            cv.putText(frame_with_keypoints, f"Stop: {decisionMaker.stop}, Move: {decisionMaker.move}", (10, 100), cv.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1)
            cv.putText(frame_with_keypoints, f"Spray Right: {decisionMaker.spray_right}, Spray Left: {decisionMaker.spray_left}", (10, 120), cv.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1)
            cv.putText(frame_with_keypoints, f"Green circles: {len(green_circle_coordinates)}", (10, 50), cv.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1)
            # stretch the image to fit the screen on the web page
            frame_with_keypoints = cv.resize(frame_with_keypoints, (frame_with_keypoints.shape[1] * 2, frame_with_keypoints.shape[0] * 2))
            queue.put(frame_with_keypoints)

            cv.imshow('Robot Controller', frame_with_keypoints)

            ######################### ACTION SECTION ##############################
            if decisionMaker.spray_left and decisionMaker.spray_right:
                nozzleControl.sprayBoth()
            elif decisionMaker.spray_left:
                nozzleControl.sprayLeft()
            elif decisionMaker.spray_right:
                nozzleControl.sprayRight()
            ###################### END ACTION SECTION #############################

            if cv.waitKey(1) & 0xFF == ord('q'):
                break
    finally:
        cv.destroyAllWindows()
        GPIO.cleanup()
        t.join()
