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
    global boy, paused, pause_key_down, item_mode, item_key_down
    
    event_list = get_events()
    for event in event_list:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYUP and event.key == SDLK_p:
            pause_key_down = False
        elif event.type == SDL_KEYUP and event.key == SDLK_i:
            item_key_down = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_p:
            if not pause_key_down:
                pause_key_down = True
                paused = not paused
                if paused:
                    boy.release_movement()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_i:
            if not item_key_down:
                item_key_down = True
                if not paused:
                    item_mode = not item_mode
        elif paused:
            continue
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            import title_mode
            game_framework.change_mode(title_mode)
            return
        elif (item_mode and event.type == SDL_KEYDOWN and
              event.key == SDLK_0):
            boy.selected_item = 'none'
        elif (item_mode and event.type == SDL_KEYDOWN and
              event.key == SDLK_1):
            boy.selected_item = 'small'
        elif (item_mode and event.type == SDL_KEYDOWN and
              event.key == SDLK_2):
            boy.selected_item = 'large'
        else:
            boy.handle_event(event)



def init():
    global boy, paused, pause_key_down, pause_image
    global item_mode, item_key_down, item_select_image

    game_world.clear()
    paused = False
    pause_key_down = False
    item_mode = False
    item_key_down = False
    pause_image = load_image('pause.png')
    item_select_image = load_image('item_select.png')
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
    if item_mode:
        center_x = get_canvas_width() // 2
        center_y = get_canvas_height() // 2
        item_select_image.draw(center_x, center_y)
        selection_y = center_y + {
            'none': 82,
            'small': 17,
            'large': -50,
        }[boy.selected_item]
        draw_rectangle(center_x - 126, selection_y - 24,
                       center_x + 126, selection_y + 24,
                       255, 215, 0)
    update_canvas()


def finish():
    global pause_image, paused, pause_key_down
    global item_mode, item_key_down, item_select_image
    game_world.clear()
    pause_image = None
    item_select_image = None
    paused = False
    pause_key_down = False
    item_mode = False
    item_key_down = False
