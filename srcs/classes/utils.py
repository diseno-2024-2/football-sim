import numpy as np


class Coordinates:
    """
    Class used to store and interact with entitie's position and movement on a
    2D plane. Speed and acceleration are represented by vectors.
    """

    def __init__(self, x=0.0, y=0.0):
        self.coordinates = np.array([x, y])
        self.speed = np.array([0.0, 0.0])
        self.acceleration = np.array([0.0, 0.0])

    def is_moving(self):
        if np.any(self.speed != 0):
            return True
        return False

    def move(self):
        self.coordinates += self.speed

    def __str__(self):
        return (f'({self.coordinates[0]:.2f} , {self.coordinates[1]:.2f})')


class Math:
    @staticmethod
    def angle_between_two_vectors_radians(a, b):

        dot_product = np.dot(a, b)

        magnitude_A = np.linalg.norm(a)
        magnitude_B = np.linalg.norm(b)

        cos_theta = dot_product / (magnitude_A * magnitude_B)

        return np.arccos(cos_theta)

    @staticmethod
    def angle_between_two_vectors_degrees(a, b):

        dot_product = np.dot(a, b)

        magnitude_A = np.linalg.norm(a)
        magnitude_B = np.linalg.norm(b)

        cos_theta = dot_product / (magnitude_A * magnitude_B)

        angle_radians = np.arccos(cos_theta)

        return np.degrees(angle_radians)

    # @staticmethod
    # def components_normalizated_vector(module):
    #     component_x = co
    #     component_y
