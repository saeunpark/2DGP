# hero_controller.py : control hero move with left and right key

import random
from pico2d import *

runnin = None
hero = None




class BackGround:
    def __init__(self):
        self.block_image = load_image('BackGround_Block.png')
        self.sky_image=load_image('BackGround_sky.png')
        self.x_move_max=init_data['BackGround']['max_x']
        self.x_move_min=init_data['BackGround']['min_x']
        self.block_x=init_data['BackGround']['min_x']
        self.block_x2=init_data['BackGround']['max_x']
        self.sky_x=init_data['BackGround']['min_x']
        self.sky_x2=init_data['BackGround']['max_x']
        self.block_moveP=init_data['BackGround']['block_moveP']
        self.sky_moveP=init_data['BackGround']['sky_moveP']
        self.screen_W=init_data['BackGround']['screen_w']
        self.sky_h=init_data['BackGround']['sky_draw_h']
        self.sky_y=init_data['BackGround']['sky_y']
        self.block_h=init_data['BackGround']['block_draw_h']
        self.block_y=init_data['BackGround']['block_y']

    def draw(self):
        self.sky_image.clip_draw(0,0,self.screen_W,self.sky_h,self.sky_x,self.sky_y)
        self.sky_image.clip_draw(0,0,self.screen_W,self.sky_h,self.sky_x2,self.sky_y)
        self.block_image.clip_draw(0,0,self.screen_W,self.block_h,self.block_x,self.block_y)
        self.block_image.clip_draw(0,0,self.screen_W,self.block_h,self.block_x2,self.block_y)
    def update(self):

        self.draw();
        self.block_x-=self.block_moveP
        self.sky_x-=self.sky_moveP
        self.block_x2-=self.block_moveP
        self.sky_x2-=self.sky_moveP

        if self.block_x<=-self.x_move_min:
            self.block_x=self.x_move_max
        if self.sky_x<=-self.x_move_min:
            self.sky_x=self.x_move_max
        if self.block_x2<=-self.x_move_min:
            self.block_x2=self.x_move_max
        if self.sky_x2<=-self.x_move_min:
            self.sky_x2=self.x_move_max
        #

class Player:
    global font
    STANDING,LEFT_MOVE,RIGHT_MOVE,UP_MOVE,DOWN_MOVE=0,1,2,3,4
    ATTACK,SKILL=5,6
    #SKILL,HIT=None
    PIXEL_PER_METER = (10.0 / 0.3) # 10 pixel 30 cm
    RUN_SPEED_KMPH = 20.0 # Km / Hour
    RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
    RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
    RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)
    def __init__(self):
        self.skill_gauge=2
        self.image = load_image('player.png')
        self.image_attack = load_image('player_attack.png')
        self.image_skill=load_image('player_skill.png')
        self.image_skill_effect=load_image('skill.png')
        self.image_skill_effect2=load_image('skill2.png')
        self.frame_y = 0
        self.frame_x = 0
        self.state = self.STANDING
        self.old_state=self.state
        self.x=200
        self.y=200
        self.hp=300
    def draw(self):
        if self.state==self.ATTACK:
            self.image_attack.clip_draw(self.frame_x * 200, self.frame_y * 115, 200, 115, self.x, self.y)
        elif self.state==self.SKILL:
            self.image_skill.clip_draw(self.frame_x * 230, self.frame_y * 150, 230, 130, self.x, self.y)
            if self.frame_x>=3 and self.frame_x<=7:
                if self.frame_x%2==0:
                    self.image_skill_effect.draw(400,300)
                else:
                    self.image_skill_effect2.draw(400,300)
                for monsteri in monster:
                    monsteri.hp=0
        else:
            self.image.clip_draw(self.frame_x * 117, self.frame_y * 115, 117, 115, self.x, self.y)
        draw_rectangle(*self.get_hitbox())
        font.draw(self.x-30,self.y+60,'hp -> %d ,gauge->%d'%(self.hp,self.skill_gauge))
    def get_hitbox(self):
         return self.x - 40, self.y+50 , self.x + 40, self.y-50
    def update(self, frame_time):
        distance = Player.RUN_SPEED_PPS * frame_time
        if self.state==self.ATTACK:
            self.frame_x = (self.frame_x + 1) % 9
            if self.frame_x==5:
                player_arrow.append(Player_Attack(self.x+30,self.y))
        elif self.state==self.SKILL:
            if self.frame_x==12:
                self.frame_x=0
                self.state=self.old_state
            self.frame_x = (self.frame_x + 1) % 13

        else:
            self.frame_x = (self.frame_x + 1) % 5


        if self.state == self.RIGHT_MOVE:
            self.x = min(750, self.x + distance)
        elif self.state == self.LEFT_MOVE:
            self.x = max(50, self.x - distance)
        elif self.state == self.UP_MOVE:
            self.y = min(325, self.y + distance)
        elif self.state == self.DOWN_MOVE:
            self.y = max(50, self.y - distance)



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
        elif (event.type, event.key) ==(SDL_KEYDOWN,SDLK_z):
            if self.state!=self.SKILL:
                self.skill_gauge-=1
                self.frame_x=0
                self.old_state=self.state
                self.state=self.SKILL





class Player_Attack:

    PIXEL_PER_METER = (10.0 / 0.3) # 10 pixel 30 cm
    RUN_SPEED_KMPH = 40.0 # Km / Hour
    RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
    RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
    RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)
    def __init__(self,x,y):
        self.image= load_image('p_attack.png') # 공격
        self.x=x
        self.y=y
    def update(self,frame_time):
        distance = Player_Attack.RUN_SPEED_PPS * frame_time
        self.x+=distance
        self.draw()
    def get_hitbox(self):
         return self.x - 30, self.y +30, self.x + 30, self.y-30
    def draw(self):
        self.image.draw(self.x, self.y)
        draw_rectangle(*self.get_hitbox())

            #



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

class Monster_Pink:
    image = None
    MOVE,HIT=2,1
    PIXEL_PER_METER = (10.0 / 0.3) # 10 pixel 30 cm
    RUN_SPEED_KMPH = 30.0 # Km / Hour
    RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
    RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
    RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)
    def __init__(self):
        if Monster_Pink.image==None:
            self.image = load_image('monster_pink.png')
        self.frame_x = 0
        self.frame_y=self.MOVE
        self.x=900
        self.y=random.randint(50,325)
        self.hp=1
        self.sense=False
    def set(x,y):
        self.x=x
        self.y=y
    def draw(self):
        self.image.clip_draw(self.frame_x * 110, self.frame_y* 110, 110, 110, self.x, self.y)
        draw_rectangle(*self.get_hitbox())
    def get_hitbox(self):
         return self.x - 40, self.y+40 , self.x + 30, self.y-50
    def update(self,frame_time):
        distance = Monster_Pink.RUN_SPEED_PPS * frame_time
        self.frame_x = (self.frame_x + 1) % 4
        self.x-=distance
        self.draw()
    def change_state(self):
        pass
    def detecting(a, self):
        pass



class Monster_Bird:
    image = None
    image_attack = None
    MOVE,ATTACK=0,1
    PIXEL_PER_METER = (10.0 / 0.3) # 10 pixel 30 cm
    RUN_SPEED_KMPH = 20.0 # Km / Hour
    RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
    RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
    RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)
    def __init__(self):
        #self.arrow=[]
        if Monster_Bird.image==None:
            self.image = load_image('monster_bird_stand.png')
        if Monster_Bird.image_attack==None:
            self.image_attack = load_image('monster_bird_attack.png')
        self.frame_x = 0
        self.frame_y=self.MOVE
        self.x=900
        self.y=random.randint(50,325)
        self.hp=1
        self.tempframe_x=0
        self.state=self.MOVE
        self.sense=False
    def set(x,y):
        self.x=x
        self.y=y
    def draw(self):
        if self.state==self.MOVE:
            self.image.clip_draw(self.frame_x * 60, self.frame_y* 55, 60, 55, self.x, self.y)
        elif self.state==self.ATTACK:
           self.image_attack.clip_draw((self.frame_x) * 150, self.frame_y* 75, 150, 75, self.x, self.y)
        draw_rectangle(*self.get_hitbox())
    def get_hitbox(self):
         return self.x - 30, self.y +30, self.x + 20, self.y-30
    def change_state(self):
        if self.state==self.MOVE and self.sense==True:
            self.state=self.ATTACK
            frame_x=0
        elif self.state==self.ATTACK and self.sense==False:
            self.state=self.MOVE
            frame_x=0
    def update(self,frame_time):
        distance = Monster_Bird.RUN_SPEED_PPS * frame_time

        if self.state==self.ATTACK:
            self.frame_x = (self.frame_x + 1) % 10
            if self.frame_x==5:
                print("new arrow")
                monster_arrow.append(Bird_Arrow(self.x,self.y))
        elif self.state==self.MOVE:
            self.frame_x = (self.frame_x + 1) % 6
        self.x-=distance
        self.draw()
    def detecting(self,a):
        left_a,top_a , right_a, bottom_a = a.get_hitbox()
        left_b, top_b, right_b,  bottom_b= self.get_hitbox()
        if right_a < left_b:
            if top_a-10 < bottom_b: return False
            if bottom_a+10 > top_b: return False
            if left_a > right_b: return False
            return True
class Bird_Arrow:
    image=None
    PIXEL_PER_METER = (10.0 / 0.3) # 10 pixel 30 cm
    RUN_SPEED_KMPH = 40.0 # Km / Hour
    RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
    RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
    RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)
    def __init__(self,x,y):
        self.x=x
        self.y=y
        if Bird_Arrow.image==None:
            self.image = load_image('bird_arrow.png')
    def update(self,frame_time):
        distance = Bird_Arrow.RUN_SPEED_PPS * frame_time
        #print("a update")
        self.x-=distance

        self.draw()
    def get_hitbox(self):
         return self.x - 10, self.y +10, self.x + 10, self.y-10
    def draw(self):
        self.image.draw(self.x, self.y)
        draw_rectangle(*self.get_hitbox())


class Monster_Alien:
    image=None
    image_attack=None
    MOVE,ATTACK=0,1
    PIXEL_PER_METER = (10.0 / 0.3) # 10 pixel 30 cm
    RUN_SPEED_KMPH = 15.0 # Km / Hour
    RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
    RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
    RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)
    def __init__(self):
        if Monster_Alien.image==None:
            self.image = load_image('monster_alien_stand.png')
        if Monster_Alien.image_attack==None:
            self.image_attack = load_image('monster_alien_attack.png')
        self.state=self.MOVE
        self.frame_x = 0
        self.tempframe_x=0
        self.frame_y=self.MOVE
        self.x=900
        self.y=random.randint(50,325)
        self.hp=1
        self.sense=False
    def set(x,y):
        self.x=x
        self.y=y
    def draw(self):
        if self.state==self.MOVE:
            self.image.clip_draw(self.frame_x * 90, self.frame_y* 65, 90, 65, self.x, self.y)
        elif self.state==self.ATTACK:
            self.image_attack.clip_draw((self.frame_x) * 275, self.frame_y* 85, 275, 85, self.x, self.y)
        draw_rectangle(*self.get_hitbox())
    def change_state(self):
        if self.state==self.MOVE and self.sense==True:
            self.state=self.ATTACK
           # frame_x=0
        elif self.state==self.ATTACK and self.sense==False:
            self.state=self.MOVE
            frame_x=0
    def get_hitbox(self):
        if self.state==self.MOVE:
            return self.x - 40, self.y+30 , self.x + 30, self.y-30
        elif self.state==self.ATTACK:
            return self.x - 40-((self.frame_x-1)*8), self.y+30 , self.x + 40, self.y-30

    def update(self,frame_time):
        distance =  Monster_Alien.RUN_SPEED_PPS * frame_time
        if self.state==self.MOVE:
            self.frame_x = (self.frame_x + 1) % 4
        elif self.state==self.ATTACK:
            self.frame_x = (self.frame_x + 1) % 13
        self.x-=distance
        self.draw()
    def detecting(self,a):
        left_a,top_a , right_a, bottom_a = a.get_hitbox()
        left_b, top_b, right_b,  bottom_b= self.get_hitbox()

        if top_a < bottom_b: return False
        if bottom_a > top_b: return False
        if left_a > right_b: return False

        if right_a < left_b-150: return False
        if right_a > left_b-150: return True

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
