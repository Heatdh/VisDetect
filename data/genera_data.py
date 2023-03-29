import cv2
import numpy as np
import os
import random
from math import radians
import json

def resize_image(image, ratio):
    h, w = image.shape[:2]
    return cv2.resize(image, (int(w * ratio), int(h * ratio)))

def rotate_image(image, angle):
    h, w = image.shape[:2]
    center = (w // 2, h // 2)
    rotation_matrix = cv2.getRotationMatrix2D(center, angle, 1)
    return cv2.warpAffine(image, rotation_matrix, (w, h))

# Load the source images and create the output directory
male_src = cv2.imread("male.png")
female_src = cv2.imread("female.png")

# Resize source images
def resize_to_height(image, new_height):
    h, w = image.shape[:2]
    scale = new_height / h
    return cv2.resize(image, (int(w * scale), int(h * scale)))

male_src = resize_to_height(male_src, 100)
female_src = resize_to_height(female_src, 100)

output_dir = "generated_images"
os.makedirs(output_dir, exist_ok=True)

# Set the dataset parameters
num_images = 1000
image_size = (1080, 1920)
female_probability = 0.85
distance = 100

BIG_IMAGE = True
if BIG_IMAGE:
    num_images = 1
    image_size = (10800, 1920)

# Calculate x-coordinates of the center-aligned columns
col1_x = 700
col2_x = col1_x + male_src.shape[1] + distance
print("Column x", col1_x, col2_x, image_size[0], image_size[1])

female_cnt = 0
male_cnt = 0
for i in range(num_images):
    canvas = np.full((*image_size, 3), 255, dtype=np.uint8)  # Set the canvas to white
    objects = []
    print("Canva size", canvas.shape)

    # Determine the number of rows
    num_rows_choice = random.choices([5, 4, 3], [0.8, 0.1, 0.1])[0]
    if BIG_IMAGE:
        num_rows_choice = 50

    # Offset for first
    offset = random.randint(-50, 100)

    for row in range(num_rows_choice):
        print("Row", row, "of", num_rows_choice)
        # Allow the first row to overlap the border or be off the border within a range of 100 pixels
        y = row * (distance + male_src.shape[0]) + offset

        for col in range(2):  # Two columns of plants
            x = col1_x if col == 0 else col2_x

            if random.random() < female_probability:
                plant = female_src.copy()
                label = "female"
                female_cnt += 1
            else:
                plant = male_src.copy()
                label = "male"
                male_cnt += 1

            resize_ratio = random.uniform(0.9, 1.1)
            plant = resize_image(plant, resize_ratio)

            rotation_angle = random.uniform(-90, 90)
            plant = rotate_image(plant, rotation_angle)

            ph, pw = plant.shape[:2]
            y_end = min(y+ph, image_size[0])
            x_end = min(x+pw, image_size[1])
            y = max(y, 0)
            print(plant.shape, y, y_end, x, x_end)

            plant_mask = np.any(plant != 0, axis=-1)
            canvas[y:y_end, x:x_end][plant_mask[:y_end-y, :x_end-x]] = plant[:y_end-y, :x_end-x][plant_mask[:y_end-y, :x_end-x]]


            objects.append({
                "label": label,
                "x": x,
                "y": y,
                "width": pw,
                "height": ph
            })

    cv2.imwrite(os.path.join(output_dir, f"image_{i:04d}.png"), canvas)

    with open(os.path.join(output_dir, f"image_{i:04d}.json"), 'w') as f:
        json.dump(objects, f)

print("Female", female_cnt, "Male", male_cnt)
