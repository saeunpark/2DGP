import random
import main_state

from pico2d import *

class Boss:
    image = None

    def __init__(self):
        self.x, self.y = 650, 470
        self.frame = random.randint(0, 7)
        self.hp = 100
        if Boss.image == None:
            Boss.image = load_image('./resource/Ghostboss.png')

    def update(self):
        self.frame = (self.frame + 1) % 7
    def draw(self):
        self.image.clip_draw((self.frame % 7)* 302, 0 ,302, 349, self.x, self.y)