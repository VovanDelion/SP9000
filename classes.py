import pygame


class Player(pygame.sprite.Sprite):
    """Класс управляемого персонажа"""
    def __init__(self, screen_width, screen_height):
        super().__init__()
        self.image = pygame.image.load('sprites/player.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.screen_width = screen_width
        self.rect.x = screen_width / 2
        self.rect.y = screen_height - 30
        self.clock = pygame.time.Clock()
        self.delta_time = self.clock.tick(30)


    def move(self, v):
        """Перемещение персонажа по указанной скорости"""
        self.rect.x += v
        if self.rect.x < 0:
            self.rect.x = 0
        if self.rect.x > self.screen_width - self.rect.width:
            self.rect.x = self.screen_width - self.rect.width

    def get_xy(self):
        """Возвращает координаты персонажа"""
        return self.rect.x + 5, self.rect.y


class Bullet(pygame.sprite.Sprite):
    """Класс пули активного персонажа"""
    def __init__(self, obj, bullets):
        super().__init__(bullets)
        self.image = pygame.image.load('sprites/bullet.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x, self.rect.y =  obj.get_xy()
        self.speed = 10
        self.active = False

    def update(self):
        self.move()

    def move(self):
        """Перемещение пули"""
        self.rect.y -= self.speed

    def draw(self, s):
        s.blit(self.image, self.rect)


class Barrier(pygame.sprite.Sprite):
    """Класс барьера"""
    def __init__(self, obj, barriers):
        super().__init__(barriers)
        self.image = pygame.image.load('sprites/barr.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x, self.rect.y =  obj.get_xy()
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
    def __init__(self, x, y, enemies):
        super().__init__(enemies)
        self.image = pygame.image.load('sprites/enemy.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = x
        self.rect.y = y
        self.speed = 0.1
        self.clock = pygame.time.Clock()
        self.delta_time = self.clock.tick(60)

    def update(self):
        self.move()


    def move(self):
        """Перемещение врага"""
        self.rect.y += self.speed * self.delta_time

