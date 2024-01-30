"""
Game classes/objects
"""

import random
from pygame.locals import *
from const import *
import func as f

class Player:
    def __init__(   self, \
                    x_pos = WIDTH/2, \
                    y_pos = HEIGHT/2) -> None:
        
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.speed = 0.5
        self.hit_distance = 3
        self.graze_distance = 6
        self.size = self.graze_distance
        self.score = 0
        self.surface = None
        self.alive = True

    def command(self, time_delta, command):
        modifier = 1
        if command[K_LSHIFT]:
            modifier = 0.4
        if command[K_UP] and self.y_pos > 0:
            self.y_pos -= self.speed * modifier * time_delta
        if command[K_DOWN] and self.y_pos < HEIGHT:
            self.y_pos += self.speed * modifier * time_delta
        if command[K_LEFT] and self.x_pos > 0:
            self.x_pos -= self.speed * modifier * time_delta
        if command[K_RIGHT] and self.x_pos < WIDTH:
            self.x_pos += self.speed * modifier * time_delta
        if command[K_z]:
            return True
        return False

class Bullet:
    def __init__(   self, \
                    x_pos = WIDTH/2, \
                    y_pos = HEIGHT/2, \
                    y_speed = 0, \
                    x_speed = 0, \
                    size = 16, \
                    colour = RED, \
                    active = True, \
                    bullet_surface = None) -> None:
        
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.x_speed = x_speed
        self.y_speed = y_speed
        self.size = size
        self.colour = colour
        self.active = active
        self.surface = bullet_surface
        self.faction = -1
    
    def move(self, time_delta, target_x = 1, target_y = 1, frame = 0):
        # Move unaffected if bullet hostile
        if self.faction == -1:
            self.x_pos += self.x_speed * time_delta * 0.01
            self.y_pos += self.y_speed * time_delta * 0.01
        
        # If bullet friendy, move towards gatherpoint
        elif self.faction == 0:
            random_int = random.randint (-15, 15)
            speed_translation = f.translate_relation((self.x_pos, self.y_pos),(target_x + random_int, target_y+30 + random_int))
            self.x_pos += speed_translation[0] * time_delta * 0.005
            self.y_pos += speed_translation[1] * time_delta * 0.005
        
        # Act of launching bullet
        elif self.faction == 1:
            speed_translation = f.translate_relation((self.x_pos, self.y_pos),(target_x, target_y))
            self.x_speed = speed_translation[0] * 0.01 + random.randint(-20, 20)*0.01
            self.y_speed = speed_translation[1] * 0.01 + random.randint(-20, 20)*0.01
            self.faction = 2

        # If bullet is launhed and enroute
        elif self.faction == 2:
            self.x_pos += self.x_speed * time_delta
            self.y_pos += self.y_speed * time_delta



if __name__ == "__main__":
    pass