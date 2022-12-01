import numpy as np
import random
from time import time
from Enemy import Enemy

class Stage:
    def __init__(self, index):
        self.setTime = time()
        print(self.setTime)
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

    def startStage(self, enemy_list):
        self.callZombie(enemy_list, (int)(self.zomCnt / 2))


    # 대충.. time을 따로 해서, zom 나오는 수 조정, gho 나오는 수 조정
    def callZombie(self, enemy_list, cnt):
        for i in range(cnt):
            enemy = Enemy('zombie', (random.randint(-32, 272), random.randint(-32, 272)))
            enemy_list.extend([enemy])
            