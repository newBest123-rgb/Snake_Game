import pygame
import pygame_menu
import sys
import random

pygame.mixer.pre_init(44100, -16, 1, 512)

bg_image = pygame.image.load("logo_snake.png")
WHITE = pygame.Color("white")
RED = pygame.Color("red")
SIZE_BLOCK = 20
COUNT_BLOCKS = 20
BLUE = (204, 255, 255)
HEADER_COLOR = (0, 204, 153)
SNAKE_COLOR = (0, 102, 0)
MARGIN = 1
HEADER_MARGIN = 70
FRAME_COLOR = (0, 255, 204)
snake_block = [[1, 2], [3, 4]]

if __name__ == "__main__":
    pygame.init()

    size = (
        SIZE_BLOCK * COUNT_BLOCKS + 2 * SIZE_BLOCK + MARGIN * COUNT_BLOCKS,
        SIZE_BLOCK * COUNT_BLOCKS
        + 2 * SIZE_BLOCK
        + MARGIN * SIZE_BLOCK
        + HEADER_MARGIN,
    )
    print(size)
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("Питон")
    timer = pygame.time.Clock()
    TNR = pygame.font.SysFont("Times New Roman", 36)

    pygame.mixer.music.load("Snake Music.mp3")
    pygame.mixer.music.play(-1)

    Apple_Music = pygame.mixer.Sound("Apple Music.mp3")
    Game_Over_Music = pygame.mixer.Sound("Game_Over Music.mp3")

    class SnakeBlock:
        def __init__(self, x, y):
            self.x = x
            self.y = y

        def is_inside(self):
            return 0 <= self.x < COUNT_BLOCKS and 0 <= self.y < COUNT_BLOCKS

        def __eq__(self, other):
            return (
                isinstance(other, SnakeBlock)
                and self.x == other.x
                and self.y == other.y
            )

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
        def get_random_empty_block():
            x = random.randint(0, COUNT_BLOCKS - 1)
            y = random.randint(0, COUNT_BLOCKS - 1)
            empty_block = SnakeBlock(x, y)
            while empty_block in snake_blocks:
                empty_block.x = random.randint(0, COUNT_BLOCKS - 1)
                empty_block.y = random.randint(0, COUNT_BLOCKS - 1)
            return empty_block

        snake_blocks = [SnakeBlock(9, 10)]
        apple = get_random_empty_block()
        d_row = buf_row = 0
        d_col = buf_col = 1
        total = 0
        speed = 1

        running = True

        while running:
            for even in pygame.event.get():
                if even.type == pygame.QUIT:
                    print("exit")
                    pygame.quit()
                    sys.exit()
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

            screen.fill(FRAME_COLOR)
            pygame.draw.rect(screen, HEADER_COLOR, [0, 0, size[0], HEADER_MARGIN])

            text_total = TNR.render(f"Счёт: {total}", True, WHITE)
            text_speed = TNR.render(f"Скорость: {speed}", True, WHITE)
            screen.blit(text_total, (SIZE_BLOCK, SIZE_BLOCK))
            screen.blit(text_speed, (SIZE_BLOCK + 200, SIZE_BLOCK))

            for row in range(COUNT_BLOCKS):
                for column in range(COUNT_BLOCKS):
                    if (row + column) % 2 == 0:
                        color = BLUE
                    else:
                        color = WHITE

                    draw_block(color, row, column)

            head = snake_blocks[-1]
            if not head.is_inside():
                Game_Over_Music.play()
                print("crash")
                break

            draw_block(RED, apple.x, apple.y)
            for block in snake_blocks:
                draw_block(SNAKE_COLOR, block.x, block.y)

            pygame.display.flip()

            if apple == head:
                total += 1
                speed = total // 5 + 1
                snake_blocks.append(apple)
                apple = get_random_empty_block()
                Apple_Music.play()

            d_row = buf_row
            d_col = buf_col
            new_head = SnakeBlock(head.x + d_row, head.y + d_col)

            if new_head in snake_blocks:
                Game_Over_Music.play()
                print("Врезался сам в себя")
                break

            snake_blocks.append(new_head)
            snake_blocks.pop(0)

            timer.tick(3 + speed)

        save_score_to_file(name.get_value(), total)

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

        if menu.is_enabled():
            menu.update(events)
            menu.draw(screen)

        pygame.display.update()
