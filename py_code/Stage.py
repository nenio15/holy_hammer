import numpy as np
import random

class Stage:
    def __init__(self, index):
        if index == 1:
            self.zomCnt = 20
            self.ghoCnt = 5
        else:
            self.zomCnt = 45
            self.ghoCnt = 15
        self.position = np.array([120, 120])

    # 대충.. time을 따로 해서, zom 나오는 수 조정, gho 나오는 수 조정
    def callZombie(self, cnt):
        self.position[0] = rand