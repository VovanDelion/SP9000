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


    [c.Enemy(i, 0, enemies) for i in range(50, 450, 100)]

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
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    c.Bullet(player, bullets)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player.move(-player_v)
        elif keys[pygame.K_RIGHT]:
            player.move(player_v)

        screen.fill((0, 0, 0))
        screen.blit(player.image, player.rect)

        bullets.update()
        bullets.draw(screen)

        enemies.update(bullets)
        enemies.draw(screen)

        col = pygame.sprite.groupcollide(bullets, enemies, True, True)
        for hit in col:
            score += 50

        draw_text(screen, str(score), 18, 20, 10)

        clock.tick(30)
        pygame.display.update()