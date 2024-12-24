import pygame
import classes as c
from classes import Bullet

if __name__ == "__main__":
    pygame.init()

    screen_width = 600
    screen_height = 600
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("SP9000")
    player_v = 5

    player = c.Player(screen_width, screen_height)
    delta_time = 0
    bullets = []
    running = True
    clock = pygame.time.Clock()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bullets.append(Bullet(player))

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player.move(-player_v)
        elif keys[pygame.K_RIGHT]:
            player.move(player_v)

        for bullet in bullets[:]:
            bullet.move()
        screen.fill((0, 0, 0))
        screen.blit(player.image, player.rect)

        for bullet in bullets:
            bullet.draw(screen)
        clock.tick(30)
        pygame.display.update()