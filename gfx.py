"""
Graphics related classes.
"""

from const import *

class Text:
    """
    Text to draw in the background.
    """
    def __init__(   self, x_pos = WIDTH / 2, y_pos = HEIGHT // 2,\
                    surface = None):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.surface = surface

class Img:
    """
    Images to display and move
    """
    def __init__(   self, x_pos = WIDTH / 2, y_pos = HEIGHT // 2,\
                    surface = None, speed_x = 0, speed_y = 0) -> None:
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.surface = surface
        self.speed_x = speed_x
        self.speed_y = speed_y
    
    def move(self, time_delta):
        self.x_pos += self.speed_x * time_delta
        self.y_pos += self.speed_y * time_delta

if __name__ == "__main__":
    pass