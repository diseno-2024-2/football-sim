import numpy as np
import random

from classes.utils import Coordinates
from shapely.geometry import Polygon



class Ball():
    def __init__(self, time):
        self.alguienlotiene = False
        self.coordinates: Coordinates = Coordinates(40,40)
        self.radius: float =  0.48# Change later to apropiate value
        self.time = time
        self.force = 0
        self.id_passed = -1
        self.movement = Movement(self)
        self.tiempo_contacto = 0.1
        self.masa = 0.420
        self.doing_something = None
        self.action_area: Polygon = Polygon([(self.coordinates.coordinates[0]+self.radius,self.coordinates.coordinates[1]+self.radius),
                                             (self.coordinates.coordinates[0]+self.radius,self.coordinates.coordinates[1]-self.radius),
                                             (self.coordinates.coordinates[0]-self.radius,self.coordinates.coordinates[1]-self.radius),
                                             (self.coordinates.coordinates[0]-self.radius,self.coordinates.coordinates[1]+self.radius)])
        self.hasidopasada = False

    def refresh(self):
        self.action_area: Polygon = Polygon([(self.coordinates.coordinates[0]+self.radius,self.coordinates.coordinates[1]+self.radius),
                                             (self.coordinates.coordinates[0]+self.radius,self.coordinates.coordinates[1]-self.radius),
                                             (self.coordinates.coordinates[0]-self.radius,self.coordinates.coordinates[1]-self.radius),
                                             (self.coordinates.coordinates[0]-self.radius,self.coordinates.coordinates[1]+self.radius)])

    def kick(self):
        pass

    def control(self):
        pass

    def stop(self):
        self.doing_something = None
        self.movement.current_vel = 0
        self.id_passed = -1

    def pass_ball(self,direction,force,id):
        self.alguienlotiene = False
        self.movement.current_vel = (force * 0.5 / self.masa)
        #print("Velocidad Inicial del Pase: ",self.movement.current_vel)
        norma = np.linalg.norm(direction)
        if norma > 0:
            self.movement.direction_pase = direction/norma
        self.doing_something = self.movement.move
        self.id_passed = id
        self.hasidopasada = True
        
        #print("Inicio del pase: ", self.id_passed)


    def catch(self,forcerebote,direction):
        self.alguienlotiene = True
        self.movement.current_vel = (forcerebote * 0.1 / self.masa)
        #print("Velocidad Inicial del Pase: ",self.movement.current_vel)
        norma = np.linalg.norm(direction)
        if norma > 0:
            self.movement.direction_pase = direction/norma
        self.doing_something = self.movement.move
        self.id_passed = -1
        self.hasidopasada = False
        pass

    def behaviour(self):
        if self.doing_something != None:
            self.doing_something()
        else:
            self.id_passed = -1
        self.refresh()
        
    
class Movement():
    def __init__(self,ball: Ball):
        self.acceleration_frenado = -9.8 * 0.4
        self.direction_pase = np.array([0,0])
        self.current_vel = 0
        self.ball= ball
    
    def move(self):
        
        v0 = self.current_vel

        self.current_vel = self.current_vel + (self.acceleration_frenado * self.ball.time)

        space = ((v0+self.current_vel)/2)* self.ball.time

        if(self.current_vel < 0):
            self.ball.stop()

        self.ball.coordinates.coordinates = self.ball.coordinates.coordinates + (self.direction_pase*space)

        


    def __str__(self):
        return (f'velocidad actual: {self.current_vel} | aceleracion: {self.current_acceleration}')


    


