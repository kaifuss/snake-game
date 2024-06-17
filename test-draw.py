
# Пример списка сегментов змейки
snake = [(100, 100), (90, 100), (80, 100), (70, 100)]
for i, segment in enumerate(snake):
    x, y = segment
    
    if i > 0:
        prev_x, prev_y = snake[i - 1]
        print(f"Текущий сегмент: {segment}, Предыдущий сегмент: {(prev_x, prev_y)}")

    if i < len(snake) - 1:
        next_x, next_y = snake[i + 1]
        print(f"Текущий сегмент: {segment}, Следующий сегмент: {(next_x, next_y)}")
