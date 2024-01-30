"""
Various general functions.
"""

import random
import math
from const import *

def colour_nudge(rgb, nudge_val=10):
    """
    Adds slight variation to color values.
    """
    r, g, b = rgb
    r = r + random.randint(-nudge_val, nudge_val)
    g = g + random.randint(-nudge_val, nudge_val)
    b = b + random.randint(-nudge_val, nudge_val)

    if r < 0:
        r = 0
    if g < 0:
        g = 0
    if b < 0:
        b = 0
    
    if r > 255:
        r = 255
    if g > 255:
        g = 255
    if b > 255:
        b = 255
    return (r, g, b)

def assign_grid(x_pos, y_pos) -> tuple:
    return (math.floor(x_pos / GRID_SIZE), math.floor(y_pos / GRID_SIZE))

def vector_lenght(source, target) -> float:
    return math.sqrt((target[0] - source[0])**2 + (target[1] - source[1])**2)

def translate_relation(relation_of, relation_to) -> tuple:
    return (relation_to[0] - relation_of[0] , relation_to[1] - relation_of[1])


if __name__ == "__main__":
    pass