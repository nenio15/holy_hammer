import numpy as np
import random
from Enemy import Enemy

class Stage:
    def __init__(self, index):
        if index == 1:
            self.zomCnt = 20
            self.ghoCnt = 5
        else:
            self.zomCnt = 45
            self.ghoCnt = 15
        # self.position = np.array([120, 120])

    # 대충.. time을 따로 해서, zom 나오는 수 조정, gho 나오는 수 조정
    def callZombie(self, enemy_list, cnt):
        for i in cnt:
            enemy = Enemy('zombie', (random.randint(-32, 272), random.randint(-32, 272)))
            enemy_list.append = enemy
            