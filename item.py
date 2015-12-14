from pico2d import *
import random
import game_framework
import main_state

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
            self.image = load_image('./resource/item.png')

        self.item_num=random.randint(1,13)
        if self.item_num<=9:
            self.item_num=(int)(self.item_num/3-1)
        elif self.item_num<=11:
            self.item_num=self.SKILL_ITEM
        else:
            self.item_num=self.HP_ITEM

        self.x=x
        self.y=y
    def update(self,frame_time):
        distance = Item.RUN_SPEED_PPS * frame_time

        self.x-=distance
        self.draw()
    def draw(self):
         self.image.clip_draw(self.item_num* 50, 0, 50, 50, self.x, self.y)
        # draw_rectangle(*self.get_bb())
    def get_bb(self):
        return self.x - 20, self.y+20 , self.x + 20, self.y-20
