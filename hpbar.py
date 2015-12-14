from pico2d import *
import random
import game_framework

class HP_BAR:
    image = None

    def __init__(self):
        self.x = 0
        self.frame = 0
        if HP_BAR.image == None:
            HP_BAR.image = load_image('./resource/HPBAR.png')

    def update(self):
        #self.x += 10
        pass
    def draw(self):
        #self.image.draw(100, 565)
        self.image.draw(121, 546)