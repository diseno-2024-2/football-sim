from classes.utils import Coordinates
import random


class Ball():
    def __init__(self, field):
        self.coordinates: Coordinates = Coordinates()
        self.radius: float = 1  # Change later to apropiate value
        self.field = field

    def kick(self):
        pass

    def control(self):
        pass

    def pass_ball(self):
        pass

    def catch(self):
        pass

    def move(self):
        print(f'Ball coordinates => {
              self.coordinates} - {self.coordinates.speed}')
        if not self.coordinates.is_moving():
            print('Set random coordinates for ball')
            self.random_pos_and_dir()
        else:
            print('Move ball')
            self.coordinates.move()
            self.coordinates.deaccelerate()

    def random_pos_and_dir(self):
        self.coordinates.coordinates[0] = random.randint(
            int(self.field.width * 0.25), int(self.field.width * 0.75))
        self.coordinates.coordinates[1] = random.randint(
            int(self.field.height * 0.25), int(self.field.height * 0.75))
        self.coordinates.speed[0] = random.uniform(-7, 7)
        self.coordinates.speed[1] = random.uniform(-7, 7)
        self.coordinates.acceleration = self.coordinates.speed * -0.05
