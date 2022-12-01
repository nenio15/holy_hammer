import numpy as np
from time import time

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
        self.rolling = -3
        self.life = 3
        self.score = 0


    def move(self, command = None):
        if self.state == 'damaged':
            # 여기서 다친거, 다치면 밀리거나, 캐릭터가 껌벅껌벅 거리거나 해야하는데, 그건 문제가..
            # self.delay = 3
            self.life -= 1
            self.score -= 100

        if time() > self.delay + 0.3: # 액션끝나도 아무것도 안 하면 돌아와야지
            self.state = 'normal'
            self.appearance = '../res/64_char_' + self.direction + ".png"

        if command['move'] == False:
            self.state = 'normal'
        
        else: # 여기 뭐 있었는지 아시는분~
            self.state = 'move'

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
        elif self.direction == 'down':
            self.appearance = '../res/char_attack_down.png'
        elif self.direction == 'left':
            self.appearance = '../res/char_attack_left.png'
        elif self.direction == 'right':
            self.appearance = '../res/char_attack_right.png'

    def dodge(self, command):
        if time() > self.rolling + 1:
            self.state = 'dodge'
            self.speed = 20 # 일단 올려놨는데,,, 프레임이 짧지않음?
            print("dodge!!")
            self.move(command)

            self.state = 'normal'
            self.speed = 6
            print("come back")