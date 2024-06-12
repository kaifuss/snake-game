import pygame
import sys
import random

#КОНСТАНТЫ ОКНА ПРОГРАММЫ
SIZE_OF_WINDOW = width, height = 800, 600            #размер окна
WINDOW_ICON = 'icon.png'                             #иконка
WINDOW_CAPTION = 'Snake-Game'                        #название окна

#КОНСТАНТЫ ИГРЫ
INITIAL_APPLES_COUNT = 3                             #количество яблок
INITIAL_GAME_SPEED  = 10                             #скорость игры
BLOCK_SIZE = 20                                      #размер квадратика
WALL_BLOCKS = 3                                      #количество блоков в стене 
AMOUNT_OF_RECTS = 20                                 #количество квадратиков
INITIAL_SNAKE_SIZE = 3                               #размер змейки
SIZE_X = (width // BLOCK_SIZE  - WALL_BLOCKS * 2)            #количество блоков поля по X
SIZE_Y = (height // BLOCK_SIZE - WALL_BLOCKS * 2)            #количество блоков поля по Y
AMOUNT_OF_BLOCKS = SIZE_X * SIZE_Y                   #количество блоков
START_X = SIZE_X // 2                                #X_0 координата головы змейки
START_Y = SIZE_Y // 2                                #Y_0 координата головы змейки

#КОНСТАНТЫ ЦВЕТОВ
BACKGROUND_COLOR = (235, 252, 207)                   #цвет заднего фона
BORDERS_COLOR = (0, 110, 22)                         #цвет границ
SNAKE_COLOR = (190, 255, 100)                        #цвет змейки
APPLE_COLOR = (255, 64, 64)                          #цвет яблока

#КОНСТАНТЫ ОТРИСОВОК
APPLE_RADIUS = BLOCK_SIZE // 4                       #радиус яблока

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
        for direction in ['in', 'up', 'right', 'left']:  #движение змейки
            if direction in events:                      #если нажата клавиша движения
                game_state["direction"] = direction
                game_state["last_direction"] = direction
                break

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
    x = START_X
    y = START_Y
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
    move_direction = game_state["direction"] if game_state["direction"] else game_state["last_direction"]
    if move_direction == "up":
        x_dir = 0
        y_dir = -1
    elif move_direction == "down":
        x_dir = 0
        y_dir = 1
    elif move_direction == "left":
        x_dir = -1
        y_dir = 0
    elif move_direction == "right":
        x_dir = 1
        y_dir = 0
    else:
        return
    head = game_state["snake"][0]
    new_head = (head[0] + x_dir, head[1] + y_dir)
    game_state["snake"].insert(0, new_head)
    game_state["snake"].pop()

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
        game_state["game_speed"] += 1

### 2.2.5 Проверить выигрыш
def check_game_won(game_state):
    if AMOUNT_OF_BLOCKS - len(game_state["snake"]) == 0:
        game_state["game_won"] = True
        game_state["game_running"] = False

### 2.3 Отрисовка состояния игры
def update_game_screen(screen_of_game, game_state):
    screen_of_game.fill(BACKGROUND_COLOR)
    
    if not game_state["game_running"]:
        draw_new_game_screen(screen_of_game)
    elif game_state["game_paused"]:
        draw_paused_screen(screen_of_game)
    else:
        draw_snake(screen_of_game, game_state["snake"])
        draw_apples(screen_of_game, game_state["apples"])

    draw_wals(screen_of_game)
    draw_score(screen_of_game, game_state["score"])
    pygame.display.update()

### 2.3.1 Отрисовать Новая игра
def draw_new_game_screen(screen_of_game):
    pass

### 2.3.2 Отрисовать Пауза
def draw_paused_screen(screen_of_game):
    pass

### 2.3.3 Отрисовать Змейка
def draw_snake(screen_of_game, snake):
    for segment in snake:
        x_segment = segment[0] * BLOCK_SIZE + BLOCK_SIZE * WALL_BLOCKS
        y_segment = segment[1] * BLOCK_SIZE + BLOCK_SIZE * WALL_BLOCKS
        rect_segment = (x_segment, y_segment, BLOCK_SIZE, BLOCK_SIZE)
        pygame.draw.rect(screen_of_game, SNAKE_COLOR, rect_segment)

### 2.3.4 Отрисовать Яблоки
def draw_apples(screen_of_game, apples):
    for apple in apples:
        x_apple = apple[0] * BLOCK_SIZE + BLOCK_SIZE * WALL_BLOCKS
        y_apple = apple[1] * BLOCK_SIZE + BLOCK_SIZE * WALL_BLOCKS
        rect_apple = (x_apple, y_apple, BLOCK_SIZE, BLOCK_SIZE)
        pygame.draw.rect(screen_of_game, APPLE_COLOR, rect_apple, border_radius=APPLE_RADIUS)


### 2.3.5 Отрисовать стены
def draw_wals(screen_of_game):
    pass

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