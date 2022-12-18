import numpy as np
from PIL import Image

class Block:
    def __init__(self, x, y):
        self.halfSize = np.array([x, y])  # size로 변경?
        self.shape = Image.open('../res/background/back_tool.png')

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

    def collision(self, position, character):   # 각 block 판정
        center = np.array([(int)(character.center[0] - (position[0] + self.halfSize[0])), (int)(character.center[1] - (position[1] + self.halfSize[1]))])
        
        if character.name != 'ghost':
            # 들어왔다의 인식
            if -self.halfSize[0] < center[0] < self.halfSize[0]:
                if -self.halfSize[1] < center[1] < self.halfSize[1]:
                    # 장애물과의 겹침 범위내에서, 실제 장애물 범위로 들어오면 돌려보냄
                    if center[0] > self.halfSize[0] - 10:
                        character.position[0] += character.speed
                    elif center[0] < -self.halfSize[0] + 10:
                        character.position[0] -= character.speed
                    
                    if center[1] > self.halfSize[1] - 10:
                        character.position[1] += character.speed
                    elif center[1] < -self.halfSize[1] + 10:
                        character.position[1] -= character.speed

        character.center = np.array([(int)(character.position[0] + character.size), (int)(character.position[1] + character.size)])