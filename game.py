import pygame
import pygame_menu
import sys
import random

# инициализируем модуль pygame, для обработки воспроизведения звука

bg_image = pygame.image.load("logo_snake.png")
WHITE = pygame.Color("white")
RED = pygame.Color("red")
SIZE_BLOCK = 20  # размер каждого блока
COUNT_BLOCKS = 20  # кол-во блоков

BLUE = (204, 255, 255)
SNAKE_COLOR = (0, 102, 0)

FRAME_COLOR = (0, 255, 204)
HEADER_COLOR = (0, 204, 153)
HEADER_MARGIN = 70


MARGIN = 1
snake_block = [
    [1, 2],
    [3, 4],
]  # список содержит два списка, представляющие начальные позиции блоков snake

if __name__ == "__main__":
    pygame.init()

    size = (460, 530)
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("Питон")
    timer = pygame.time.Clock()  # таймер для управления частотой кадров
    TNR = pygame.font.SysFont("Times New Roman", 36)  # шрифт

    pygame.mixer.music.load("Snake Music.mp3")  # фоновая музыка
    pygame.mixer.music.play(-1)

    Apple_Music = pygame.mixer.Sound("Apple Music.mp3")  # музыка поедания яблока
    Game_Over_Music = pygame.mixer.Sound("Game_Over Music.mp3")  # музыка проигрыша

    class SnakeBlock:
        def __init__(self, x, y):
            self.x = x
            self.y = y

        # Функция для проверки, не вышла ли змейка за поля
        def is_inside(self):
            return 0 <= self.x < COUNT_BLOCKS and 0 <= self.y < COUNT_BLOCKS

        def __eq__(self, other):
            return (
                isinstance(other, SnakeBlock)
                and self.x == other.x
                and self.y == other.y
            )

    # рисуем блок
    def draw_block(color, row, column):
        pygame.draw.rect(
            screen,
            color,
            [
                SIZE_BLOCK + column * SIZE_BLOCK + MARGIN * (column + 1),
                HEADER_MARGIN + SIZE_BLOCK + row * SIZE_BLOCK + MARGIN * (row + 1),
                SIZE_BLOCK,
                SIZE_BLOCK,
            ],
        )

    def save_score_to_file(names, total):
        with open("scores.txt", "a") as file:
            file.write(f"Имя: {names}, Результат: {total}\n")

    def start_the_game():
        # Функция с помощью которой яблоко появляется на поле постоянно в рандомном месте
        def get_random_empty_block():
            x = random.randint(0, COUNT_BLOCKS - 1)
            y = random.randint(0, COUNT_BLOCKS - 1)
            apple_block = SnakeBlock(x, y)
            while apple_block in snake_blocks:
                apple_block.x = random.randint(0, COUNT_BLOCKS - 1)
                apple_block.y = random.randint(0, COUNT_BLOCKS - 1)
            return apple_block

        snake_blocks = [SnakeBlock(9, 10)]  # Голова змейки
        apple = get_random_empty_block()

        # переменные для считывания событий на клавиатуре
        d_row = buf_row = 0
        d_col = buf_col = 1
        total = 0  # результат змейки
        speed = 1  # скорость змейки

        running = True

        while running:
            for even in pygame.event.get():
                if even.type == pygame.QUIT:
                    print("Выход")
                    pygame.quit()
                    sys.exit()

                # Считываем события с клавиатуры
                elif even.type == pygame.KEYDOWN:
                    if even.key == pygame.K_UP and d_col != 0:
                        buf_row = -1
                        buf_col = 0
                    elif even.key == pygame.K_DOWN and d_col != 0:
                        buf_row = 1
                        buf_col = 0
                    elif even.key == pygame.K_RIGHT and d_row != 0:
                        buf_row = 0
                        buf_col = 1
                    elif even.key == pygame.K_LEFT and d_row != 0:
                        buf_row = 0
                        buf_col = -1
            d_row = buf_row
            d_col = buf_col

            screen.fill(FRAME_COLOR)
            pygame.draw.rect(screen, HEADER_COLOR, [0, 0, size[0], HEADER_MARGIN])

            # Выводим на экран результат и скорость змейки
            text_total = TNR.render(f"Счёт: {total}", True, WHITE)
            text_speed = TNR.render(f"Скорость: {speed}", True, WHITE)
            screen.blit(text_total, (SIZE_BLOCK, SIZE_BLOCK))
            screen.blit(text_speed, (SIZE_BLOCK + 200, SIZE_BLOCK))

            # Рисуем квадратики в шахматном порядке
            for row in range(COUNT_BLOCKS):
                for column in range(COUNT_BLOCKS):
                    if (row + column) % 2 == 0:
                        color = BLUE
                    else:
                        color = WHITE

                    draw_block(color, row, column)

            head = snake_blocks[-1]  # Назначаем голову змейки

            # Проверка на выход змейки за поле
            if not head.is_inside():
                Game_Over_Music.play()
                print("Вышел за поле")
                break

            # назначаем первоначальное направление змейки (вправо)
            draw_block(RED, apple.x, apple.y)
            for block in snake_blocks:
                draw_block(SNAKE_COLOR, block.x, block.y)

            pygame.display.flip()

            # проверка на поедание яблока
            if apple == head:
                total += 1
                speed = total // 5 + 1
                snake_blocks.append(apple)
                apple = get_random_empty_block()
                Apple_Music.play()

            new_head = SnakeBlock(head.x + d_row, head.y + d_col)

            if new_head in snake_blocks:
                Game_Over_Music.play()
                print("Врезался сам в себя")
                break

            snake_blocks.append(new_head)
            snake_blocks.pop(0)

            timer.tick(3 + speed)  # Увеличение скорости змейки

        save_score_to_file(name.get_value(), total)  # аргументы для сохранения в .txt

    # Создаем меню
    main_theme = pygame_menu.themes.THEME_DARK.copy()
    main_theme.set_background_color_opacity(0.6)  # Прозрачность меню

    menu = pygame_menu.Menu("Game_Snake", 300, 220, theme=main_theme)

    name = menu.add.text_input("Имя :", default="Игрок 1")
    menu.add.button("Играть", start_the_game)
    menu.add.button("Выход", pygame_menu.events.EXIT)

    while True:
        screen.blit(bg_image, (0, 0))

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                exit()

        if menu.is_enabled():  # проверяем включено ли меню
            menu.update(events)
            menu.draw(screen)  # рисуем меню

        pygame.display.update()
