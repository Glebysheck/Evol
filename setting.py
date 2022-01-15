import pygame


class Setting:
    pygame.init()

    height = 1080
    width = 600

    screen = pygame.display.set_mode((0, 0))
    pygame.display.set_caption("Evol")
    clock = pygame.time.Clock()
    fps = 60
