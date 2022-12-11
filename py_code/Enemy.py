import numpy as np
import random
from PIL import Image

class Enemy:
    def __init__(self, typee, spawn_position):
        self.shape = Image.open('../res/simple_zombie_right.png')
        self.size = 16
        self.width = 16
        self.name = typee
        self.speed = 1
        self.hit = 0
        self.swing = random.randint(-4, 5)  # -5 ~ 5
        self.frame = 0

        if typee == 'ghost':    # 변칙적이진 않다만, 플레이어 속도를 쫓아온다는 위협성..
            self.shape = Image.open('../res/simple_ghost.png')
            self.size = 8
            self.speed = 2      # 3으로 할거면 달리기가 필요..

        self.state = 'alive'
        self.position = np.array([(spawn_position[0] - self.size), (spawn_position[1] - self.size)])
        self.center = np.array([(self.position[0] + self.size), (self.position[1] + self.size)])
        self.direction = 'right'
        
    def movSwing(self):
        if self.swing > 0:
            self.swing += 1
            if self.direction == 'right' or 'left':
                self.position[1] += 1
            else:
                self.position[0] += 1

            if self.swing > 4:
                self.swing = 0

        elif self.swing < 0:
            self.swing -= 1
            if self.direction == 'right' or 'left':
                self.position[1] -= 1
            else:
                self.position[0] -= 1

            if self.swing < -4:
                self.swing = 0
                
        else:
            self.swing = random.randint(-4, 5)


    # 얘는 거리 비례에서 speed를 약간 조절할까요..? ex) speed / (distance)
    def move(self, char_center):
        # 3 > speed: speed += 0.1 (점점 되돌아오기...)
        self.frame += 1
        if self.frame < 2 and self.name != 'ghost':
            return

        self.frame = 0

        if(self.center[1] < char_center[1]):
            self.position[1] += self.speed
            self.direction = 'down'

        elif(self.center[1] > char_center[1]):
            self.position[1] -= self.speed
            self.direction = 'up'

        if(self.center[0] < char_center[0]):
            self.position[0] += self.speed
            self.direction = 'right'
            if self.size == 16:
                self.shape = Image.open('../res/simple_zombie_right.png')

        elif(self.center[0] > char_center[0]):
            self.position[0] -= self.speed
            self.direction = 'left'
            if self.size == 16:
                self.shape = Image.open('../res/simple_zombie_left.png')
            # print(self.position[0])

        if self.name == 'zombie':
            self.movSwing()

        self.center = np.array([(self.position[0] + self.size), (self.position[1] + self.size)])


    def collision_check(self, character):   # obj도 추가할 것
        
        collision = self.overlapCharacter(self.center, character)

        # 캐릭터 공격
        if collision == 'hit':
            character.state = 'damaged' #여기서 함수를 호출해도 되는데 그건 조금?

        # 피격
        if collision == 'damaged':
            print(self.hit)
            self.hit += 1       # 이거 그대로 3 올라가는데요?
            collision = 'none'
            if self.hit > 2:
                self.state = 'dead'
                # 시체는 없을거야. 근데 뿅하고 사라지겠네
                if self.size == 16: 
                    character.score += 100
                if self.size == 8:
                    character.score += 50


    def overlapCharacter(self, ego_center, c):
        # 새 충돌에서 방향받아서, 그 방향의 망치 범위일때가 필요한 거야
        center_col = np.array([(ego_center[0] - c.center[0]), (ego_center[1] - c.center[1])])
        
        # 렉이 걸릴 수준이면, 판정이 인식이 안 된다..
        if c.state == 'punch': # ddd
            if c.direction == 'up':
                # up이 가장 이상해..
                if 0 > center_col[1] > -self.size - 24 and abs(center_col[0]) < 16:
                    return 'damaged'

            if c.direction == 'down':
                if -8 < center_col[1] < self.size + 24 and abs(center_col[0]) < 16:
                    return 'damaged'
                    
            # 왼쪽만 머가 이상함...
            if c.direction == 'left':
                if 24 > center_col[0] > -self.width - 16 and abs(center_col[1]) < 24:
                    return 'damaged'
                    
            if c.direction == 'right':
                if 0 < center_col[0] < self.width + 32 and abs(center_col[1]) < 24:
                    return 'damaged'

        # x좌표는 28, y좌표는 54 정도가 적정선? 지금의,
        if c.state != 'dodge': # 회피처리
            if abs(center_col[0]) < 12 and abs(center_col[1]) < 24:
                return 'hit'