import numpy as np
from PIL import Image

class Block:
    def __init__(self, x, y, status):
        # 충돌해서 막히는 판정.. (근데 몬스터는 지나갈거야?)
        self.halfSize = np.array([16, 16])
        self.shape = Image.open('../res/block32_1.png')
        if status == '64':
            self.halfSize = np.array([32, 32])
            self.shape = Image.opne('../res/block16_1.png')

        self.position = np.array([(int)(x), (int)(y)])
        self.center = np.array([x + self.halfSize[0], y + self.halfSize[1]])#, [20, 20]) #, [100, 100])

    def mapLimit(self, character):  # 맵은 여기서 처리.. (아니면 맵을 확장하던가)
        if character.center[0] < -5:
            character.position[0] += character.speed
        elif character.center[0] > 245:
            character.position[0] -= character.speed

        if character.center[1] < -5:
            character.position[1] += character.speed
        elif character.center[1] > 245:
            character.position[1] -= character.speed

        character.center = np.array([(int)(character.position[0] + character.size), (int)(character.position[1] + character.size)])

    def collision(self, character): #충돌했다(이쪽으로 이동을 시도했다. -> 기존의 자리로 되돌린다.(how?))
        # 캐릭터의 구분이 필요?
        center = np.array([(int)(character.center[0] - self.center[0]), (int)(character.center[1] - self.center[1])])

        if character.name != 'ghost':
            # 들어왔다의 인식
            if -self.halfSize[0] < center[0] < self.halfSize[0]:
                if -self.halfSize[1] < center[1] < self.halfSize[1]:
                    # 장애물과의 겹침 범위내에서, 실제 장애물 범위로 들어오면 돌려보냄
                    # 다만 좀비가 바보가 됨
                    if center[0] > self.halfSize[0] - 10:
                        character.position[0] += character.speed
                    elif center[0] < -self.halfSize[0] + 10:
                        character.position[0] -= character.speed
                    
                    if center[1] > self.halfSize[1] - 10:
                        character.position[1] += character.speed
                    elif center[1] < -self.halfSize[1] + 10:
                        character.position[1] -= character.speed

        character.center = np.array([(int)(character.position[0] + character.size), (int)(character.position[1] + character.size)])