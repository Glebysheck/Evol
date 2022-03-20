import pygame
from setting import Setting


class Slider:
    stripe_width = 150
    stripe_height = 4

    roll_radius = 8

    darkGrayColor = (128, 128, 128)
    grayColor = (204, 204, 204)

    list_slider = []

    def __init__(self, location_x, location_y, obj):
        self.stripe_location_x = location_x
        self.stripe_location_y = location_y
        self.roll_location_x = location_x
        self.roll_location_y = location_y
        self.obj = obj

    def move(self):
        if pygame.mouse.get_pressed()[0]:
            x = pygame.mouse.get_pos()[0]
            y = pygame.mouse.get_pos()[1]
            if self.roll_location_y - 10 < y < self.roll_location_y + 10:
                if self.stripe_location_x < x < self.stripe_location_x + self.stripe_width:
                    self.roll_location_x = x
                    self.obj[0] = int((x - self.stripe_location_x) / 3)
                    if self.obj[1] > self.obj[0]:
                        self.obj[1] = self.obj[0]

    @classmethod
    def rendering(cls):
        for i in cls.list_slider:
            x = i.stripe_location_x
            y = i.stripe_location_y
            pygame.draw.rect(Setting.screen, cls.grayColor, (x, y, i.stripe_width, i.stripe_height))
            x = i.roll_location_x + cls.stripe_height / 2
            y = i.roll_location_y + cls.stripe_height / 2
            pygame.draw.circle(Setting.screen, cls.darkGrayColor, (x, y), i.roll_radius)
