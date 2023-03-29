import cv2
import json

# Read image
img = cv2.imread("generated_images/image_0000.png")
# Object annotation
# In format: [{"label": "male", "x": 700, "y": 94, "width": 104, "height": 109}, {"label": "male", "x": 896, "y": 94, "width": 100, "height": 104}, {"label": "male", "x": 700, "y": 294, "width": 98, "height": 102}, {"label": "male", "x": 896, "y": 294, "width": 95, "height": 99}, {"label": "male", "x": 700, "y": 494, "width": 86, "height": 90}, {"label": "male", "x": 896, "y": 494, "width": 97, "height": 101}, {"label": "female", "x": 700, "y": 694, "width": 84, "height": 90}, {"label": "male", "x": 896, "y": 694, "width": 86, "height": 90}, {"label": "male", "x": 700, "y": 894, "width": 91, "height": 95}, {"label": "female", "x": 896, "y": 894, "width": 93, "height": 99}]
objects = json.load(open("generated_images/image_0000.json"))

# Crop images size (1080, 1920) from (10800, 1920)
y = 0
for i in range(105):
    x = 0
    y = y + 100
    w = 1920
    h = 1080
    crop_img = img[y:y+h, x:x+w]
    cv2.imwrite("generated_images/image_consecutive_{}.png".format(i), crop_img)