import os

import game_framework
import title_mode
from pico2d import *

image = None


def init():
    global image, logo_start_time
    asset_dir = os.path.dirname(os.path.abspath(__file__))
    image = load_image(os.path.join(asset_dir, 'tuk_credit.png'))
    logo_start_time = get_time()


def handle_events():
    for event in get_events():
        if event.type == SDL_QUIT or (
            event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE
        ):
            game_framework.quit()


def finish():
    global image
    image = None


def update():
    if get_time() - logo_start_time >= 2.0:
        game_framework.change_mode(title_mode)


def render():
    clear_canvas()
    image.draw(get_canvas_width() // 2, get_canvas_height() // 2,
               get_canvas_width(), get_canvas_height())
    update_canvas()