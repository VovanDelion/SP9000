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
    elasers = pygame.sprite.Group()
    bases = pygame.sprite.Group()
    barriers = pygame.sprite.Group()
    power = pygame.sprite.Group()
    portals = pygame.sprite.Group()
    ls = pygame.sprite.Group()

    player = c.Player(screen_width, screen_height, bullets, barriers)
    player_v = 5

    last_line = c.LastLine()
    ls.add(last_line)
    [c.Enemy(i, 90, enemies, ebullets) for i in range(100, 500, 90)]
    [c.Base(i, 510, bases) for i in range(40, 550, 110)]
    c.Enemy2(250, 60, enemies, ebullets)
    c.Enemy2(350, 60, enemies, ebullets)
    c.Enemy3(screen_width // 2, 0, enemies, elasers)

    score = 0

    font_name = pygame.font.match_font('arial')
    def draw_text(surf, text, size, x, y):
        font = pygame.font.Font(font_name, size)
        text_surface = font.render(text, True, (255, 255, 255))
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        surf.blit(text_surface, text_rect)

    def draw_shield_bar(surf, x, y, pct):
        if pct < 0:
            pct = 0
        BAR_LENGTH = 200
        BAR_HEIGHT = 20
        fill = (pct / 500) * BAR_LENGTH
        outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
        fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
        pygame.draw.rect(surf, (0, 255, 0), fill_rect)
        pygame.draw.rect(surf, (255, 255, 255), outline_rect, 2)

    def win():
        screen.fill((0, 0, 0))
        draw_text(screen, "Ура победа!", 64, screen_width / 2, screen_height / 2.5)
        draw_text(screen, f"Ваш результат: {score}", 32, screen_width / 2, screen_height / 1.8)
        pygame.display.flip()
        pygame.time.delay(3000)
        pygame.quit()

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
        buttons = pygame.mouse.get_pressed()
        if keys[pygame.K_a]:
            player.move(-player_v)
        elif keys[pygame.K_d]:
            player.move(player_v)
        if buttons[0]:
            if player.power == 3:
                player.shoot()

        screen.fill((0, 0, 0))
        screen.blit(player.image, player.rect)
        player.update()

        bullets.update()
        bullets.draw(screen)

        barriers.update()
        barriers.draw(screen)

        ebullets.update()
        ebullets.draw(screen)
        elasers.update()
        elasers.draw(screen)

        enemies.update()
        enemies.draw(screen)

        bases.update()
        bases.draw(screen)

        power.update()
        power.draw(screen)

        portals.update()
        portals.draw(screen)

        col = pygame.sprite.groupcollide(enemies, bullets, True, True)
        for hit in col:
            if hit.lv == 1 or hit.lv == 2:
                score += 50
            elif hit.lv == 3:
                score += 100
            if random.random() > 0.1:
                power.add(c.Pow(hit.rect.center))

        hits = pygame.sprite.spritecollide(player, power, True)
        for hit in hits:
            if hit.type == 'rem':
                for b in bases:
                    b.hp += 20
                    if b.hp > 100:
                        b.hp = 100
            elif hit.type == 'el_pow':
                player.electrup()
            elif hit.type == 'laser':
                player.laserup()
            elif hit.type == 'dbull':
                player.dbullup()
            elif hit.type == 'port':
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
        col3 = pygame.sprite.groupcollide(ls, ebullets, False, True)
        for hit in col3:
            player.hp -= 5
        col4 = pygame.sprite.groupcollide(bases, elasers, False, True)
        for hit in col4:
            hit.hp -= 15
        col5 = pygame.sprite.groupcollide(ls, elasers, False, True)
        for hit in col5:
            player.hp -= 15

        pygame.sprite.groupcollide(ebullets, barriers, True, True)
        draw_text(screen, str(score), 18, 20, 10)
        draw_text(screen, str(pygame.time.get_ticks()), 18, 20, 30)

        if not enemies:
            win()
            running = False

        draw_shield_bar(screen, screen_width // 2 - 100, 5, player.hp)
        if player.hp <= 0:
            player.kill()
            running = False
        clock.tick(30)
        pygame.display.update()