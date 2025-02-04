import sqlite3
import pygame
import sys
import main
import classes as c


pygame.init()

WIDTH = 600
HEIGHT = 600
FPS = 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BUTTON_COLOR = (100, 100, 100)
BUTTON_HOVER_COLOR = (150, 150, 150)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
# menu_background = pygame.image.load("fonmenu_space_invaders.jpg")
pygame.display.set_caption("Space Invaders")
clock = pygame.time.Clock()

font = pygame.font.Font(pygame.font.match_font('arial'), 30)

def load_scores():
    return dict()

def save_scores():
    pass


def draw_text(surf, text, size, x, y, color):
    font = pygame.font.Font(pygame.font.match_font('arial'), size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)


class Button:
    def __init__(self, x, y, width, height, text, action, color=BUTTON_COLOR, hover_color=BUTTON_HOVER_COLOR):
        self.rect = pygame.Rect(x, y, width, height)  # Прямоугольник кнопки
        self.text = text  # Текст
        self.action = action  # Функция при нажатии
        self.color = color  # Цвет
        self.hover_color = hover_color  # Цвет при наведении
        self.is_hovered = False  # Флаг для отслеживания наведения мыши


    def draw(self, surface):
        if self.is_hovered:  # Если мышь наведена, то рисуем цветом наведения
            pygame.draw.rect(surface, self.hover_color, self.rect)
        else:  # Иначе рисуем обычным цветом
            pygame.draw.rect(surface, self.color, self.rect)
        draw_text(surface, self.text, 24, self.rect.centerx, self.rect.y + 10, WHITE)  # Рисуем текст кнопки


    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.is_hovered = self.rect.collidepoint(event.pos)  # Проверяем, наведена ли мышь
        if event.type == pygame.MOUSEBUTTONDOWN:  # Если нажали кнопку мыши
            if event.button == 1 and self.is_hovered:  # Если это левая кнопка и мышь наведена
                self.action()  # Вызываем связанную функцию

def open_levels():
    global menu_state  # Делаем переменную глобальной, чтоб мы могли ее изменить
    menu_state = "LEVEL_MENU"  # Переключаем в меню уровней
    print("Открыто меню уровней")

def load_level(level):
    print(f"Загрузка уровня {level}")
    global menu_state  # Делаем переменную глобальной, чтоб мы могли ее изменить
    menu_state = "MENU"

def open_settings():
    print("Настройки")


def open_rating():
    global menu_state  # Делаем menu_state глобальной
    menu_state = "RATING"  # Переключаемся в состояние рейтинга
    print("Рейтинг")


def draw_rating_screen():
    screen.fill(BLACK)
    conn = sqlite3.connect('db/score.sqlite')
    cursor = conn.cursor()
    last_scores = cursor.execute("""select map, score from score""").fetchall()
    best_score = cursor.execute("""select map, score from score where score = (SELECT MAX(score) FROM score)""").fetchone()
    conn.close()
    draw_text(screen, "Рейтинг", 40, WIDTH // 2, 50, WHITE)
    draw_text(screen, f"Лучший результат:", 30, WIDTH // 2, 100, "yellow")
    draw_text(screen, f"Уровень {best_score[0]}, очков {best_score[1]}", 30, WIDTH // 2, 150, WHITE)
    draw_text(screen, f"Последнии игры:", 30, WIDTH // 2, 200, WHITE)
    draw_text(screen, f"Уровень               Очки", 30, WIDTH // 2, 250, WHITE)
    h = 300
    for i in last_scores[::-1]:
        draw_text(screen, '                  '.join(str(x) for x in i), 30, WIDTH // 2, h, WHITE)
        h += 50
        if h == 500:
            break
    back_button.draw(screen)

def draw_level_menu():
    """
    Отрисовывает меню выбора уровня.
    """
    screen.fill(BLACK)  # Заполняем экран черным цветом
    draw_text(screen, "Уровни", 40, WIDTH // 2, 50, WHITE)  # Заголовок экрана
    level1_button.draw(screen)  # Отрисовка кнопки уровня 1
    level2_button.draw(screen)  # Отрисовка кнопки уровня 2
    level3_button.draw(screen)  # Отрисовка кнопки уровня 3
    boss_button.draw(screen)  # Отрисовка кнопки уровня с боссом
    back_button.draw(screen)  # Кнопка "Назад"


play_button = Button(WIDTH // 2 - 100, 200, 200, 50, "Играть", open_levels)  # Кнопка Играть
rating_button = Button(WIDTH // 2 - 100, 300, 200, 50, "Рейтинг", open_rating)  # Кнопка Рейтинг
back_button = Button(WIDTH // 2 - 100, 500, 200, 50, "Назад", lambda: set_menu_state("MENU"))  # Кнопка "Назад" в меню

level1_button = Button(WIDTH // 2 - 100, 100, 200, 50, "Уровень 1",
                       lambda: main.lv1())
level2_button = Button(WIDTH // 2 - 100, 200, 200, 50, "Уровень 2",
                       lambda: main.lv2())
level3_button = Button(WIDTH // 2 - 100, 300, 200, 50, "Уровень 3",
                       lambda: main.lv3())
boss_button = Button(WIDTH // 2 - 100, 400, 200, 50, "Босс",
                     lambda: main.game(), "red", (255, 150, 150))


def set_menu_state(state):
    global menu_state
    menu_state = state

menu_state = "MENU"

running = True

all_sprites = pygame.sprite.Group()
all_sprites.add(c.anim_guy((WIDTH // 2), 450))

while running:
    # screen.blit(menu_background, (0, 0))
    clock.tick(FPS)
    pygame.mouse.set_visible(True)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if menu_state == "MENU":
            play_button.handle_event(event)
            rating_button.handle_event(event)
        elif menu_state == "RATING":
            back_button.handle_event(event)
        elif menu_state == "LEVEL_MENU":  # Если находимся в меню выбора уровней
            level1_button.handle_event(event)  # Обрабатываем события кнопки "Уровень 1"
            level2_button.handle_event(event)  # Обрабатываем события кнопки "Уровень 2"
            level3_button.handle_event(event)  # Обрабатываем события кнопки "Уровень 3"
            boss_button.handle_event(event)  # Обрабатываем события кнопки "Босс"
            back_button.handle_event(event)

    if menu_state == "MENU":
        # screen.blit(menu_background, (0, 0))
        screen.fill(BLACK)
        draw_text(screen, "Space Invaders", 60, WIDTH // 2, 50, GREEN)  # Заголовок меню
        draw_text(screen, "9000", 60, WIDTH // 2, 110, GREEN)
        play_button.draw(screen)
        rating_button.draw(screen)
        all_sprites.update()
        all_sprites.draw(screen)
    elif menu_state == "RATING":  # Если в рейтинге
        draw_rating_screen()
    elif menu_state == "LEVEL_MENU":  # Если находимся в меню выбора уровней
        draw_level_menu()


    pygame.display.flip()
    clock.tick(30)
    pygame.display.update()

pygame.quit()
sys.exit()