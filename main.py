import pygame

import classes as c


if __name__ == "__main__":
    pygame.init()

    screen_width = 800
    screen_height = 800
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("SP9000")

    player = c.Player()

    running = True
    clock = pygame.time.Clock()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player.rect.x -= player.speed
                    if player.rect.x <= 0:
                        player.rect.x = 0
                elif event.key == pygame.K_RIGHT:
                    player.rect.x += player.speed
                    if player.rect.x >= screen_width - player.rect.width:
                        player.rect.x = screen_width - player.rect.width

        screen.fill((0, 0, 0))
        screen.blit(player.image, player.rect)
        clock.tick(60)
        pygame.display.update()