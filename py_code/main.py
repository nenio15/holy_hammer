from PIL import Image, ImageDraw, ImageFont
from PIL import Image
import time
import random
import cv2 as cv
import numpy as np
from colorsys import hsv_to_rgb

from Character import Character
from Joystick import Joystick

def main():
    space = 10
    joystick = Joystick()
    my_image = Image.new("RGBA", (joystick.width + space, joystick.height + space))
    my_img = Image.open("64_char.png")
    background = Image.open("background1.png")
    # my_img = img.resize((32, 32))
    my_draw = ImageDraw.Draw(my_image)
    # 배경화면 초기화?
    my_draw.rectangle((space, space, joystick.width + space, joystick.height + space), fill=(255, 0, 0, 100))
    joystick.disp.image(my_image, 180, space, space)
    # 캐릭터 위치, 배경화면 초기화
    my_character = Character(joystick.width, joystick.height)
    # my_draw.rectangle((0, 0, joystick.width, joystick.height), fill = (255, 255, 255, 100))
    my_image.paste(background, (space, space))
    
    enemy_1 = Enemy('ghost', (50, 50))
    enemy_list = [enemy_1]

    while True:
        command = {'move': False, 'up_pressed': False, 'down_pressed': False, 'left_pressed': False, 'right_pressed': False}
        if not joystick.button_U.value:  # up pressed
            command['up_pressed'] = True
            command['move'] = True

        if not joystick.button_D.value:  # down pressed
            command['down_pressed'] = True
            command['move'] = True

        if not joystick.button_L.value:  # left pressed
            command['left_pressed'] = True
            command['move'] = True

        if not joystick.button_R.value:  # right pressed
            command['right_pressed'] = True
            command['move'] = True
            
        if not joystick.button_A.value:
            print("A_pressed")

        my_character.move(command)

        #그리는 순서가 중요합니다. 배경을 먼저 깔고 위에 그림을 그리고 싶었는데 그림을 그려놓고 배경으로 덮는 결과로 될 수 있습니다.

        my_image.paste(background, (space, space))
        # 얘는 음수로 가면 오류나네요, 막기는 쉬운데.. 약간은 캐릭터가 들어가도록 하고 싶은데...
        # my_image.alpha_composite(my_img, tuple(my_character.position))
        my_image.paste(my_img, tuple(my_character.position), my_img)
        
        for enemy in enemy_list:
            if enemy.state != 'die':
                my_image.paste(enemy.shape, tuple(enemy.position), enemy.shape)

        
    #좌표는 동그라미의 왼쪽 위, 오른쪽 아래 점 (x1, y1, x2, y2)
        joystick.disp.image(my_image, 180, space, space)


if __name__ == '__main__':
    main()