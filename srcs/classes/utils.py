import numpy as np
import math
from typing import List



class Coordinates:
    """
    Class used to store and interact with entitie's position and movement on a
    2D plane. Speed and acceleration are represented by vectors.
    """

    def __init__(self, x:float, y:float):
        self.coordinates = np.array([0.0, 0.0])
        self.coordinates[0] = x
        self.coordinates[1] = y
        self.speed = np.array([0.0, 0.0])
        self.acceleration = np.array([0.0, 0.0])

    def __str__(self):
        return (f'({self.coordinates[0]:.2f} , {self.coordinates[1]:.2f})')

class Math:

    gravedad: float = 9.8


    def media_geometrica_ponderada(valores,pesos):
        return np.prod(np.power(valores,pesos))



    def convierteminutos(min:float):
        if(min < 10):
            return "0"+str(min)
        return str(min)   

    def rotarvector(vector:np.array,angulo:float):
        angulo_radianes = np.radians(angulo)
        matriz_rotacion = np.array([
            [np.cos(angulo_radianes), -np.sin(angulo_radianes)],
            [np.sin(angulo_radianes),  np.cos(angulo_radianes)]
        ])
        return np.dot(matriz_rotacion, vector)

    def menordistancia(listcoordinates: List[np.array],coordinates:np.array):
        id = 0
        mindistance = Math.distancia(listcoordinates[0],coordinates)

        for i in range(1,len(listcoordinates)):
            distance = Math.distancia(listcoordinates[i],coordinates)
            if distance < mindistance:
                mindistance = distance
                id = i
        
        return id


    def distancia(p1,p2):
        return math.sqrt(math.pow(p1[0]-p2[0],2) + math.pow(p1[1]-p2[1],2))

    def vector(p1,p2):
        return p2 - p1

    @staticmethod
    def angle_between_two_vectors_radians(a,b):
        
        dot_product = np.dot(a, b)

    
        magnitude_A = np.linalg.norm(a)
        magnitude_B = np.linalg.norm(b)

    
        cos_theta = dot_product / (magnitude_A * magnitude_B)

    
        return np.arccos(cos_theta)

    @staticmethod
    def angle_between_two_vectors_degrees(a,b):
        
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
