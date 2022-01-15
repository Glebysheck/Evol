class Food:
    radius = 10

    def __init__(self, location_x, location_y):
        self.location_x = location_x
        self.location_y = location_y

    def __str__(self):
        return "{}_{}".format(self.location_x - self.radius, self.location_y - self.radius)
