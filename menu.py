import sqlite3
import pygame
import sys
import main


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
pygame.display.set_caption("Space Invaders Menu")
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


def start_game():
    main.game()


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
    last_score = cursor.execute("""select * from score where id = (SELECT max(id) FROM score)""").fetchone()
    best_score = cursor.execute("""select * from score where score = (SELECT MAX(score) FROM score)""").fetchone()
    conn.close()
    draw_text(screen, "Рейтинг", 40, WIDTH // 2, 50, WHITE)
    draw_text(screen, f"Лучший результат: {best_score}", 30, WIDTH // 2, 150, WHITE)
    draw_text(screen, f"Последняя игра: {last_score}", 30, WIDTH // 2, 200, WHITE)
    back_button.draw(screen)


play_button = Button(WIDTH // 2 - 100, 200, 200, 50, "Играть", start_game)  # Кнопка Играть
settings_button = Button(WIDTH // 2 - 100, 300, 200, 50, "Настройки", open_settings)  # Кнопка Настройки
rating_button = Button(WIDTH // 2 - 100, 400, 200, 50, "Рейтинг", open_rating)  # Кнопка Рейтинг
back_button = Button(WIDTH // 2 - 100, 500, 200, 50, "Назад", lambda: set_menu_state("MENU"))  # Кнопка "Назад" в меню


def set_menu_state(state):
    global menu_state
    menu_state = state

menu_state = "MENU"

running = True

while running:
    # screen.blit(menu_background, (0, 0))
    clock.tick(FPS)
    pygame.mouse.set_visible(True)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if menu_state == "MENU":
            play_button.handle_event(event)
            settings_button.handle_event(event)
            rating_button.handle_event(event)
        elif menu_state == "RATING":
            back_button.handle_event(event)

    if menu_state == "MENU":
        # screen.blit(menu_background, (0, 0))
        screen.fill(BLACK)
        draw_text(screen, "Space Invaders Menu", 60, WIDTH // 2, 50, WHITE)  # Заголовок меню
        play_button.draw(screen)
        settings_button.draw(screen)
        rating_button.draw(screen)
    elif menu_state == "RATING":  # Если в рейтинге
        draw_rating_screen()

    pygame.display.flip()

pygame.quit()
sys.exit()