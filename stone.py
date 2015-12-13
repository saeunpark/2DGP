from pico2d import *
import random
import game_framework

class Stone:
    def __init__(self):
        self.x =0

        self.image = load_image('./resource/stone.png')
    def initialize(self):
        self.x=0
    def update(self):
        self.x = (self.x+5)%400
    def draw(self):
        self.image.draw(804-self.x,30)
        self.image.draw(402-self.x,30)