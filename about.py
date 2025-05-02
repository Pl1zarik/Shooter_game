from pygame import *
import pygame
import sys

# Константы
WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (66,170,255)
screen_flag = True
FPS = 60

# Настройка дисплея
main_win = display.set_mode((WIDTH, HEIGHT))
display.set_caption("Шутер")
back = transform.scale(image.load('back_about.png'), (WIDTH, HEIGHT))


def about():

    clock = time.Clock()

    while screen_flag!= False:
        for e in event.get():
            if e.type == QUIT:
                pygame.quit()
                sys.exit()
    
        main_win.blit(back, (0, 0))
        display.flip()
        clock.tick(FPS)