import pygame
import sys
import random

#КОНСТАНТЫ ОКНА ПРОГРАММЫ
SIZE_OF_WINDOW = width, height = 800, 600            #размер окна
WINDOW_ICON = 'icon.png'                             #иконка
WINDOW_CAPTION = 'Snake-Game'                        #название окна

#КОНСТАНТЫ ИГРЫ
INITIAL_APPLES_COUNT = 3                             #количество яблок
INITIAL_GAME_SPEED  = 5                              #скорость игры
BLOCK_SIZE = 20                                      #размер квадратика
WALL_BLOCKS = 3                                      #количество блоков в стене 
AMOUNT_OF_RECTS = 20                                 #количество квадратиков
INITIAL_SNAKE_SIZE = 3                               #размер змейки
SIZE_X = (width // BLOCK_SIZE  - WALL_BLOCKS * 2)            #количество блоков поля по X
SIZE_Y = (height // BLOCK_SIZE - WALL_BLOCKS * 2)            #количество блоков поля по Y
AMOUNT_OF_BLOCKS = SIZE_X * SIZE_Y                   #количество блоков
START_SNAKE_X = SIZE_X // 2                                #X_0 координата головы змейки
START_SNAKE_Y = SIZE_Y // 2                                #Y_0 координата головы змейки

#КОНСТАНТЫ ЦВЕТОВ
WALLS_COLOR = (0, 110, 22)                      #цвет заднего фона
GAME_FIELD_COLOR = (235, 252, 207)                   #цвет игрового поля
SNAKE_COLOR = (190, 255, 100)                        #цвет змейки
APPLE_COLOR = (255, 64, 64)                          #цвет яблока

#КОНСТАНТЫ ОТРИСОВОК
APPLE_RADIUS = BLOCK_SIZE // 3                       #радиус яблока
SNAKE_RADIUS = BLOCK_SIZE // 4                       #радиус змейки

############## 1. ФУНКЦИИ БЛОКА MAIN

### 1.1 Инициализация программы
def initialize_program():
    pygame.init()
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
        "apples": [],
        "snake": [],
        "direction": None,
        "last_direction": None,
        "score": 0,
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
    if game_state["game_running"]:                      # если игра запущена
        move_snake(game_state)                          # передвинуть змейку
        check_collisions(game_state)                    # проверить столкновения
        check_eat_apple(game_state)                     # проверить съедание яблока
        check_game_won(game_state)                      # проверить выигрыш

### 2.2.1 Обработка событий нажатия клавиш
def process_keys_events(game_state, events):
    if "quit" in events:                                #если событие - выход
        game_state["program_running"] = False
    elif not game_state["game_running"]:                #если игра не запущена
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
    place_snake(INITIAL_SNAKE_SIZE, game_state)
    # положение яблок
    place_apples(INITIAL_APPLES_COUNT, game_state)
    # направление движения
    game_state["direction"] = 'right'
    game_state["last_direction"] = 'right'
    # на паузе ли игра
    game_state["game_paused"] = False
    # сколько очков
    game_state["score"] = 0
    # скорость игры
    game_state["game_speed"] = INITIAL_GAME_SPEED  

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
    if len(game_state["snake"]) > len(set(game_state["snake"])):
        game_state["game_running"] = False

### 2.2.4 Проверить съедание яблока
def check_eat_apple(game_state):
    x_head, y_head = game_state["snake"][0]
    if (x_head, y_head) in game_state["apples"]:
        game_state["apples"].remove((x_head, y_head))
        game_state["snake"].append((x_head, y_head))
        place_apples(1, game_state)
        game_state["score"] += 1
        game_state["game_speed"] += 0.5

### 2.2.5 Проверить выигрыш
def check_game_won(game_state):
    if AMOUNT_OF_BLOCKS - len(game_state["snake"]) == 0:
        game_state["game_won"] = True
        game_state["game_running"] = False

### 2.3 Отрисовка состояния игры
def update_game_screen(screen_of_game, game_state):
    screen_of_game.fill(GAME_FIELD_COLOR)
    
    if not game_state["game_running"]:
        draw_new_game_screen(screen_of_game)
    elif game_state["game_paused"]:
        draw_paused_screen(screen_of_game)
    else:
        draw_snake(screen_of_game, game_state["snake"])
        draw_apples(screen_of_game, game_state["apples"])
    draw_walls(screen_of_game)
    draw_score(screen_of_game, game_state["score"])
    pygame.display.update()

### 2.3.1 Отрисовать Новая игра
def draw_new_game_screen(screen_of_game):
    font = pygame.font.Font(None, 74)
    text = font.render("Snake Game", True, (255, 255, 255))
    text_rect = text.get_rect(center=(SIZE_OF_WINDOW[0] // 2, SIZE_OF_WINDOW[1] // 3))
    screen_of_game.blit(text, text_rect)

    font = pygame.font.Font(None, 36)
    text = font.render("Press Enter to Start", True, (255, 255, 255))
    text_rect = text.get_rect(center=(SIZE_OF_WINDOW[0] // 2, SIZE_OF_WINDOW[1] // 2))
    screen_of_game.blit(text, text_rect)

### 2.3.2 Отрисовать Пауза
def draw_paused_screen(screen_of_game):
    pass

### 2.3.3 Отрисовать Змейка
def draw_snake(screen_of_game, snake):
    for segment in snake:
        x_segment = segment[0] * BLOCK_SIZE + BLOCK_SIZE * WALL_BLOCKS
        y_segment = segment[1] * BLOCK_SIZE + BLOCK_SIZE * WALL_BLOCKS
        rect_segment = (x_segment, y_segment, BLOCK_SIZE, BLOCK_SIZE)
        pygame.draw.rect(screen_of_game, SNAKE_COLOR, rect_segment, border_radius=SNAKE_RADIUS)

### 2.3.4 Отрисовать Яблоки
def draw_apples(screen_of_game, apples):
    for apple in apples:
        x_apple = apple[0] * BLOCK_SIZE + BLOCK_SIZE * WALL_BLOCKS
        y_apple = apple[1] * BLOCK_SIZE + BLOCK_SIZE * WALL_BLOCKS
        rect_apple = (x_apple, y_apple, BLOCK_SIZE, BLOCK_SIZE)
        pygame.draw.rect(screen_of_game, APPLE_COLOR, rect_apple, border_radius=APPLE_RADIUS)

### 2.3.5 Отрисовать Стены
def draw_walls(screen_of_game):
    #верхняя стена
    pygame.draw.rect(screen_of_game, WALLS_COLOR, ((0, 0), (width, WALL_BLOCKS * BLOCK_SIZE)), border_radius=0)
    #нижняя стена
    pygame.draw.rect(screen_of_game, WALLS_COLOR, ((0, height - WALL_BLOCKS * BLOCK_SIZE), (width,WALL_BLOCKS * BLOCK_SIZE)), border_radius=0)
    #левая стена
    pygame.draw.rect(screen_of_game, WALLS_COLOR, ((0, WALL_BLOCKS * BLOCK_SIZE), (WALL_BLOCKS * BLOCK_SIZE, height - WALL_BLOCKS * BLOCK_SIZE)), border_radius=0)
    #правая стена
    pygame.draw.rect(screen_of_game, WALLS_COLOR, ((width - WALL_BLOCKS * BLOCK_SIZE, WALL_BLOCKS * BLOCK_SIZE), (width, height - WALL_BLOCKS * BLOCK_SIZE)), border_radius=0)

### 2.3.6 Отрисовать счет
def draw_score(screen_of_game, score):
    pass

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


'''
#само окно игры
screenOfGame = pygame.display.set_mode(size)        #размер окна
pygame.display.set_caption('Snake-Game')            #название окна

#объект clock для управления частотой игры
clock = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            print('Выход из игры')
            quit()
    
    #применение цвета
    screenOfGame.fill(backgroundColor)          
    #красота

    #создание полей для игры ( x_0, y_0, ширина, высота )
    for column in range(amountOfRects):
        for row in range(amountOfRects):
            if (column + row) % 2 == 0:
                pygame.draw.rect(screenOfGame, rectgColor, [130 + column * rectSize + column, 20 + row * rectSize + row, rectSize, rectSize])
            else:
                pygame.draw.rect(screenOfGame, secondRectgColor, [130 + column * rectSize + column, 20 + row * rectSize + row, rectSize, rectSize])
    
    #применение всех изменений каждым кадром
    pygame.display.update()
    clock.tick(10)

#конец
pygame.quit()
sys.exit()'''