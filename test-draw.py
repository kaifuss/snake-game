import pygame
import sys

# Инициализация Pygame
pygame.init()
size = width, height = 800, 600
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()

# Цвета
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)

# Пример списка сегментов змейки
snake = [(100, 100), (90, 100), (80, 100), (70, 100)]

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.fill(white)

    for i, segment in enumerate(snake):
        x, y = segment
        pygame.draw.rect(screen, green, pygame.Rect(x, y, 10, 10))
        
        if i > 0:
            prev_x, prev_y = snake[i - 1]
            print(f"Текущий сегмент: {segment}, Предыдущий сегмент: {(prev_x, prev_y)}")

        if i < len(snake) - 1:
            next_x, next_y = snake[i + 1]
            print(f"Текущий сегмент: {segment}, Следующий сегмент: {(next_x, next_y)}")
        
    pygame.display.flip()
    clock.tick(60)
