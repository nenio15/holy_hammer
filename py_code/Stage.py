import numpy as np
import random
from time import time
from Enemy import Enemy
from Block import Block

class Stage:
    def __init__(self, index):
        self.setTime = time()
        self.stage = 1
        self.step = -1
        self.stage_list = [5, 10, 11, 23] #이걸로 숫자 조정하자..
        # index는 이거 아니야...
        if index == 1:
            self.zomCnt = 10
            self.ghoCnt = 5
        else:
            self.zomCnt = 45
            self.ghoCnt = 15
        # self.position = np.array([120, 120])

    # 스테이지를 바꾸는 애니메이션도 있어야죠..? ( 언제 호출할지는 main의 함수를 따로 둘겁니다만..)
    def showStage(self, blocks):
        if self.stage == 1 and self.step == -1:
            block_list = [Block(50, 50, '32'), Block(30, 30, '32')]
            
            print('stage 1 start!!')
            return block_list
        return blocks

    # 항상 main에서 갱신. 여기서 showStage할것.?
    def startStage(self, enemy_list):
        progress = time() - self.setTime
        # step을 index, progress를 원소로 지녀서 관리..?(stage_list처럼)
        if self.step == -1 and progress > 0:
            self.step += 1

        if self.step == 0 and progress > 3 :
            print('call...1')
            self.callZombie(enemy_list, self.stage_list[self.step])
            self.step += 1
        elif self.step == 1 and progress > 30:
            print('going more..2')
            self.callZombie(enemy_list, self.stage_list[self.step])
            self.step += 1


    # 대충.. time을 따로 해서, zom 나오는 수 조정, gho 나오는 수 조정
    def callZombie(self, enemy_list, cnt):
        for i in range(cnt):
            # 맵 밖에서 소환..(다시 돌지를 않네..?)
            pos = np.array([random.randint(-32, 272), random.randint(-32, 272)])
            # if (pos[0] < 0 or pos[0] > 240) and (pos[1] < 0 or pos[1] > 240):
            # print('call zombie')
            enemy = Enemy('zombie', (random.randint(-32, 272), random.randint(-32, 272)))
            enemy_list.extend([enemy])
            # else:
            #    i -= 1
            #    print('reroll')
