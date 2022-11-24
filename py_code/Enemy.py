import numpy as np
from PIL import Image

class Enemy:
    def __init__(self, type, spawn_position):
        self.shape = Image.open('../simple_zombie.png')
        self.size = 32
        self.name = type
        if type == 'ghost':
            self.shape = Image.open('../res/simple_ghost.png')
            self.size = 28

        self.state = 'alive'
        self.speed = 1
        self.position = np.array([(spawn_position[0] - 16), (spawn_position[1] - 16)])
        self.center = np.array([(self.position[0] + 16), (self.position[1] + 16)])
        self.outline = '#FFFFFF'
        

    def move(self, char_center):
        if(self.center[0] < char_center[0]):
            self.position[0] += self.speed

        elif(self.center[0] > char_center[0]):
            self.position[0] -= self.speed
            # print(self.position[0])

        if(self.center[1] < char_center[1]):
            self.position[1] += self.speed

        elif(self.center[1] > char_center[1]):
            self.position[1] -= self.speed

        self.center = np.array([(self.position[0] + 16), (self.position[1] + 16)])

    def collision_check(self, character):   # obj도 추가할 것
        collision = self.overlapCharacter(self.center, character)

        if collision == 'hit':
            print("character hit!!")

    def overlapCharacter(self, ego_center, c):
        # 캐릭터와의 거리 -> 캐릭터의 액션 상태(punch, run) -> 그리고 반환값 여럿
        # 아닌데.. 캐릭터가 공격한 상태에서는 새로운 충돌판정을 물어야해
        # 새 충돌에서 방향받아서, 그 방향의 망치 범위일때가 필요한 거야.

        if c.status == 'punch': # 
            if c.diretion == 'up':
                if abs(ego_center[0] - c.center[0]) < (64 + 32) and abs(ego_center[1] - c.center[1]) < (64 + 32):
                    return

        if abs(ego_center[0] - c.center[0]) < (64 + 32) and abs(ego_center[1] - c.center[1]) < (64 + 32):
            return 'hit'
