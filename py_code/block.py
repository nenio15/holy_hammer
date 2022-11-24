import numpy as np

class block:
    def __init__(self, x, y, status):
        # 충돌해서 막히는 판정.. (근데 몬스터는 지나갈거야?)
        # 맵이면, 밀어낸다.
        # 벽같은 obj는, array로 좌표를 지닌다.
        # 필요 요소는 center그리고 width, height
        if status == 'map': # map은 자신의 내부에 넣어야됨... 반대로 해야하는데?
            self.width = 240
            self.height = 240
        if status == 'wall':
            self.width = 20
            self.height = 60
        self.center = np.array([(int)(x), (int)(y)])

    def collision(self, character): #충돌했다(이쪽으로 이동을 시도했다. -> 기존의 자리로 되돌린다.(how?))
        # 캐릭터의 구분이 필요?
        if character.name == 'midory':
            if character.center[0] < self.center[0]:
                character.position[0] -= character.speed
        elif character.name == 'zombie':
            if character.center[0] < self.center[0]:
                character.position[0] -= character.speed
