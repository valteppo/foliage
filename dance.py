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
        self.phase_1_zoom_target = (    WIDTH / 2 + random.randint(-300,300),\
                                        HEIGHT / 2 + random.randint(-300,300))
        self.phase_2_counter = 0
    
    def actuate(self, frame, target_xy):
        phase_1 = [0 + self.start_frame ,   300 + self.start_frame]
        phase_2 = [520 + self.start_frame,  1100 + self.start_frame]
        phase_3 = [1170 + self.start_frame,  2200 + self.start_frame]
        frame = self.start_frame + frame

        # Phase 1
        if frame < phase_1[1]:
            start_width = WIDTH
            end_width = 40
            zoom_step = (WIDTH-end_width) / phase_1[1] * frame
            points = 50
            inner_circle = pattern.pointed_circle(      target_xy= (self.phase_1_zoom_target[0], self.phase_1_zoom_target[1]),\
                                                        radius= start_width - zoom_step,\
                                                        points=points)
            outer_circle = pattern.pointed_circle(      target_xy= (self.phase_1_zoom_target[0], self.phase_1_zoom_target[1]),\
                                                        radius= start_width - zoom_step + 20,\
                                                        points=points)
            out_bound_bullets = []
            for i in range(len(inner_circle)):
                io_relation = f.translate_relation(inner_circle[i], outer_circle[i])
                mixer = random.randint(-5,5)
                out_bound_bullets.append(obj.Bullet(    x_pos=inner_circle[i][0] + mixer,\
                                                        y_pos=inner_circle[i][1] + mixer, \
                                                        x_speed= io_relation[0],\
                                                        y_speed= io_relation[1]))
            return out_bound_bullets
        
        # phase 2
        elif frame > phase_2[0] and frame < phase_2[1]:
            if frame % 20 == 0:
                self.phase_2_counter += 1
                start_width = WIDTH - 10
                start_height = 40
                shots = 3
                bullet_count = 7
                out_bound_bullets = []
                shot_locations = []
                for shot in range(shots):
                    shot_locations.append(((start_width + self.phase_2_counter * 100) % (WIDTH-10), start_height))
                for shot_coordinate in shot_locations:
                    for n in range(bullet_count):
                        mixer = random.randint(-10,10)
                        shot_xy_speed = f.translate_relation(shot_coordinate , (target_xy[0] + random.randint(-5,5), target_xy[1] + random.randint(-5,5)))
                        out_bound_bullets.append(obj.Bullet(    x_pos=shot_coordinate[0],\
                                                                y_pos=shot_coordinate[1],\
                                                                x_speed=shot_xy_speed[0] * 0.13,\
                                                                y_speed=shot_xy_speed[1] * 0.13))
                return out_bound_bullets
            else:
                return None
            
        # phase 3
        elif frame > phase_3[0] and frame < phase_3[1]:
            if frame % 30 == 0:
                out_bound_bullets = []
                bullets_in_circle = 7
                n_circles = random.randint(5,12)
                start_x = 10
                start_y = random.randint(10 , int(HEIGHT/2))
                end_x = WIDTH - start_x
                end_y = (HEIGHT/2) - start_y
                the_line = pattern.angled_line( origin_xy=(start_x , start_y),\
                                                target_xy=(end_x , end_y),\
                                                points=n_circles)
                for coordinate in the_line:
                    circle_radius = random.randint(12, 30)
                    bullet_spawn = pattern.pointed_circle(  target_xy=coordinate,\
                                                            radius=circle_radius,\
                                                            points=bullets_in_circle)
                    for sub_coordinate in bullet_spawn:
                        out_bound_bullets.append(obj.Bullet(    x_pos=sub_coordinate[0],\
                                                                y_pos=sub_coordinate[1],\
                                                                x_speed=0,\
                                                                y_speed=20))
                return out_bound_bullets
            else:
                return None

        # End
        else:
            return None





if __name__ == "__main__":
    pass