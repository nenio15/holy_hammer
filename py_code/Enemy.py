import numpy as np
from PIL import Image

class Enemy:
    def __init__(self, typee, spawn_position):
        self.shape = Image.open('../res/simple_zombie.png')
        self.size = 32
        self.width = 16
        self.name = typee
        self.speed = 1
        self.hit = 0
        if typee == 'ghost':    # 변칙적이진 않다만, 플레이어 속도를 쫓아온다는 위협성..
            self.shape = Image.open('../res/simple_ghost.png')
            self.size = 20
            self.speed = 1      # 3으로 할거면 달리기가 필요..

        self.state = 'alive'
        
        self.position = np.array([(spawn_position[0] - 16), (spawn_position[1] - 16)])
        self.center = np.array([(self.position[0] + 16), (self.position[1] + 16)])
        self.outline = '#FFFFFF'
        
    # 얘는 거리 비례에서 speed를 약간 조절할까요..? ex) speed / (distance)
    def move(self, char_center):
        # 3 > speed: speed += 0.1 (점점 되돌아오기...)

        if(self.center[0] < char_center[0]):
            self.position[0] += self.speed

        elif(self.center[0] > char_center[0]):
            self.position[0] -= self.speed
            # print(self.position[0])

        if(self.center[1] < char_center[1] + 10):
            self.position[1] += self.speed

        elif(self.center[1] > char_center[1] + 10):
            self.position[1] -= self.speed

        self.center = np.array([(self.position[0] + 16), (self.position[1] + 16)])

    def collision_check(self, character):   # obj도 추가할 것
        
        collision = self.overlapCharacter(self.center, character)

        if collision == 'hit':
            character.state = 'damaged' #여기서 함수를 호출해도 되는데 그건 조금?
# 이동의 변칙성.. 속도 차이. 직선, 지그재그 등의 변칙성
            # print("character hit!!")
        if collision == 'damaged':
            self.hit += 1
            if self.hit > 1:
                self.state = 'dead'
                # 시체는 없을거야. 근데 뿅하고 사라지겠네
                if self.size == 32: 
                    character.score += 100
                if self.size == 20:
                    character.score += 50

    def overlapCharacter(self, ego_center, c):
        # 캐릭터와의 거리 -> 캐릭터의 액션 상태(punch, run) -> 그리고 반환값 여럿
        # 아닌데.. 캐릭터가 공격한 상태에서는 새로운 충돌판정을 물어야해
        # 새 충돌에서 방향받아서, 그 방향의 망치 범위일때가 필요한 거야
        center_col = np.array([abs(ego_center[0] - c.center[0]), abs(ego_center[1] - c.center[1])])
        
        # 맞는 것은 적. 충돌 판정은 후할지도..?
        if c.state == 'punch': # ddd
            if c.direction == 'up':
                if center_col[0] < self.width + 16 and center_col[1]< self.size:
                    return 'damaged'

            if c.direction == 'down':
                if center_col[0] < self.width + 16 and center_col[1] + 20 < self.size:
                    return 'damaged'
                    
            if c.direction == 'left':
                if center_col[0] - 10 < self.width + 16 and center_col[1] + 10 < self.size:
                    return 'damaged'
                    
            if c.direction == 'right':
                if center_col[0] + 10 < self.width + 16 and center_col[1] + 10 < self.size:
                    return 'damaged'

        # x좌표는 28, y좌표는 54 정도가 적정선? 지금의,
        if c.state != 'dodge': # 회피처리
            if center_col[0] < 28 and center_col[1] < 54:
                return 'hit'
        