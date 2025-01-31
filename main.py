import random
import pygame
import classes as c
import sqlite3


def game():
    pygame.init()

    conn = sqlite3.connect('db/score.sqlite')
    cursor = conn.cursor()

    screen_width = 600
    screen_height = 600
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("SP9000")
    map_name = "level_1"

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

    boss = pygame.sprite.Group()
    bossBullet = pygame.sprite.Group()
    tentacle = pygame.sprite.Group()
    peaks = pygame.sprite.Group()
    at = pygame.sprite.Group()
    bosss = c.Boss(screen_width // 2, 50, boss, bossBullet, tentacle, at, peaks, player)

    last_line = c.LastLine()
    ls.add(last_line)
    # [c.Enemy(i, 90, enemies, ebullets) for i in range(100, 500, 90)]
    [c.Base(i, 510, bases) for i in range(40, 550, 110)]
    # c.Enemy2(250, 60, enemies, ebullets)
    # c.Enemy2(350, 60, enemies, ebullets)
    # c.Enemy3(screen_width // 2, 0, enemies, elasers)
    score = 0

    font_name = pygame.font.match_font('arial')
    def draw_text(surf, text, size, x, y, color=(255, 255, 255)):
        font = pygame.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        surf.blit(text_surface, text_rect)

    def draw_hp_bar(surf, x, y, pct, color, piecies):
        if pct < 0:
            pct = 0
        BAR_LENGTH = 200
        BAR_HEIGHT = 20
        fill = (pct / piecies) * BAR_LENGTH
        outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
        fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
        pygame.draw.rect(surf, color, fill_rect)
        pygame.draw.rect(surf, (255, 255, 255), outline_rect, 2)

    def win():
        screen.fill((0, 0, 0))
        draw_text(screen, "Ура победа!", 64, screen_width / 2, screen_height / 2.5)
        draw_text(screen, f"Ваш результат: {score}", 32, screen_width / 2, screen_height / 1.8)
        pygame.display.flip()
        pygame.time.delay(3000)

    def lose():
        screen.fill((0, 0, 0))
        draw_text(screen, "Ты проиграл!", 64, screen_width / 2, screen_height / 2.5, "red")
        pygame.display.flip()
        pygame.time.delay(3000)

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
        if keys[pygame.K_SPACE]:
            player.perecat()
        if buttons[0]:
            if player.power == 4:
                player.shoot()

        pygame.mouse.set_visible(False)

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

        boss.update()
        boss.draw(screen)
        bossBullet.update()
        bossBullet.draw(screen)
        tentacle.update()
        tentacle.draw(screen)
        peaks.update()
        peaks.draw(screen)
        at.update()
        at.draw(screen)

        bases.update()
        bases.draw(screen)

        power.update()
        power.draw(screen)

        portals.update()
        portals.draw(screen)

        hits = pygame.sprite.spritecollide(player, power, True)
        for hit in hits:
            player.power_sound.play()
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
        hits3 = pygame.sprite.spritecollide(player, tentacle, False)
        for hit in hits3:
            player.hp -= 5
            player.damage_sound.play()
            if hit.type == "right":
                player.rect.centerx += 20
            else:
                player.rect.centerx -= 20
        hits4 = pygame.sprite.spritecollide(player, bossBullet, False)
        for hit in hits4:
            if hit.type == "bLaser":
                player.hp -= 25
                player.damage_sound.play()
            else:
                player.hp -= 10
                hit.kill()
                player.damage_sound.play()
        hits5 = pygame.sprite.spritecollide(player, peaks, True)
        for hit in hits5:
            player.hp -= 50
            player.damage_sound.play()

        col = pygame.sprite.groupcollide(enemies, bullets, True, True)
        for hit in col:
            if hit.lv == 1 or hit.lv == 2:
                score += 50
            elif hit.lv == 3:
                score += 100
            if random.random() > 0.1:
                power.add(c.Pow(hit.rect.center))

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
        col6 = pygame.sprite.groupcollide(bases, tentacle, False, False)
        for hit in col6:
            hit.rect.centerx += 20
        col8 = pygame.sprite.groupcollide(boss, bullets, False, True)
        for hit in col8:
            hit.hp -= 10
        col9 = pygame.sprite.groupcollide(bossBullet, barriers, False, True)
        for hit in col9:
            if hit.type == "bLaser":
                pass
            else:
                hit.kill()
        col9 = pygame.sprite.groupcollide(ls, enemies, False, True)
        for hit in col9:
            player.hp -= 200

        pygame.sprite.groupcollide(ebullets, barriers, True, True)
        pygame.sprite.groupcollide(at, tentacle, True, False)

        draw_text(screen, str(score), 18, 20, 50)
        draw_text(screen, str(pygame.time.get_ticks()), 18, 20, 70)

        if not (enemies or boss):
            win()
            running = False

        draw_hp_bar(screen, screen_width // 4 - 140, 5, player.hp, 'green', 500)
        draw_hp_bar(screen, 390, 5, bosss.hp, 'red', 1000)
        if player.hp <= 0:
            lose()
            running = False
        clock.tick(30)
        pygame.display.update()

    cursor.execute(f"""insert into score (score, map) values ({score}, '{map_name}')""")
    conn.commit()
    conn.close()