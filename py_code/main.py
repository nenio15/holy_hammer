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
    joystick = Joystick()
    my_image = Image.new("RGBA", (joystick.width, joystick.height))
    my_img = Image.open("32_char.png").convert("RGBA")
    background = Image.open("background1.png")
    # my_img = img.resize((32, 32))
    my_draw = ImageDraw.Draw(my_image)
    # 배경화면 초기화?
    my_draw.rectangle((0, 0, joystick.width, joystick.height), fill=(255, 0, 0, 100))
    joystick.disp.image(my_image)
    # 캐릭터 위치, 배경화면 초기화
    my_character = Character(joystick.width, joystick.height)
    # my_draw.rectangle((0, 0, joystick.width, joystick.height), fill = (255, 255, 255, 100))
    my_image.paste(background, (0, 0))
    while True:
        command = None
        if not joystick.button_U.value:  # up pressed
            command = 'up_pressed'

        elif not joystick.button_D.value:  # down pressed
            command = 'down_pressed'

        elif not joystick.button_L.value:  # left pressed
            command = 'left_pressed'

        elif not joystick.button_R.value:  # right pressed
            command = 'right_pressed'
            
        else:
            command = None

        my_character.move(command)

        #그리는 순서가 중요합니다. 배경을 먼저 깔고 위에 그림을 그리고 싶었는데 그림을 그려놓고 배경으로 덮는 결과로 될 수 있습니다.
        # my_draw.rectangle((0, 0, joystick.width, joystick.height), fill = (255, 255, 255, 100))
        # my_draw.ellipse(tuple(my_circle.position), outline = my_circle.outline, fill = (0, 0, 0))
        # my_image.paste(my_img, (0, 0))

        my_image.paste(background, (0, 0))
        my_image.paste(my_img, tuple(my_character.position))
        
    #좌표는 동그라미의 왼쪽 위, 오른쪽 아래 점 (x1, y1, x2, y2)
        joystick.disp.image(my_image)


if __name__ == '__main__':
    main()