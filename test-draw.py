
def draw_snake_body_left(snake):
    print('Рисуется левая часть')

def draw_snake_body_top(snake):
    print('Рисуется верхняя часть')

def draw_snake_body_right(snake):
    print('Рисуется правая часть')

def draw_snake_body_bottom(snake):
    print('Рисуется нижняя часть')


# Пример списка сегментов змейки
snake = [(2, 5), (2, 6), (2, 7), (3, 7), (4, 7), (4, 6), (5, 6), (5, 5), (5, 4), (4, 4), (4, 3), (4, 2), (3, 2), (3, 3), (2,3 ), (1, 3), (1, 4), (2, 4), (3,4), (3,5)]
for i, segment in enumerate(snake[1:-1]):
    i +=1                                   #счётчик сегментов +1 т.к. начинаем со snake[1]
    x_0, y_0 = segment                      #кооридаты текущего сегмента
    x_next, y_next = snake[i + 1]           #кооридаты следующего сегмента
    x_prev, y_prev = snake[i - 1]           #кооридаты предыдущего сегмента

    delta_x_next = x_0 - x_next             #изменение X координаты по отношению к СЛЕДУЮЩЕМУ
    delta_y_next = y_0 - y_next             #изменение Y координаты по отношению к СЛЕДУЮЩЕМУ
    delta_x_prev = x_0 - x_prev             #изменение X координаты по отношению к ПРЕДЫДУЩЕМУ
    delta_y_prev = y_0 - y_prev             #изменение Y координаты по отношению к ПРЕДЫДУЩЕМУ

    print(f'Текущий элемент {i}-й по счету: {segment}')
    
    if (delta_x_next > 0 or delta_x_prev > 0):
        draw_snake_body_left(snake)
    if (delta_x_next < 0 or delta_x_prev < 0):
        draw_snake_body_right(snake)
    if (delta_y_next > 0 or delta_y_prev > 0):
        draw_snake_body_bottom(snake)
    if (delta_y_next < 0 or delta_y_prev < 0):
        draw_snake_body_top(snake)