from PIL import Image, ImageDraw, ImageFont
from time import time
import random
import cv2 as cv
import numpy as np
from colorsys import hsv_to_rgb

from Character import Character
from Joystick import Joystick
from Enemy import Enemy

def main():
    space = 0
    joystick = Joystick()
    my_image = Image.new("RGBA", (joystick.width + space, joystick.height + space))
    my_img = Image.open("64_char.png")
    background = Image.open("background1.png")
    # my_img = img.resize((32, 32))
    my_draw = ImageDraw.Draw(my_image)
    # # 배경화면 초기화?
    my_draw.rectangle((space, space, joystick.width + space, joystick.height + space), fill=(255, 0, 0, 100))
    joystick.disp.image(my_image, 180, space, space)
    # 캐릭터 위치, 배경화면 초기화
    my_character = Character(joystick.width, joystick.height)
    # my_draw.rectangle((0, 0, joystick.width, joystick.height), fill = (255, 255, 255, 100))
    my_image.paste(background, (space, space))
    
    rand_x = random.randint(-32, 240)
    rand_y = random.randint(-32, 240)
    print(rand_x)
    print(rand_y)
    enemy_1 = Enemy('ghost', (rand_x, rand_y))
    enemy_list = [enemy_1]

    while True:
        command = {'move': False, 'up_pressed': False, 'down_pressed': False, 'left_pressed': False, 'right_pressed': False}
        # this can move to other def?
        command = playerCommand(command, joystick, my_character)
        my_character.move(command)
        my_img = Image.open(my_character.appearance)

        #그리는 순서가 중요합니다. 배경을 먼저 깔고 위에 그림을 그리고 싶었는데 그림을 그려놓고 배경으로 덮는 결과로 될 수 있습니다.
        my_image.paste(background, (space, space))

        
        for enemy in enemy_list:
            if enemy.state != 'die':
                enemy.move(my_character.center)
                enemy.collision_check(my_character)
                my_image.paste(enemy.shape, tuple(enemy.position), enemy.shape)
        my_image.paste(my_img, tuple(my_character.position), my_img)

        #좌표는 이미지만 넣으면 180도 돌릴필요 엄서요..
        joystick.disp.image(my_image, 180, space, space)

def playerCommand(command, joystick, character):
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
            character.action()
            character.delay = time() # 누른 시간 기록
            # print("A_pressed")
    return command

if __name__ == '__main__':
    main()