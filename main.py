import random
import pygame
import classes as c


if __name__ == "__main__":
    pygame.init()

    screen_width = 600
    screen_height = 600
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("SP9000")

    bullets = pygame.sprite.Group()
    enemies = pygame.sprite.Group()
    ebullets = pygame.sprite.Group()
    bases = pygame.sprite.Group()
    barriers = pygame.sprite.Group()
    power = pygame.sprite.Group()
    portals = pygame.sprite.Group()

    player = c.Player(screen_width, screen_height, bullets, barriers)
    player_v = 5

    [c.Enemy(i, 0, enemies, ebullets) for i in range(50, 550, 100)]
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
                    player.shoot()
                if event.button == 3:
                    player.deffen()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            player.move(-player_v)
        elif keys[pygame.K_d]:
            player.move(player_v)

        screen.fill((0, 0, 0))
        screen.blit(player.image, player.rect)
        player.update()

        bullets.update()
        bullets.draw(screen)

        barriers.update()
        barriers.draw(screen)

        ebullets.update()
        ebullets.draw(screen)

        enemies.update()
        enemies.draw(screen)

        bases.update()
        bases.draw(screen)

        power.update()
        power.draw(screen)

        portals.update()
        portals.draw(screen)

        col = pygame.sprite.groupcollide(bullets, enemies, True, True)
        for hit in col:
            score += 50
            if random.random() > 0.1:
                power.add(c.Pow(hit.rect.center))

        hits = pygame.sprite.spritecollide(player, power, True)
        for hit in hits:
            if hit.type == 'rem':
                for b in bases:
                    b.hp += 20
                    if b.hp > 100:
                        b.hp = 100
            if hit.type == 'el_pow':
                player.powerup()
            if hit.type == 'port':
                p1 = c.Portal(20, 560)
                p2 = c.Portal(580, 560)
                p2.image = pygame.transform.flip(p2.image, True, False)
                portals.add(p1)
                portals.add(p2)

        hits2 = pygame.sprite.spritecollide(player, portals, False)
        for hit in hits2:
            if hit == p1:
                player.rect.x = p2.rect.x - 15
            if hit == p2:
                player.rect.x = p1.rect.x + 15

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