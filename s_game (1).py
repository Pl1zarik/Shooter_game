# модули
from time import time as timer
import pygame
from pygame import *
from random import randint
from time import perf_counter

# константы
patrons = 20
health = 100
W = 800
H = 600
screen_flag = True
finish = False
time_boss = 60
boss_lost = 40
# boss_speed_x = 5

# настройки окна
# pygame.init()
# main_win = display.set_mode((W, H), FULLSCREEN)
main_win = display.set_mode((W, H))
display.set_caption("Шутер")
back = transform.scale(image.load("sky.jpg"), (W, H))

FPS = 60


# Конструктор класса
class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        main_win.blit(self.image, (self.rect.x, self.rect.y))


class Player(GameSprite):
    def update(self):
        keys_pressed = key.get_pressed()
        if keys_pressed[K_d] and self.rect.x < W - 85:
            self.rect.x += self.speed
        if keys_pressed[K_a] and self.rect.x > 5:
            self.rect.x -= self.speed

    def FIRE(self):
        global patrons
        bullet = Bullet("bullet.png", self.rect.centerx, self.rect.top, 15, 20, 15)
        bullets.add(bullet)
        patrons -= 1


class Enemy(GameSprite):
    def update(self):
        global lost
        self.rect.y += self.speed
        if self.rect.y > H:
            self.rect.y = 0
            self.rect.x = randint(80, W - 80)
            lost += 1  # тут


class Sprites(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y > H:
            self.rect.y = 0
            self.rect.x = randint(80, W - 80)


class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()


# class Boss(GameSprite):
#     def update(self):
#         if boss.rect.x > W - 100: #or ball.rect.y < 0
#             boss_speed_x *= -1
#         if boss.rect.x < W - 700: #or ball.rect.y < 0
#             boss_speed_x *= -1

# Музыка
mixer.init()
fire = mixer.Sound("laser-blast.ogg")

# текст
font.init()
font1 = font.SysFont("Arial", 28)
font2 = font.SysFont("Arial", 50)

# очки
score = 0  # сбито
lost = 0  # пропущено

# параметры спрайтов
monsters_max = 5  # колл-во монстров на экране
asteroid_max = 2  # колл-во астероидов на экране
boosts_max = 1  # колл-во бустов на экране
# группы и спрайты
player = Player("rocket_100hp.png", W // 2, H - 130, 100, 120, 5)
# boss = Boss('boss.png', W//2, H - 130, 100, 120, 5)
monsters = sprite.Group()
for i in range(monsters_max):
    monster = Enemy("ufo.png", randint(80, W - 80), -40, 80, 50, randint(1, 3))
    monsters.add(monster)

no_break_monsters = sprite.Group()
for i in range(asteroid_max):
    asteroid = Sprites("asteroid.png", randint(80, W - 80), -40, 80, 50, randint(1, 2))
    no_break_monsters.add(asteroid)

boosts_health = sprite.Group()

for i in range(boosts_max):
    health_png = Sprites("health.png", randint(80, W - 80), -40, 80, 50, randint(1, 5))
    boosts_health.add(health_png)

boosts_cartridges = sprite.Group()
for i in range(boosts_max):
    patron_png = Sprites(
        "cartridges.png", randint(80, W - 80), -40, 80, 50, randint(1, 5)
    )
    boosts_cartridges.add(patron_png)

bullets = sprite.Group()


# отрисовка спрайтов
def draw_sprite():
    main_win.blit(back, (0, 0))
    monsters.draw(main_win)
    boosts_health.draw(main_win)
    boosts_cartridges.draw(main_win)
    bullets.draw(main_win)
    no_break_monsters.draw(main_win)


# движение спрайтов
def move_sprites():
    no_break_monsters.update()
    player.update()
    monsters.update()
    boosts_cartridges.update()
    boosts_health.update()
    bullets.update()
    # boss.update()


# столкновение групп
def collide_group():
    global score, health, patrons
    sprites_list = sprite.groupcollide(bullets, monsters, True, True)
    for f in sprites_list:
        score += 1
        monster = Enemy("ufo.png", randint(80, W - 80), -40, 80, 50, randint(1, 2))
        monsters.add(monster)

    asteroids_list = sprite.groupcollide(bullets, no_break_monsters, True, False)

    asteroid_list = sprite.spritecollide(player, no_break_monsters, True)
    for g in asteroid_list:
        asteroid = Enemy(
            "asteroid.png", randint(80, W - 80), -40, 80, 50, randint(1, 2)
        )
        no_break_monsters.add(asteroid)
        health -= 50

    restore = sprite.spritecollide(player, boosts_health, True)
    for n in restore:
        health_png = Sprites("health.png", randint(80, W - 80), -40, 80, 50, 1)
        boosts_health.add(health_png)
        health += 20

    cartridge = sprite.spritecollide(player, boosts_cartridges, True)
    for m in cartridge:
        patron_png = Sprites(
            "cartridges.png", randint(80, W - 80), -40, 80, 50, randint(1, 5)
        )
        boosts_cartridges.add(patron_png)
        patrons += 5

    lost_list = sprite.spritecollide(player, monsters, True)
    for c in lost_list:
        monster = Enemy("ufo.png", randint(80, W - 80), -40, 80, 50, randint(1, 2))
        monsters.add(monster)
        health -= 25


# текст
def texts():
    text_score = font1.render("Счёт:" + " " + str(score), 1, (255, 255, 255))
    text_lost = font1.render("Пропущено:" + " " + str(lost), 1, (255, 255, 255))
    cartridges = font1.render(str(patrons) + "/" + "20", 1, (255, 255, 255))
    hp = font1.render("Здоровье: " + str(health), 1, (255, 255, 255))
    # u_win = font2.render('ТЫ выиграл!!!', 1, (0, 255, 0))
    main_win.blit(text_score, (10, 20))
    main_win.blit(text_lost, (10, 50))
    main_win.blit(hp, (10, 80))
    main_win.blit(cartridges, (10, 110))


def ifs():
    global health, patrons
    if health <= 100 and health > 75:
        player.image = img1
    elif health <= 75 and health > 50:
        player.image = img2
    elif health <= 50 and health > 25:
        player.image = img3
    elif health <= 25 and health > 0:
        player.image = img4

    # if lost >= 3:
    #     main_win.blit(u_lose, (W//2 - 80, H//2 - 20))
    #     finish = Truе

    if health > 100:
        health = 100

    if patrons > 20:
        patrons = 20

    if patrons < 0:
        patrons = 0

    if health < 0:
        health = 0

    # if boss_flag != True:
    #     sprite.Group.empty(monsters)
    #     sprite.Group.empty(no_break_monsters)


img1 = transform.scale(image.load("rocket_100hp.png"), (100, 120))
img2 = transform.scale(image.load("rocket_75hp.png"), (100, 120))
img3 = transform.scale(image.load("rocket_50hp.png"), (100, 120))
img4 = transform.scale(image.load("rocket_25hp.png"), (130, 150))


FLAG = False


def game():
    global lost, score, FLAG, health, current_time, start_time, finish, time_boss, boss_lost
    mixer.music.load('space.ogg')
    is_music = False
    if not is_music:
        mixer.music.play(-1)
        is_music = True
    ####################
    start_time = perf_counter()
    boss_and_speed_time = timer()
    ####################
    finish = False
    # игровой цикл
    clock = time.Clock()
    game = True
    while game:
        current_time = timer()
        for e in event.get():
            if e.type == QUIT:
                game = False
                is_music = True
                mixer.music.load("menu_music.ogg")
                # screen_flag = True
            elif e.type == KEYDOWN:
                if (
                    e.key == K_SPACE
                    and patrons != 0
                    and float(current_time) - float(start_time) >= 0.50
                ):
                    fire.play()
                    # mixer.fire.set_volume(0.2)
                    player.FIRE()
                    start_time = current_time
        if finish != True:
            FLAG = True
            # отрисовка
            draw_sprite()
            player.reset()
            # boss.reset()

            # движение
            move_sprites()

            # столкновение групп
            collide_group()

            # тексты
            texts()
            u_lose = font2.render("Ты проиграл!!!", 1, (139, 0, 0))

            # условия
            ifs()
            if health <= 0:
                health = 0
                main_win.blit(u_lose, (W // 2 - 80, H // 2 - 20))
                finish = True
            # if int(current_time) - int(boss_and_speed_time) == time_boss or lost >= boss_lost:
            #     print(int(current_time-boss_and_speed_time))
            #     boss_and_speed_time = current_time
            #     sprite.Group.empty(monsters)
            #     sprite.Group.empty(no_break_monsters)
            #     time_boss += current_time
            #     time_boss *= 1.5
            #     boss_lost += lost
            #     boss_lost *= 1.5

        clock.tick(FPS)
        display.update()
