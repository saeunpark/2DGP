from pico2d import *
import random
import math
import json
import game_framework
import main_state

class Shot:
    image = None

    SHOT, BIM = 0, 1

    def __init__(self,x,y):

        self.x , self.y = x ,y
        self.bgm = load_wav('./resource/shot.wav')
        self.bgm.set_volume(24)
        self.bgm.play()

        self.state = self.SHOT
        if Shot.image == None:
            Shot.image = load_image('./resource/bullet.png')

    def update(self):
        pass
    def draw(self):
        self.image.clip_draw(0,self.state*34,43,34,self.x,self.y)
        self.x += 25

    def get_bb(self):
        return self.x - 15, self.y - 15, self.x +15, self.y +15