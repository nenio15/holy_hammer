import numpy as np
from time import time

class Character:
    def __init__(self, width, height):
        self.appearance = '../res/char_right.png'
        self.name = 'midory'
        self.state = 'normal'
        self.power = 1
        self.speed = 3
        self.highspeed = 6
        self.size = 16 # half_size
        self.position = np.array([(int)(width/2 - self.size), (int)(height/2 - self.size)])
        self.center = np.array([(self.position[0] + self.size), (self.position[1] + self.size)])
        self.direction = 'right'
        self.delay = -3
        self.damageDelay = -3
        self.rolling = -3
        self.life = 5
        self.score = 0
        self.pushB = 0  # 이거 초기화 어디가서함?
        self.effect = 0
        self.invisibe = 0
        self.hitted = 0
        # self.item = 0

    def checkManager(self, command = None):
        checkTime = time()

        # 피격 판정
        if checkTime > self.damageDelay + 2:
            if self.state == 'damaged':
                # 여기서 다친거, 다치면 밀리거나, 캐릭터가 껌벅껌벅 거리거나 해야하는데, 그건 문제가..
                # 이펙트 처리..
                # get ani(damaged)
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
        
    def special(self, index): # 1:power 2:speed 3:heart 4:invisibility
        if self.effect == 0: # 지닌 아이템이 있는 경우 초기화
            self.power = 1
            self.speed = 3
            self.highspeed = 6
            self.invisibe = 0

        if time() > self.effect: # 처음 세팅
            self.effect = time()
            if index == 1:      # power
                self.power = 2
            elif index == 2:    # speed
                self.speed = 5
                self.highspeed = 8
            elif index == 3:    # heart
                if self.life < 5:
                    self.life += 1
            elif index == 4:    # invisibility
                self.invisibe = 1
        
        elif time() < self.effect + 15: # 지속 시간 동안, 효과 보이기
        
            pass    # 각 버프 이펙트 추가..

        elif time() > self.effect + 15: # 효과 종료
            if index == 1:
                self.power = 1
            elif index == 2:
                self.speed = 3  # back
            elif index == 4:
                self.invisibe = 0
                
        return ('yes', self.effect) # 이펙트 네임. 그리고 효과시작시간 반환?