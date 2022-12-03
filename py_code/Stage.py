import numpy as np
import random
from time import time
from Enemy import Enemy

class Stage:
    def __init__(self, index):
        self.setTime = time()
        self.step = 0
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
    def showStage(self, time):

        if time() <= time + 3:
            time = 0    #draw를 하고 싶긴한디... 복잡해지네

    # 항상 main에서 갱신. 여기서 showStage할것.?
    # 스테이지 변경은... enemy가 얼만큼 남았느냐의 문제거든요?
    # 1. enemy_cnt를 따로 취급(이 경우, enemy.class에서 따로 변수 --)
    # 2. enemy_list가 empty인지의 여부 확인(해당 스테이지의 몬스터 전부 나오고서..)
    def startStage(self, enemy_list):
        progress = time() - self.setTime

        if self.step == 0 and progress < 10 :
            print('start 1')
            self.callZombie(enemy_list, self.stage_list[self.step])
            self.step += 1
        elif self.step == 1 and progress < 30:
            print('going more..2')
            self.callZombie(enemy_list, self.stage_list[self.step])
            self.step += 1



    # 대충.. time을 따로 해서, zom 나오는 수 조정, gho 나오는 수 조정
    def callZombie(self, enemy_list, cnt):
        for i in range(cnt):
            # 맵 밖에서 소환..
            pos = np.array([random.randint(-32, 272), random.randint(-32, 272)])
            if (pos[0] < 0 or pos[0] > 240) and (pos[1] < 0 or pos[1] > 240):
                enemy = Enemy('zombie', (random.randint(-32, 272), random.randint(-32, 272)))
                enemy_list.extend([enemy])
            else:
                i -= 1
