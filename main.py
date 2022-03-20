from random import randint
import pygame
from bacterium import Bacterium
from vegetable import Vegetable
from meat import Meat
from wall import Wall
from setting import Setting
from slider import Slider
from rect import Rect
import time


pygame.init()
WHITE = (250, 250, 250)

Wall.create()
Slider.list_slider.append(Slider(15, 50, Setting.steps))

font = pygame.font.Font(None, 30)
text = font.render("Скорость", True, [0, 0, 0])


def logic():
    # Генератор растительности
    if len(Vegetable.vegetables_dict) <= 600:
        Vegetable.generation(Rect.square_object["bacterium_dict"], Rect.square_object["walls_dict"])

    # Добавление бактерий при отсутствии их на поле
    if len(Rect.square_object["bacterium_dict"]) < 1:
        Bacterium.creating_bacteria()

    rotten = []
    for meat in Meat.meat_dict.values():
        meat.rotting()
        if meat.nutritional_value <= 0:
            rotten.append(meat)

    for meat in rotten:
        Meat.meat_dict.pop(str(meat))

    Bacterium.step()


while Setting.running:
    Setting.clock.tick()

    # Отслеживане нажатых клавиш
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            Setting.running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                Bacterium.creating_bacteria()

    Setting.screen.fill(WHITE)

    Slider.rendering()

    if Setting.steps[1] >= 50:
        logic()
        Setting.steps[1] = Setting.steps[0]
    else:
        Setting.steps[1] += 1

    for i in Rect.square_object["walls_dict"].values():
        pygame.draw.rect(Setting.screen, (0, 0, 0), (i.location_x, i.location_y, i.size, i.size))

    for i in Vegetable.vegetables_dict.values():
        pygame.draw.circle(Setting.screen, i.color, (i.location_x, i.location_y), i.radius)

    for i in Meat.meat_dict.values():
        pygame.draw.circle(Setting.screen, i.color, (i.location_x, i.location_y), i.radius)

    for i in Slider.list_slider:
        i.move()

    for i in Rect.square_object["bacterium_dict"].values():
        pygame.draw.rect(Setting.screen, i.color, (i.location_x, i.location_y, i.size, i.size))

    Setting.screen.blit(text, (15, 15))

    pygame.display.update()

pygame.quit()
