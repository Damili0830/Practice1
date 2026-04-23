import math

class Clock:
    def __init__(self, center_x, center_y):
        self.center_x = center_x
        self.center_y = center_y

    def get_second_hand(self, seconds):
        angle = math.radians(seconds * 6 - 90)
        x = self.center_x + 200 * math.cos(angle)
        y = self.center_y + 200 * math.sin(angle)
        return x, y

    def get_minute_hand(self, minutes):
        angle = math.radians(minutes * 6 - 90)
        x = self.center_x + 150 * math.cos(angle)
        y = self.center_y + 150 * math.sin(angle)
        return x, y