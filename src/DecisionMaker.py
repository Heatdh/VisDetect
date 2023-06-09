import numpy as np
class DecisionMaker:
    def __init__(self):
        self.move = 0
        self.stop = 0
        self.spray_right = 0
        self.spray_left = 0
        self.distance_to_green = 10000 # Default big value in number of pixels

    def update_control(self, circle_data, green_circle_coordinates, green_intersection, intersection_side):
        if len(circle_data) == 0:
            self.move = 0
            self.stop = 1
        else:
            self.move = 1
            self.stop = 0
            closest_circle = None
            for circle in green_circle_coordinates:
                if circle[1] < len(green_circle_coordinates)/2:
                    continue  # skip circles below the line
                if closest_circle is None or circle[1] < closest_circle[1]:
                    closest_circle = circle
            if closest_circle is not None:
                # calculate distance to closest green circle
                frame_center = np.array([len(green_circle_coordinates[0])/2, len(green_circle_coordinates)/2])
                self.distance_to_green = int(closest_circle[0] - frame_center[0])
            else:
                self.distance_to_green = 99999999

        if green_intersection:
            self.stop = 1
            self.move = 0
            if intersection_side == 'right':
                self.spray_right = 1
                self.spray_left = 0
            elif intersection_side == 'left':
                self.spray_right = 0
                self.spray_left = 1
        else:
            self.spray_right = 0
            self.spray_left = 0