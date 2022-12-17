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
from Stage import Stage, Item

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
            command['punch'] = True
            # character.action()
            character.delay = time() # 누른 시간 기록
        
    if not joystick.button_B.value:
        command['dash'] = True
        #command['move'] = True
        
    # 애매함. 봉인
#    if joystick.button_B.value:
        # pushB 눌린정도. rolling 쿨타임
        # print(character.state)
#        if character.state == 'dash' and character.pushB < 100 and time() > character.rolling + 0.7:
                # print("dodged!!!")
                # character.dodge(command) # 일단 보류(이미지도 없엉)
#                character.rolling = time()
#                command['move'] = False
#                character.pushB = 0
#        character.speed = 4

    return command

def blinkBody(my_img, start_time, replace = 0.5, alpha = 0.5):
    s = replace
    if time() > start_time + replace:
        s = s + 0.5

    if s == replace:
        my_img_trans = Image.new("RGBA", my_img.size)
        my_img_trans = Image.blend(my_img_trans, my_img, alpha)
        return my_img_trans
    else:
        return my_img


def main():
    space = 0
    joystick = Joystick()
    stage = Stage(2)    #1 is start, #0 is title..?
    blockManager = Block(120, 120, '32')
    my_image = Image.new("RGBA", (joystick.width + space, joystick.height + space))
    #background = Image.open('../res/background/background_1.png')
    my_draw = ImageDraw.Draw(my_image)
    # # 배경화면 초기화?
    my_draw.rectangle((space, space, joystick.width + space, joystick.height + space), fill=(255, 0, 0, 100))
    joystick.disp.image(my_image, 180, space, space)
    # 캐릭터 위치, 배경화면 초기화
    my_character = Character(joystick.width, joystick.height)
    my_img = Image.open(my_character.appearance)
    my_image.paste(stage.background, (space, space))
    # hitted = 0 # 이걸로 될려나..
    
    enemy_list = []
    block_list = stage.showStage()
    item_list = [Item(50, 100, 1), Item(120, 180, 2)]
    
    while True:
        if my_character.life < 1: # game over..
            print('life zero')
            return

        command = {'move': False, 'punch': False, 'dash': False,'up_pressed': False, 'down_pressed': False, 'left_pressed': False, 'right_pressed': False}
        command = playerCommand(command, joystick, my_character)
        my_character.checkManager(command) #my_character.move(command)
        my_img = Image.open(my_character.appearance)

        #block_list[0].mapLimit(my_character)    # ... need to change
        blockManager.mapLimit(my_character)

        #그리는 순서가 중요합니다. 배경을 먼저 깔고 위에 그림을 그리고 싶었는데 그림을 그려놓고 배경으로 덮는 결과로 될 수 있습니다.
        my_image.paste(stage.background, (space, space))
        
        for block in block_list:
            my_image.paste(blockManager.shape, tuple(block), blockManager.shape) # 벽 콜리더 시각화
            print(block)
            print(block[0], block[1])
            blockManager.collision(block, my_character)

        for item in item_list:
            if item.state != 'get':
                item.getItem(my_character)
                my_image.paste(item.shape, tuple(item.position), item.shape)
            else:
                item_list.remove(item)
        
        for enemy in enemy_list:
            if enemy.state != 'dead':
                enemy.move(my_character.center)
                for block in block_list:
                    blockManager.collision(block, my_character)

                enemy.collision_check(my_character, item_list)
                my_image.paste(enemy.shape, tuple(enemy.position), enemy.shape)
            else:
                # 이거... 다른 list에 영향을 줌(시각적으로)(귀찮아)
                enemy_list.remove(enemy)   
        
        if my_character.hitted: # 피격시, 투명도 설정
            my_img = blinkBody(my_img, my_character.damageDelay, 0.3, 0.7)
        my_image.paste(my_img, tuple(my_character.position), my_img)

        s = stage.startStage(enemy_list)
        if s != 0:
            block_list = stage.showStage()  # d여러번 호출이라.. 따로 처리해? 말어?
            #print('show title..')
            if s < 10:
                my_draw.text((100, 80), 'STAGE ' + str(s), fill="#000000", stroke_fill="#FFFFFF")   # text는 따로인가?
            elif s == 10:
                my_draw.text((100, 80), 'CLEAR!!!', fill='#FFFFFF')
                
        my_draw.text((0, 0), "score "+ str(my_character.score), fill="#FFFFFF")
        my_draw.text((180, 0), "LIFE : "+str(my_character.life), fill="#FFFFFF") # ani로 하고 싶었어...

        #좌표는 이미지만 넣으면 180도 돌릴필요 엄서요..
        joystick.disp.image(my_image) #, 180, space, space)

if __name__ == '__main__':
    main()