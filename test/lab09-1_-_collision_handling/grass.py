import random

from pico2d import *

class Grass:
    def __init__(self):
        self.image = load_image('grass.png')

    def draw(self):
        self.image.draw(400, 30)

    # fill here

    def draw_bb(self):
        draw_rectangle(*self.get_bb())


