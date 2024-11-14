import numpy as np
import random

from classes.utils import Coordinates


class Ball():
    def __init__(self, field):
        self.coordinates: Coordinates = Coordinates()
        self.destination = self.coordinates.coordinates.copy()
        self.distance = 0.0
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

    def update(self):
        if np.all(np.abs(self.coordinates.coordinates - self.destination) < 0.1):
            self.random_destination_and_speed()
            return
        self.coordinates.move()
        new_distance = self.coordinates.distance(self.destination)
        if self.distance != 0 and new_distance > self.distance:
            print(f'{new_distance} > {self.distance}')
            self.coordinates.coordinates = self.destination.copy()
            self.distance = 0.0
            return
        self.distance = new_distance

    def random_destination_and_speed(self):
        destination = np.array([0.0, 0.0])
        destination[0] = random.randint(0, self.field.width)
        destination[1] = random.randint(0, self.field.height)
        force = random.uniform(1, 7)
        self.move(destination, force)

    def move(self, destination, force):
        self.destination = destination.copy()
        direction = (self.destination - self.coordinates.coordinates) / \
            self.coordinates.distance(self.destination)
        self.coordinates.speed = force * direction
