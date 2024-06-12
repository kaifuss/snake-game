import pygame
import sys

#инициализация
pygame.init()

#переменные
size = width, height = 800, 800             #размер окна
backgroundColor = (0, 110, 22)              #цвет заднего фона
rectgColor = (149, 236, 0)                  #цвет первого квадратика поля
secondRectgColor = (235, 252, 207)          #цвет второго квадратика поля
rectSize = 25                               #размер квадратика
amountOfRects = 20                          #количество квадратиков

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
sys.exit()