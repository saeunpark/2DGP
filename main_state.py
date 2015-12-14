import random

from pico2d import *

import game_framework
import title_state
import clear_state
import gameover_state
import hold_state
from score import Score
from score import*
from stone import Stone
from hpbar import HP_BAR
from hero import Hero
from mon import*
from Map1 import Map1
from shot import Shot
from item import Item
from bim import *
from boss import Boss
import shot_type

name = "MainState"

hero = None
stone = None
hpbar = None
mon01 = None
mon02 = None
mon03 = None
mon04 = None
maps = None
shot = None
item = None
font = None
score = None
bim = None
boss = None


def enter():
    global hero, stone, mon01, mon02, mon03, mon04, maps, shots, font, shots, items, score, hpbar, bims, boss
    hero = Hero()
    stone = Stone()
    hpbar = HP_BAR()
    mon01 = [Mon1() for i in range(70)]
    mon02 = [Mon2() for i in range(50)]
    mon03 = [Mon3() for i in range(40)]
    mon04 = [Mon4() for i in range(30)]
    shots = []
    bims = []
    maps = Map1(800,600)
    #maps = Map1()
    items = []
    boss = Boss()
    score = 0
    font = load_font('Typo_CrayonM.TTF')

def fire():
    global shots
    shots.append(Shot(hero.x + 10,hero.y))
def fire2():
    global bims
    bims.append(Bim(hero.x + 10,hero.y))
def exit():
    global hero, stone, mon01, mon02, mon03, mon04, maps, font


    del(hero)
    del(stone)
    del(mon01)
    del(mon02)
    del(mon03)
    del(mon04)
    del(maps)
    del(font)


def pause():
    font.draw(250, 300, 'HOLD: PRESS H KEY TO RESUME')
    update_canvas()

def collide(a, b):
    left_a, bottom_a, right_a, top_a = a.get_bb()
    left_b, bottom_b, right_b, top_b = b.get_bb()

    if left_a > right_b: return False
    if right_a < left_b: return False
    if top_a < bottom_b: return False
    if bottom_a > top_b: return False

    return True

def resume():
    pass


def handle_events(frame_time):
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type==SDL_KEYDOWN and event.key==SDLK_ESCAPE:
            game_framework.change_state(title_state)
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_h):
            game_framework.push_state(hold_state)
        elif(event.type, event.key) == (SDL_KEYDOWN, SDLK_SPACE):
            hero.handle_event(event) #or ( fire() and fire2() )
            if shot_type.shot == False:
                if shot_type.bim == False:
                        fire()
            if shot_type.shot == False:
                if shot_type.bim == True:
                        fire2()


        else:
            hero.handle_event(event) or maps.handle_event(event)






def update(frame_time):
    global hero,Mon1,Mon2,shot,maps,Mon3,score,boss
    #maps.update(frame_time)
    maps.update(frame_time)
    hero.update(frame_time)
    boss.update()

    for Mon1 in mon01:
        Mon1.update(frame_time)
        if collide(hero, Mon1):
            print("player Life: %d" % hero.hp)
            hero.hp -=1
    for Mon2 in mon02:
        Mon2.update(frame_time)
        if collide(hero, Mon2):
            print("player Life: %d" % hero.hp)
            hero.hp -=2
    for Mon3 in mon03:
        Mon3.update(frame_time)
        if collide(hero, Mon3):
            print("player Life: %d" % hero.hp)
            hero.hp -=3
    for Mon4 in mon04:
        Mon4.update(frame_time)
        if collide(hero, Mon4):
            print("player Life: %d" % hero.hp)
            hero.hp -=5

    for Mon1 in mon01:
        Mon1.update(frame_time)
        for shot in shots:
            if collide(Mon1, shot):
                Mon1.hp -= 1;
                shots.remove(shot)
        if Mon1.hp<=0:
            if random.randint(0,2)==0:
                items.append(Item(Mon1.x,Mon1.y))
            mon01.remove(Mon1)
            score+=50
    for Mon2 in mon02:
        Mon2.update(frame_time)
        for shot in shots:
            if collide(Mon2, shot):
                Mon2.hp -= 1;
                shots.remove(shot)
        if Mon2.hp<=0:
            if random.randint(0,2)==0:
                items.append(Item(Mon2.x,Mon2.y))
            mon02.remove(Mon2)
            score+=100
    for Mon3 in mon03:
        Mon3.update(frame_time)
        for shot in shots:
            if collide(Mon3, shot):
                Mon3.hp -= 1;
                shots.remove(shot)
        if Mon3.hp<=0:
            if random.randint(0,2)==0:
                items.append(Item(Mon3.x,Mon3.y))
            mon03.remove(Mon3)
            score+=150
    for Mon4 in mon04:
        Mon4.update(frame_time)
        for shot in shots:
            if collide(Mon4, shot):
                Mon4.hp -= 1;
                shots.remove(shot)
        if Mon4.hp<=0:
            if random.randint(0,2)==0:
                items.append(Item(Mon4.x,Mon4.y))
            mon04.remove(Mon4)
            score+=200

    for Mon1 in mon01:
        Mon1.update(frame_time)
        for bim in bims:
            if collide(Mon1, bim):
                Mon1.hp -= 3;
                bims.remove(bim)
        if Mon1.hp<=0:
            if random.randint(0,2)==0:
                items.append(Item(Mon1.x,Mon1.y))
            mon01.remove(Mon1)
            score+=50
    for Mon2 in mon02:
        Mon2.update(frame_time)
        for bim in bims:
            if collide(Mon2, bim):
                Mon2.hp -= 3;
                bims.remove(bim)
        if Mon2.hp<=0:
            if random.randint(0,2)==0:
                items.append(Item(Mon2.x,Mon2.y))
            mon02.remove(Mon2)
            score+=100
    for Mon3 in mon03:
        Mon3.update(frame_time)
        for bim in bims:
            if collide(Mon3, bim):
                Mon3.hp -= 3;
                bims.remove(bim)
        if Mon3.hp<=0:
            if random.randint(0,2)==0:
                items.append(Item(Mon3.x,Mon3.y))
            mon03.remove(Mon3)
            score+=150

    for Mon4 in mon04:
        Mon4.update(frame_time)
        for bim in bims:
            if collide(Mon4, bim):
                Mon4.hp -= 3;
                bims.remove(bim)
        if Mon4.hp<=0:
            if random.randint(0,2)==0:
                items.append(Item(Mon4.x,Mon4.y))
            mon04.remove(Mon4)
            score+=200


    for item in items:
            if collide(hero,item):
                if item.item_num<2:
                    boss.hp-=5
                elif item.item_num==2:
                    boss.hp-=10
                    #if boss.hp<=0:
                     #   boss.remove(Boss)
                elif item.item_num==3:
                     shot_type.bim = True
                     shot_type.shot = False
                else:
                    hero.hp+=5
                items.remove(item)
                hero.eat(item)






    #for shot in shots:
            #shot.update(frame_time)
           # if shot.x>1000:
           #     shots.remove(shot)

            #else:
             #   item.update(frame_time)


#    for Mon3 in mon03:
#        Mon3.update(frame_time)
#        for shot in shots:
#            if collide(Mon3, shot):
#                mon03.remove(Mon3)
#                shots.remove(shot)

    if(hero.hp <= 0):
        game_framework.change_state(gameover_state)
    if (boss.hp<=0):
        game_framework.change_state(clear_state)


def draw(frame_time):
    global hero,stone, Mon1, Mon2, Mon3, Mon4, shot, item, hpbar, boss
    clear_canvas()
    maps.draw()
    stone.draw()
    hero.draw()
    hpbar.draw()
    boss.draw()
    #boss.draw()
    font.draw(90,567,'HP : %d'%(hero.hp))
    font.draw(90,523,'SCORE : %d'%(score))
    font.draw(650,567,'BOSS HP : %d'%(boss.hp))

    for Mon1 in mon01:
        Mon1.draw()
    for Mon2 in mon02:
        Mon2.draw()
    for Mon3 in mon03:
        Mon3.draw()
    for Mon4 in mon04:
        Mon4.draw()
    for shot in shots:
        shot.draw()
    for item in items:
        item.draw()
    for bim in bims:
        bim.draw()




    update_canvas()


    delay(0.05)




