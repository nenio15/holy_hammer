import numpy as np
from time import time, sleep

class Character:
    def __init__(self, width, height):
        self.appearance = '../res/char_right.png'
        self.name = 'midory'
        self.state = 'normal'
        self.speed = 6
        self.size = 32 # half_size
        self.position = np.array([(int)(width/2 - self.size), (int)(height/2 - self.size)])
        self.center = np.array([(self.position[0] + self.size), (self.position[1] + self.size)])
        self.outline = '#FFFFFF'
        self.direction = 'right'
        self.delay = -3
        

    def move(self, command = None):
        if command['move'] == False:
            self.state = None
            # self.outline = '#FFFFFF' #검정색상 코드!
        
        elif time() > self.delay + 3 : # 후딜 3초 후.. 왜 이거 무거워 보이지..
            self.state = 'move'
            # self.outline = "#FF0000" #빨강색상 코드!

            if command['up_pressed']:
                self.position[1] -= self.speed
                self.appearance = '../res/64_char_up.png'
                self.direction = 'up'

            if command['down_pressed']:
                self.position[1] += self.speed
                self.appearance = '../res/64_char_down.png'
                self.direction = 'down'

            if command['left_pressed']:
                self.position[0] -= self.speed
                self.appearance = '../res/char_left.png'
                self.direction = 'left'
                
            if command['right_pressed']:
                self.position[0] += self.speed
                self.appearance = '../res/char_right.png'
                self.direction = 'right'

            #center update
            self.center = np.array([(int)(self.position[0] + self.size), (int)(self.position[1] + self.size)])

    def action(self):   # direction은 언제나 방향성을 유지한다.
        self.state = 'punch'    # 이걸로..?
        if self.direction == 'up':
            self.appearance = '../res/char_attack_up.png'
            sleep(3)    # 캐릭터만 잘까요? 프로그램이 잘까요?
            print("action delay...")
        elif self.direction == 'down':
            self.appearance = '../res/char_attack_down.png'
        elif self.direction == 'left':
            self.appearance = '../res/char_attack_left.png'
        elif self.direction == 'right':
            self.appearance = '../res/char_attack_right.png'
