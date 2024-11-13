from classes.utils import Coordinates


class Ball():
    def __init__(self):
        self.coordinates: Coordinates = Coordinates()
        self.radius: float = 1  # Change later to apropiate value

    def kick(self):
        pass

    def control(self):
        pass

    def pass_ball(self):
        pass

    def catch(self):
        pass

    def move(self):
        if not self.coordinates.is_moving():
            self.coordinates.speed[0] = 1
            self.coordinates.speed[1] = 1
        else:
            self.coordinates.move()
            print(self.coordinates)
