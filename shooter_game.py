# модули
import time 
import pygame
from pygame import *
from random import randint
def game():

    W = 700
    H = 500
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
            bullet = Bullet('bullet.png', self.rect.centerx, self.rect.top, 15, 20, 15)
            bullets.add(bullet)
    class Enemy(GameSprite):
        def update(self):
            global lost 
            self.rect.y += self.speed
            if self.rect.y > H:
                self.rect.y = 0
                self.rect.x = randint(80, W - 80)
                lost += 1 # тут
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
    #Музыка
    mixer.init()
    mixer.music.load('space.ogg')
    mixer.music.play()
    fire = mixer.Sound('fire.ogg')

    # текст
    font.init()
    font1 = font.SysFont('Arial', 28)
    font2 = font.SysFont('Arial', 50)
    # очки
    score  = 0 # сбито
    lost = 0 # пропущено 

    # экран
    FPS = 60
    # pygame.init()
    # main_win = display.set_mode((W, H), FULLSCREEN)
    main_win = display.set_mode((W, H))
    display.set_caption('Шутер')
    back = transform.scale(image.load('sky.jpg'), (W, H))
    #спрайты
    x1, y1 = 200, 200
    x2, y2 = 250, 250
    x3, y3 = 0, 0
    monsters_max = 5 # колл-во монстров на экране
    asteroid_max = 2 # колл-во астероидов на экране
    boosts_max = 1 # колл-во бустов на экране
    player = Player('rocket.png', W//2, H - 110, 80, 100, 5)  
    monsters = sprite.Group()
    for i in range(monsters_max):
        monster = Enemy('ufo.png', randint(80, W - 80), -40, 80, 50, randint(1,2))
        monsters.add(monster)
    no_break_monsters = sprite.Group()
    for i in range(asteroid_max):
        asteroid = Sprites('asteroid.png', randint(80, W - 80), -40, 80, 50, randint(1,2))
        no_break_monsters.add(asteroid)

    flag = False
    restore_hp = sprite.Group()
    for i in range(boosts_max):
        health_png = Sprites('health.png', randint(80, W - 80), -40, 80, 50, randint(1,5))
        restore_hp.add(health_png)
    bullets = sprite.Group()
    health = 100
    # игровой цикл
    clock = time.Clock()
    game = True
    finish = False
    while game:
        for e in event.get():
            if e.type == QUIT:
                game = False
            elif e.type == KEYDOWN:
                if e.key == K_SPACE:
                    fire.play()
                    player.FIRE()
        if finish != True:
            # if health < 75:
            #     player = Player('rocket.png', rect.x, rect.y, 80, 100, 5)  и тут тоже тестовая шняга в минус ушла
            main_win.blit(back, (0, 0))
            # отрисовка
            player.reset()
            monsters.draw(main_win)
            restore_hp.draw(main_win)
            bullets.draw(main_win)
            no_break_monsters.draw(main_win)
            # движение
            no_break_monsters.update()
            player.update()
            monsters.update()
            restore_hp.update()
            bullets.update()
            sprites_list = sprite.groupcollide(bullets, monsters, True, True)
            for f in sprites_list:
                score += 1
                monster = Enemy('ufo.png', randint(80, W - 80), -40, 80, 50, randint(1,2))
                monsters.add(monster)

            asteroids_list = sprite.groupcollide(bullets, no_break_monsters, True,  False)
            asteroid_list = sprite.spritecollide(player, no_break_monsters, True)

            for g in asteroid_list:
                asteroid = Enemy('asteroid.png', randint(80, W - 80), -40, 80, 50, randint(1,2))
                no_break_monsters.add(asteroid)
                health -= 50
            text_score = font1.render('Счёт:' + ' ' + str(score), 1, (255, 255, 255))
            text_lost = font1.render('Пропущено:' + ' ' + str(lost), 1, (255, 255, 255))
            # u_win = font2.render('ТЫ выиграл!!!', 1, (0, 255, 0))
            u_lose = font2.render('Ты проиграл!!!', 1, (139, 0, 0))
            main_win.blit(text_score, (10, 20))
            main_win.blit(text_lost, (10, 50))

            restore = sprite.spritecollide(player, restore_hp, True)
            for n in restore:
                health_png = Sprites('health.png', randint(80, W - 80), -40, 80, 50, 1)
                restore_hp.add(health_png)
                health += 20
            
            # if lost >= 3:
            #     main_win.blit(u_lose, (W//2 - 80, H//2 - 20))
            #     finish = True

            lost_list = sprite.spritecollide(player, monsters, True)
            for c in lost_list:
                monster = Enemy('ufo.png', randint(80, W - 80), -40, 80, 50, randint(1,2))
                monsters.add(monster)
                health -= 25

            if health <= 0:
                health = 0 
                main_win.blit(u_lose, (W//2 - 80, H//2 - 20))
                finish = True

            if health > 100:
                health = 100
            
            # if True:
            #     time.set_timer(pygame.USEREVENT, 15)
            #     boss_flag = False

            # if boss_flag != True:
            #     sprite.Group.empty(monsters) 
            #     sprite.Group.empty(no_break_monsters)
            #     boss_flag = True
                
            hp = font1.render('Здоровье: ' +  str(health), 1, (255, 255, 255))
            main_win.blit(hp, (10, 80))
        clock.tick(FPS)
        display.update()

