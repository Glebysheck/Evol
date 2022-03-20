from random import randint
from food import Food
from setting import Setting


class Vegetable(Food):
    nutritional_value = 30
    color = (0, 128, 0)

    vegetables_dict = {}

    @classmethod
    def generation(cls, bacterium_dict, walls_dict):
        for i in range(0, 15):
            rand_x = randint(1 + Setting.h_indent, int(Setting.height / (cls.radius * 2)) - 2 + Setting.h_indent)
            veg_x = rand_x * cls.radius * 2 + cls.radius
            rand_y = randint(1 + Setting.v_indent, int(Setting.width / (cls.radius * 2)) - 2 + Setting.v_indent)
            veg_y = rand_y * cls.radius * 2 + cls.radius

            vegetable = Vegetable(veg_x, veg_y)

            if not (str(vegetable) in walls_dict):
                if not (str(vegetable) in cls.vegetables_dict):
                    if not (str(vegetable) in bacterium_dict):
                        cls.vegetables_dict[str(vegetable)] = vegetable
