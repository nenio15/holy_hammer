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
        # 한 번에 50마리는 무리. 30마리가 최대?
        self.stage_list = [5, 10, 11, 23] #이걸로 숫자 조정하자.. #2차원배열이어야..? 아니면 스테이지 바뀌면 거시기
        self.stage_ghost = [1, 2, 0, 0]

        if index == 1:
            self.stage_zombie = [5, 10, 11, 23]
            self.stage_ghost = [1, 2, 0, 0]
            self.background = Image.open('../res/background/background_1.png')
        else:
            self.stage_zombie = [4, 8, 4, 0]
            self.stage_ghost = [2, 6, 8, 0]
            self.background = Image.open('../res/background/background_2.png')

    # 스테이지를 바꾸는 애니메이션도 있어야죠..? ( 언제 호출할지는 main의 함수를 따로 둘겁니다만..)
    def showStage(self):
        if self.stage == 1:
            # 배경그림으로 만들것.
            # + x,y좌표가 center가 아닐수도 있음에 주의
            block_list = [Block(60, 30, '32'), Block(30, 60, '32'), Block(60, 60, '32'),
                    Block(150, 30, '32'), Block(180, 60, '32'), Block(150, 60, '32'),
                    Block(30, 150, '32'), Block(60, 180, '32'), Block(60, 150, '32'),
                    Block(180, 150, '32'), Block(150, 180, '32'), Block(150, 150, '32')]
            
        elif self.stage == 2:
            block_list = [Block(30, 30, '32'), Block(60, 30, '32'), Block(90, 30, '32'),
                    Block(150, 60, '32'), Block(180, 60, '32'), Block(210, 60, '32'),
                    Block(0, 150, '32'), Block(30, 150, '32'), Block(60, 150, '32'),
                    Block(120, 180, '32'), Block(150, 180, '32'), Block(180, 180, '32')]

        return block_list

    # 항상 main에서 갱신
    def startStage(self, enemy_list):
        progress = time() - self.setTime
        # step을 index, progress를 원소로 지녀서 관리..?(stage_list처럼)
        if self.step == -1 and progress < 5:            
            return self.stage     # 기본값은..?
        elif self.step == -1:     # title 넘기기
            self.step += 1
        elif self.step == 0 and progress > 5 :
            print('call...1')
            self.callZombie(enemy_list, self.stage_zombie[self.step])
            self.callGhost(enemy_list, self.stage_ghost[self.step])
            self.step += 1
        elif self.step == 1 and progress > 15:
            print('going more..2')
            self.callZombie(enemy_list, self.stage_zombie[self.step])
            self.callGhost(enemy_list, self.stage_ghost[self.step])
            self.step += 1
        elif self.step == 2 and progress > 20:
            # 적이 전부 죽어야 다음 스테이지로..
            if len(enemy_list) < 1:
                print('zero end')
                self.stage += 1
                self.step += 1
                self.clearTime = time()
        elif self.step == 3:
            print('go')
            if time() - self.clearTime > 5:
                self.background = Image.open('../res/background/background_2.png')
                print('next stage')
                self.step = -1
                self.clearTime = 0
                print(self.stage)

            return 10

        return False

    # 대충.. time을 따로 해서, zom 나오는 수 조정, gho 나오는 수 조정
    def callZombie(self, enemy_list, cnt):
        for i in range(cnt):
            # 맵 밖에서 소환..(구현 필요..) 대충 for로 ??
            pos = np.array([random.randint(-32, 272), random.randint(-32, 272)])
            # if (pos[0] < 0 or pos[0] > 240) and (pos[1] < 0 or pos[1] > 240):
            enemy = Enemy('zombie', (random.randint(-32, 272), random.randint(-32, 272)))
            enemy_list.extend([enemy])
            # else:
            #    i -= 1
            #    print('reroll')

    def callGhost(self, enemy_list, cnt):
        for i in range(cnt):
            pos = np.array([random.randint(-32, 272), random.randint(-32, 272)])
            enemy = Enemy('ghost', (random.randint(-32, 272), random.randint(-32, 272)))
            enemy_list.extend([enemy])
            

class Item:
    def __init__(self, x, y, index):
        self.position = np.array([x, y])
        self.center = np.array([x - 8, y - 8])
        self.number = index # 1:power 2:speed 3:heart 4:invincibility
        self.state = 'field'
        # self.delay = 0  # 무슨 용도더라..
        if index == 1:
            self.shape = Image.open('../res/item/item_p.png')
        elif index == 2:
            self.shape = Image.open('../res/item/item_s.png')
        elif index == 3:
            self.shape = Image.open('../res/item/item_h.png')
        elif index == 4:
            self.shape = Image.open('../res/item/item_i.png')

    def getItem(self, char):
        if abs(char.center[0] - self.center[0]) < 10:
            if abs(char.center[1] - self.center[1]) < 10:
                char.effect = time()
                char.special(self.number)
                self.state = 'get'
