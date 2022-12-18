import numpy as np
import random
from time import time
from PIL import Image
from Enemy import Enemy
from Block import Block

class Stage:
    def __init__(self, index = 0):
        self.setTime = time()
        self.clearTime = 0
        self.stage = index
        self.step = -1
        self.background = Image.open('../res/background/background_0.png')

        # 한 번에 50마리는 무리. 30마리가 최대?
        if index == 1:
            self.stage_zombie = [5, 10, 8, 10]
            self.stage_ghost = [1, 2, 0, 4]
            #self.background = Image.open('../res/background/background_1.png')  # 초기 정의 필요
        elif index == 2:
            self.stage_zombie = [4, 8, 4, 5]
            self.stage_ghost = [2, 6, 8, 1]
            #self.background = Image.open('../res/background/background_2.png')
        else:
            self.stage_zombie = [4, 8, 6, 6]
            self.stage_ghost = [0, 2, 4, 4]
            #self.background = Image.open('../res/background/background_3.png')

    def showStage(self):

        if self.stage == 0:
            self.background = Image.open('../res/background/background_0.png')
            block_list = [(0,0)]
        elif self.stage == 1:
            self.background = Image.open('../res/background/background_1.png')
            block_list = [(60, 30), (30, 60), (60, 60),
                    (150, 30), (180, 60), (150, 60),
                    (30, 150), (60, 180), (60, 150),
                    (180, 150), (150, 180), (150, 150)]
        elif self.stage == 2:
            self.background = Image.open('../res/background/background_2.png')
            block_list = [(30, 30), (60, 30), (90, 30),
                        (150, 60), (180, 60), (210, 60),
                        (0, 150), (30, 150), (60, 150),
                        (120, 180), (150, 180), (180, 180)]
        else:
            self.background = Image.open('../res/background/background_3.png')
            block_list = [(60, 30), (90, 30), (120, 30),
                        (180, 60), (180, 90), (180, 120),
                        (30, 90), (30, 120), (30, 150),
                        (90 ,180), (120, 180), (150, 180)]

        return block_list

    # 항상 main에서 갱신
    def startStage(self, enemy_list, char_pos):
        progress = time() - self.setTime
        # step을 index, progress를 원소로 관리(stage_list처럼)
        if self.step == -1 and progress < 5:            
            return self.stage
        elif self.step == -1:     # title 넘기기
            self.step += 1
            return -1
        elif self.step == 0 and progress > 5 :
            print('call...1')
            self.callEnemy(char_pos, enemy_list, self.stage_zombie[self.step])
            self.callEnemy(char_pos, enemy_list, self.stage_ghost[self.step], 'ghost')
            self.step += 1
            if self.stage == 3:     # summon boss
                enemy = Enemy('boss', (120, 80))
                enemy_list.extend([enemy])
        elif self.step == 1 and progress > 15:
            print('going more..2')
            self.callEnemy(char_pos, enemy_list, self.stage_zombie[self.step])
            self.callEnemy(char_pos, enemy_list, self.stage_ghost[self.step], 'ghost')
            self.step += 1
        elif self.step == 2 and progress > 20:
            print('getter..3')
            self.callEnemy(char_pos, enemy_list, self.stage_zombie[self.step])
            self.callEnemy(char_pos, enemy_list, self.stage_ghost[self.step], 'ghost')
            self.step += 1
        elif self.step == 3 and progress > 30:
            print('final..4')
            self.callEnemy(char_pos, enemy_list, self.stage_zombie[self.step])
            self.callEnemy(char_pos, enemy_list, self.stage_ghost[self.step], 'ghost')
            self.step += 1
        elif self.step == 4 and progress > 30:
            # 적이 전부 죽어야 다음 스테이지로 이동
            if len(enemy_list) < 1:
                print('zero end')
                self.stage += 1
                self.step += 1
                self.clearTime = time()
        elif self.step == 5:
            #print('go')
            if time() - self.clearTime > 5:
                self.setTime = time()
                #print('next stage')
                self.step = -1
                self.clearTime = 0
                if self.stage > 3:
                    self.stage = 4
                    self.step = 5
                    #print('all complete')
                
            return 10

        return 0

    # zom, gho 나오는 수 조정(시간에 따라서)
    def callEnemy(self, char_pos, enemy_list, cnt = 0, name = 'zombie'):
        for i in range(cnt):
            pos = np.array([random.randint(-32, 272), random.randint(-32, 272)])
            center = np.array([(pos[0] - char_pos[0]), (pos[1] - char_pos[1])])

            # 캐릭터와 겹치지 않게끔 소환
            if -16 < center[0] < 16 and -16 < center[1] < 16:
                if center[0] > 0:
                    pos[0] += 45
                else:
                    pos[0] -= 45
                if center[1] > 0:
                    pos[1] += 45
                else:
                    pos[1] -= 45
                
            enemy = Enemy(name, pos)
            enemy_list.extend([enemy])
            

class Item:
    def __init__(self, x, y, index):
        self.position = np.array([x, y])
        self.center = np.array([x + 8, y + 8])
        self.number = index # 1:power 2:speed 3:heart 4:invincibility
        self.state = 'field'
        if index == 1:
            self.shape = Image.open('../res/item/item_p.png')
        elif index == 2:
            self.shape = Image.open('../res/item/item_s.png')
        elif index == 3:
            self.shape = Image.open('../res/item/item_h.png')
        elif index == 4:
            self.shape = Image.open('../res/item/item_i.png')

    def getItem(self, char):    # 아이템 먹는 판정
        if abs(char.center[0] - self.center[0]) < 10:
            if abs(char.center[1] - self.center[1]) < 10:
                char.special(self.number)
                self.state = 'get'
