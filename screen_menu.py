from s_game import game, FLAG, finish  # , about
from about import about
from pygame import *
import pygame
import sys
from random import randint

# Константы
WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (66, 170, 255)
screen_flag = True
FPS = 60


# класс
class Object:
    def __init__(self, object_image, object_x, object_y, size_x, size_y):
        self.image = transform.scale(image.load(object_image), (size_x, size_y))
        self.rect = self.image.get_rect()
        self.rect.x = object_x
        self.rect.y = object_y

    def reset(self):
        screen.blit(self.image, (self.rect.x, self.rect.y))


# Инициализация Pygame
font.init()


def draw_text(text, size, x, y):
    font = pygame.font.SysFont("Arial", size)
    text_surface = font.render(text, True, (0, 0, 0))
    text_rect = text_surface.get_rect(center=(x, y))
    screen.blit(text_surface, text_rect)


# музыка
mixer.init()
mixer.music.load("menu_music.ogg")
mixer.music.set_volume(0.2)
# if FLAG == True:
#     mixer.music.pause()
# elif FLAG == False:
#     mixer.music.unpause()

button_play = Object("button_play.png", WIDTH / 2 - 70, HEIGHT / 2 + 150, 140, 60)
button_about = Object("button_about.png", WIDTH / 2 - 70, HEIGHT / 2 + 209, 140, 60)
back = transform.scale(image.load("back_menu.jpg"), (WIDTH, HEIGHT))


# Настройка дисплея
screen = display.set_mode((WIDTH, HEIGHT))
display.set_caption("Шутер")

is_play_music = False

clock = time.Clock()
while screen_flag:
    if not is_play_music:
        mixer.music.play(-1)
        is_play_music = True
    for e in event.get():
        if e.type == QUIT:
            pygame.quit()
            sys.exit()
            game.finish = False
            # screen_flag = False
        if e.type == MOUSEBUTTONDOWN:
            if e.button == 1:
                click = True

    # screen.fill(WHITE)
    screen.blit(back, (0, 0))
    draw_text("Добро пожаловать!", 40, WIDTH / 2, HEIGHT / 4)
    mx, my = mouse.get_pos()
    button_play.reset()
    button_about.reset()
    button_1 = Rect(WIDTH / 2 - 70, HEIGHT / 2 + 150, 140, 50)
    button_2 = Rect(WIDTH / 2 - 70, HEIGHT / 2 + 150 + 60, 140, 50)
    draw_text("Play", 30, WIDTH / 2, HEIGHT / 2 + 175)
    draw_text("About", 30, WIDTH / 2, HEIGHT / 2 + 235)

    if button_1.collidepoint((mx, my)):
        if click:
            mixer.music.stop()
            is_play_music = False
            game()
        # finish = False
    if button_2.collidepoint((mx, my)):
        if click:
            about()

    click = False
    display.flip()
    clock.tick(FPS)
