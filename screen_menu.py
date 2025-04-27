from s_game import game, FLAG, about
from pygame import *
import pygame
import sys
# from time import 
from random import randint

# музыка
mixer.init()
mixer.music.load('menu_music.ogg')
mixer.music.set_volume(0.2)
mixer.music.play()
# if FLAG == True:
#     mixer.music.pause()
# elif FLAG == False:
#     mixer.music.unpause()

def draw_text(text, size, x, y):
    font = pygame.font.SysFont('Arial', size)
    text_surface = font.render(text, True, (0, 0, 0))
    text_rect = text_surface.get_rect(center=(x, y))
    screen.blit(text_surface, text_rect)

# Инициализация Pygame
# pygame.init()
mixer.init()
font.init()

# Константы
WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (66,170,255)
screen_flag = True

# Настройка дисплея
screen = display.set_mode((WIDTH, HEIGHT))
display.set_caption("Шутер")

clock = time.Clock()

while screen_flag!= False:
    for e in event.get():
        if e.type == QUIT:
            pygame.quit()
            sys.exit()
            game.finish = False
            # screen_flag = False
        if e.type == MOUSEBUTTONDOWN:
            if e.button == 1:
                click = True
    
    screen.fill(WHITE)
    draw_text("Добро пожаловать!", 40, WIDTH/2, HEIGHT/4)
    mx, my = mouse.get_pos()
    button_1 = Rect(WIDTH/2 - 70, HEIGHT/2, 140, 50)
    button_2 = Rect(WIDTH/2 - 70, HEIGHT/2 + 60, 140, 50)
    if button_1.collidepoint((mx, my)):
        if click: game()
    if button_2.collidepoint((mx, my)):
        if click: about()

    draw.rect(screen, GREEN, button_1)
    draw.rect(screen, BLUE, button_2)
    draw_text("Play", 30, WIDTH/2, HEIGHT/2 + 25)
    draw_text("About", 30, WIDTH/2, HEIGHT/2 + 85)
    click = False
    display.flip()
    clock.tick(60)

 