import pygame


class Player:
    """Класс управляемого персонажа"""
    def __init__(self, screen_width, screen_height):
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


class Bullet():
    """Класс пули активного персонажа"""
    def __init__(self, player):
        self.image = pygame.image.load('sprites/bullet.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y =  player.get_xy()
        self.speed = 10
        self.active = False


    def move(self):
        """Перемещение пули"""
        self.rect.y -= self.speed

    def draw(self, s):
        s.blit(self.image, self.rect)


class Enemy():
    """Класс врага"""
    def __init__(self, x, y):
        self.image = pygame.image.load('sprites/enemy.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = 0.1
        self.clock = pygame.time.Clock()
        self.delta_time = self.clock.tick(60)

    def move(self):
        """Перемещение врага"""
        self.rect.y += self.speed * self.delta_time