import pygame
import sys

# Инициализация Pygame
pygame.init()

# Константы
WIDTH = 1280  # Ширина окна
HEIGHT = 720  # Высота окна
FPS = 60  # Частота кадров в секунду
WHITE = (255, 255, 255)  # Белый цвет
BLACK = (0, 0, 0)  # Черный цвет
RED = (255, 0, 0)  # Красный цвет
GREEN = (0, 255, 0)  # Зеленый цвет
BLUE = (0, 0, 255)  # Синий цвет
BUTTON_COLOR = (100, 100, 100)  # Цвет кнопки
BUTTON_HOVER_COLOR = (150, 150, 150)  # Цвет кнопки при наведении
BUTTON_WIDTH = 200  # Ширина кнопок
BUTTON_HEIGHT = 50  # Высота кнопок

# Настройки окна
screen = pygame.display.set_mode((WIDTH, HEIGHT))  # Создание окна
try:
    menu_background = pygame.image.load("fonmenu_space_invaders.jpg")  # Загрузка фона
except pygame.error as e:
    print(f"Error loading background image: {e}")
    menu_background = None  # Если не удалось загрузить фон, то он будет None
pygame.display.set_caption("Space Invaders Menu")  # Заголовок окна
clock = pygame.time.Clock()  # Игровые часы

# Шрифты
font = pygame.font.Font(pygame.font.match_font('arial'), 30)  # Шрифт для текста

# Функции для работы с рекордами (пока не используются)
def load_scores():
    # Загрузка рекордов из файла (пока не используется)
    return {"best_score": 0, "last_score": 0}  # Возвращаем начальные значения

def save_scores(scores):
    # Сохранение рекордов в файл (пока не используется)
    pass

# Загрузка рекордов
scores = load_scores()  # Загружаем начальные рекорды
best_score = scores.get("best_score", 0)  # Получаем лучший счет
last_score = scores.get("last_score", 0)  # Получаем последний счет

# Функция для отрисовки текста
def draw_text(surf, text, size, x, y, color):
    font = pygame.font.Font(pygame.font.match_font('arial'), size)  # Загрузка шрифта
    text_surface = font.render(text, True, color)  # Рендеринг текста
    text_rect = text_surface.get_rect()  # Получаем прямоугольник для текста
    text_rect.midtop = (x, y)  # Устанавливаем положение текста
    surf.blit(text_surface, text_rect)  # Рисуем текст на поверхности


# Класс для кнопок
class Button:
    def __init__(self, x, y, width, height, text, action, color=BUTTON_COLOR, hover_color=BUTTON_HOVER_COLOR):
        self.rect = pygame.Rect(x, y, width, height)  # Прямоугольник кнопки
        self.text = text  # Текст кнопки
        self.action = action  # Функция, выполняемая при нажатии
        self.color = color  # Цвет кнопки
        self.hover_color = hover_color  # Цвет кнопки при наведении
        self.is_hovered = False  # Флаг наведения мыши

    def draw(self, surface):
        if self.is_hovered:  # Если мышь наведена на кнопку
            pygame.draw.rect(surface, self.hover_color, self.rect)  # Рисуем кнопку с цветом наведения
        else:
            pygame.draw.rect(surface, self.color, self.rect)  # Рисуем кнопку обычным цветом
        draw_text(surface, self.text, 24, self.rect.centerx, self.rect.y + 10, WHITE)  # Рисуем текст на кнопке

    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:  # Если мышь двигается
            self.is_hovered = self.rect.collidepoint(event.pos)  # Проверяем, наведена ли мышь
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Если нажата левая кнопка мыши
            if self.is_hovered:  # Если мышь наведена на кнопку
                self.action()  # Выполняем действие, связанное с кнопкой

# Функции для действий кнопок
def start_game():
    global best_score, last_score  # Делаем переменные глобальными, чтоб мы могли их изменить
    # Имитация результата игры
    last_score = int(pygame.time.get_ticks() / 1000) % 1000  # Имитация результата игры
    if last_score > best_score:
        best_score = last_score  # Обновляем лучший счет, если новый результат лучше
    scores["best_score"] = best_score  # Сохраняем лучший счет
    scores["last_score"] = last_score  # Сохраняем последний счет
    save_scores(scores)  # Сохраняем рекорды в файл
    print("Запуск игры!")

def open_levels():
    global menu_state  # Делаем переменную глобальной, чтоб мы могли ее изменить
    menu_state = "LEVEL_MENU"  # Переключаем в меню уровней
    print("Открыто меню уровней")

def open_rating():
    global menu_state  # Делаем переменную глобальной, чтоб мы могли ее изменить
    menu_state = "RATING"  # Переключаем в меню рейтинга
    print("Открыто меню рейтинга")

def set_menu_state(state):
    global menu_state  # Делаем переменную глобальной, чтоб мы могли ее изменить
    menu_state = state  # Устанавливаем состояние

def draw_rating_screen():
    screen.fill(BLACK)  # Заполняем экран черным цветом
    draw_text(screen, "Рейтинг", 40, WIDTH // 2, 50, WHITE)  # Заголовок экрана
    draw_text(screen, f"Лучший результат: {best_score}", 30, WIDTH // 2, 150, WHITE)  # Отображение лучшего счета
    draw_text(screen, f"Последняя игра: {last_score}", 30, WIDTH // 2, 200, WHITE)  # Отображение последнего результата
    back_button.draw(screen)  # Кнопка "Назад"

def draw_level_menu():
    screen.fill(BLACK)  # Заполняем экран черным цветом
    draw_text(screen, "Уровни", 40, WIDTH // 2, 50, WHITE)  # Заголовок экрана
    level1_button.draw(screen)  # Отрисовка кнопки уровня 1
    level2_button.draw(screen)  # Отрисовка кнопки уровня 2
    level3_button.draw(screen)  # Отрисовка кнопки уровня 3
    boss_button.draw(screen)  # Отрисовка кнопки уровня с боссом
    back_button.draw(screen)  # Кнопка "Назад"

def load_level(level):
    print(f"Загрузка уровня {level}")
    global menu_state  # Делаем переменную глобальной, чтоб мы могли ее изменить
    menu_state = "MENU"  # Возвращаемся в главное меню


# Создание кнопок
# Кнопки главного меню
play_button = Button(WIDTH // 2 - BUTTON_WIDTH // 2, 200, BUTTON_WIDTH, BUTTON_HEIGHT, "Играть", start_game)
levels_button = Button(WIDTH // 2 - BUTTON_WIDTH // 2, 300, BUTTON_WIDTH, BUTTON_HEIGHT, "Уровни", open_levels)
rating_button = Button(WIDTH // 2 - BUTTON_WIDTH // 2, 400, BUTTON_WIDTH, BUTTON_HEIGHT, "Рейтинг", open_rating)

# Кнопки меню уровней
level1_button = Button(100, HEIGHT // 2 - 70, BUTTON_WIDTH, BUTTON_HEIGHT, "Уровень 1",
                       lambda: load_level(1))
level2_button = Button(400, HEIGHT // 2 - 70, BUTTON_WIDTH, BUTTON_HEIGHT, "Уровень 2",
                       lambda: load_level(2))
level3_button = Button(700, HEIGHT // 2 - 70, BUTTON_WIDTH, BUTTON_HEIGHT, "Уровень 3",
                       lambda: load_level(3))
boss_button = Button(1000, HEIGHT // 2 - 70, BUTTON_WIDTH, BUTTON_HEIGHT, "Босс",
                     lambda: load_level("boss"), RED)

# Кнопка "Назад"
back_button = Button(WIDTH // 2 - BUTTON_WIDTH // 2, 550, BUTTON_WIDTH, BUTTON_HEIGHT, "Назад",
                     lambda: set_menu_state("MENU"))

# Главные переменные
menu_state = "MENU"  # Начальное состояние меню: "MENU", "RATING", "LEVEL_MENU"

# Главный игровой цикл
running = True
while running:
    for event in pygame.event.get():  # Получаем все события
        if event.type == pygame.QUIT:  # Если событие выхода, то выходим
            running = False
        if menu_state == "MENU":  # Если находимся в главном меню
            play_button.handle_event(event)  # Обрабатываем события кнопки "Играть"
            levels_button.handle_event(event)  # Обрабатываем события кнопки "Уровни"
            rating_button.handle_event(event)  # Обрабатываем события кнопки "Рейтинг"
        elif menu_state == "RATING":  # Если находимся в меню рейтинга
            back_button.handle_event(event)  # Обрабатываем события кнопки "Назад"
        elif menu_state == "LEVEL_MENU":  # Если находимся в меню выбора уровней
            level1_button.handle_event(event)  # Обрабатываем события кнопки "Уровень 1"
            level2_button.handle_event(event)  # Обрабатываем события кнопки "Уровень 2"
            level3_button.handle_event(event)  # Обрабатываем события кнопки "Уровень 3"
            boss_button.handle_event(event)  # Обрабатываем события кнопки "Босс"
            back_button.handle_event(event)  # Обрабатываем события кнопки "Назад"

    # Отрисовка
    if menu_background:  # Если загружен фон, то рисуем его
        screen.blit(menu_background, (0, 0))
    else:
        screen.fill(BLACK)  # Иначе, заливаем экран черным цветом

    if menu_state == "MENU":  # Если находимся в главном меню
        play_button.draw(screen)  # Рисуем кнопку "Играть"
        levels_button.draw(screen)  # Рисуем кнопку "Уровни"
        rating_button.draw(screen)  # Рисуем кнопку "Рейтинг"
    elif menu_state == "RATING":  # Если находимся в меню рейтинга
        draw_rating_screen()  # Рисуем экран рейтинга
    elif menu_state == "LEVEL_MENU":  # Если находимся в меню выбора уровней
        draw_level_menu()  # Рисуем меню выбора уровней

    pygame.display.flip()  # Обновляем экран
    clock.tick(FPS)  # Контроль FPS

pygame.quit()  # Выход из Pygame
sys.exit()  # Выход из системы