from pico2d import *
import random
import math
import json
import game_framework
import main_state


class Bim:
    image = None
    def __init__(self,x,y):
        self.x , self.y = x ,y
        self.bgm = load_wav('./resource/shot.wav')
        self.bgm.set_volume(64)
        self.bgm.play()

        if Bim.image == None:
            Bim.image = load_image('./resource/bim.png')
    def update(self):
        pass
    def draw(self):
        self.image.clip_draw(0,0,40,43,self.x,self.y)
        self.x += 25

    def get_bb(self):
        return self.x - 15, self.y - 15, self.x +15, self.y +15