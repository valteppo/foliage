"""
Patterns spawn bullets.
"""
from pygame.locals import *
import math

from const import *
import obj

def angled_line(origin_xy, target_xy, points) -> list:
    """
    Returns a line of points oriented towards a point.
    """
    x_origin = origin_xy[0]
    y_origin = origin_xy[1]
    x_target = target_xy[0]
    y_target = target_xy[1]

    values = []
    for n in range(points):
        x_val = ((x_target - x_origin) / points) * n + x_origin
        y_val = ((y_target - y_origin) / points) * n + y_origin
        values.append([x_val , y_val])
    return values
    

def pointed_circle(target_xy, radius, points) -> list:
    """
    Transforms origin coordinates to a ring of coordinates with point number and radius r.
    Returns list.
    """
    if points < 2:
        return [target_xy]
    x_origin = target_xy[0]
    y_origin = target_xy[1]

    single_angle = (2*math.pi)/points
    values = []
    for n in range(0, points):
        y_val = (math.sin(single_angle * n) * radius) + y_origin
        x_val = (math.cos(single_angle * n) * radius) + x_origin
        values.append([x_val , y_val])
    return values


if __name__ == "__main__":
    pass