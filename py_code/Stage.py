import numpy as np
import random
from time import time
from Enemy import Enemy

class Stage:
    def __init__(self, index):
        self.setTime = time()
        if index == 1:
            self.zomCnt = 20
            self.ghoCnt = 5
        else:
            self.zomCnt = 45
            self.ghoCnt = 15
        # self.position = np.array([120, 120])

    def showStage(self, time):
        if time() <= time + 3:
            time = 0    #draw를 하고 싶긴한디... 복잡해지네

    # 대충.. time을 따로 해서, zom 나오는 수 조정, gho 나오는 수 조정
    def callZombie(self, enemy_list, cnt):
        for i in cnt:
            enemy = Enemy('zombie', (random.randint(-32, 272), random.randint(-32, 272)))
            enemy_list.append = enemy
            