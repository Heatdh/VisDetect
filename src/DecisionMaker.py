import numpy as np
class DecisionMaker:
    def __init__(self):
        self.move = 0
        self.stop = 0
        self.spray_right = 0
        self.spray_left = 0

    def update_control(self, green_circle_coordinates, green_intersection, intersection_side):
        if len(green_circle_coordinates) == 0:
            self.move = 0
            self.stop = 1
        else:
            self.move = 1
            self.stop = 0
            green_center = np.mean(green_circle_coordinates, axis=0)
            frame_center = np.array([len(green_circle_coordinates[0])/2, len(green_circle_coordinates)/2])
            self.distance_to_green = int(green_center[0] - frame_center[0])

        if green_intersection:
            self.stop = 1
            if intersection_side == 'right':
                self.spray_right = 1
                self.spray_left = 0
            elif intersection_side == 'left':
                self.spray_right = 0
                self.spray_left = 1
        else:
            self.spray_right = 0
            self.spray_left = 0