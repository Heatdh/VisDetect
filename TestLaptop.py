import cv2 as cv
import numpy as np
from queue import Queue
from threading import Thread
from flask import Flask, render_template, Response
import time
from threading import Thread
#import Jetson.GPIO as GPIO
#import board


from src.VisualDetector import VisualDetector
from src.DecisionMaker import DecisionMaker
#from src.NozzleControl import NozzleControl
from src.LaptopCamera import LaptopCamera
from src.PiCamera import PiCamera
#from src.JetsonRobotMovement import JetsonRobotMovement


# NOTE: adafruit_blinka already called GPIO.setmode(GPIO.TEGRA_SOC)
# the rest of the software MUST use this pin mode naming.

# define pins here
NOZZLE_LEFT_CHANNEL=4
NOZZLE_RIGHT_CHANNEL=15


app = Flask(__name__)
#cap = PiCamera()
cap = LaptopCamera()
#nozzleControl = NozzleControl(NOZZLE_LEFT_CHANNEL, NOZZLE_RIGHT_CHANNEL)

# Set up board
#GPIO.setmode(GPIO.BOARD)
# TODO define pins here
LEFT_MOTOR_PINS = [11, 13, 15, 16]
RIGHT_MOTOR_PINS = [18, 22, 32, 36]

# TODO Define Raspberry Pi camera parameters
CAMERA_HEIGHT_CM = 55.0
FOCAL_LENGTH_X_CM = 50.0
FOCAL_LENGTH_Y_CM = 50.0
PRINCIPLA_POINT_X = 0
PRINCIPLA_POINT_Y = 0
ONE_FRAME_IN_REAL_WORLD_SPACE_CM = 21.0
MOVE_STEP_CM = 0.5

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

def convert_pixels_to_cm_y_axis(pixels, frame_height):
    """ Convert distance in pixels in camera space to distance in centimeter in real world space.
    From manual measurement, 1 frame height from camera at 55 cm is 21cm in real world space.
    Args:
        pixels (int): number of pixels in camera space
    """
    # TODO Check if this is correct
    return  pixels / frame_height * ONE_FRAME_IN_REAL_WORLD_SPACE_CM
    

if __name__ == "__main__":
    queue = Queue() 
    vision_detector = VisualDetector()
    decisionMaker = DecisionMaker()
    #robot_movement = JetsonRobotMovement()
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
                #nozzleControl.sprayBoth()
                pass
            elif decisionMaker.spray_left:
                #nozzleControl.sprayLeft()
                pass
            elif decisionMaker.spray_right:
                #nozzleControl.sprayRight()
                pass
            ###################### END ACTION SECTION #############################

            if cv.waitKey(1) & 0xFF == ord('q'):
                break
            
            ########################## ROBOT MOVEMENT #############################
            # Convert movement need in pixels to movement need in centimeters
            # Check distanct to closest green circle
            # Each step we move forward 0.5 cm
            frame_height = frame.shape[0]
            distance_to_green_circle_pixels = decisionMaker.distance_to_green
            distance_to_green_circle_cm = convert_pixels_to_cm_y_axis(distance_to_green_circle_pixels, frame_height)
            
            # Move forward if distance to green circle is greater than 0.5 cm
            if distance_to_green_circle_cm > MOVE_STEP_CM:
                print(f"Moving forward {MOVE_STEP_CM} cm")
                #robot_movement.move_forward(MOVE_STEP_CM)
            
    finally:
        cv.destroyAllWindows()
        #GPIO.cleanup()
        t.join()
