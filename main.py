import random
import pygame
import classes as c


if __name__ == "__main__":
    pygame.init()

    screen_width = 600
    screen_height = 600
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("SP9000")

    player = c.Player(screen_width, screen_height)
    player_v = 5

    bullets = pygame.sprite.Group()
    enemies = pygame.sprite.Group()
    ebullets = pygame.sprite.Group()
    bases = pygame.sprite.Group()
    barriers = pygame.sprite.Group()

    [c.Enemy(i, 0, enemies) for i in range(50, 550, 100)]
    [c.Base(i, 510, bases) for i in range(100, 550, 128)]

    score = 0

    font_name = pygame.font.match_font('arial')
    def draw_text(surf, text, size, x, y):
        font = pygame.font.Font(font_name, size)
        text_surface = font.render(text, True, (255, 255, 255))
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        surf.blit(text_surface, text_rect)

    delta_time = 0
    running = True
    clock = pygame.time.Clock()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    c.Bullet(player, bullets)
                if event.button == 3:
                    c.Barrier(player, barriers)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            player.move(-player_v)
        elif keys[pygame.K_d]:
            player.move(player_v)

        screen.fill((0, 0, 0))
        screen.blit(player.image, player.rect)

        bullets.update()
        bullets.draw(screen)

        barriers.update()
        barriers.draw(screen)

        ebullets.update()
        ebullets.draw(screen)

        enemies.update()
        enemies.draw(screen)
        for enemy in enemies:
            if pygame.time.get_ticks() % 200 == 0:
                c.EBullet(enemy, ebullets)

        bases.update()
        bases.draw(screen)

        col = pygame.sprite.groupcollide(bullets, enemies, True, True)
        for hit in col:
            score += 50

        col1 = pygame.sprite.groupcollide(bases, enemies, False, True)
        for hit in col1:
            hit.hp -= 5
        col2 = pygame.sprite.groupcollide(bases, ebullets, False, True)
        for hit in col2:
            hit.hp -= 5

        pygame.sprite.groupcollide(ebullets, barriers, True, True)

        draw_text(screen, str(score), 18, 20, 10)
        draw_text(screen, str(pygame.time.get_ticks()), 18, 20, 30)
        clock.tick(30)
        pygame.display.update()