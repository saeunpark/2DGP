from pico2d import *
import random
import game_framework
import main_state


class Mon1:
    image = None

    def __init__(self):
        self.x , self.y = random.randint(500, 5000),85
        self.frame = random.randint(0, 7)
        self.hp = 1
        if Mon1.image == None:
            Mon1.image = load_image('./resource/monster1_snake.png')

    def update(self,frame_time):
        self.frame = (self.frame + 1 ) % 8
        self.x -= 2

    def draw(self):
        self.image.clip_draw((self.frame % 3) * 126, 0 * 100, 126, 102,  self.x  , self.y)

    def draw_bb(self):
        draw_rectangle(*self.get_bb())

    def get_bb(self):
        return self.x - 30, self.y - 30, self.x + 30, self.y + 30

class Mon2:
    image = None

    def __init__(self):
        self.x , self.y = random.randint(1500, 10000),87
        self.frame = random.randint(0, 7)
        self.hp = 2
        if Mon2.image == None:
            Mon2.image = load_image('./resource/monster2_doll.png')

    def update(self,frame_time):
        self.frame = (self.frame + 1 ) % 8
        self.x -= 1

    def draw(self):
        self.image.clip_draw((self.frame % 3) * 126, 0 * 100, 126, 102,  self.x  , self.y)

    def draw_bb(self):
        draw_rectangle(*self.get_bb())

    def get_bb(self):
        return self.x - 30, self.y - 30, self.x + 30, self.y + 30

class Mon3:
    image = None

    def __init__(self):
        self.x , self.y = random.randint(5000, 15000),90
        self.frame = random.randint(0, 7)
        self.hp = 9
        if Mon3.image == None:
            Mon3.image = load_image('./resource/monster3_ghost.png')

    def update(self,frame_time):
        self.frame = (self.frame + 1 ) % 8
        self.x -= 2

    def draw(self):
        self.image.clip_draw((self.frame % 3) * 126, 0 * 100, 126, 102,  self.x  , self.y)

    def draw_bb(self):
        draw_rectangle(*self.get_bb())

    def get_bb(self):
        return self.x - 30, self.y - 30, self.x + 30, self.y + 30

class Mon4:
    image = None

    def __init__(self):
        self.x , self.y = random.randint(7000,20000),90
        self.frame = random.randint(0, 7)
        self.hp = 12
        if Mon4.image == None:
            Mon4.image = load_image('./resource/monster4_Tiger.png')

    def update(self,frame_time):
        self.frame = (self.frame + 1 ) % 8
        self.x -= 3

    def draw(self):
        self.image.clip_draw((self.frame % 8)* 150, 0 *100 , 150, 90, self.x, self.y)

    def draw_bb(self):
        draw_rectangle(*self.get_bb())

    def get_bb(self):
        return self.x - 30, self.y - 30, self.x + 30, self.y + 30
