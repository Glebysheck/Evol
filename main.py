from random import randint
import pygame
from bacteriums import Bacterium
from vegetables import Vegetable
import meats
from walls import Wall
from setting import Setting

WHITE = (250, 250, 250)

Wall.create()

running = True
while running:
    Setting.clock.tick(Setting.fps)

    # Отслеживане нажатых клавиш
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                Bacterium.creating_bacteria()
            if event.key == pygame.K_1:
                Setting.fps = 1
            if event.key == pygame.K_2:
                Setting.fps = 10
            if event.key == pygame.K_3:
                Setting.fps = 25
            if event.key == pygame.K_4:
                Setting.fps = 50
            if event.key == pygame.K_5:
                Setting.fps = 200

    Setting.screen.fill(WHITE)

    for i in Wall.walls_list:
        pygame.draw.rect(Setting.screen, (0, 0, 0), (i.location_x, i.location_y, i.width, i.height))

    # Генератор растительности
    if len(Vegetable.vegetables_dict) <= 300:
        Vegetable.generation(Bacterium.bacterium_dict, Wall.walls_dict)

    # Добавление бактерий при отсутствии их на поле
    if len(Bacterium.bacterium_dict) < 1:
        Bacterium.creating_bacteria()

    for i in Vegetable.vegetables_dict.values():
        pygame.draw.circle(Setting.screen, i.color, (i.location_x, i.location_y), i.radius)

    rotten = []
    for i in meats.Meat.meat_dict.values():
        i.rotting()
        if i.nutritional_value <= 0:
            rotten.append(i)
        pygame.draw.circle(Setting.screen, i.color, (i.location_x, i.location_y), i.radius)

    for i in rotten:
        meats.Meat.meat_dict.pop(str(i))

    Bacterium.step()

    pygame.display.update()

pygame.quit()
