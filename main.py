"""
Main execution
"""

# System modules
import pygame
import os
import sys
import random
from pygame.locals import *

# Game modules
from const import *
import func as f
import obj
import gfx
import pattern as p
import dance


## Engine initialization
pygame.init()
pygame.font.init()
pygame.display.set_caption("Foliage")
screen_surface = pygame.display.set_mode(size=(WIDTH, HEIGHT))


## Game initialisation block start ##
# System related
global dir
dir = os.getcwd()

# Game settings
global difficulty_selection
global in_menu
difficulty_selection = "easy"
in_menu = True

# Controls
global command
command = { K_UP:       False,\
            K_DOWN:     False,\
            K_LEFT:     False,\
            K_RIGHT:    False,\
            K_LSHIFT:   False,\
            K_z:        False}

# Timing
global clock
global time_delta
global frame

clock = pygame.time.Clock()
time_delta = clock.tick(FPS_LIMIT)
frame = 0

# Fonts
global menu_font_big
global menu_font_med
global menu_font_sml

menu_font_big = pygame.font.SysFont(MENU_FONT, 50)
menu_font_med = pygame.font.SysFont(MENU_FONT, 16)
menu_font_sml = pygame.font.SysFont(MENU_FONT, 12)

# Images
# Background images
img_treetops_horizon =  pygame.image.load(dir+"\\gfx\\treetops_horizon.png").convert_alpha()
img_treetops_bg_scroll= pygame.image.load(dir+"\\gfx\\treetops_bg_scroll.png").convert_alpha()
img_treetops_sky =      pygame.image.load(dir+"\\gfx\\treetops_sky.png").convert_alpha()
# Other moving small background images
img_cloud_1_fluffy =    pygame.image.load(dir+"\\gfx\\cloud_1_fluffy.png").convert_alpha()
img_cloud_1_small =     pygame.image.load(dir+"\\gfx\\cloud_1_small.png").convert_alpha()
img_cloud_1_streak =    pygame.image.load(dir+"\\gfx\\cloud_1_streak.png").convert_alpha()
img_cloud_2_fluffy =    pygame.image.load(dir+"\\gfx\\cloud_2_fluffy.png").convert_alpha()
img_cloud_3_fluffy =    pygame.image.load(dir+"\\gfx\\cloud_3_fluffy.png").convert_alpha()
img_one_bird =          pygame.image.load(dir+"\\gfx\\one_bird.png").convert_alpha()
img_three_birds =       pygame.image.load(dir+"\\gfx\\three_birds.png").convert_alpha()
# Bullets
img_bl_32px_red_orb =   pygame.image.load(dir+"\\gfx\\bl_32px_red_orb.png").convert_alpha()
img_bl_32px_green_orb = pygame.image.load(dir+"\\gfx\\bl_32px_green_orb.png").convert_alpha()
img_bl_32px_blue_orb =  pygame.image.load(dir+"\\gfx\\bl_32px_blue_orb.png").convert_alpha()
img_bl_32px_teal_orb =  pygame.image.load(dir+"\\gfx\\bl_32px_teal_orb.png").convert_alpha()
img_bl_12px_red =       pygame.image.load(dir+"\\gfx\\bl_12px_red.png").convert_alpha()
img_bl_12px_green =     pygame.image.load(dir+"\\gfx\\bl_12px_green.png").convert_alpha()
img_bl_12px_blue =      pygame.image.load(dir+"\\gfx\\bl_12px_blue.png").convert_alpha()
img_bl_12px_teal =      pygame.image.load(dir+"\\gfx\\bl_12px_teal.png").convert_alpha()
img_bl_6px_red =        pygame.image.load(dir+"\\gfx\\bl_6px_red.png").convert_alpha()
img_bl_6px_green =      pygame.image.load(dir+"\\gfx\\bl_6px_green.png").convert_alpha()
img_bl_6px_blue =       pygame.image.load(dir+"\\gfx\\bl_6px_blue.png").convert_alpha()
img_bl_6px_teal =       pygame.image.load(dir+"\\gfx\\bl_6px_teal.png").convert_alpha()

bullet_surface_32 = [
    img_bl_32px_red_orb,
    img_bl_32px_green_orb,
    img_bl_32px_blue_orb,
    img_bl_32px_teal_orb
    ]


# Player
global player_one

player_one = obj.Player()

pygame.display.flip()
## Game initialisation block end ##


def main_menu() -> dict:
    # Globals affected
    # Timings
    global clock
    global time_delta
    frame = 0 # no need to have global frames
    # Game settings
    global difficulty_selection
    global in_menu

    # Menu init
    menu_anchor = {"x":WIDTH*0.05, "y":HEIGHT*0.5}
    text_foil_surface = pygame.Surface((200,200)).convert_alpha()
    text_foil_surface.fill((0,0,0,150))
    pygame.draw.rect(text_foil_surface, BLACK, rect=(   menu_anchor["x"],       menu_anchor["y"],\
                                                        menu_anchor["x"]+100,   menu_anchor["y"]+100))
    text_foil = gfx.Img(x_pos=menu_anchor["x"]+10, \
                        y_pos=menu_anchor["y"]+10, surface=text_foil_surface)

    # Background image
    menu_background = gfx.Img(x_pos=0, y_pos=0, surface=img_treetops_horizon)

    # Animated background
    clouds_far = gfx.Img(x_pos= WIDTH-250, y_pos= -20, speed_x=-0.005)
    clouds_far.surface = img_cloud_1_fluffy.copy()
    clouds_far.surface = pygame.transform.scale_by(clouds_far.surface, 0.8)

    # Menu Text
    game_name = menu_font_big.render("Game", True, WHITE)
    render_game_name = gfx.Text(x_pos=menu_anchor["x"]+20, \
                                y_pos=menu_anchor["y"]+20, surface=game_name)
    select_difficulty = menu_font_med.render("Select difficulty:", True, WHITE)
    render_select_difficulty = gfx.Text(    x_pos=menu_anchor["x"]+20, \
                                            y_pos=menu_anchor["y"]+80, surface=select_difficulty)
    press_space = menu_font_med.render("Press space to start.", True, WHITE)

    while in_menu:
        time_delta = clock.tick(FPS_LIMIT)
        frame += 1

        # Draw queues
        background_draw_queue = []
        bullet_draw_queue = []
        player_draw_queue = []
        hud_draw_queue = []
        draw_queue = [  background_draw_queue,\
                        bullet_draw_queue,\
                        player_draw_queue,\
                        hud_draw_queue]

        # Handle interaction
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            # Keypresses
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                # Select difficulty
                if event.key == K_RIGHT:
                    difficulty_selection = "hard"
                if event.key == K_LEFT:
                    difficulty_selection = "easy"
                # Confirm selection
                if event.key == K_SPACE:
                    out = {"difficulty":difficulty_selection}
                    return out

        # Menu display 
        background_draw_queue.append(menu_background)
        clouds_far.move(time_delta)
        background_draw_queue.append(clouds_far)
        background_draw_queue.append(text_foil)
        background_draw_queue.append(render_game_name)
        background_draw_queue.append(render_select_difficulty)
        if difficulty_selection == "easy":
            select_easy = menu_font_med.render("> EASY", True, WHITE)
            select_hard = menu_font_med.render("   HARD", True, WHITE)
        else:
            select_easy = menu_font_med.render("   EASY", True, WHITE)
            select_hard = menu_font_med.render("> HARD", True, WHITE)
        background_draw_queue.append(gfx.Text(x_pos=menu_anchor["x"]+20, \
                                              y_pos=menu_anchor["y"]+110, surface=select_easy))
        background_draw_queue.append(gfx.Text(x_pos=menu_anchor["x"]+80, \
                                              y_pos=menu_anchor["y"]+110, surface=select_hard))
        
        background_draw_queue.append(gfx.Text(x_pos=menu_anchor["x"]+20, \
                                              y_pos=menu_anchor["y"]+140, surface=press_space))

        # Draw
        for queue in draw_queue:
            for this_surface in queue:
                if this_surface != None:
                    screen_surface.blit(this_surface.surface, (this_surface.x_pos, this_surface.y_pos))

        pygame.display.flip()


def main_game(menu_settings)-> dict:
    # Globals affected
    # Timings
    global clock
    global time_delta
    frame = 0 # no need to have global frames
    global command
    global player_one

    command = { K_UP:       False,\
                K_DOWN:     False,\
                K_LEFT:     False,\
                K_RIGHT:    False,\
                K_LSHIFT:   False,\
                K_z:        False}

    player_objects = []
    pattern_objects = []
    bullet_objects = []
    deletion_objects = []

    level_bg_y_start = img_treetops_bg_scroll.get_size()
    level_bg_y_start = int(level_bg_y_start[1] - HEIGHT)
    level_background = gfx.Img(x_pos=0, y_pos=-level_bg_y_start, speed_y=0.02, surface=img_treetops_bg_scroll)
    player_one = obj.Player()
    player_one.surface = img_bl_32px_blue_orb

    while True:
        time_delta = clock.tick(FPS_LIMIT)
        frame += 1

        # Draw queues reset
        background_draw_queue = []
        bullet_draw_queue = []
        player_draw_queue = []
        hud_draw_queue = []
        draw_queue = [  background_draw_queue,\
                        bullet_draw_queue,\
                        player_draw_queue,\
                        hud_draw_queue]

        # Handle interaction
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            # Keypresses
            if event.type == KEYDOWN:
                command[event.key] = True
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            if event.type == KEYUP:
                command[event.key] = False
        
        # Append background to draw
        level_background.move(time_delta)
        background_draw_queue.append(level_background)

        # Player actions
        bullet_release = player_one.command(time_delta, command)
        player_draw_queue.append(player_one)

        # Bullet deployment from dances
        if frame == 30:
            intro = dance.Intro(frame)
            pattern_objects.append(intro)

        for pattern in pattern_objects:
            if pattern.active:
                incoming = pattern.actuate(frame)
                if incoming != None:
                    
                    for incoming_bullet in incoming:
                        incoming_bullet.surface = img_bl_32px_red_orb
                        bullet_objects.append(incoming_bullet)
            else:
                deletion_objects.append(pattern_objects.pop(pattern_objects.index(pattern)))


        # Determine player grid and neighbourhood
        player_grid = f.assign_grid(player_one.x_pos, player_one.y_pos)
        grid_modifier = [(j,i) for i in range(-1,2) for j in range(-1,2)]
        grids_surrounding_player = [(modifier[0] + player_grid[0], modifier[1] + player_grid[1]) for modifier in grid_modifier]
        
        # Bullet actions
        index = 0
        while index < len(bullet_objects):
            single_bullet = bullet_objects[index]
            single_bullet.move( time_delta =    time_delta, \
                                target_x =      player_one.x_pos, \
                                target_y =      player_one.y_pos)
            # Out of bounds
            if single_bullet.x_pos < 0 - single_bullet.size or single_bullet.x_pos > WIDTH + single_bullet.size\
                or single_bullet.y_pos < 0 - single_bullet.size or single_bullet.y_pos > HEIGHT + single_bullet.size:
                single_bullet.active = False

            if single_bullet.active:
                bullet_draw_queue.append(single_bullet)
                this_bullet_grid = f.assign_grid(x_pos=single_bullet.x_pos, \
                                                 y_pos=single_bullet.y_pos)
                # If in the neighbourhood of player
                if this_bullet_grid in grids_surrounding_player:
                    bullet_distance = f.vector_lenght(  source=(single_bullet.x_pos, single_bullet.y_pos),\
                                                        target=(player_one.x_pos, player_one.y_pos))
                    # Grazing bullet
                    if bullet_distance < single_bullet.size + player_one.graze_distance and single_bullet.faction < 0:
                        player_one.score += 1
                    # Touching bullet
                    if bullet_distance < single_bullet.size/2 + player_one.hit_distance and single_bullet.faction < 0:
                        return player_one.score
                    # Recruit bullet
                    if single_bullet.y_pos - player_one.y_pos > 20 and abs(abs(player_one.x_pos) - abs(single_bullet.x_pos)) < 30 and single_bullet.faction == -1:
                        single_bullet.surface = img_bl_12px_green
                        single_bullet.faction = 0
                    # If bullet is released
                    if bullet_release and single_bullet.faction == 0:
                        single_bullet.faction = 1
                    
            else: # Move to del
                deletion_objects.append(bullet_objects.pop(index))
            index += 1

        # Handle object deletion
        deletion_objects = []

        # Dev monitoring
        if frame % 5 == 0:
            print(frame, len(bullet_objects), len(deletion_objects))

        # Draw
        for queue in draw_queue:
            for this_surface in queue:
                if this_surface != None:
                    try:
                        screen_surface.blit(this_surface.surface, (this_surface.x_pos - this_surface.size/2 , this_surface.y_pos - this_surface.size/2))
                    except:
                        screen_surface.blit(this_surface.surface, (this_surface.x_pos, this_surface.y_pos))
        pygame.display.flip()


def main_score(game_output) -> None:
    print("Game over, score ", game_output)


def main():
    while True:
        menu_settings = main_menu()
        game_output = main_game(menu_settings)
        main_score(game_output)

if __name__ == "__main__":
    main()