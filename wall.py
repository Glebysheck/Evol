from setting import Setting


class Wall:
    width, height = 20, 20
    colour = (0, 0, 0)

    num = 0

    walls_list = []
    walls_dict = {}

    def __init__(self, location_x, location_y):
        self.location_x = location_x
        self.location_y = location_y

    def __str__(self):
        return "{}_{}".format(self.location_x, self.location_y)

    # Создание стен
    @classmethod
    def create(cls):
        for i in range(0, int(Setting.height / cls.width)):
            cls.walls_list.append(Wall(i * cls.width, 0))
        for i in range(1, int(Setting.width / cls.height)):
            cls.walls_list.append(Wall((int(Setting.height / cls.width) - 1) * cls.width, i * cls.width))
        for i in range(0, int(Setting.height / cls.width) - 1):
            cls.walls_list.append(Wall(i * cls.width, (int(Setting.width / cls.height) - 1) * cls.height))
        for i in range(1, int(Setting.width / cls.height) - 1):
            cls.walls_list.append(Wall(0, i * cls.height))

        for i in range(2, int(Setting.width / cls.width) - 2):
            cls.walls_list.append(Wall(int(Setting.height / cls.height / 2) * cls.height, i * cls.width))
        for i in range(2, int(Setting.height / cls.width) - 2):
            cls.walls_list.append(Wall(i * cls.width, int(Setting.width / cls.height / 2) * cls.width))

        for i in cls.walls_list:
            cls.walls_dict[str(i)] = i
