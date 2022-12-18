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
            character.delay = time() # 누른 시간 기록
        
    if not joystick.button_B.value:
        command['dash'] = True

    return command

def blinkBody(my_img, start_time, replace = 0.5, alpha = 0.7):
    s = replace
    if time() > start_time + replace:
        s = s + 0.5

    if s == replace:
        my_img_trans = Image.new("RGBA", my_img.size)
        my_img_trans = Image.blend(my_img_trans, my_img, alpha)
        return my_img_trans
    else:
        return my_img

def dropItem(enemy, item_list):
    # 1.드롭확률이랑, 아이템 확률을 달리한다. 2.각 아이템의 드롭확률을 조정한다.
    # 이때 한 아이템만 드롭해야한다.
    get = random.random()
    if get < 0.3:
        if random.random() < 0.1:
            item_list.extend([Item(enemy.position[0], enemy.position[1], 4)])
        elif random.random() < 0.35:
            item_list.extend([Item(enemy.position[0], enemy.position[1], 1)])
        elif random.random() < 0.3:
            item_list.extend([Item(enemy.position[0], enemy.position[1], 2)])
        else: # 베이스는 하트(이지 난이도)
            item_list.extend([Item(enemy.position[0], enemy.position[1], 3)])

def gameRestart(char, stage, joystick):
    char.life = 5
    char.position = np.array([(int)(joystick.width / 2 - char.size), (int)(joystick.height / 2 - char.size)])
    char.score = 0
    char.effect -= 10
    char.state = 'noraml'

    stage.stage = 1
    stage.step = -1
    stage.setTime = time()

def main():
    space = 0
    joystick = Joystick()
    stage = Stage(0)    #1 is start, #2, #3 (3 is boss round)
    blockManager = Block(16, 16)
    my_image = Image.new("RGBA", (joystick.width + space, joystick.height + space))
    my_draw = ImageDraw.Draw(my_image)
    # # 배경화면 초기화
    my_draw.rectangle((space, space, joystick.width + space, joystick.height + space), fill=(255, 0, 0, 100))
    joystick.disp.image(my_image) #, 180, space, space)
    # 캐릭터 위치, 배경화면 초기화
    my_character = Character(joystick.width, joystick.height)
    my_img = Image.open(my_character.appearance)
    my_image.paste(stage.background, (space, space))
    
    block_list = stage.showStage()
    enemy_list = []
    item_list = [] #[Item(50, 100, 1), Item(120, 180, 2)]
    
    while stage.stage == 0:
        my_image.paste(stage.background, (space, space))
        my_draw.text((5, 220), "joystick : move", fill="#FFFFFF")
        my_draw.text((5, 230), "A : punch, B : dash", fill="#FFFFFF")

        my_draw.text((60, 170), "PRESS 'A' For start...", fill="#FFFFFF")
        if not joystick.button_A.value:
            stage.stage = 1
            stage.setTime = time()

        joystick.disp.image(my_image)

    while True:
        if my_character.life <= 0: # game over..
            #print('life zero')
            my_draw.text((90, 80), 'GAME OVER...', fill='#FFFFFF')
            my_draw.text((60, 180), "PRESS 'A' For restart...", fill='#000000')

            if not joystick.button_A.value: # restart 전부 다 초기화
                enemy_list.clear()
                item_list.clear()
                gameRestart(my_character, stage, joystick)

            joystick.disp.image(my_image)
            continue    # skip

        command = {'move': False, 'punch': False, 'dash': False,'up_pressed': False, 'down_pressed': False, 'left_pressed': False, 'right_pressed': False}
        command = playerCommand(command, joystick, my_character)
        my_character.checkManager(command)          #my_character.move(command)
        my_img = Image.open(my_character.appearance)

        blockManager.mapLimit(my_character)

        # 그림 순서 | 배경(벽) -> 아이템 -> 적 -> 캐릭터(+효과) -> 시스템 메세지
        my_image.paste(stage.background, (space, space))
        
        for block in block_list:
            # my_image.paste(blockManager.shape, tuple(block), blockManager.shape) # 벽 콜리더 시각화
            blockManager.collision(block, my_character)

        for item in item_list:
            if item.state != 'get': # 필드 아이템
                item.getItem(my_character)
                my_image.paste(item.shape, tuple(item.position), item.shape)
            else: # 아이템 획득
                item_list.remove(item)
        
        for enemy in enemy_list:
            if enemy.state != 'dead':
                enemy.move(my_character.center)
                for block in block_list:
                    blockManager.collision(block, enemy)

                enemy.collision_check(my_character)
                my_image.paste(enemy.shape, tuple(enemy.position), enemy.shape)
            else:
                dropItem(enemy, item_list)
                enemy_list.remove(enemy)   
        
        my_character.special() # effect end check
        if my_character.effect != 0: # 아이템 효과 있
            my_effect = Image.open(my_character.eshape)
            my_image.paste(my_effect, tuple(my_character.position), my_effect)
        
        if my_character.hitted: # 피격시, 투명도 설정
            my_img = blinkBody(my_img, my_character.damageDelay)
        my_image.paste(my_img, tuple(my_character.position), my_img)

        s = stage.startStage(enemy_list, my_character.position)
        if s != 0:
            block_list = stage.showStage()
            #print('show title..')
            if s == -1: # item 클리어(맵 바뀌어서 시작하면)
                item_list.clear()
            elif s < 10:
                my_draw.text((100, 80), 'STAGE ' + str(s), fill="#FFFFFF")
            elif s == 10:
                if stage.stage != 4:
                    my_draw.text((100, 80), 'CLEAR!!!', fill='#FFFFFF')
                else:   # boss clear!!
                    my_draw.text((90, 80), 'ALL CLEAR!!!', fill='#FFFFFF')
                    my_draw.text((60, 180), "PRESS 'B' For restart...", fill='#000000')

                    if not joystick.button_B.value: # restart 전부 다 초기화
                        enemy_list.clear()
                        item_list.clear()
                        gameRestart(my_character, stage, joystick)
                
        my_draw.text((0, 0), "score "+ str(my_character.score), fill="#FFFFFF")
        my_draw.text((180, 0), "LIFE : "+str(my_character.life), fill="#FFFFFF")

        joystick.disp.image(my_image)

if __name__ == '__main__':
    main()