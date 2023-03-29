import cv2
import json

# Read image
img = cv2.imread("generated_images/image_0033.png")
# Object annotation
# In format: [{"label": "male", "x": 700, "y": 94, "width": 104, "height": 109}, {"label": "male", "x": 896, "y": 94, "width": 100, "height": 104}, {"label": "male", "x": 700, "y": 294, "width": 98, "height": 102}, {"label": "male", "x": 896, "y": 294, "width": 95, "height": 99}, {"label": "male", "x": 700, "y": 494, "width": 86, "height": 90}, {"label": "male", "x": 896, "y": 494, "width": 97, "height": 101}, {"label": "female", "x": 700, "y": 694, "width": 84, "height": 90}, {"label": "male", "x": 896, "y": 694, "width": 86, "height": 90}, {"label": "male", "x": 700, "y": 894, "width": 91, "height": 95}, {"label": "female", "x": 896, "y": 894, "width": 93, "height": 99}]
objects = json.load(open("generated_images/image_0033.json"))

# Draw bounding boxes
for obj in objects:
    x = obj["x"]
    y = obj["y"]
    w = obj["width"]
    h = obj["height"]
    cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
    cv2.putText(img, obj["label"], (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)

cv2.imshow("Image", img)
cv2.waitKey(0)

