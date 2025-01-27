import random
import pygame
import math


def calculate_angle(player_pos, target_pos):
    dx = target_pos[0] - player_pos[0]
    dy = target_pos[1] - player_pos[1]
    angle = math.atan2(dy, dx)
    angle_degrees = math.degrees(angle)
    return angle_degrees


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
        self.shoot_sound = pygame.mixer.Sound('saunds/player_shoot.mp3')
        self.damage_sound = pygame.mixer.Sound('saunds/player_damage.mp3')
        self.power_sound = pygame.mixer.Sound('saunds/power_up.mp3')
        self.hp = 500
        self.bullets = bullets
        self.barr = barr
        self.last_shot = 0
        self.shoot_delay = 300
        self.last_perecat = 0
        self.perecat_dalat = 800
        self.power = 1
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
        if self.power == 4:
            self.image = pygame.image.load('sprites/laser_player.png').convert_alpha()
        elif self.power == 3:
            self.image = pygame.image.load('sprites/db_player.png').convert_alpha()
        elif self.power == 2:
            self.image = pygame.image.load('sprites/electro_player.png').convert_alpha()
        elif self.power == 1:
            self.image = pygame.image.load('sprites/player.png').convert_alpha()
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
        self.power = 4
        self.power_time = pygame.time.get_ticks()

    def dbullup(self):
        self.power = 3
        self.power_time = pygame.time.get_ticks()

    def shoot(self):
        if self.power == 4:
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
                self.shoot_sound.play()
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
            elif self.power == 3:
                b1 = DoubleB(self.rect.centerx - 1, self.rect.centery, -1)
                b1.rect.y -= 7
                b2 = DoubleB(self.rect.centerx - 1, self.rect.centery, 1)
                self.bullets.add(b1)
                self.bullets.add(b2)

    def deffen(self):
        self.barr.add(Barrier(self.rect.centerx - 1, self.rect.y))

    def perecat(self):
        now = pygame.time.get_ticks()
        if now - self.last_perecat > self.perecat_dalat:
            self.last_perecat = now
            keys = pygame.key.get_pressed()
            if keys[pygame.K_a]:
                self.rect.centerx -= 40
            if keys[pygame.K_d]:
                self.rect.centerx += 40


class LastLine(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.rect = pygame.Rect(0, 600, 600, 1)


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
        if self.rect.bottom > 600:
            self.kill()


class Portal(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load('sprites/portal.png').convert_alpha()
        self.image = pygame.transform.scale(self.image,
                                            (self.image.get_width() * 2, self.image.get_height() * 2))
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
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load('sprites/ebullet.png').convert_alpha()
        self.type = "standart"
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.centerx, self.rect.y =  x, y
        self.speed = 6

    def update(self):
        self.move()
        if self.rect.top > 600:
            self.kill()

    def move(self):
        """Перемещение пули"""
        self.rect.y += self.speed


class BossLaser(EBullet):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.image = pygame.image.load('sprites/laser.png').convert_alpha()
        self.image = pygame.transform.scale(self.image,
                                            (self.image.get_width() * 10, self.image.get_height() * 20))
        self.image = pygame.transform.flip(self.image, False, True)
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.centerx, self.rect.y = x, y
        self.speed = 25
        self.type = "bLaser"


class Barrier(pygame.sprite.Sprite):
    """Класс барьера"""
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load('sprites/barr.png').convert_alpha()
        self.image = pygame.transform.scale(self.image,
                                            (self.image.get_width() * 2, self.image.get_height() * 1))
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.centerx, self.rect.y =  x + 1, y
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
        self.image = pygame.transform.scale(self.image,
                                            (self.image.get_width() * 4, self.image.get_height() * 2))
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.hp = 100
        self.rect.x = x
        self.rect.y = y

    def update(self):
        if self.hp <= 100:
            self.image = pygame.image.load('sprites/wall.png').convert_alpha()
            self.image = pygame.transform.scale(self.image,
                                                (self.image.get_width() * 4, self.image.get_height() * 2))
        if self.hp <= 80:
            self.image = pygame.image.load('sprites/wall1.png').convert_alpha()
            self.image = pygame.transform.scale(self.image,
                                                (self.image.get_width() * 4, self.image.get_height() * 2))
        if self.hp <= 60:
            self.image = pygame.image.load('sprites/wall2.png').convert_alpha()
            self.image = pygame.transform.scale(self.image,
                                                (self.image.get_width() * 4, self.image.get_height() * 2))
        if self.hp <= 40:
            self.image = pygame.image.load('sprites/wall3.png').convert_alpha()
            self.image = pygame.transform.scale(self.image,
                                                (self.image.get_width() * 4, self.image.get_height() * 2))
        if self.hp <= 20:
            self.image = pygame.image.load('sprites/wall4.png').convert_alpha()
            self.image = pygame.transform.scale(self.image,
                                                (self.image.get_width() * 4, self.image.get_height() * 2))
        if self.hp <= 0:
            self.kill()
        if self.rect.left > 600:
            self.kill()


class Enemy(pygame.sprite.Sprite):
    """Класс врага"""
    def __init__(self, x, y, enemies, eb):
        super().__init__(enemies)
        self.image = pygame.image.load('sprites/enemy.png').convert_alpha()
        self.image = pygame.transform.scale(self.image,
                                            (self.image.get_width() * 2, self.image.get_height() * 2))
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.shoot_sound = pygame.mixer.Sound('saunds/enemy_shoot.mp3')
        self.lv = 1
        self.eb = eb
        self.rect.x = x
        self.rect.y = y
        self.speedx = 0
        self.speedy = 0.1
        self.last_shot = 0
        self.shoot_delay = 1400
        self.clock = pygame.time.Clock()
        self.delta_time = self.clock.tick(60)

    def update(self):
        self.move()
        self.shoot()

    def move(self):
        """Перемещение врага"""
        self.rect.y += self.speedy * self.delta_time
        self.rect.x += self.speedx * self.delta_time
        if self.rect.right >= 500 or self.rect.left <= 100:
            self.speedx = -self.speedx

    def shoot(self):
        """Стрельба врага"""
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            if self.lv == 1:
                self.eb.add(EBullet(self.rect.centerx, self.rect.centery))
                self.shoot_sound.play()
            elif self.lv == 2:
                self.eb.add(EBullet(self.rect.centerx, self.rect.centery))
                self.eb.add(EBullet(self.rect.centerx, self.rect.centery + 10))
                self.shoot_sound.play()


class Enemy2(Enemy):
    def __init__(self, x, y, enemies, eb):
        super().__init__(x, y, enemies, eb)
        self.image = pygame.image.load('sprites/enemy2.png').convert_alpha()
        self.image = pygame.transform.scale(self.image,
                                            (self.image.get_width() * 3, self.image.get_height() * 2))
        self.lv = 2
        self.shoot_delay = 2400


class Enemy3(Enemy):
    def __init__(self, x, y, enemies, eb):
        super().__init__(x, y, enemies, eb)
        self.image = pygame.image.load('sprites/enemy3.png').convert_alpha()
        self.image = pygame.transform.scale(self.image,
                                            (self.image.get_width() * 2, self.image.get_height() * 2))
        self.laser_shoot_sound = pygame.mixer.Sound('saunds/enemy_laser_shoot.mp3')
        self.lv = 3
        self.shoot_delay = 1800

    def shoot(self):
        """Стрельба врага"""
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            self.laser_shoot_sound.play()
            b = EBullet(self.rect.centerx + 7, self.rect.centery)
            b.image = b.image = pygame.image.load('sprites/laser.png').convert_alpha()
            b.image = pygame.transform.flip(b.image, False, True)
            self.eb.add(b)


class Boss(pygame.sprite.Sprite):
    def __init__(self, x, y, boss, eb, tent, at, peaks, player):
        super().__init__(boss)
        self.image = pygame.image.load('sprites/Boss.png').convert_alpha()
        self.image = pygame.transform.scale(self.image,
                                            (self.image.get_width() * 30, self.image.get_height() * 15))
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.spawn_sound = pygame.mixer.Sound('saunds/boss_spawn.mp3')
        self.shoot_sound = pygame.mixer.Sound('saunds/enemy_shoot.mp3')
        self.laser_shoot_sound = pygame.mixer.Sound('saunds/enemy_laser_shoot.mp3')
        self.eb = eb
        self.at = at
        self.tent = tent
        self.peaks = peaks
        self.player = player
        self.rect.centerx = x
        self.rect.centery = y
        self.hp = 1000
        self.speedx = 0
        self.speedy = 0
        self.last_shot = 2600
        self.shoot_delay = 1400
        self.last_tent = 0
        self.tent_delay = 4000
        self.last_peaks = 0
        self.peaks_delay = 6000
        self.laser_charge = 0
        self.clock = pygame.time.Clock()
        self.delta_time = self.clock.tick(60)
        t = Tentacle(20, 480)
        self.tent.add(t)
        self.spawn_sound.play()

    def update(self):
        if self.laser_charge >= 6 and self.hp <= 750:
            self.laser_charge = 0
            self.eb.add(BossLaser(self.rect.centerx, self.rect.centery))
            self.laser_shoot_sound.play()
        else:
            now = now2 = pygame.time.get_ticks()
            if now2 - self.last_shot > self.shoot_delay and self.hp > 500:
                self.last_shot = now2
                self.eb.add(EBullet(self.rect.centerx, self.rect.centery + 30))
                self.eb.add(EBullet(self.rect.left + 70, self.rect.centery + 30))
                self.eb.add(EBullet(self.rect.right - 70, self.rect.centery + 30))
                self.shoot_sound.play()
            if now2 - self.last_shot > self.shoot_delay and (250 < self.hp <= 500):
                self.last_shot = now2
                self.eb.add(EBullet(self.rect.centerx, self.rect.centery + 30))
                self.eb.add(EBullet(self.rect.right - 70, self.rect.centery + 30))
                self.shoot_sound.play()
            if now2 - self.last_shot > self.shoot_delay and self.hp <= 250:
                self.last_shot = now2
                self.eb.add(EBullet(self.rect.centerx, self.rect.centery + 30))
                self.shoot_sound.play()
            if now - self.last_tent > self.tent_delay:
                i = random.randint(0,2)
                if now - self.last_tent > self.tent_delay:
                    if  i == 0:
                        if now - self.last_tent > self.tent_delay:
                            self.last_tent = now
                            t = Tentacle(20, 500)
                            t.destroy_point = 400
                            self.tent.add(t)
                            self.laser_charge += 1
                    elif i == 1:
                        if now - self.last_tent > self.tent_delay:
                            self.last_tent = now
                            t = Tentacle(580, 500)
                            t.image = pygame.transform.flip(t.image, True, False)
                            t.type = "left"
                            t.speed = -10
                            t.destroy_point = 200
                            self.tent.add(t)
                            self.laser_charge += 1
                if now - self.last_peaks > self.peaks_delay:
                    self.last_peaks = now
                    self.peaks.add(Peak(150, 150, self.player))
                    self.peaks.add(Peak(450, 150, self.player))

            if self.hp <= 750:
                self.image = pygame.image.load('sprites/Boss_laser.png').convert_alpha()
                self.image = pygame.transform.scale(self.image,
                                                    (self.image.get_width() * 30, self.image.get_height() * 15))
            if self.hp <= 500:
                self.image = pygame.image.load('sprites/hl_boss.png').convert_alpha()
                self.image = pygame.transform.scale(self.image,
                                                    (self.image.get_width() * 30, self.image.get_height() * 15))
            if self.hp <= 250:
                self.image = pygame.image.load('sprites/ql_boss.png').convert_alpha()
                self.image = pygame.transform.scale(self.image,
                                                    (self.image.get_width() * 30, self.image.get_height() * 15))
            if self.hp <= 0:
                self.kill()


class Tentacle(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load('sprites/tentacle.png').convert_alpha()
        self.image = pygame.transform.scale(self.image,
                                            (self.image.get_width() * 1, self.image.get_height() * 3))
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.centerx = x
        self.rect.centery = y
        self.sound = pygame.mixer.Sound("saunds/tent_sound.mp3")
        self.type = "right"
        self.speed = 10
        self.destroy_point = 800
        self.sound.play()


    def update(self):
        self.rect.x += self.speed
        if self.speed > 0:
            if self.rect.right > self.destroy_point:
                self.kill()
        if self.speed < 0:
            if self.rect.left <= self.destroy_point:
                self.kill()


class Peak(pygame.sprite.Sprite):
    def __init__(self, x, y, player):
        super().__init__()
        self.image = pygame.image.load('sprites/peak.png').convert_alpha()
        self.image = pygame.transform.scale(self.image,
                                            (self.image.get_width() * 3, self.image.get_height() * 3))
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.sound = pygame.mixer.Sound("saunds/peak_spawn.mp3")
        self.shoot_sound = pygame.mixer.Sound("saunds/peak_shoot.mp3")
        self.rect.centerx = x
        self.rect.centery = y
        self.speed = 0
        self.last_shot = pygame.time.get_ticks()
        self.shoot_delay = 2000
        self.player = player
        player_x, player_y = self.player.rect.center
        self.angle = math.atan2(player_y - self.rect.centery, player_x - self.rect.centerx)
        self.sound.play()

    def update(self):
        now = pygame.time.get_ticks()
        self.move_toward_player()
        if now - self.last_shot > self.shoot_delay:
            self.shoot_sound.play()
            self.speed = 40
        else:
            self.rotate_toward_player()
            player_x, player_y = self.player.rect.center
            self.angle = math.atan2(player_y - self.rect.centery, player_x - self.rect.centerx)
        if self.rect.top >= 600:
            self.kill()

    def rotate_toward_player(self):
        self.image = pygame.transform.rotate(pygame.image.load('sprites/peak.png').convert_alpha(),
                                             -math.degrees(self.angle) + 90)
        self.rect = self.image.get_rect(center=self.rect.center)

    def move_toward_player(self):
        self.rect.x += self.speed * math.cos(self.angle)
        self.rect.y += self.speed * math.sin(self.angle)


class Atention(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load('sprites/atent.png').convert_alpha()
        self.image = pygame.transform.scale(self.image,
                                            (self.image.get_width() * 1, self.image.get_height() * 1))
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.centerx = x
        self.rect.centery = y
        self.life_time = pygame.time.get_ticks()

    def update(self):
        if self.life_time == 2000:
            self.kill()