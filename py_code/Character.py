import numpy as np

class Character:
    def __init__(self, width, height):
        self.appearance = '64_char.png'
        self.state = None
        self.speed = 5
        self.size = 32 # half_size
        self.position = np.array([(int)(width/2 - self.size), (int)(height/2 - self.size)])
        self.center = np.array([(int)(self.position[0] + self.size), (int)(self.position[1] + self.size)])
        self.outline = '#FFFFFF'
        self.direction = 'right'
        

    def move(self, command = None):
        if command['move'] == False:
            self.state = None
            self.outline = '#FFFFFF' #검정색상 코드!
        
        else:
            self.state = 'move'
            self.outline = "#FF0000" #빨강색상 코드!

            if command['up_pressed']:
                self.position[1] -= self.speed
                self.appearance = '../res/64_char_up.png'
                self.direction = 'up'

            if command['down_pressed']:
                self.position[1] += self.speed
                self.appearance = '../res/64_char_down.png'
                self.direction = 'down'

            if command['left_pressed']:
                self.position[0] -= self.speed
                self.appearance = '../res/64_char_left.png'
                self.direction = 'left'
                
            if command['right_pressed']:
                self.position[0] += self.speed
                self.appearance = '../res/64_char_right.png'
                self.direction = 'right'

            #center update
            self.center = np.array([(int)(self.position[0] + self.size), (int)(self.position[1] + self.size)])

    def action(self):
        if self.direction == 'up':
            #self.appearance = '../res/char_attack_up.png'
            print('up action')
        elif self.direction == 'down':
            #self.appearance = '../res/char_attack_down.png'
            print('down action')
        elif self.direction == 'left':
            #self.appearance = '../res/char_attack_left.png'
            print('left action')
        elif self.direction == 'right':
            #self.appearance = '../res/char_attack_right.png'
            print('right action')

