import numpy as np
from time import time

class Character:
    def __init__(self, width, height):
        self.appearance = '../res/char_right.png'
        self.eshape = '../res/item/effect_p.png'
        self.name = 'midory'
        self.state = 'normal'
        self.power = 1  # info = (1, 3, 6) ? .... change?
        self.speed = 3
        self.highspeed = 6
        self.size = 16 # half_size
        self.position = np.array([(int)(width/2 - self.size), (int)(height/2 - self.size)])
        self.center = np.array([(self.position[0] + self.size), (self.position[1] + self.size)])
        self.direction = 'right'
        self.delay = -3 # 폐기..?
        self.damageDelay = -3
        self.rolling = -3 # 폐기
        self.life = 5
        self.score = 0
        self.pushB = 0  # 폐기될 데이터
        self.effect = 0
        self.invincible = 0
        self.hitted = 0
        # self.item = 0

    def checkManager(self, command = None):
        checkTime = time()

        # 피격 판정
        if checkTime > self.damageDelay + 4: # 4초 딜레이
            if self.state == 'damaged':
                # 다치면.. 공격판정이 이상해진다. 캐릭터 문제거나, 좀비쪽 문제
                self.state = 'normal'
                self.hitted = 1
                self.life -= 1
                self.score -= 100
                self.damageDelay = checkTime
            else:
                self.hitted = 0 #..?
        
        # 공격
        if command['punch']:    # 이거 다음에 move시켜도 됨?(어차피 필요없기도 한데... 흠...)
            self.action()

        # 달리기        
        if command['dash']:
            self.dash()

        self.move(checkTime, command)
        

    def move(self, curTime, command = None): # move가 아니라,, 체크인데?

        if command['move'] == False:
            if curTime > self.delay + 0.3: # 액션끝나도 아무것도 안 하면 돌아와야지
                self.state = 'normal'
                self.appearance = '../res/char_' + self.direction + ".png"

        elif curTime > self.delay + 0.3: # 여기 뭐 있었는지 아시는분~
            # self.state = 'move'

            if command['up_pressed']:
                self.position[1] -= self.speed
                self.appearance = '../res/char_up.png'
                self.direction = 'up'

            if command['down_pressed']:
                self.position[1] += self.speed
                self.appearance = '../res/char_down.png'
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


    def action(self):
        self.state = 'punch'    # 이걸로..?
        #print(self.direction)
        if self.direction == 'up':
            self.appearance = '../res/char_up_punch.png'
        elif self.direction == 'down':
            self.appearance = '../res/char_down_punch.png'
        elif self.direction == 'left':
            self.appearance = '../res/char_left_punch.png'
        elif self.direction == 'right':
            self.appearance = '../res/char_right_punch.png'

    def dash(self):
        self.speed = self.highspeed
        #self.state = 'dash'
        #self.pushB += 1

    def dodge(self, command):   # 폐기
        self.state = 'dodge'
        self.speed = 20 # 일단 올려놨는데,,, 프레임이 짧지않음?
        # 프레임으로 할당할거면, 달리, 대충 여기다가 애니하나 넣어야..
        self.move(command)
        self.state = 'normal'
        
    def special(self, index = 0): # 1:power 2:speed 3:heart 4:invincibility
        if index != 0 and self.effect != 0: # 새 아이템 get시
            print('change')
            self.power = 1
            self.speed = 3
            self.highspeed = 6
            self.invincible = 0
            self.effect = 0

        if index != 0 and self.effect == 0: # 처음 세팅
            #print('setting')
            self.effect = time()
            if index == 1:      # power
                self.power = 2
                self.eshape = '../res/item/effect_p.png'
            elif index == 2:    # speed
                self.speed = 5
                self.highspeed = 8
                self.eshape = '../res/item/effect_s.png'
            elif index == 3:    # heart
                if self.life < 5:
                    self.life += 1
                    self.effect -= 8 # 2초후 이펙트 종료
                    self.eshape = '../res/item/effect_h.png'
                else:
                    self.effect = 0
            elif index == 4:    # invincibility
                self.invincible = 1
                self.eshape = '../res/item/effect_i.png'
        
        elif self.effect != 0 and time() > self.effect + 10: # 효과 종료
            print('effect end')
            self.power = 1
            self.speed = 3
            self.highspeed = 6
            self.invincible = 0
            self.effect = 0