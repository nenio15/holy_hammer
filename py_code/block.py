import numpy as np

class Block:
    def __init__(self, x, y, status):
        # 충돌해서 막히는 판정.. (근데 몬스터는 지나갈거야?)
        # 맵이면, 밀어낸다.
        # 벽같은 obj는, array로 좌표를 지닌다.
        # 필요 요소는 center그리고 width, height
        if status == 'map': # 이거 필요하진 않을텐데...?
            self.width = 240
            self.height = 240
        if status == 'wall':
            self.width = 20
            self.height = 60
        self.center = np.array([(int)(x), (int)(y)])

    def mapLimit(self, character):  # 맵은 여기서 처리..
        if character.center[0] < -5:
            character.position[0] += character.speed
        elif character.center[0] > 245:
            character.position[0] -= character.speed

        if character.center[1] < -5:
            character.position[1] += character.speed
        elif character.center[1] > 245:
            character.position[1] -= character.speed


    def collision(self, character): #충돌했다(이쪽으로 이동을 시도했다. -> 기존의 자리로 되돌린다.(how?))
        # 캐릭터의 구분이 필요?
        if character.name == 'midory':
            if character.center[0] < self.center[0]:
                character.position[0] -= character.speed
        elif character.name == 'zombie':
            if character.center[0] < self.center[0]:
                character.position[0] -= character.speed
