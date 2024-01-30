"""
Dance is a sequence of patterns.
"""
from const import *
import obj
import pattern
import func as f

class Intro:
    def __init__(self, frame) -> None:
        self.x_pos = WIDTH / 2
        self.y_pos = HEIGHT / 2
        self.start_frame = frame
        self.active = True
    
    def actuate(self, frame):
        match frame % self.start_frame: # Radiate from center
            case 0:
                inner_circle = pattern.pointed_circle(      target_xy= (self.x_pos , self.y_pos),\
                                                            radius= 100,\
                                                            points=30)
                outer_circle = pattern.pointed_circle(      target_xy= (self.x_pos , self.y_pos),\
                                                            radius= 120,\
                                                            points=30)
                out_bound_bullets = []
                for i in range(len(inner_circle)):
                    io_relation = f.translate_relation(inner_circle[i], outer_circle[i])
                    out_bound_bullets.append(obj.Bullet(    x_pos=inner_circle[i][0],\
                                                            y_pos=inner_circle[i][1], \
                                                            x_speed= io_relation[0],\
                                                            y_speed= io_relation[1]))
                print("success", len(out_bound_bullets))
                return out_bound_bullets
            case 100:
                self.active = False
                return None
            case _:
                return None



if __name__ == "__main__":
    pass