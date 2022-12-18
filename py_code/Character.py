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
        self.delay = -3         # 공격 후딜
        self.damageDelay = -3   # 피격 후딜
        self.life = 5
        self.score = 0
        self.effect = 0
        self.invincible = 0
        self.hitted = 0

    def checkManager(self, command = None):
        checkTime = time()

        # 피격 판정
        if checkTime > self.damageDelay + 4: # 4초 딜레이
            if self.state == 'damaged':
                self.state = 'normal'
                self.hitted = 1
                self.life -= 1
                self.score -= 100
                self.damageDelay = checkTime
            else:
                self.hitted = 0 #..?
        
        # 공격
        if command['punch']:
            self.action()

        # 달리기        
        if command['dash']:
            self.dash()
        else:
            self.speed = self.highspeed - 3

        self.move(checkTime, command)
        
    def move(self, curTime, command = None):
        if command['move'] == False:
            if curTime > self.delay + 0.3: # 액션끝나도 아무것도 안 하면 돌아와야지
                self.state = 'normal'
                self.appearance = '../res/char_' + self.direction + ".png"
                
        elif curTime > self.delay + 0.3:
            self.state = 'move'

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
        self.state = 'punch'
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

    # 사용하지 않음 (애니 넣는게 좋은데, 없음)
    def dodge(self, command):   # 폐기
        self.state = 'dodge'
        self.speed = 20
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