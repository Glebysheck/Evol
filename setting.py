import pygame


class Setting:
    h_indent = 18
    v_indent = 1

    height = 980
    width = 500

    screen = pygame.display.set_mode((0, 0))
    pygame.display.set_caption("Evol")
    clock = pygame.time.Clock()

    steps = [1, 1]

    running = True
