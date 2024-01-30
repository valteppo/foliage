"""
Patterns spawn bullets.
Functions as a rule return coordinate/coordinates.
"""
from pygame.locals import *
import math

from const import *
import obj
import func as f

def pivot(pivot_point_xy, coordinate_xy, pivot_degree) -> list:
    """
    Pivots the point in relation to pivot-point.
    Returns single coordinate.
    """
    pivot_rad = 2 * math.pi * pivot_degree / 360
    vector = f.vector_lenght(pivot_point_xy, coordinate_xy)
    x_val = math.cos(pivot_rad) * vector
    y_val = math.sin(pivot_rad) * vector
    return [x_val , y_val]


def angled_line(origin_xy, target_xy, points) -> list:
    """
    Returns a line of points oriented towards a point.
    Returns a list of coordinates
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
    Returns list of coordinates.
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