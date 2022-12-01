import numpy as np

class Block:
    def __init__(self, x, y, status):
        # 충돌해서 막히는 판정.. (근데 몬스터는 지나갈거야?)
        # 벽같은 obj는, array로 좌표를 지닌다... obj로 개별적? 아니면 걍 array?
        self.center = np.array([(int)(x), (int)(y)])
        # self.array = np.array()

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
        if character.name == 'midory':
            if character.center[0] < self.center[0]:
                character.position[0] -= character.speed
        elif character.name == 'zombie':
            if character.center[0] < self.center[0]:
                character.position[0] -= character.speed