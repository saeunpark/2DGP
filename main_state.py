# hero_controller.py : control hero move with left and right key
import time
import random
import hold_state
import json
from pico2d import *

runnin = None

monster=[]
monster_arrow=[]
player_arrow=[]
items=[]
init_data_file=open('init.txt','r')
init_data=json.load(init_data_file)
init_data_file.close()

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
#
# class Bgm:
#     def __init__(self):
#         self.bgm = load_music('VoodooKingdom.mp3')
#         self.bgm.set_volume(64)
#         self.bgm.repeat_play()



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

class Player_Attack:
        #SKILL,HIT=None
    PIXEL_PER_METER = (10.0 / 0.3) # 10 pixel 30 cm
    RUN_SPEED_KMPH = 40.0 # Km / Hour
    RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
    RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
    RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)
    def __init__(self,x,y):
        self.image= load_image('p_attack.png')
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
        self.skill_Skill=2
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
        self.hp=100
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
        #font.draw(self.x-50,self.y+80,' SKILL: %d '%(self.skill_Skill))


        # [HP : %d], self.hp,
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
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_h):
               self.push_state(hold_state)
        elif (event.type, event.key) ==(SDL_KEYDOWN,SDLK_a):
            if self.state!=self.SKILL:
                self.skill_Skill-=1
                self.frame_x=0
                self.old_state=self.state
                self.state=self.SKILL




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
                print("새의 공격")
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


class Item:
    image=None
    PIXEL_PER_METER = (10.0 / 0.3) # 10 pixel 30 cm
    RUN_SPEED_KMPH = 10.0 # Km / Hour
    RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
    RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
    RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)
    SCORE_ITEM1,SCORE_ITEM2,SCORE_ITEM3,SKILL_ITEM,HP_ITEM=0,1,2,3,4
    def __init__(self,x,y):
        if Item.image==None:
            self.image = load_image('item.png')

        self.item_num=random.randint(1,13)
        if self.item_num<=9:
            self.item_num=(int)(self.item_num/3-1)
        elif self.item_num<=11:
            self.item_num=self.SKILL_ITEM
        else:
            self.item_num=self.HP_ITEM
        #self.item_num=0

        self.x=x
        self.y=y
    def update(self,frame_time):
        distance = Item.RUN_SPEED_PPS * frame_time

        self.x-=distance
        self.draw()
    def draw(self):
         self.image.clip_draw(self.item_num* 50, 0, 50, 50, self.x, self.y)
         draw_rectangle(*self.get_hitbox())
    def get_hitbox(self):
        return self.x - 20, self.y+20 , self.x + 20, self.y-20




def collide(a, b):
        left_a,top_a , right_a, bottom_a = a.get_hitbox()
        left_b, top_b, right_b,  bottom_b= b.get_hitbox()

        if left_a > right_b: return False
        if right_a < left_b: return False
        if top_a < bottom_b: return False
        if bottom_a > top_b: return False

        return True


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

    score=0
    global running
    global player,font,mo
    font=load_font('THEpoodingW.TTF')
    background = BackGround()
    player=Player()
    test_monster1=Monster_Pink()
    test_monster2=Monster_Bird()
    test_monster3=Monster_Alien()

    #monster.append(Monster_Pink());
    #monster.append(test_monster2);
   # monster.append(test_monster3);
  #  items.append(Item(100,200))
    running = True;
    current_time = get_time()
    while running:



        frame_time = time.clock() - current_time
        current_time += frame_time


        handle_events()

        for monsteri in monster:
            for p_arrow in player_arrow:
                if collide(p_arrow,monsteri):
                    monsteri.hp-=1;
                    player_arrow.remove(p_arrow)
            if monsteri.hp==0:
                if random.randint(0,2)==0:
                    items.append(Item(monsteri.x,monsteri.y))
                print("공격충돌")
                monster.remove(monsteri)


            if collide(player,monsteri):
                monsteri.hp-=1
                player.hp-=1
                print("몬스터에게 공격받음")

            if monsteri.detecting(player) and monsteri.sense==False:
                monsteri.sense=True
                monsteri.change_state()
            elif monsteri.detecting(player)==False and monsteri.sense==True:
                monsteri.sense=False
                monsteri.change_state()
        for arrow in monster_arrow:
            if collide(player,arrow):
                monster_arrow.remove(arrow)
                player.hp-=1;
                print("총알에 공격받음")
        if current_time%3.0<0.1:
            temp=random.randint(1,4)
            if temp==1:
                monster.append(Monster_Pink())
            elif temp==2:
                monster.append(Monster_Bird())
            else:
                monster.append(Monster_Alien())
        for item in items:
            if item.x<-150:
                items.remove(item)

       # clear_canvas()
        background.update()

        #font.draw(50,50,'score: %d time: %f'%(score, current_time))
        for item in items:
            if collide(player,item):
                if item.item_num<3:
                    score+=200
                elif item.item_num==3:
                    player.skill_Skill+=1
                else:
                    player.hp+=1
                items.remove(item)

            else:
                item.update(frame_time)
        for p_arrow in player_arrow:
            p_arrow.update(frame_time)
            if p_arrow.x>1000:
                player_arrow.remove(p_arrow)

        for monsteri in monster:
            monsteri.update(frame_time)
        for arrow in monster_arrow:
            arrow.update(frame_time)
            if arrow.x<-150:
                monster_arrow.remove(arrow)
                print("새공격이 캐릭터충돌")

        player.update(frame_time)

        update_canvas()

        delay(0.05)

    del(font)
    close_canvas()


if __name__ == '__main__':
    main()