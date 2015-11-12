# hero_controller.py : control hero move with left and right key

import random
from pico2d import *

runnin = None
hero = None



class BackGround:
    def __init__(self):
        self.block_image = load_image('BackGround_Block.png')
        self.sky_image=load_image('BackGround_sky.png')

        self.block_x=400;
        self.block_x2=1200;
        self.sky_x=400;
        self.sky_x2=1200;


    def draw(self):
        self.sky_image.clip_draw(0,0,800,300,self.sky_x,450)
        self.sky_image.clip_draw(0,0,800,300,self.sky_x2,450)
        self.block_image.clip_draw(0,0,800,350,self.block_x,130)
        self.block_image.clip_draw(0,0,800,350,self.block_x2,130)
    def update(self):

        self.draw();
        self.block_x-=4
        self.sky_x-=2
        self.block_x2-=4
        self.sky_x2-=2

        if self.block_x<=-400:
            self.block_x=1200
        if self.sky_x<=-400:
            self.sky_x=1200
        if self.block_x2<=-400:
            self.block_x2=1200
        if self.sky_x2<=-400:
            self.sky_x2=1200


class Player:

    STANDING,LEFT_MOVE,RIGHT_MOVE,UP_MOVE,DOWN_MOVE=0,1,2,3,4
    ATTACK,SKILL=5,6
    #SKILL,HIT=None

    def __init__(self):
        self.image = load_image('player.png')
        self.image_attack = load_image('player_attack.png')
        self.image_skill=load_image('player_skill.png')
        self.frame_y = 0
        self.frame_x = 0
        self.state = self.STANDING
        self.old_state=self.state
        self.x=200
        self.y=350
        self.hp=5
    def draw(self):
        if self.state==self.ATTACK:
            self.image_attack.clip_draw(self.frame_x * 200, self.frame_y * 115, 200, 115, self.x, self.y)
        elif self.state==self.SKILL:
            self.image_skill.clip_draw(self.frame_x * 230, self.frame_y * 150, 230, 130, self.x, self.y)
        else:
            self.image.clip_draw(self.frame_x * 117, self.frame_y * 115, 117, 115, self.x, self.y)

    def update(self):
        if self.state==self.ATTACK:
            self.frame_x = (self.frame_x + 1) % 9
        elif self.state==self.SKILL:
            if self.frame_x==12:
                self.frame_x=0
                self.state=self.old_state
            self.frame_x = (self.frame_x + 1) % 13

        else:
            self.frame_x = (self.frame_x + 1) % 5


        if self.state == self.RIGHT_MOVE:
            self.x = min(750, self.x + 5)
        elif self.state == self.LEFT_MOVE:
            self.x = max(50, self.x - 5)
        elif self.state == self.UP_MOVE:
            self.y = min(750, self.y + 5)
        elif self.state == self.DOWN_MOVE:
            self.y = max(50, self.y - 5)



        self.draw();
    def handle_event(self, event):

        if (event.type, event.key) == (SDL_KEYDOWN, SDLK_LEFT):
            if self.state==self.SKILL:
                self.old_state=self.LEFT_MOVE
            else:
                self.state=self.LEFT_MOVE
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_RIGHT):
            if self.state==self.SKILL:
                self.old_state=self.RIGHT_MOVE
            else:
                self.state=self.RIGHT_MOVE
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_UP):
            if self.state==self.SKILL:
                self.old_state=self.UP_MOVE
            else:
                self.state=self.UP_MOVE
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_DOWN):
            if self.state==self.SKILL:
                self.old_state=self.DOWN_MOVE
            else:
                self.state=self .DOWN_MOVE
        elif (event.type, event.key) == (SDL_KEYUP, SDLK_LEFT):
            if self.state==self.LEFT_MOVE:
                self.state=self .STANDING
            elif self.state==self.SKILL:
                self.old_state=self.STANDING
        elif (event.type, event.key) == (SDL_KEYUP, SDLK_RIGHT):
            if self.state==self.RIGHT_MOVE:
                self.state=self.STANDING
            elif self.state==self.SKILL:
                self.old_state=self.STANDING
        elif (event.type, event.key) == (SDL_KEYUP, SDLK_UP):
            if self.state==self.UP_MOVE:
                self.state=self.STANDING
            elif self.state==self.SKILL:
                self.old_state=self.STANDING
        elif (event.type, event.key) == (SDL_KEYUP, SDLK_DOWN):
            if self.state==self.DOWN_MOVE:
                self.state=self.STANDING
            elif self.state==self.SKILL:
                self.old_state=self.STANDING
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_SPACE):
            if self.state==self.SKILL:
                self.old_state=self.ATTACK
            else:
                self.frame_x=0
                self.state=self.ATTACK
        elif (event.type, event.key) == (SDL_KEYUP, SDLK_SPACE):
            if self.state==self.ATTACK:
                self.state=self .STANDING
            elif self.state==self.SKILL:
                self.old_state=self.STANDING
        elif (event.type, event.key) ==(SDL_KEYDOWN,SDLK_a):
            if self.state!=self.SKILL:
                self.frame_x=0
                self.old_state=self.state
                self.state=self.SKILL


class Monster_stand:
    MOVE,ATTACK=0,1
    def __init__(self):
        self.image = load_image('monster_stand.png')
        self.frame_x = 0
        self.tempframe_x=0
        self.frame_y=self.MOVE
        self.x=600
        self.y=325
        self.hp=1
    def set(x,y):
        self.x=x
        self.y=y
    def draw(self):
        self.image.clip_draw(self.frame_x * 90, self.frame_y* 65, 90, 65, self.x, self.y)
    def update(self):
        self.frame_x = (self.frame_x + 1) % 4
        self.tempframe_x = (self.tempframe_x + 1) % 13
        self.draw()



def handle_events():
    global running
    global player
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            running = False
        else:
            player.handle_event(event);




def main():

    open_canvas()


    global running
    global player

    background = BackGround()
    player=Player()

    test_monster3=Monster_stand()
    running = True;
    while running:
        handle_events()


        clear_canvas()
        background.update()
        player.update()

        test_monster3.update()

        update_canvas()

        delay(0.05)

    close_canvas()


if __name__ == '__main__':
    main()

    # class Background:
    # PIXEL_PER_METER = (10.0 / 0.3)           # 10 pixel 30 cm
    # SCROLL_SPEED_KMPH = 20.0                    # Km / Hour
    # SCROLL_SPEED_MPM = (SCROLL_SPEED_KMPH * 1000.0 / 60.0)
    # SCROLL_SPEED_MPS = (SCROLL_SPEED_MPM / 60.0)
    # SCROLL_SPEED_PPS = (SCROLL_SPEED_MPS * PIXEL_PER_METER)
    #
    # def __init__(self, w, h):
    #     self.image = load_image('background.png') # 960x272
    #     self.speed = 0
    #     self.upspeed = 0
    #     self.left = 0
    #     self.bottom = 0
    #     self.screen_width = w
    #     self.screen_height = h
    #
    # def draw(self):
    #     x = int(self.left)
    #     y = int(self.bottom)
    #     w = min(self.image.w - x, self.screen_width)
    #     h = min(self.image.h - y, self.screen_height)
    #     self.image.clip_draw_to_origin(x, y, w, h, 0, 0) # left bottom width height x y 좌측하단
    #     self.image.clip_draw_to_origin(0,y, self.screen_width-w, h, w, 0) # 우측하단
    #     self.image.clip_draw_to_origin(x,0, w, y, 0, h) #좌측상단
    #     self.image.clip_draw_to_origin(0,0, self.screen_width-w, y, w, h) #우측상단
    #
    # def update(self, frame_time):
    #     self.left = (self.left + frame_time * self.speed) % self.image.w
    #     self.bottom = (self.bottom + frame_time *self.upspeed) %self.image.h
    #
    # def handle_event(self, event):
    #     if event.type == SDL_KEYDOWN:
    #         if event.key == SDLK_LEFT: self.speed -= Background.SCROLL_SPEED_PPS
    #         elif event.key == SDLK_RIGHT: self.speed += Background.SCROLL_SPEED_PPS
    #         elif event.key == SDLK_UP: self.upspeed += Background.SCROLL_SPEED_PPS
    #         elif event.key == SDLK_DOWN: self.upspeed -= Background.SCROLL_SPEED_PPS
    #     if event.type == SDL_KEYUP:
    #         if event.key == SDLK_LEFT: self.speed += Background.SCROLL_SPEED_PPS
    #         elif event.key == SDLK_RIGHT: self.speed -= Background.SCROLL_SPEED_PPS
    #         elif event.key == SDLK_UP: self.upspeed -= Background.SCROLL_SPEED_PPS
    #         elif event.key == SDLK_DOWN: self.upspeed += Background.SCROLL_SPEED_PPS

