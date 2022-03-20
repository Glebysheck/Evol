from setting import Setting
from rect import Rect


class Wall(Rect):
    colour = (0, 0, 0)

    num = 0

    Rect.square_object["walls_dict"] = {}

    # Создание стен
    @classmethod
    def create(cls):
        for i in range(Setting.h_indent, int(Setting.height / cls.size) + Setting.h_indent):
            wall_x = i * cls.size
            wall_y = Setting.v_indent * cls.size
            Rect.square_object["walls_dict"]["{}_{}".format(wall_x, wall_y)] = Wall(wall_x, wall_y)
        for i in range(Setting.v_indent + 1, int(Setting.width / cls.size) + Setting.v_indent):
            wall_x = (int(Setting.height / cls.size) + Setting.h_indent - 1) * cls.size
            wall_y = i * cls.size
            Rect.square_object["walls_dict"]["{}_{}".format(wall_x, wall_y)] = Wall(wall_x, wall_y)
        for i in range(Setting.h_indent, int(Setting.height / cls.size) + Setting.h_indent - 1):
            wall_x = i * cls.size
            wall_y = (int(Setting.width / cls.size) + Setting.v_indent - 1) * cls.size
            Rect.square_object["walls_dict"]["{}_{}".format(wall_x, wall_y)] = Wall(wall_x, wall_y)
        for i in range(Setting.v_indent + 1, int(Setting.width / cls.size) + Setting.v_indent - 1):
            wall_x = Setting.h_indent * cls.size
            wall_y = i * cls.size
            Rect.square_object["walls_dict"]["{}_{}".format(wall_x, wall_y)] = Wall(wall_x, wall_y)

        for i in range(Setting.v_indent + 2, int(Setting.width / cls.size) + Setting.v_indent - 2):
            wall_x = int(Setting.height / cls.size / 2 + Setting.h_indent) * cls.size
            wall_y = i * cls.size
            Rect.square_object["walls_dict"]["{}_{}".format(wall_x, wall_y)] = Wall(wall_x, wall_y)
        for i in range(Setting.h_indent + 2, int(Setting.height / cls.size) + Setting.h_indent - 2):
            wall_x = i * cls.size
            wall_y = int(Setting.width / cls.size / 2 + Setting.v_indent) * cls.size
            Rect.square_object["walls_dict"]["{}_{}".format(wall_x, wall_y)] = Wall(wall_x, wall_y)
