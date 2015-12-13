from pico2d import *
import random
import math
import json
import game_framework
import main_state

class Boss_Shot:
    image=None
    PIXEL_PER_METER = (10.0 / 0.3) # 10 pixel 30 cm
    RUN_SPEED_KMPH = 40.0 # Km / Hour
    RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
    RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
    RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)
    def __init__(self,x,y):
        self.x=x
        self.y=y
        if Boss_Shot.image==None:
            self.image = load_image('./resource/shot.png')

    def update(self,frame_time):
        distance = Boss_Shot.RUN_SPEED_PPS * frame_time
        self.x-=distance
        self.draw()

    def draw(self):
        self.image.draw(self.x, self.y)
        draw_rectangle(*self.get_bb())

    def get_bb(self):
        return self.x - 15, self.y - 15, self.x +15, self.y +15