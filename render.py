import pygame
from setting import Setting
from wall import Wall
from meat import Meat


class Render:

    @classmethod
    def rendering(cls, *items):
        for i in items:
            if i.shape == "rect":
                cls._draw_rect(i)

    @staticmethod
    def _draw_rect(item):
        for i in item:
            pygame.draw.rect(Setting.screen, i.colour, (i.location_x, i.location_y, i.size, i.size))
