import numpy as np
from time import time
import random
from PIL import Image
#from Stage import Item

class Enemy:
    def __init__(self, typee, spawn_position):
        self.shape = Image.open('../res/simple_zombie_right.png')
        self.size = 16
        self.width = 16
        self.name = typee
        self.speed = 1
        #self.hit = 0
        self.health = 7
        self.swing = random.randint(-4, 5)  # -5 ~ 5
        self.frame = 0


        if typee == 'ghost':    # 변칙적이진 않다만, 플레이어 속도를 쫓아온다는 위협성..
            self.shape = Image.open('../res/simple_ghost.png')
            self.size = 8
            self.speed = 2      # 3으로 할거면 달리기가 필요..
            self.health = 1
        elif typee == 'boss':
            self.shape = Image.open('../res/simple_boss_right.png')
            self.size = 32
            self.width = 32
            self.health = 150

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
        if self.frame < 2 and self.name != 'ghost': # zombie의 속도를 늦추기
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
            elif self.size == 32:
                self.shape = Image.open('../res/simple_boss_right.png')

        elif(self.center[0] > char_center[0]):
            self.position[0] -= self.speed
            self.direction = 'left'
            if self.size == 16:
                self.shape = Image.open('../res/simple_zombie_left.png')
            elif self.size == 32:
                self.shape = Image.open('../res/simple_boss_left.png')
            # print(self.position[0])

        if self.name == 'zombie':
            self.movSwing()

        self.center = np.array([(self.position[0] + self.size), (self.position[1] + self.size)])


    def collision_check(self, character, item_list):   # obj도 추가할 것
        
        collision = self.overlapCharacter(self.center, character)

        # 캐릭터 공격
        if collision == 'hit':
            character.state = 'damaged' #여기서 함수를 호출해도 되는데 그건 조금?

        # 피격
        if collision == 'damaged':
            self.blinkBody(time(), 0.3)  # 중복되어서 들어감
            self.health -= character.power #self.hit += character.power      # punch가 지속되는 동안 올라감. 그래서 health를 크게 줬음
            if self.health <= 0:
                self.state = 'dead'
                
                if self.size == 16: 
                    character.score += 100
                elif self.size == 8:
                    character.score += 50
                else:
                    character.score += 10000


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
        if c.state != 'dodge' and c.invincible != 1: # 회피처리
            if abs(center_col[0]) < 12 and abs(center_col[1]) < 24:
                return 'hit'

    def blinkBody(self, start_time, replace = 0.5, alpha = 0.7):
        s = replace
        if time() > start_time + replace:
            s = s + 0.5

        if s == replace:
            img_trans = Image.new("RGBA", self.shape.size)
            img_trans = Image.blend(img_trans, self.shape, alpha)
            self.shape = img_trans
        