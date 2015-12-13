from pico2d import *
import random
import game_framework

class Hero:
    image = None
    eat_sound = None

    LEFT_ATT, RIGHT_ATT, LEFT_RUN, RIGHT_RUN, LEFT_STAND, RIGHT_STAND = 0, 1, 2, 3, 4, 5
    def __init__(self):
        self.x, self.y = 50, 89
        self.frame = random.randint(0, 7)
        self.hp = 50
        self.state = self.RIGHT_STAND
        if Hero.image == None:
            Hero.image = load_image('./resource/player.png')
        if Hero.eat_sound == None:
            Hero.eat_sound = load_wav('./resource/pickup.wav')
            Hero.eat_sound.set_volume(60)



    def update(self,frame_time):
        self.frame = (self.frame + 1) % 8
        if self.state == self.RIGHT_RUN:
            self.x = min(800, self.x + 8)
        elif self.state == self.LEFT_RUN:
            self.x = max(0, self.x - 8)
        elif self.state == self.LEFT_ATT:
            self.x = max(0, self.x - 8)

    def eat(self, item):
        self.eat_sound.play()


    def handle_event(self, event):
        if (event.type, event.key) == (SDL_KEYDOWN, SDLK_LEFT):
            if self.state in (self.RIGHT_STAND, self.LEFT_STAND, self.RIGHT_RUN):
                self.state = self.LEFT_RUN
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_RIGHT):
            if self.state in (self.RIGHT_STAND, self.LEFT_STAND, self.LEFT_RUN):
                self.state = self.RIGHT_RUN
        elif (event.type, event.key) == (SDL_KEYUP, SDLK_LEFT):
            if self.state in (self.LEFT_RUN,):
                self.state = self.LEFT_STAND
        elif (event.type, event.key) == (SDL_KEYUP, SDLK_RIGHT):
            if self.state in (self.RIGHT_RUN,):
                self.state = self.RIGHT_STAND
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_SPACE):
            if self.state in (self.RIGHT_RUN, self.RIGHT_STAND):
                self.state = self.RIGHT_ATT
            elif self.state in (self.LEFT_RUN,self.RIGHT_STAND):
                self.state = self.LEFT_ATT
        elif (event.type, event.key) == (SDL_KEYUP, SDLK_SPACE):
            if self.state in (self.RIGHT_ATT,):
                self.state = self.RIGHT_STAND
            elif self.state in (self.LEFT_ATT,):
                self.state = self.LEFT_STAND

    def draw(self):
        self.image.clip_draw((self.frame % 8) * 100, self.state * 100, 100, 100, self.x, self.y)



    def get_bb(self):
        return self.x - 30, self.y - 30, self.x + 30, self.y + 30

