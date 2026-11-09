import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
from pico2d import *
from sdl2 import (SDL_KEYDOWN, SDL_KEYUP, SDLK_0, SDLK_1, SDLK_2,
                  SDLK_i, SDLK_p)
import game_framework
import game_world
from boy import Boy
from grass import Grass

paused = False
pause_key_down = False
pause_image = None
item_mode = False
item_key_down = False
item_select_image = None


def handle_events():
    global boy, paused, pause_key_down, item_mode
    
    event_list = get_events()
    for event in event_list:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYUP and event.key == SDLK_p:
            pause_key_down = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_p:
            if not pause_key_down:
                pause_key_down = True
                paused = not paused
                if paused:
                    boy.release_movement()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_i:
            if not paused:
                item_mode = not item_mode
        elif paused:
            continue
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            import title_mode
            game_framework.change_mode(title_mode)
            return
        else:
            boy.handle_event(event)



def init():
    global boy, paused, pause_key_down, pause_image

    game_world.clear()
    paused = False
    pause_key_down = False
    pause_image = load_image('pause.png')
    boy = Boy()
    game_world.add_oject(boy)

    grass = Grass()
    game_world.add_oject(grass, 0)



def update():
    if not paused:
        game_world.update()


def render():
    clear_canvas()
    game_world.render()
    if paused:
        pause_image.draw(get_canvas_width() // 2, get_canvas_height() // 2)
    update_canvas()


def finish():
    global pause_image, paused, pause_key_down
    game_world.clear()
    pause_image = None
    paused = False
    pause_key_down = False
