import pygame
import sys
import random

pygame.init()

#КОНСТАНТЫ ОКНА ПРОГРАММЫ
SIZE_OF_WINDOW = WIDTH_OF_WINDOW, HEIGHT_OF_WINDOW = 800, 600       #размер окна
WINDOW_ICON = 'icon.png'                                            #иконка
WINDOW_CAPTION = 'Snake-Game'                                       #название окна

#КОНСТАНТЫ ИГРОВОГО ПОЛЯ
BLOCK_SIZE = 20                                     #размер квадратика
WALL_BLOCKS = 3                                     #количество блоков в стене 
AMOUNT_OF_RECTS = 20                                #количество квадратиков
SIZE_X = (WIDTH_OF_WINDOW // BLOCK_SIZE  - WALL_BLOCKS * 2)     #количество блоков поля по X
SIZE_Y = (HEIGHT_OF_WINDOW // BLOCK_SIZE - WALL_BLOCKS * 2)     #количество блоков поля по Y
AMOUNT_OF_BLOCKS = SIZE_X * SIZE_Y                  #количество блоков

#КОНСТАНТЫ ОТРИСОВКИ ИГРЫ
START_SNAKE_X = SIZE_X // 2                         #X_0 координата головы змейки
START_SNAKE_Y = SIZE_Y // 2                         #Y_0 координата головы змейки
APPLE_RADIUS = BLOCK_SIZE // 2                      #радиус яблока
HALF_BLOCK_SIZE = BLOCK_SIZE // 2                   #половина размера квадратика
THREE_QUARTERS_BLOCK_SIZE = BLOCK_SIZE * 3 / 4      #три четверти размера квадратика
QUARTER_BLOCK_SIZE = BLOCK_SIZE // 4                #четверть размера квадратика
BORDERS_SIZE = BLOCK_SIZE * WALL_BLOCKS             #размер границ


#КОНСТАНТЫ ИГРОВОГО ПРОЦЕССА
INITIAL_APPLES_COUNT = 3                            #постоянное количество яблок
INITIAL_GAME_SPEED  = 5                             #начальная скорость игры
INITIAL_SNAKE_SIZE = 3                              #начальный размер змейки
MAX_GAME_SPEED = 15                                 #максимальная скорость игры
APPLES_TO_INCREASE_SPEED = SIZE_X * SIZE_Y // MAX_GAME_SPEED // 5    #количество яблок для увеличения скорости

# КОНСТАНТЫ ЦВЕТОВ ИГРЫ
WALLS_COLOR = (34, 139, 34)                     # цвет стен (более мягкий зелёный)
GAME_FIELD_COLOR = (240, 255, 240)              # цвет игрового поля (мягкий зелёный)
GAME_FIELD_ADD_COLOR = (220, 225, 220)          # цвет клеток (темный серый)
SNAKE_COLOR = (50, 205, 50)                     # цвет змейки (светло-зелёный)
APPLE_COLOR = (255, 69, 0)                      # цвет яблока (оранжево-красный)

# КОНСТАНТЫ ТЕКСТА
CAPTION_FONT_COLOR = (255, 255, 255)
TEXT_FONT_COLOR = (255, 255, 255)
CAPTION_FONT_SIZE = BLOCK_SIZE * (WALL_BLOCKS + 1)  # размер шрифта заголовка
CAPTION_FONT = pygame.font.SysFont('roboto', CAPTION_FONT_SIZE)  # шрифт заголовка
TEXT_FONT_SIZE = BLOCK_SIZE * 2  # размер шрифта текста
TEXT_FONT = pygame.font.SysFont('roboto', TEXT_FONT_SIZE)  # шрифт текста

# КОНСТАНТЫ БЛОКИ
SNAKE_X_SEGMENT = (HALF_BLOCK_SIZE, QUARTER_BLOCK_SIZE)     #размер сегмента змейки по OX
SNAKE_Y_SEGMENT = (QUARTER_BLOCK_SIZE, HALF_BLOCK_SIZE)     #размер сегмента змейки по OY

############## 1. ФУНКЦИИ БЛОКА MAIN

### 1.1 Инициализация программы
def initialize_program():
    #pygame.init()
    pygame.display.set_caption(WINDOW_CAPTION)                  #название окна 
    icon = pygame.image.load(WINDOW_ICON)                       #загрузка иконки
    pygame.display.set_icon(icon)                               #установка иконки
    screen_of_game = pygame.display.set_mode(SIZE_OF_WINDOW)    #инициализация окна
    clock = pygame.time.Clock()                                 #инициализация clock для стабильности             

    return screen_of_game, clock

### 1.2 Инициализация состояния игры
def initialize_game_state():
    game_state = {
        "program_running": True,
        "game_running": False,
        "game_paused": False,
        "game_won": False,
        "game_over": False,
        "apples": [],
        "snake": [],
        "direction": None,
        "last_direction": None,
        "score": 0,
        "apples_eaten": 0,
        "game_speed": INITIAL_GAME_SPEED
    }
    return game_state

### 1.3 Завершение игры
def perform_ending_actions():
    pygame.quit()
    sys.exit()


############## 2. ФУНКЦИИ состояния игры

### 2.1 Получение событий игры
def get_game_events():
    events = []                                 #список всех событий
    for event in pygame.event.get():            #получаем событие
        if event.type == pygame.QUIT:           #если событие - выход
            events.append('quit')
        elif event.type == pygame.KEYDOWN:      #если событие - нажатие клавиши
            if event.key == pygame.K_UP:        #вверх
                events.append('up')
            elif event.key == pygame.K_DOWN:    #вниз
                events.append('down')
            elif event.key == pygame.K_LEFT:    #влево
                events.append('left')
            elif event.key == pygame.K_RIGHT:   #вправо
                events.append('right')
            elif event.key == pygame.K_RETURN:  #Enter
                events.append('enter')
            elif event.key == pygame.K_SPACE:   #пробел
                events.append('space')
            elif event.key == pygame.K_ESCAPE:  #ESC
                events.append('escape')
             
    return events

### 2.2 Обновление состояния игры внутри программы
def update_game_state(game_state, events):
    process_keys_events(game_state, events)             #обработать нажатия клавиш
    if game_state["game_running"] and not game_state["game_paused"]:# если игра запущена и не на паузе
        move_snake(game_state)                          # передвинуть змейку
        check_collisions(game_state)                    # проверить столкновения
        check_eat_apple(game_state)                     # проверить съедание яблока
        check_game_won(game_state)                      # проверить выигрыш

### 2.2.1 Обработка событий нажатия клавиш
def process_keys_events(game_state, events):
    if "quit" in events:                                #если событие - выход
        game_state["program_running"] = False
    elif not game_state["game_running"] and not game_state["game_over"]:#если игра не запущена
        if "escape" in events:                          #если нажата ESC
            game_state["program_running"] = False
        elif "enter" in events:                         #если нажата Enter
            initialize_new_game(game_state)             #начать новую игру
            game_state["game_running"] = True
    elif game_state["game_paused"] == True:             #если игра на паузе
        if "escape" in events:                          #если нажата ESC
            game_state["game_running"] = False
        elif "space" in events:                         #если нажата пробел
            game_state["game_paused"] = False
    elif game_state["game_over"]:
        if "escape" in events:                          #если нажата ESC
            game_state["program_running"] = False
        elif "enter" in events:                         #если нажата Enter
            game_state["game_over"] = False
            game_state["game_running"] = True
            initialize_new_game(game_state)             #начать новую игру

    else:                                               #игра запущена
        if "escape" in events or "space" in events:     #если нажата пауза
            game_state["game_paused"] = True
        for direction in ['down', 'up', 'right', 'left']:  #движение змейки
            if direction in events:                      #если нажата клавиша движения
                game_state["direction"] = direction
                break
            else:
                game_state["direction"] = game_state["last_direction"]

### 2.2.1.1 Начать новую игру
def initialize_new_game(game_state):
    # положение змейки
    game_state["snake"] = []
    place_snake(INITIAL_SNAKE_SIZE, game_state)
    # положение яблок
    game_state["apples"] = []
    place_apples(INITIAL_APPLES_COUNT, game_state)
    # направление движения змейки
    game_state["direction"] = 'right'
    game_state["last_direction"] = 'right'
    # состояние игры
    game_state["game_paused"] = False
    game_state["game_over"] = False
    game_state["game_speed"] = INITIAL_GAME_SPEED  
    # сколько очков
    game_state["score"] = 0

### 2.2.1.1.1 Разместить змейку
def place_snake(length, game_state):
    x = START_SNAKE_X
    y = START_SNAKE_Y
    game_state["snake"].append((x, y))
    for i in range(1, length):
        game_state["snake"].append((x - i, y))

### 2.2.1.1.2 Разместить яблоки
def place_apples(amount, game_state):
    for i in range(amount):
        x = random.randint(0, SIZE_X - 1)
        y = random.randint(0, SIZE_Y - 1)
        while (x, y) in game_state["apples"] or (x, y) in game_state["snake"]:
            x = random.randint(0, SIZE_X - 1)
            y = random.randint(0, SIZE_Y - 1)
        game_state["apples"].append((x, y))

### 2.2.2 Передвинуть змейку
def move_snake(game_state):
    if game_state["direction"] == "up" and game_state["last_direction"] != "down":
        x_dir, y_dir = get_x_y_directions("up")
        game_state["last_direction"] = "up"
    elif game_state["direction"] == "down" and game_state["last_direction"] != "up":
        x_dir, y_dir = get_x_y_directions("down")
        game_state["last_direction"] = "down"
    elif game_state["direction"] == "left" and game_state["last_direction"] != "right":
        x_dir, y_dir = get_x_y_directions("left")
        game_state["last_direction"] = "left"
    elif game_state["direction"] == "right" and game_state["last_direction"] != "left":
        x_dir, y_dir = get_x_y_directions("right")
        game_state["last_direction"] = "right"
    else:
        x_dir, y_dir = get_x_y_directions(f"{game_state['last_direction']}")
    head = game_state["snake"][0]
    new_head = (head[0] + x_dir, head[1] + y_dir)
    game_state["snake"].insert(0, new_head)
    game_state["snake"].pop()

### 2.2.2.1 Расшифровать движения
def get_x_y_directions(forward):
    if forward == "right":
        return (1, 0)
    elif forward == "left":
        return (-1, 0)
    elif forward == "up":
        return (0, -1)
    elif forward == "down":
        return (0, 1)
    
### 2.2.3 Проверить столкновения
def check_collisions(game_state):
    x_head, y_head = game_state["snake"][0]
    if x_head < 0 or x_head >= SIZE_X or y_head < 0 or y_head >= SIZE_Y:
        game_state["game_running"] = False
        game_state["game_over"] = True
    if len(game_state["snake"]) > len(set(game_state["snake"])):
        game_state["game_running"] = False
        game_state["game_over"] = True

### 2.2.4 Проверить съедание яблока
def check_eat_apple(game_state):
    x_head, y_head = game_state["snake"][0]
    if (x_head, y_head) in game_state["apples"]:
        game_state["apples"].remove((x_head, y_head))
        game_state["snake"].append((x_head, y_head))
        place_apples(1, game_state)
        game_state["score"] += 1
        game_state["apples_eaten"] += 1
        if (game_state["game_speed"] < MAX_GAME_SPEED) and (game_state["apples_eaten"] % APPLES_TO_INCREASE_SPEED) == 0:
            game_state["game_speed"] += 1

### 2.2.5 Проверить выигрыш
def check_game_won(game_state):
    if AMOUNT_OF_BLOCKS - len(game_state["snake"]) == 0:
        game_state["game_won"] = True
        game_state["game_running"] = False

### 2.3 Отрисовка состояния игры
def update_game_screen(screen_of_game, game_state):
    screen_of_game.fill(GAME_FIELD_COLOR)
    if not game_state["game_running"] and not game_state["game_over"]:
        draw_new_game_screen(screen_of_game)
    elif game_state["game_won"]:
        draw_game_won_screen(screen_of_game)
    elif game_state["game_over"]:
        draw_game_over_screen(screen_of_game)
    else:
        draw_game_field(screen_of_game)
        draw_snake(screen_of_game, game_state["snake"], game_state["direction"])
        draw_apples(screen_of_game, game_state["apples"])
        draw_score(screen_of_game, game_state["score"])
        if game_state["game_paused"]:
            draw_paused_screen(screen_of_game)
        draw_walls(screen_of_game)
    pygame.display.update()

######ТЕСТ Отрисовать Игровое поле
def draw_game_field(screen_of_game):
    for column in range(SIZE_X):
        for row in range(SIZE_Y):
            rect = pygame.Rect(BORDERS_SIZE + column * BLOCK_SIZE, BORDERS_SIZE + row * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)
            if (column + row) % 2 == 0:
                pygame.draw.rect(screen_of_game, GAME_FIELD_COLOR, rect)
            else:
                pygame.draw.rect(screen_of_game, GAME_FIELD_ADD_COLOR, rect)    

### 2.3.1 Отрисовать Новая игра
def draw_new_game_screen(screen_of_game):
    screen_of_game.fill(WALLS_COLOR)
    newgame_caption_text = CAPTION_FONT.render("Змейка", True, CAPTION_FONT_COLOR)
    start_game_text = TEXT_FONT.render("Нажмите Enter для начала игры", True, TEXT_FONT_COLOR)
    exit_text = TEXT_FONT.render("Нажмите Escape для выхода", True, TEXT_FONT_COLOR)

    newgame_caption_rect = newgame_caption_text.get_rect(center=(SIZE_OF_WINDOW[0] // 2, SIZE_OF_WINDOW[1] // 3))
    start_game_rect = start_game_text.get_rect(center=(SIZE_OF_WINDOW[0] // 2, SIZE_OF_WINDOW[1] // 2))
    exit_rect = exit_text.get_rect(center=(SIZE_OF_WINDOW[0] // 2, SIZE_OF_WINDOW[1] // 1.5))

    screen_of_game.blit(newgame_caption_text, newgame_caption_rect)
    screen_of_game.blit(start_game_text, start_game_rect)
    screen_of_game.blit(exit_text, exit_rect)

### 2.3.2 Отрисовать Пауза
def draw_paused_screen(screen_of_game):
    overlay = pygame.Surface((SIZE_OF_WINDOW))
    overlay.set_alpha(180)          # Устанавливаем прозрачность
    overlay.fill((0, 0, 0))         # Черный фон
    screen_of_game.blit(overlay, (0, 0))
    
    pause_caption_text = CAPTION_FONT.render("Игра на паузе", True, CAPTION_FONT_COLOR)
    continue_text = TEXT_FONT.render("Нажмите Пробел для продолжения", True, TEXT_FONT_COLOR)
    exit_text = TEXT_FONT.render("Нажмите Escape чтобы выйти", True, TEXT_FONT_COLOR)
    
    pause_caption_rect = pause_caption_text.get_rect(center=(SIZE_OF_WINDOW[0] // 2, SIZE_OF_WINDOW[1] // 3))
    continue_rect = continue_text.get_rect(center=(SIZE_OF_WINDOW[0] // 2, SIZE_OF_WINDOW[1] // 2))
    exit_rect = exit_text.get_rect(center=(SIZE_OF_WINDOW[0] // 2, SIZE_OF_WINDOW[1] // 1.6))
    
    screen_of_game.blit(pause_caption_text, pause_caption_rect)
    screen_of_game.blit(continue_text, continue_rect)
    screen_of_game.blit(exit_text, exit_rect)

### 2.3.3 Отрисовать Змейка
def draw_snake(screen_of_game, snake, direction):
    draw_snake_head(screen_of_game, snake[0], snake[1])
    draw_snake_body(screen_of_game, snake)
    draw_snake_tail(screen_of_game, snake[-2], snake[-1])

### 2.3.3.1 Отрисовать Голову
def draw_snake_head(screen_of_game, head, neck):
    x_head, y_head = head
    x_prev, y_prev = neck
    delta_x_prev = x_head - x_prev             #изменение X координаты по отношению к ПРЕДЫДУЩЕМУ
    delta_y_prev = y_head - y_prev             #изменение Y координаты по отношению к ПРЕДЫДУЩЕМУ

    if (delta_x_prev > 0):
        draw_snake_body_left(screen_of_game, x_head, y_head)
    if (delta_y_prev > 0):
        draw_snake_body_top(screen_of_game, x_head, y_head)
    if (delta_x_prev < 0):
        draw_snake_body_right(screen_of_game, x_head, y_head)
    if (delta_y_prev < 0):
        draw_snake_body_bottom(screen_of_game, x_head, y_head)
    
    x_start_point = (x_head * BLOCK_SIZE + BORDERS_SIZE) + HALF_BLOCK_SIZE
    y_start_point = (y_head * BLOCK_SIZE + BORDERS_SIZE) + HALF_BLOCK_SIZE
    pygame.draw.circle(screen_of_game, SNAKE_COLOR, (x_start_point, y_start_point), HALF_BLOCK_SIZE)

### 2.3.3.2 Отрисовать Тело
def draw_snake_body(screen_of_game, snake):
    for i, segment in enumerate(snake[1:-1]):
        i +=1                                   #счётчик сегментов +1 т.к. начинаем со snake[1]
        x_0, y_0 = segment                      #кооридаты текущего сегмента
        x_next, y_next = snake[i + 1]           #кооридаты следующего сегмента
        x_prev, y_prev = snake[i - 1]           #кооридаты предыдущего сегмента

        delta_x_next = x_0 - x_next             #изменение X координаты по отношению к СЛЕДУЮЩЕМУ
        delta_y_next = y_0 - y_next             #изменение Y координаты по отношению к СЛЕДУЮЩЕМУ
        delta_x_prev = x_0 - x_prev             #изменение X координаты по отношению к ПРЕДЫДУЩЕМУ
        delta_y_prev = y_0 - y_prev             #изменение Y координаты по отношению к ПРЕДЫДУЩЕМУ

        if (delta_x_next > 0 or delta_x_prev > 0):
            draw_snake_body_left(screen_of_game, x_0, y_0)
        if (delta_y_next > 0 or delta_y_prev > 0):
            draw_snake_body_top(screen_of_game, x_0, y_0)
        if (delta_x_next < 0 or delta_x_prev < 0):
            draw_snake_body_right(screen_of_game, x_0, y_0)
        if (delta_y_next < 0 or delta_y_prev < 0):
            draw_snake_body_bottom(screen_of_game, x_0, y_0)
        if (not (delta_x_next == 0 and delta_x_prev == 0)) or (not (delta_y_next == 0 and delta_y_prev == 0)):
            draw_snake_body_circle(screen_of_game, x_0, y_0)

### 2.3.3.2.1 Отрисовать Тело ЛЕВУЮ часть сегмента тела
def draw_snake_body_left(screen_of_game, x_0, y_0):
    x_start_point = x_0 * BLOCK_SIZE + BORDERS_SIZE
    y_start_point = (y_0 * BLOCK_SIZE + BORDERS_SIZE) + QUARTER_BLOCK_SIZE
    rect_segement = (x_start_point, y_start_point, HALF_BLOCK_SIZE, HALF_BLOCK_SIZE)
    pygame.draw.rect(screen_of_game, SNAKE_COLOR, rect_segement)

### 2.3.3.2.2 Отрисовать Тело ВЕРХНЮЮ часть сегмента тела
def draw_snake_body_top(screen_of_game, x_0, y_0):
    x_start_point = (x_0 * BLOCK_SIZE + BORDERS_SIZE) + QUARTER_BLOCK_SIZE
    y_start_point = y_0 * BLOCK_SIZE + BORDERS_SIZE
    rect_segement = (x_start_point, y_start_point, HALF_BLOCK_SIZE, HALF_BLOCK_SIZE)
    pygame.draw.rect(screen_of_game, SNAKE_COLOR, rect_segement)

### 2.3.3.2.3 Отрисовать Тело ПРАВУЮ часть сегмента тела
def draw_snake_body_right(screen_of_game, x_0, y_0):
    x_start_point = (x_0 * BLOCK_SIZE + BORDERS_SIZE) + HALF_BLOCK_SIZE
    y_start_point = (y_0 * BLOCK_SIZE + BORDERS_SIZE) + QUARTER_BLOCK_SIZE
    rect_segement = (x_start_point, y_start_point, HALF_BLOCK_SIZE, HALF_BLOCK_SIZE)
    pygame.draw.rect(screen_of_game, SNAKE_COLOR, rect_segement) 

### 2.3.3.2.4 Отрисовать Тело НИЖНЮЮ часть сегмента тела
def draw_snake_body_bottom(screen_of_game, x_0, y_0):
    x_start_point = (x_0 * BLOCK_SIZE + BORDERS_SIZE) + QUARTER_BLOCK_SIZE
    y_start_point = (y_0 * BLOCK_SIZE + BORDERS_SIZE) + HALF_BLOCK_SIZE
    rect_segement = (x_start_point, y_start_point, HALF_BLOCK_SIZE, HALF_BLOCK_SIZE)
    pygame.draw.rect(screen_of_game, SNAKE_COLOR, rect_segement)

### 2.3.3.2.5 Отрисовать Тело КРУГ для сглаживания
def draw_snake_body_circle(screen_of_game, x_0, y_0):
    x_start_point = (x_0 * BLOCK_SIZE + BORDERS_SIZE) + HALF_BLOCK_SIZE
    y_start_point = (y_0 * BLOCK_SIZE + BORDERS_SIZE) + HALF_BLOCK_SIZE
    pygame.draw.circle(screen_of_game, SNAKE_COLOR, (x_start_point, y_start_point), QUARTER_BLOCK_SIZE)

### 2.3.3.3 Отрисовать Хвост
def draw_snake_tail(screen_of_game, pretail, tail):
    x_tail, y_tail = tail
    x_next, y_next = pretail

    x_tail_delta = x_tail - x_next
    y_tail_delta = y_tail - y_next

    if (x_tail_delta < 0):
        draw_snake_tail_left(screen_of_game, x_tail, y_tail)
    if (y_tail_delta < 0):
        draw_snake_tail_top(screen_of_game, x_tail, y_tail)
    if (x_tail_delta > 0):
        draw_snake_tail_right(screen_of_game, x_tail, y_tail)
    if (y_tail_delta > 0):
        draw_snake_tail_bottom(screen_of_game, x_tail, y_tail)
    pass

### 2.3.3.3.1 Отрисовать Хвост ЛЕВУЮ часть сегмента тела
def draw_snake_tail_left(screen_of_game, x_0, y_0):
    draw_snake_body_right(screen_of_game, x_0, y_0)

    tail_points = []
    tail_points.append((x_0 * BLOCK_SIZE + BORDERS_SIZE, y_0 * BLOCK_SIZE + BORDERS_SIZE + HALF_BLOCK_SIZE))
    tail_points.append((x_0 * BLOCK_SIZE + BORDERS_SIZE + HALF_BLOCK_SIZE, y_0 * BLOCK_SIZE + BORDERS_SIZE + QUARTER_BLOCK_SIZE))
    tail_points.append((x_0 * BLOCK_SIZE + BORDERS_SIZE + HALF_BLOCK_SIZE, y_0 * BLOCK_SIZE + BORDERS_SIZE + BLOCK_SIZE  * 3 / 4))
    
    pygame.draw.polygon(screen_of_game, SNAKE_COLOR, tail_points)
    tail_points = []

### 2.3.3.3.2 Отрисовать Хвост ВЕРХНЮЮ часть сегмента тела
def draw_snake_tail_top(screen_of_game, x_0, y_0):
    draw_snake_body_bottom(screen_of_game, x_0, y_0)

    tail_points = []
    tail_points.append((x_0 * BLOCK_SIZE + BORDERS_SIZE + HALF_BLOCK_SIZE, y_0 * BLOCK_SIZE + BORDERS_SIZE))
    tail_points.append((x_0 * BLOCK_SIZE + BORDERS_SIZE + THREE_QUARTERS_BLOCK_SIZE, y_0 * BLOCK_SIZE + BORDERS_SIZE + HALF_BLOCK_SIZE))
    tail_points.append((x_0 * BLOCK_SIZE + BORDERS_SIZE + QUARTER_BLOCK_SIZE, y_0 * BLOCK_SIZE + BORDERS_SIZE + HALF_BLOCK_SIZE))
    
    pygame.draw.polygon(screen_of_game, SNAKE_COLOR, tail_points)
    tail_points = []

### 2.3.3.3.3 Отрисовать Хвост ПРАВУЮ часть сегмента тела
def draw_snake_tail_right(screen_of_game, x_0, y_0):
    draw_snake_body_left(screen_of_game, x_0, y_0)

    tail_points = []
    tail_points.append((x_0 * BLOCK_SIZE + BORDERS_SIZE + BLOCK_SIZE, y_0 * BLOCK_SIZE + BORDERS_SIZE + HALF_BLOCK_SIZE))
    tail_points.append((x_0 * BLOCK_SIZE + BORDERS_SIZE + HALF_BLOCK_SIZE, y_0 * BLOCK_SIZE + BORDERS_SIZE + THREE_QUARTERS_BLOCK_SIZE))
    tail_points.append((x_0 * BLOCK_SIZE + BORDERS_SIZE + HALF_BLOCK_SIZE, y_0 * BLOCK_SIZE + BORDERS_SIZE + QUARTER_BLOCK_SIZE))
    
    pygame.draw.polygon(screen_of_game, SNAKE_COLOR, tail_points)
    tail_points = []

### 2.3.3.3.4 Отрисовать Хвост НИЖНЮЮ часть сегмента тела
def draw_snake_tail_bottom(screen_of_game, x_0, y_0):
    draw_snake_body_top(screen_of_game, x_0, y_0)

    tail_points = []
    tail_points.append((x_0 * BLOCK_SIZE + BORDERS_SIZE + HALF_BLOCK_SIZE, y_0 * BLOCK_SIZE + BORDERS_SIZE + BLOCK_SIZE))
    tail_points.append((x_0 * BLOCK_SIZE + BORDERS_SIZE + QUARTER_BLOCK_SIZE, y_0 * BLOCK_SIZE + BORDERS_SIZE + HALF_BLOCK_SIZE))
    tail_points.append((x_0 * BLOCK_SIZE + BORDERS_SIZE + THREE_QUARTERS_BLOCK_SIZE, y_0 * BLOCK_SIZE + BORDERS_SIZE + HALF_BLOCK_SIZE))
    
    pygame.draw.polygon(screen_of_game, SNAKE_COLOR, tail_points)
    tail_points = []

### 2.3.4 Отрисовать Яблоки
def draw_apples(screen_of_game, apples):
    for apple in apples:
        x_apple = apple[0] * BLOCK_SIZE + BORDERS_SIZE
        y_apple = apple[1] * BLOCK_SIZE + BORDERS_SIZE
        rect_apple = (x_apple, y_apple, BLOCK_SIZE, BLOCK_SIZE)
        pygame.draw.rect(screen_of_game, APPLE_COLOR, rect_apple, border_radius=APPLE_RADIUS)

### 2.3.5 Отрисовать Стены
def draw_walls(screen_of_game):
    #верхняя стена
    pygame.draw.rect(screen_of_game, WALLS_COLOR, ((0, 0), (WIDTH_OF_WINDOW, BORDERS_SIZE)), border_radius=0)
    #нижняя стена
    pygame.draw.rect(screen_of_game, WALLS_COLOR, ((0, HEIGHT_OF_WINDOW - BORDERS_SIZE), (WIDTH_OF_WINDOW,BORDERS_SIZE)), border_radius=0)
    #левая стена
    pygame.draw.rect(screen_of_game, WALLS_COLOR, ((0, BORDERS_SIZE), (BORDERS_SIZE, HEIGHT_OF_WINDOW - BORDERS_SIZE)), border_radius=0)
    #правая стена
    pygame.draw.rect(screen_of_game, WALLS_COLOR, ((WIDTH_OF_WINDOW - BORDERS_SIZE, BORDERS_SIZE), (WIDTH_OF_WINDOW, HEIGHT_OF_WINDOW - BORDERS_SIZE)), border_radius=0)

### 2.3.6 Отрисовать счет
def draw_score(screen_of_game, score):
    pass

### 2.3.7 Отрисовать Выигрыш
def draw_game_won_screen(screen_of_game):
    pass

### 2.3.8 Отрисовать Поражение
def draw_game_over_screen(screen_of_game):
    screen_of_game.fill(WALLS_COLOR)
    font = pygame.font.Font(None, 74)
    text = font.render("Проигрыш", True, (220, 220, 220))
    text_rect = text.get_rect(center=(SIZE_OF_WINDOW[0] // 2, SIZE_OF_WINDOW[1] // 3))
    screen_of_game.blit(text, text_rect)

    font = pygame.font.Font(None, 36)
    text = font.render("Нажмите Enter чтобы начать с начала", True, (255, 255, 255))
    text_rect = text.get_rect(center=(SIZE_OF_WINDOW[0] // 2, SIZE_OF_WINDOW[1] // 2))
    screen_of_game.blit(text, text_rect)

############## MAIN ##############
def main():
    screen_of_game, clock = initialize_program()
    game_state = initialize_game_state()

    while game_state["program_running"]:
        clock.tick(game_state["game_speed"])

        # 1. считать все события
        events = get_game_events()

        # 2. изменить состояние игры внутри pyhton
        update_game_state(game_state, events)

        # 3. отрисовать состояние игры на игре
        update_game_screen(screen_of_game, game_state)

    perform_ending_actions()

if __name__ == "__main__":
    main()
