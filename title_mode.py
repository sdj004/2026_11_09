import os

import game_framework
from pico2d import *

image = None


def init():
    global image
    asset_dir = os.path.dirname(os.path.abspath(__file__))
    image = load_image(os.path.join(asset_dir, 'title.png'))


def handle_events():
    for event in get_events():
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN:
            if event.key == SDLK_ESCAPE:
                game_framework.quit()
            elif event.key == SDLK_SPACE:
                import play_mode
                game_framework.change_mode(play_mode)
                return


def update():
    pass


def render():
    clear_canvas()
    image.draw(get_canvas_width() // 2, get_canvas_height() // 2,
               get_canvas_width(), get_canvas_height())
    update_canvas()


def finish():
    global image
    image = None
