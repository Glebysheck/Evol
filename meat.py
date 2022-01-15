from food import Food


class Meat(Food):
    nutritional_value = 65
    color = (250, 128, 114)

    meat_dict = {}

    def rotting(self):
        self.nutritional_value -= 2
