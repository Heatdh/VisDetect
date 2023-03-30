import numpy as np
class DecisionMaker:
    def __init__(self):
        self.move = 0
        self.stop = 0
        self.spray_right = 0
        self.spray_left = 0
        self.distance_to_green = 10000 # Default big value in number of pixels

    def update_control(self, green_circle_coordinates, green_intersection, intersection_side):
        if len(green_circle_coordinates) == 0:
            self.move = 0
            self.stop = 1
        else:
            self.move = 1
            self.stop = 0
            closest_circle = None
            for circle in green_circle_coordinates:
                if circle[1] >= len(green_circle_coordinates)/2:
                    if closest_circle is None or abs(circle[0] - len(green_circle_coordinates[0])/2) < abs(closest_circle[0] - len(green_circle_coordinates[0])/2):
                        closest_circle = circle
            if closest_circle is not None:
                # calculate distance to closest green circle
                frame_center = np.array([len(green_circle_coordinates[0])/2, len(green_circle_coordinates)/2])
                self.distance_to_green = int(closest_circle[0] - frame_center[0])
            else:
                self.distance_to_green = 0

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