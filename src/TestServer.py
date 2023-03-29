import cv2 as cv
import time
from flask import Flask, render_template, Response
from queue import Queue
import numpy as np

from camera.laptop_camera import LaptopCamera
from vision.detection import detect_circles_blob

app = Flask(__name__)
DEFAULT_RESIZED_WIDTH = 640

def gen(queue):
    while True:
        if not queue.empty():
            frame = queue.get()
            ret, jpeg = cv.imencode('.jpg', frame)
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n')
        else:
            time.sleep(0.01)

# @app.route('/')
# def index():
#     return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(gen(app.queue),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

def run_web_server(queue):
    app.queue = queue
    app.run()

def main():
    queue = Queue()
    camera = LaptopCamera()

    # Start the web server in a separate thread
    from threading import Thread
    t = Thread(target=run_web_server, args=(queue,))
    t.start()

    while True:
        ret, frame = camera.get_frame()
        if not ret:
            break
        
        # Process the frame here
        width = DEFAULT_RESIZED_WIDTH
        height = int(frame.shape[0] * width / frame.shape[1])
        dim = (width, height)
        frame = cv.resize(frame, dim, interpolation=cv.INTER_AREA)

        circle_data = detect_circles_blob(frame)
        processed_frame = cv.drawKeypoints(frame, [data[0] for data in circle_data], np.array([]), (0, 0, 255),
                                                cv.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
        queue.put(processed_frame)
        print("Frame processed")

if __name__ == '__main__':
    main()
