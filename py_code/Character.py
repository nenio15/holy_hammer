import numpy as np

class Character:
    def __init__(self, width, height):
        self.appearance = '64_char.png'
        self.state = None
        self.speed = 5
        self.size = 32 # half_size
        self.position = np.array([(int)(width/2 - self.size), (int)(height/2 - self.size)])
        self.center = np.array([(int)(self.position[0] + self.size), (int)(self.position[1] + self.size)])
        self.outline = "#FFFFFF"
        

    def move(self, command = None):
        if command['move'] == False:
            self.state = None
            self.outline = "#FFFFFF" #검정색상 코드!
        
        else:
            self.state = 'move'
            self.outline = "#FF0000" #빨강색상 코드!

            if command['up_pressed']:
                self.position[1] -= self.speed
                self.appearance = "../res/64_char_up.png"

            if command['down_pressed']:
                self.position[1] += self.speed
                self.appearance = "../res/64_char_down.png"

            if command['left_pressed']:
                self.position[0] -= self.speed
                self.appearance = "../res/64_char_left.png"
                
            if command['right_pressed']:
                self.position[0] += self.speed
                self.appearance = "../res/64_char_right.png"

            #center update
            self.center = np.array([(int)(self.position[0] + self.size), (int)(self.position[1] + self.size)])