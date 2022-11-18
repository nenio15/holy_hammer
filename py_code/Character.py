import numpy as np

class Character:
    def __init__(self, width, height):
        self.appearance = 'circle'
        self.state = None
        # self.position = np.array([width/2 - 20, height/2 - 20, width/2 + 20, height/2 + 20])
        self.position = np.array([(int)(width/2 - 32), (int)(height/2 - 32)])
        self.outline = "#FFFFFF"
        # self.x = (int)(width/2 - 20)
        # self.y = (int)(height/2 - 20)

    def move(self, command = None):
        if command == None:
            self.state = None
            self.outline = "#FFFFFF" #검정색상 코드!
        
        else:
            self.state = 'move'
            self.outline = "#FF0000" #빨강색상 코드!

            if command == 'up_pressed':
                self.position[1] -= 5

            elif command == 'down_pressed':
                self.position[1] += 5

            elif command == 'left_pressed':
                self.position[0] -= 5
                
            elif command == 'right_pressed':
                self.position[0] += 5