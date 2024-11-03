import numpy as np


class Coordinates:
    """Class used to store and interact with entitie's coordinates"""

    def __init__(self, x, y):
        self.coordinates = np.array([0.0, 0.0])

    def __str__(self):
        return (f'({self.coordinates[0]:.2f} , {self.coordinates[1]:.2f})')
