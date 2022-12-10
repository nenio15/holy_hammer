from PIL import Image, ImageDraw, ImageFont
from time import time
import random
import cv2 as cv
import numpy as np
from colorsys import hsv_to_rgb

from Character import Character
from Joystick import Joystick
from Enemy import Enemy
from Block import Block
from Stage import Stage

def main():
    space = 0
    joystick = Joystick()
    # block = Block(50, 50, 'map')
    my_image = Image.new("RGBA", (joystick.width + space, joystick.height + space))
    background = Image.open("background1.png")
    my_draw = ImageDraw.Draw(my_image)
    # # 배경화면 초기화?
    my_draw.rectangle((space, space, joystick.width + space, joystick.height + space), fill=(255, 0, 0, 100))
    joystick.disp.image(my_image, 180, space, space)
    # 캐릭터 위치, 배경화면 초기화
    my_character = Character(joystick.width, joystick.height)
    my_img = Image.open(my_character.appearance)
    # my_draw.rectangle((0, 0, joystick.width, joystick.height), fill = (255, 255, 255, 100))
    my_image.paste(background, (space, space))
    
    rand_x = random.randint(-32, 240)
    rand_y = random.randint(-32, 240)
    enemy_1 = Enemy('ghost', (rand_x, rand_y))
    enemy_list = [enemy_1]
    block_list = []
    stage = Stage(1)    #1

    while True:
        if stage.startStage(enemy_list):    # 스테이지 처음에만 실행
            block_list = stage.showStage(block_list)


        command = {'move': False, 'up_pressed': False, 'down_pressed': False, 'left_pressed': False, 'right_pressed': False}
        # this can move to other def?
        command = playerCommand(command, joystick, my_character)
        my_character.move(command)
        block_list[0].mapLimit(my_character)
        #block.collision(my_character)

        my_img = Image.open(my_character.appearance)

        #그리는 순서가 중요합니다. 배경을 먼저 깔고 위에 그림을 그리고 싶었는데 그림을 그려놓고 배경으로 덮는 결과로 될 수 있습니다.
        my_image.paste(background, (space, space))
        my_draw.text((0, 0), "score "+ str(my_character.score), fill="#FFFFFF")
        my_draw.text((180, 0), "LIFE : "+str(my_character.life), fill="#FFFFFF") # ani로 하고 싶었어...

        for block in block_list:
            my_image.paste(block.shape, tuple(block.position), block.shape)
            block.collision(my_character)
        
        for enemy in enemy_list:
            if enemy.state != 'dead':
                enemy.move(my_character.center)
                for block in block_list:
                    block.collision(enemy)

                #block.collision(enemy)
                enemy.collision_check(my_character)
                my_image.paste(enemy.shape, tuple(enemy.position), enemy.shape)
            else:
                enemy_list.remove(enemy) # 이거... 다른 list에 영향을 줌(시각적으로)
        
        # 피격시에는, 달리 해야...?
        my_image.paste(my_img, tuple(my_character.position), my_img)
        
        # get blend
        # my_img_trans = Image.new("RGBA", my_img.size)
        # my_img_trans = Image.blend(my_img_trans, my_img, 0.5)
        # my_image.paste(my_img_trans, tuple(my_character.position), my_img_trans)
        
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
        if time() > character.delay + 0.3:
            character.action()
            character.delay = time() # 누른 시간 기록
        
    if not joystick.button_B.value:
        character.dash(command)
        

    if joystick.button_B.value:
        # pushB 눌린정도. rolling 쿨타임
        # print(character.state)
        if character.state == 'dash' and character.pushB < 100 and time() > character.rolling + 0.7:
                # print("dodged!!!")
                # character.dodge(command) # 일단 보류(이미지도 없엉)
                character.rolling = time()
                command['move'] = False
                character.pushB = 0
        character.speed = 4

    return command

if __name__ == '__main__':
    main()