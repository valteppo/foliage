"""
Dance is a sequence of patterns.
"""
import random

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
    
    def actuate(self, frame, target_xy):
        phase_1_end = 300 + self.start_frame
        phase_2_end = 900 + self.start_frame
        frame = self.start_frame + frame

        # Phase 1
        if frame < phase_1_end:
            start_width = WIDTH
            end_width = 50
            zoom_step = (WIDTH-end_width) / phase_1_end * frame
            points = 50
            inner_circle = pattern.pointed_circle(      target_xy= target_xy,\
                                                        radius= start_width - zoom_step,\
                                                        points=points)
            outer_circle = pattern.pointed_circle(      target_xy= target_xy,\
                                                        radius= start_width - zoom_step + 20,\
                                                        points=points)
            out_bound_bullets = []
            for i in range(len(inner_circle)):
                io_relation = f.translate_relation(inner_circle[i], outer_circle[i])
                mixer = random.randint(-10,10)
                out_bound_bullets.append(obj.Bullet(    x_pos=inner_circle[i][0] + mixer,\
                                                        y_pos=inner_circle[i][1] + mixer, \
                                                        x_speed= io_relation[0],\
                                                        y_speed= io_relation[1]))
            return out_bound_bullets
        
        # phase 2
        elif frame < phase_2_end:
            return None


        # End
        else:
            return None





if __name__ == "__main__":
    pass