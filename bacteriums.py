from random import randint
import pygame
import vegetables
from meats import Meat
from walls import Wall
from setting import Setting


class Bacterium:
    width, height = 30, 30
    color = (45, 84, 67)

    orientations = [[-1, 1], [0, 1], [1, 1], [1, 0], [1, -1], [0, -1], [-1, -1], [-1, 0]]
    orientation = orientations[randint(0, len(orientations) - 1)]

    foods = 100
    standard_days = 200
    days = 0
    health = 100

    reaction_to = 0

    bacterium_dict = {}
    new_bacterium_dict = {}

    def __init__(self, location_x, location_y, reaction_to):
        self.location_x = location_x
        self.location_y = location_y
        self.days = self.standard_days
        self.reaction_to = reaction_to

    def __str__(self):
        return "{}_{}".format(self.location_x, self.location_y)

    def motion(self):
        self.days -= 1

        if self.health < 100:
            self.health += 5
            self.foods -= 5
        if self.__str__() in vegetables.Vegetable.vegetables_dict:
            vegetables.Vegetable.vegetables_dict.pop(self.__str__())
            self.foods += vegetables.Vegetable.nutritional_value
        if self.__str__() in Meat.meat_dict:
            Meat.meat_dict.pop(self.__str__())
            self.foods += Meat.nutritional_value

        view = "{}_{}".format(self.location_x + self.orientation[0] * 30, self.location_y + self.orientation[1] * 30)

        if view in Wall.walls_dict:
            self.reaction("walls")
        elif view in vegetables.Vegetable.vegetables_dict:
            self.reaction("vegetable")
        elif view in self.bacterium_dict:
            if self.bacterium_dict[view].color == self.color:
                self.reaction("like bacterium")
            else:
                self.reaction("bacterium")
        elif view in Meat.meat_dict:
            self.reaction("meat")
        else:
            if self.foods >= 200:
                self.division()
            else:
                self.reaction("empty cell")

    def reaction(self, to):
        react = self.reaction_to[to][0]
        self.reaction_to[to][0] += 1

        if self.reaction_to[to][0] == len(self.reaction_to[to]):
            self.reaction_to[to][0] = 1

        if self.reaction_to[to][react] == 0:
            self.turn_right()
        elif self.reaction_to[to][react] == 1:
            self.turn_left()
        elif self.reaction_to[to][react] == 2:
            if to == "bacterium" or to == "like bacterium":
                self.bite()
            else:
                self.moving_forward()

    def division(self):
        self.foods -= 100
        rea = {}

        for key, value in self.reaction_to.items():
            rea[key] = value.copy()

        bac = Bacterium(self.location_x + self.orientation[0] * 30, self.location_y + self.orientation[1] * 30, rea)
        bac.color = self.color
        bac.standard_days = self.standard_days
        bac.orientation = self.orientation

        for key in bac.reaction_to.keys():
            bac.reaction_to[key][0] = 1

        for mut in range(0, 4):
            bac.mutation()
        self.new_bacterium_dict[str(bac)] = bac

    def turn_right(self):
        orient = self.orientations.index(self.orientation) - 1
        if orient < 0:
            orient = 7
        self.orientation = self.orientations[orient]

    def turn_left(self):
        orient = self.orientations.index(self.orientation) + 1
        if orient > 7:
            orient = 0
        self.orientation = self.orientations[orient]

    def moving_forward(self):
        self.location_x += self.orientation[0] * 30
        self.location_y += self.orientation[1] * 30
        self.foods -= 10

    def bite(self):
        self.foods -= 10
        view = "{}_{}".format(self.location_x + self.orientation[0] * 30, self.location_y + self.orientation[1] * 30)

        self.bacterium_dict[view].health -= 25

    def mutation(self):
        if randint(0, 4) == 1:
            if randint(0, 10) == 1:
                self.color = (randint(0, 255), randint(0, 255), randint(0, 255))
            if randint(0, 20) == 1:
                self.standard_days += randint(-5, 20)
            if randint(0, 20) == 1:
                self.reaction_to["walls"][randint(1, len(self.reaction_to["walls"]) - 1)] = randint(0, 1)
                if randint(0, 40) == 1:
                    self.reaction_to["walls"].append(randint(0, 1))
            if randint(0, 20) == 1:
                react = ["vegetable", "meat", "bacterium", "like bacterium", "empty cell"]
                react = react[randint(0, len(react) - 1)]
                self.reaction_to[react][randint(1, len(self.reaction_to[react]) - 1)] = randint(0, 2)
                if randint(0, 40) == 1:
                    self.reaction_to[react].append(randint(0, 2))

    @classmethod
    def creating_bacteria(cls):
        for i in range(0, 10):
            bac_x = randint(0, int(Setting.width / cls.width)) * cls.width
            bac_y = randint(0, int(Setting.height / cls.height)) * cls.height
            reac = {"walls": [1, 0, 0, 0], "vegetable": [1, 0, 0, 0], "meat": [1, 0, 0, 0],
                    "bacterium": [1, 0, 0, 0], "like bacterium": [1, 0, 0, 0], "empty cell": [1, 0, 0, 0]}
            bacterium = Bacterium(bac_x, bac_y, reac)

            if str(bacterium) in Wall.walls_dict:
                pass
            else:
                if str(bacterium) in cls.bacterium_dict:
                    pass
                else:
                    for j in range(0, 30):
                        bacterium.mutation()
                    cls.new_bacterium_dict[str(bacterium)] = bacterium

    @classmethod
    def step(cls):
        cls.new_bacterium_dict = {}

        for i in cls.bacterium_dict.values():
            if i.health <= 0:
                meat = Meat(i.location_x + Meat.radius, i.location_y + Meat.radius)
                Meat.meat_dict[str(meat)] = meat
            elif i.foods <= 0 or i.days <= 0:
                meat = Meat(i.location_x + Meat.radius, i.location_y + Meat.radius)
                meat.nutritional_value -= 50
                Meat.meat_dict[str(meat)] = meat
            else:
                i.motion()
                cls.new_bacterium_dict[str(i)] = i

            pygame.draw.rect(Setting.screen, i.color, (i.location_x, i.location_y, i.width, i.height))

        cls.bacterium_dict = cls.new_bacterium_dict
