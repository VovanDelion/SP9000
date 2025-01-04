import random
import pygame


p_images = dict()
p_images['rem'] = 'sprites/rem.png'
p_images['el_pow'] = 'sprites/electro_pow.png'
p_images['port'] = 'sprites/portal_pow.png'
p_images['laser'] = 'sprites/laser_pow.png'
p_images['dbull'] = 'sprites/dbull_pow.png'

POWERUP_TIME = 5000
PORTAL_TIME = 10000

class Player(pygame.sprite.Sprite):
    """Класс управляемого персонажа"""
    def __init__(self, screen_width, screen_height, bullets, barr):
        super().__init__()
        self.image = pygame.image.load('sprites/player.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.screen_width = screen_width
        self.rect.x = screen_width / 2
        self.rect.y = screen_height - 30
        self.bullets = bullets
        self.barr = barr
        self.last_shot = 0
        self.shoot_delay = 300
        self.power = 4
        self.power_time = pygame.time.get_ticks()
        self.clock = pygame.time.Clock()
        self.delta_time = self.clock.tick(30)

    def update(self):
        if self.power == 4 and pygame.time.get_ticks() - self.power_time > POWERUP_TIME:
            self.power = 1
            self.power_time = pygame.time.get_ticks()
        elif self.power == 3 and pygame.time.get_ticks() - self.power_time > POWERUP_TIME:
            self.power = 1
            self.power_time = pygame.time.get_ticks()
        elif self.power == 2 and pygame.time.get_ticks() - self.power_time > POWERUP_TIME:
            self.power = 1
            self.power_time = pygame.time.get_ticks()

    def move(self, v):
        """Перемещение персонажа по указанной скорости"""
        self.rect.x += v
        if self.rect.x < 0:
            self.rect.x = 0
        if self.rect.x > self.screen_width - self.rect.width:
            self.rect.x = self.screen_width - self.rect.width

    def electrup(self):
        self.power = 2
        self.power_time = pygame.time.get_ticks()

    def laserup(self):
        self.power = 3
        self.power_time = pygame.time.get_ticks()

    def dbullup(self):
        self.power = 4
        self.power_time = pygame.time.get_ticks()

    def shoot(self):
        if self.power == 3:
            b = Bullet(self.rect.centerx - 1, self.rect.centery)
            b.image = pygame.image.load('sprites/laser.png').convert_alpha()
            b.rect.y -= 6
            self.bullets.add(b)
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            if self.power == 1:
                bullet = Bullet(self.rect.centerx, self.rect.top)
                self.bullets.add(bullet)
            elif self.power == 2:
                b1 = Bullet(self.rect.centerx - 7, self.rect.centery)
                b1.image = pygame.image.load('sprites/electro_bull.png').convert_alpha()
                b1.speedx = -10
                b1.image = pygame.transform.rotate(b1.image, 30)
                b2 = Bullet(self.rect.centerx - 1, self.rect.centery)
                b2.image = pygame.image.load('sprites/electro_bull.png').convert_alpha()
                b3 = Bullet(self.rect.centerx + 5, self.rect.centery)
                b3.image = pygame.image.load('sprites/electro_bull.png').convert_alpha()
                b3.image = pygame.transform.rotate(b3.image, -30)
                b3.speedx = 10
                self.bullets.add(b1)
                self.bullets.add(b2)
                self.bullets.add(b3)
            elif self.power == 4:
                b1 = DoubleB(self.rect.centerx - 1, self.rect.centery, -1)
                b2 = DoubleB(self.rect.centerx - 1, self.rect.centery, 1)
                self.bullets.add(b1)
                self.bullets.add(b2)

    def deffen(self):
        self.barr.add(Barrier(self.rect.centerx - 1, self.rect.y))


class Pow(pygame.sprite.Sprite):
    """Класс бафов для игрока"""
    def __init__(self, center):
        super().__init__()
        self.type = random.choice(['rem', 'el_pow', 'port', 'laser', 'dbull'])
        self.image = pygame.image.load(p_images[self.type]).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.speedy = 3

    def update(self):
        self.rect.y += self.speedy
        if self.rect.top > 600:
            self.kill()


class Portal(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load('sprites/portal.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x, self.rect.y = x, y
        self.life_time = pygame.time.get_ticks()

    def update(self):
        if pygame.time.get_ticks() - self.life_time > PORTAL_TIME:
            self.kill()


class Bullet(pygame.sprite.Sprite):
    """Класс пули активного персонажа"""
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load('sprites/bullet.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x, self.rect.y = self.start_x, _ =  x, y
        self.speedy = 20
        self.speedx = 0

    def update(self):
        self.move()
        if self.rect.top <= 0:
            self.kill()

    def move(self):
        """Перемещение пули"""
        self.rect.y -= self.speedy
        self.rect.x += self.speedx

class DoubleB(Bullet):
    """Класс двойной пули активного персонажа"""
    def __init__(self, x, y, vec):
        super().__init__(x, y)
        self.image = pygame.image.load("sprites/dbull.png")
        self.speedy = 10
        self.speedx = 3
        self.speedx *= vec

    def update(self):
        self.move()
        if self.rect.x <= self.start_x - 10:
            self.speedx = -self.speedx
        elif self.rect.x >= self.start_x + 8:
            self.speedx = -self.speedx
        if self.rect.top <= 0:
            self.kill()

class EBullet(pygame.sprite.Sprite):
    """Класс пули вражеского персонажа"""
    def __init__(self, obj, ebullets):
        super().__init__(ebullets)
        self.image = pygame.image.load('sprites/ebullet.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x, self.rect.y =  obj.get_xy()
        self.speed = 6

    def update(self):
        self.move()
        if self.rect.top > 600:
            self.kill()

    def move(self):
        """Перемещение пули"""
        self.rect.y += self.speed

class Barrier(pygame.sprite.Sprite):
    """Класс барьера"""
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load('sprites/barr.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x, self.rect.y =  x, y
        self.rect.x -= 5
        self.speed = 10

    def update(self):
        self.move()

    def move(self):
        self.rect.y -= self.speed


class Base(pygame.sprite.Sprite):
    """Класс базы"""
    def __init__(self, x, y, bases):
        super().__init__(bases)
        self.image = pygame.image.load('sprites/wall.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.hp = 100
        self.rect.x = x
        self.rect.y = y

    def update(self):
        if self.hp <= 100:
            self.image = pygame.image.load('sprites/wall.png').convert_alpha()
        if self.hp <= 80:
            self.image = pygame.image.load('sprites/wall1.png').convert_alpha()
        if self.hp <= 50:
            self.image = pygame.image.load('sprites/wall2.png').convert_alpha()
        if self.hp <= 20:
            self.image = pygame.image.load('sprites/wall3.png').convert_alpha()
        if self.hp <= 0:
            self.image = pygame.image.load('sprites/wall4.png').convert_alpha()


class Enemy(pygame.sprite.Sprite):
    """Класс врага"""
    def __init__(self, x, y, enemies, eb):
        super().__init__(enemies)
        self.image = pygame.image.load('sprites/enemy.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.eb = eb
        self.rect.x = x
        self.rect.y = y
        self.speedx = 0.15
        self.speedy = 0.1
        self.last_shot = 0
        self.shoot_delay = 1400
        self.power_time = pygame.time.get_ticks()
        self.clock = pygame.time.Clock()
        self.delta_time = self.clock.tick(60)

    def update(self):
        self.move()
        self.shoot()

    def move(self):
        """Перемещение врага"""
        self.rect.y += self.speedy * self.delta_time
        self.rect.x += self.speedx * self.delta_time
        if self.rect.x >= 600 or self.rect.x <= 0:
            self.speedx = -self.speedx


    def shoot(self):
        """Стрельба врага"""
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            EBullet(self, self.eb)

    def get_xy(self):
        """Возвращает координаты персонажа"""
        return self.rect.x + 5, self.rect.y

