import numpy as np

class Character:
    def __init__(self, width, height):
        self.appearance = 'circle'
        self.state = None
        self.position = np.array([(int)(width/2 - 32), (int)(height/2 - 32)])
        self.center = np.array([(int)(self.position[0] + 32), (int)(self.position[1] + 32)])
        self.outline = "#FFFFFF"
        

    def move(self, command = None):
        if command['move'] == False:
            self.state = None
            self.outline = "#FFFFFF" #검정색상 코드!
        
        else:
            self.state = 'move'
            self.outline = "#FF0000" #빨강색상 코드!

            if command['up_pressed']:
                self.position[1] -= 5

            if command['down_pressed']:
                self.position[1] += 5

            if command['left_pressed']:
                self.position[0] -= 5
                
            if command['right_pressed']:
                self.position[0] += 5

            #center update
            self.center = np.array([(int)(self.position[0] + 32), (int)(self.position[1] + 32)])