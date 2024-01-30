import pygame
import os
import sys
from pygame.locals import *
import math
import random
import time

# Constants
WIDTH = 960
HEIGHT = 600
GRID_SIZE = 50

BLACK = (0,0,0)
WHITE = (255,255,255)
TEAL = (0,128,128)
PINK = (255,20,147)
RED = (255,0,0)
SILVER = (135,135,135)
GOLD = (255,215,0)
ROYAL_BLUE = (65,105,225)
DIFFICULTY_COLOUR = {True:WHITE,\
                     False:SILVER}


# Engine initialization.
pygame.init()
pygame.font.init()
dispSurf = pygame.display.set_mode(size=(WIDTH, HEIGHT))
pygame.display.set_caption("Bullet hell")


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


class Player:
    def __init__(self, x_pos = WIDTH/2, y_pos = HEIGHT - 20, speed = 0.18):
        self.x_pos = float(x_pos)
        self.y_pos = float(y_pos)
        self.speed = speed
        self.alive = True
        self.score = 0
        self.graze_range = 12
        self.hit_range = 4
        self.jubilate_font = pygame.font.SysFont("Calibri", 13)
        self.jubilate_surface = self.jubilate_font.render("+1", False, colour_nudge(RED, 50)).set_alpha(200)
        self.score_cooldown = 0

    def move(self, move_command):
        modifier = 1
        if move_command[K_LSHIFT]:
            modifier = 0.4
        if move_command[K_UP] and self.y_pos > 0:
            self.y_pos -= self.speed * modifier
        if move_command[K_DOWN] and self.y_pos < HEIGHT:
            self.y_pos += self.speed * modifier
        if move_command[K_LEFT] and self.x_pos > 0:
            self.x_pos -= self.speed * modifier
        if move_command[K_RIGHT] and self.x_pos < WIDTH:
            self.x_pos += self.speed * modifier
    
    def get_grid(self):
        return (math.floor(self.x_pos/GRID_SIZE), math.floor(self.y_pos/GRID_SIZE))
    
    def draw(self):
        # Graze radius
        pygame.draw.circle( surface =   dispSurf, \
                            color =     PINK, 
                            center =    (self.x_pos, self.y_pos), \
                            radius=     self.graze_range, \
                            width=      0)
        # Player hitbox
        pygame.draw.circle( surface =   dispSurf, \
                            color =     WHITE, 
                            center =    (self.x_pos, self.y_pos), \
                            radius=     self.hit_range, \
                            width=      0)
    
    def jubilate(self):
        self.jubilate_surface = self.jubilate_font.render("GRAZE", False, colour_nudge(RED, 50))
        dispSurf.blit(self.jubilate_surface, ((self.x_pos + random.randint(-20, 20)), (self.y_pos + random.randint(-20, 20))))


class Bullet:
    def __init__(self, x_pos, y_pos, x_speed, y_speed, size, colour=ROYAL_BLUE, activation_delay=0):
        self.x_pos = float(x_pos)
        self.y_pos = float(y_pos)
        self.x_speed = float(x_speed)
        self.y_speed = float(y_speed)
        self.size = size
        self.visible_circle = pygame.Surface((size, size))
        self.visible_circle_area = self.visible_circle.get_rect()
        self.visible_circle_area.left = math.floor(x_pos)
        self.visible_circle_area.top = math.floor(x_pos)
        self.colour = colour_nudge(colour, 30)
        self.activation_delay = activation_delay
        if activation_delay == 0:
            self.active = True
        else:
            self.active = False
        self.delete = False
        self.creation_time = int(time.time_ns() / 1_000_000)

    def post_time(self, time_outside_ms):
        if time_outside_ms > self.creation_time + self.activation_delay:
            self.active = True

    def get_grid(self):
        return [math.floor(self.x_pos / GRID_SIZE), math.floor(self.y_pos / GRID_SIZE)]

    def move(self):
        speed_modifier = 1
        if not self.active:
            return
        if difficulty["easy"] == True:
            speed_modifier = 0.7
        self.x_pos = self.x_pos + self.x_speed * speed_modifier * 0.7
        self.y_pos = self.y_pos + self.y_speed * speed_modifier * 0.7
    
    def draw(self):
        if not self.active:
            return
        
        # Ring
        pygame.draw.circle( surface =   dispSurf, \
                            color =     self.colour, 
                            center =    (self.x_pos, self.y_pos), \
                            radius=     self.size, \
                            width=      0)
        # Inner
        pygame.draw.circle( surface =   dispSurf, \
                            color =     WHITE, 
                            center =    (self.x_pos, self.y_pos), \
                            radius=     self.size-4, \
                            width=      0)


class MovingBGimage:
    def __init__(self, image_file_name, speed = 0.01, pos = [0,0]) -> None:
        self.image = pygame.image.load(image_file_name)
        self.image_height = self.image.get_height()
        self.speed = speed
        self.x_pos = pos[0]
        self.y_pos = pos[1] - self.image_height + HEIGHT

    def actuate(self):
        self.y_pos += self.speed
        dispSurf.blit(self.image, (self.x_pos, self.y_pos))


class PatternSpraySpam:
    def __init__(self, x_pos = WIDTH/2, y_pos = 20) -> None:
        self.x_pos = x_pos
        self.y_pos = y_pos
    
    def deploy(self):
        spawn_width = 45
        start = self.x_pos - spawn_width
        end = self.x_pos + spawn_width
        for x_nudge in range(math.floor(start), math.floor(end), 40):
            bullet_list.append(Bullet(  x_pos = x_nudge,\
                                        y_pos = self.y_pos, \
                                        x_speed = (random.randint(-10, 10) / 12)*(random.randint(1, 10)/30),\
                                        y_speed = 0.2, \
                                        size= 10))


class PatternAimedWall:
    def __init__(self, x_pos = WIDTH-30, y_pos = 20, player_pos_x = WIDTH/2, player_pos_y = HEIGHT-20) -> None:
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.target_x = player_pos_x
        self.target_y = player_pos_y
    
    def deploy(self):
        for j in range (12):
            for i in range (6):
                lateral = 0
                if self.x_pos < self.target_x:
                    lateral = self.target_x + self.x_pos
                else:
                    lateral = (self.target_x + self.x_pos) * -1

                horizontal = 0
                if self.y_pos < self.target_y:
                    horizontal = self.target_y - self.y_pos
                else:
                    horizontal = (self.target_y - self.y_pos) * -1
                
                bullet_list.append(Bullet(  x_pos=self.x_pos - i*i,\
                                            y_pos=(self.y_pos + i*i)*j*j,\
                                            x_speed=lateral*0.0001*(0.4*i+0.1),\
                                            y_speed=horizontal*0.0001,\
                                            size=17,\
                                            colour=RED))

# Game initialization
difficulty = {"easy":True,\
              "hard":False}
dispSurf.fill(BLACK)
# Load graphics
gfx_dir = os.getcwd()+"\\gfx\\"
ch1_bg = gfx_dir+"treetops_bg_scroll.jpg"
bg = MovingBGimage(ch1_bg)
bullet_list = []
pygame.display.flip()
player_one = Player()
patterns = []
move_command = {    K_UP:False,\
                    K_DOWN:False,\
                    K_LEFT:False,\
                    K_RIGHT:False,\
                    K_LSHIFT:False}
tstart = time.time_ns() / 1_000_000
time.sleep(0.01)
frame = 1
in_menu = True

def game_init():
    global difficulty
    global dispSurf
    global gfx_dir
    global ch1_bg
    global bg 
    global bullet_list
    global player_one
    global patterns
    global move_command
    global tstart
    global frame
    global in_menu

    difficulty = {"easy":True,\
              "hard":False}
    dispSurf.fill(BLACK)
    # Load graphics
    gfx_dir = os.getcwd()+"\\gfx\\"
    ch1_bg = gfx_dir+"treetops_bg_scroll.jpg"
    bg = MovingBGimage(ch1_bg)

    
    bullet_list = []
    pygame.display.flip()
    player_one = Player()
    patterns = []
    move_command = {    K_UP:False,\
                        K_DOWN:False,\
                        K_LEFT:False,\
                        K_RIGHT:False,\
                        K_LSHIFT:False}
    tstart = time.time_ns() / 1_000_000
    time.sleep(0.01)
    frame = 1
    in_menu = True

# Font initialization
readout_font = pygame.font.SysFont("Calibri", 16)
readout_surface = readout_font.render(f"test", False, WHITE)
score_font = pygame.font.SysFont("Calibri", 30)
score_surface = score_font.render(f"{player_one.score}", True, WHITE)

# Main loop
while True:
    ### Menu loop
    while in_menu:
            dispSurf.fill(BLACK)

            # Headers
            group_font = pygame.font.SysFont("Calibri", 72)
            title_font = pygame.font.SysFont("Calibri", 38)
            title_sub_font = pygame.font.SysFont("Calibri", 22)
            group_surface = group_font.render("E1", True, WHITE)
            title_surface = title_font.render("Dodge to live", True, WHITE)
            start_surface = title_sub_font.render("Press space to start.", True, colour_nudge(TEAL, 20))
            dispSurf.blit(group_surface, ((WIDTH/2)-200, (HEIGHT/2)-100-100))
            dispSurf.blit(title_surface, ((WIDTH/2)-200, (HEIGHT/2)-20))
            dispSurf.blit(start_surface, ((WIDTH/2)-200, (HEIGHT/2)+15))

            # Difficulty
            easy_surface = title_font.render("[easy]", True, DIFFICULTY_COLOUR[difficulty["easy"]])
            hard_surface = title_font.render("[hard]", True, DIFFICULTY_COLOUR[difficulty["hard"]])
            dispSurf.blit(easy_surface, ((WIDTH/2)-200, (HEIGHT/2)-20-50))
            dispSurf.blit(hard_surface, ((WIDTH/2)-200+100, (HEIGHT/2)-20-50))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == KEYDOWN:
                    if event.key == K_SPACE:
                        in_menu = False
                    if event.key == K_RIGHT:
                        difficulty["easy"] = False
                        difficulty["hard"] = True
                    if event.key == K_LEFT:
                        difficulty["easy"] = True
                        difficulty["hard"] = False
                    if event.key == K_ESCAPE:
                        pygame.quit()
                        sys.exit()
            pygame.display.flip()
    
    ### Game
    difficulty_modifier = 1
    if difficulty["hard"]:
        difficulty_modifier = 0.2
    dispSurf.fill(BLACK)

    # Draw background
    backgrounds = []
    bg.actuate()

    # Timing
    tm = time.time_ns() / 1_000_000

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == KEYDOWN:
            move_command[event.key] = True
            if event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()

        elif event.type == KEYUP:
            move_command[event.key] = False
        
    player_one.move(move_command)

    # Deploy patterns
    if frame % (300 * (difficulty_modifier * 0.5)) == 0:
        patterns.append(PatternSpraySpam(frame % WIDTH))
    if frame % (1500 * difficulty_modifier * 3) == 0:
        patterns.append(PatternAimedWall(player_pos_x=player_one.x_pos, player_pos_y=player_one.y_pos))
    for pattern in patterns:
        pattern.deploy()

    # Handle bullets
    marked_for_del = []
    bullet_grid = []
    bullet_index = 0
    while bullet_index < len(bullet_list):
        active_bullet = bullet_list[bullet_index]
        active_bullet.post_time(tm)
        active_bullet.move()
        # Arena edge
        if active_bullet.x_pos < 0 - active_bullet.size or active_bullet.x_pos > WIDTH + active_bullet.size \
            or active_bullet.y_pos < 0 - active_bullet.size or active_bullet.y_pos > HEIGHT + active_bullet.size:
            active_bullet.delete = True
            active_bullet.active = False

        if active_bullet.active:
            active_bullet.draw()
            bullet_grid.append([active_bullet.get_grid(), active_bullet])
        elif active_bullet.delete:
            marked_for_del.append(active_bullet)
        bullet_index += 1
    
    # Check interaction
    player_grid = player_one.get_grid()
    grid_modifier = [(i, j) for i in range(-1, 2) for j in range(-1, 2)]
    grids_to_check = []
    for modifier in grid_modifier:
        grids_to_check.append([player_grid[0]+modifier[0] , player_grid[1]+modifier[1]])
    # Check bullet distance for bullets in nearby grids
    for singular_bullet in bullet_grid:
        bullet_grid_value = singular_bullet[0]
        active_bullet = singular_bullet[1]
        if bullet_grid_value in grids_to_check:
            bullet_distance = math.sqrt(((player_one.x_pos - active_bullet.x_pos)**2) + ((player_one.y_pos - active_bullet.y_pos)**2))
            # Graze bullet
            if bullet_distance < active_bullet.size + player_one.graze_range and active_bullet.active:
                if player_one.score_cooldown + 10 < tm:
                    player_one.score_cooldown = tm
                    player_one.score += 1
                    player_one.jubilate()
            # Touch bullet
            if bullet_distance < active_bullet.size and active_bullet.active:
                player_one.alive = False

    # Delete bullets
    for deletion_bullet in marked_for_del:
        bullet_list.remove(deletion_bullet)
    
    # Delete patterns
    patterns = []

    # Player draw
    player_one.draw()

    # Readout draw
    tdif = tm-tstart
    readout_surface = readout_font.render(f"frame {frame} time elapsed {round(tdif / 1000, 3)} av fps {round(frame / (tdif/1000), 3)}", False, WHITE)
    dispSurf.blit(readout_surface, (20,20))
    score_surface = score_font.render(f"{player_one.score}", True, WHITE)
    dispSurf.blit(score_surface, (20,50))

    pygame.display.flip()
    frame += 1

    # Death screen
    if not player_one.alive:
        time.sleep(1)
    while not player_one.alive:
        dispSurf.fill(BLACK)
        score_surface = score_font.render(f" Final score : {player_one.score}", True, WHITE)
        dispSurf.blit(score_surface, ((WIDTH/2)-140,(HEIGHT/2)-50))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_SPACE:
                    # New game init
                    game_init()
                    pygame.display.flip()
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
        pygame.display.flip()
