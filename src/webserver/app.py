from flask import Flask, Response
import cv2
import numpy as np
from controller.circle import circle_detection

app = Flask(__name__)
camera = cv2.VideoCapture(0)

# Parameters
FREQUENCY = 6
DISPLAY_WIDTH = 640

def generate_frames():
    frame_id = 0
    while True:
        # Read the video stream from the camera
        success, frame = camera.read()
        if not success:
            break
        
        print("FrameId", frame_id)
        if frame_id % FREQUENCY == 0:
            # Call the circle_detection function to process the frame
            circles, processed_frame = circle_detection(frame, return_image=True)

            # print their shapes
            # print("Shape:", processed_frame.shape, gray.shape)
            
            # Convert these frames to concat them together
            # processed_frame = cv2.cvtColor(processed_frame, cv2.COLOR_BGR2RGB)
            # gray = cv2.cvtColor(gray, cv2.COLOR_GRAY2RGB)
            # print("After:", processed_frame.shape, gray.shape)

            # Combine the original and processed frames side by side
            # combined_frame = np.concatenate((processed_frame, gray), axis=1)
            
            # Resize processed frame so width is DISPLAY_WIDTH, keep aspect ratio
            height = int(processed_frame.shape[0] * DISPLAY_WIDTH / processed_frame.shape[1])
            processed_frame = cv2.resize(processed_frame, (DISPLAY_WIDTH, height))

            # Convert the combined frame to a byte array
            ret, buffer = cv2.imencode('.jpg', processed_frame)
            frame = buffer.tobytes()
            
            # Yield the video frame as a response to the client
            yield (b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

        frame_id += 1


@app.route('/')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(debug=True)
