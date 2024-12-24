import pygame


class Player:
    def __init__(self):
        self.image = pygame.image.load('sprites/player.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 792
        self.speed = 5

    def move(self, booli):
        if booli:
            self.rect.x += self.speed
        else:
            self.rect.x -= self.speed
