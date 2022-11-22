import numpy as np

class Enemy:
    def __init__(self, type, spawn_position):
        if type == 'zombie':
            self.shape = '../simple_zombie.png'
        else:
            self.shape = '../simple_ghost.png'
        self.state = 'alive'
        self.speed = 3
        self.position = np.array([(int)(spawn_position[0] - 16), (int)(spawn_position[1] - 16)])
        self.center = np.array([(int)(self.position[0] + 16), (int)(self.position[1] + 16)])
        self.outline = '#FFFFFF'

    def move(self, char_center):
        if(self.center[0] - char_center[0] < 0):
            self.position[0] += self.speed
        elif(self.center[0] - char_center[0] > 0):
            self.position[0] -= self.speed
        if(self.center[1] - char_center[1] < 0):
            self.position[1] += self.speed
        elif(self.center[1] - char_center[1] > 0):
            self.position[1] -= self.speed

    def collision_check(self, character, obj):
        collision = self.overlapCharacter(self.center, character.center)

        if collision:
            print("character hit!!")

    def overlapCharacter(self, ego_center, char_center):
        # | c_x - e_x | < c_R + e_r
        return abs(ego_center[0] - char_center[0]) < (64 + 32) and abs(ego_center[1] - char_center[1]) < (64 + 32)


