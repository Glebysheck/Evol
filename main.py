import pygame
from random import randint

pygame.init()
width = 1080
height = 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Evol")
clock = pygame.time.Clock()
fps = 60

WHITE = (250, 250, 250)


class Wall:
    width, height = 30, 30
    colour = (0, 0, 0)
    location_x, location_y = 0, 0

    num = 0

    def __init__(self, location_x, location_y):
        self.location_x = location_x
        self.location_y = location_y

    def __str__(self):
        return "{}_{}".format(self.location_x, self.location_y)


class Food:
    radius = 15
    location_x, location_y = 0, 0

    def __init__(self, location_x, location_y):
        self.location_x = location_x
        self.location_y = location_y

    def __str__(self):
        return "{}_{}".format(self.location_x - self.radius, self.location_y - self.radius)


class Meat(Food):
    nutritional_value = 75
    color = (250, 128, 114)

    def rotting(self):
        self.nutritional_value -= 2


class Vegetables(Food):
    nutritional_value = 25
    color = (0, 128, 0)


class Bacterium:
    width, height = 30, 30
    color = (45, 84, 67)
    location_x, location_y = 0, 0

    orientations = [[-1, 1], [0, 1], [1, 1], [1, 0], [1, -1], [0, -1], [-1, -1], [-1, 0]]
    orientation = orientations[randint(0, len(orientations) - 1)]

    foods = 100
    standard_days = 200
    days = 0
    health = 100

    reaction_to = 0

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
        if self.__str__() in vegetables_dict:
            vegetables_dict.pop(self.__str__())
            self.foods += Vegetables.nutritional_value
        if self.__str__() in meat_dict:
            meat_dict.pop(self.__str__())
            self.foods += Meat.nutritional_value

        view = "{}_{}".format(self.location_x + self.orientation[0] * 30, self.location_y + self.orientation[1] * 30)

        if view in walls_dict:
            self.reaction("walls")
        elif view in vegetables_dict:
            self.reaction("vegetable")
        elif view in bacterium_dict:
            if bacterium_dict[view].color == self.color:
                self.reaction("like bacterium")
            else:
                self.reaction("bacterium")
        elif view in meat_dict:
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
        new_bacterium_dict[str(bac)] = bac

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
        self.foods -= 5

    def bite(self):
        self.foods -= 10
        view = "{}_{}".format(self.location_x + self.orientation[0] * 30, self.location_y + self.orientation[1] * 30)

        bacterium_dict[view].health -= 25

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


bacterium_dict = {}

vegetables_dict = {}
meat_dict = {}

walls_list = []

# Создание стен
for i in range(0, int(width / Wall.width)):
    walls_list.append(Wall(i * Wall.width, 0))
for i in range(1, int(height / Wall.height)):
    walls_list.append(Wall((int(width / Wall.width) - 1) * Wall.width, i * Wall.width))
for i in range(0, int(width / Wall.width) - 1):
    walls_list.append(Wall(i * Wall.width, (int(height / Wall.height) - 1) * Wall.height))
for i in range(1, int(height / Wall.height) - 1):
    walls_list.append(Wall(0, i * Wall.height))

for i in range(2, int(height / Wall.height) - 2):
    walls_list.append(Wall(int(width / Wall.width / 2) * Wall.width, i * Wall.height))
for i in range(2, int(width / Wall.width) - 2):
    walls_list.append(Wall(i * Wall.width, int(height / Wall.height / 2) * Wall.width))

walls_dict = {}
for i in walls_list:
    walls_dict[str(i)] = i


running = True
while running:
    clock.tick(fps)

    # Отслеживане нажатых клавиш
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                for i in range(0, 10):
                    bac_x = randint(0, int(width / Bacterium.width)) * Bacterium.width
                    bac_y = randint(0, int(height / Bacterium.height)) * Bacterium.height
                    reac = {"walls": [1, 0, 0, 0], "vegetable": [1, 0, 0, 0], "meat": [1, 0, 0, 0],
                            "bacterium": [1, 0, 0, 0], "like bacterium": [1, 0, 0, 0], "empty cell": [1, 0, 0, 0]}
                    bacterium = Bacterium(bac_x, bac_y, reac)

                    if str(bacterium) in walls_dict:
                        pass
                    else:
                        if str(bacterium) in bacterium_dict:
                            pass
                        else:
                            for j in range(0, 30):
                                bacterium.mutation()
                            bacterium_dict[str(bacterium)] = bacterium
            if event.key == pygame.K_1:
                fps = 1
            if event.key == pygame.K_2:
                fps = 10
            if event.key == pygame.K_3:
                fps = 25
            if event.key == pygame.K_4:
                fps = 50
            if event.key == pygame.K_5:
                fps = 200

    screen.fill(WHITE)

    for i in walls_list:
        pygame.draw.rect(screen, (0, 0, 0), (i.location_x, i.location_y, i.width, i.height))

    # Генератор растительности
    if len(vegetables_dict) <= 300:
        for i in range(0, 35):
            veg_x = randint(0, int(width / (Vegetables.radius * 2))) * Vegetables.radius * 2 + Vegetables.radius
            veg_y = randint(0, int(height / (Vegetables.radius * 2))) * Vegetables.radius * 2 + Vegetables.radius

            vegetable = Vegetables(veg_x, veg_y)

            if not (str(vegetable) in walls_dict):
                if not (str(vegetable) in vegetables_dict):
                    if not (str(vegetable) in bacterium_dict):
                        vegetables_dict[str(vegetable)] = vegetable

    if len(bacterium_dict) <= 1:
        for i in range(0, 10):
            bac_x = randint(0, int(width / Bacterium.width)) * Bacterium.width
            bac_y = randint(0, int(height / Bacterium.height)) * Bacterium.height
            reac = {"walls": [1, 0, 0, 0], "vegetable": [1, 0, 0, 0], "meat": [1, 0, 0, 0],
                    "bacterium": [1, 0, 0, 0], "like bacterium": [1, 0, 0, 0], "empty cell": [1, 0, 0, 0]}
            bacterium = Bacterium(bac_x, bac_y, reac)

            if str(bacterium) in walls_dict:
                pass
            else:
                if str(bacterium) in bacterium_dict:
                    pass
                else:
                    for j in range(0, 30):
                        bacterium.mutation()

                    bacterium_dict[str(bacterium)] = bacterium

    for i in vegetables_dict.values():
        pygame.draw.circle(screen, i.color, (i.location_x, i.location_y), i.radius)

    rotten = []
    for i in meat_dict.values():
        i.rotting()
        if i.nutritional_value <= 0:
            rotten.append(i)
        pygame.draw.circle(screen, i.color, (i.location_x, i.location_y), i.radius)

    for i in rotten:
        meat_dict.pop(str(i))

    new_bacterium_dict = {}
    for i in bacterium_dict.values():
        if i.health <= 0:
            meat = Meat(i.location_x + Meat.radius, i.location_y + Meat.radius)
            meat_dict[str(meat)] = meat
        elif i.foods <= 0 or i.days <= 0:
            meat = Meat(i.location_x + Meat.radius, i.location_y + Meat.radius)
            meat.nutritional_value -= 50
            meat_dict[str(meat)] = meat
        else:
            i.motion()
            new_bacterium_dict[str(i)] = i

        pygame.draw.rect(screen, i.color, (i.location_x, i.location_y, i.width, i.height))
    bacterium_dict = new_bacterium_dict

    pygame.display.update()

pygame.quit()
