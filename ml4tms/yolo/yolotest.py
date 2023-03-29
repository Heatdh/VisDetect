import cv2
import torch
import numpy as np
from pykalman import KalmanFilter

model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)

class Tracker:
    def __init__(self):
        self.kf = KalmanFilter(4, 2)
        self.kf.transition_matrices = np.eye(4)
        self.kf.observation_matrices = np.eye(2, 4)
        self.kf.initial_state_mean = np.zeros(4)
        self.kf.initial_state_covariance = np.eye(4) * 1e-1
        self.kf.observation_covariance = np.eye(2) * 1e-1
        self.kf.transition_covariance = np.eye(4) * 1e-3

    def init(self, x, y):
        self.kf.initial_state_mean = np.array([x, y, 0, 0])
        self.state = self.kf.filter_update(self.kf.initial_state_mean, self.kf.initial_state_covariance, np.array([x, y]))

    def update(self, x, y):
        self.state = self.kf.filter_update(self.state[0], self.state[1], np.array([x, y]))
        return self.state[0][:2]

cap = cv2.VideoCapture(0)
trackers = {}
input_size = 320
confidence_threshold = 0.7

while cap.isOpened():
    ret, frame = cap.read()
    if ret:
        results = model(frame, size=input_size)
        for *xyxy, conf, cls in results.xyxy[0]:
            index = int(cls)

            # Only process car (COCO index 2) and truck (COCO index 7) detections
            if (index == 2 or index == 7) and conf >= confidence_threshold:
                x1, y1, x2, y2 = map(int, xyxy)
                cx, cy = (x1 + x2) // 2, (y1 + y2) // 2

                if index not in trackers:
                    trackers[index] = Tracker()
                    trackers[index].init(cx, cy)
                else:
                    cx, cy = trackers[index].update(cx, cy)
                    x1, y1, x2, y2 = int(cx - (x2 - x1) / 2), int(cy - (y2 - y1) / 2), int(cx + (x2 - x1) / 2), int(cy + (y2 - y1) / 2)

                label = f'{model.names[index]}: {conf:.2f}'
                cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 2)
                cv2.putText(frame, label, (x1, y1 - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

        cv2.imshow('frame', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        break

cap.release()
cv2.destroyAllWindows()
