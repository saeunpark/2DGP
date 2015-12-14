import json

from pico2d import *


import game_framework
import title_state

name = "RankingState"
image = None
font = None

def enter():
    global image, font

    image = load_image('./resource/blackboard.png')
    font = load_font('./resource/Typo_CrayonM.TTF', 30)


def exit():
    global image, font
    del(image)
    del(font)

def update(frame_time):
    pass


def get_key(item):
    return item['time']

def draw_score():
    with open('score.txt', 'r') as f:
        score_list = json.load(f)
    score_list.sort(key=get_key, reverse=True)
    top10 = score_list[:10]
    font.draw(300, 500, '[RANKING]', (255,255,255))
    for i, record in enumerate(top10):
        font.draw(100, 450 - i * 40, '#%2d (Time:%4.1f, x:%3d, y:%3d)' % (i+1,record['time'],record['x'],record['y']), (255,255,255))


def draw(frame_time):
    global image
    clear_canvas()
    image.draw(400, 300)
    draw_score()
    update_canvas()

def handle_events(frame_time):
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        else:
            if (event.type, event.key) == (SDL_KEYDOWN, SDLK_ESCAPE):
                game_framework.change_state(title_state)


def pause(): pass
def resume(): pass
