import pygame


class Setting:
    pygame.init()

    width = 1080
    height = 600

    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Evol")
    clock = pygame.time.Clock()
    fps = 60
