from abc import ABC, abstractmethod
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from enum import Enum
from shapely.geometry import Polygon
import math
import random
from classes.utils import Math
import numpy as np


from classes.utils import Coordinates

from classes.field import Field



class PlayerRole(Enum):
    """Enum used to represent the player's role."""
    GOALKEEPER = 1
    DEFENDER = 2
    MIDFIELDER = 3
    FORWARD = 4


class PlayerAttributes():
    """Class containing all relevant player stats."""

    def __init__(self, data):
        # Should read data from the database with player stats and asign it to
        # the corresponding stats. (Define which stats will be used and the
        # data format before implementing)
        pass



class Player(ABC):
    """Abstract class representing a generic player."""

    def __init__(self, name: str, number: int, coordinates: Coordinates,field: Field,time: float):
        self.name: str = name
        self.number: int = number
        self.attributes: PlayerAttributes = None
        self.coordinates: Coordinates = coordinates
        self.role: PlayerRole = None
        self.field: Field = field
        self.time = time
        #wingspan = math.sqrt(math.pow(self.wingspan,2)+ math.pow(self.wingspan,2))
        self.movement: Movement = Movement(self)
        self.doing_something = None
        self.wingspan = 1.7
        self.action_area: Polygon = Polygon([(coordinates.coordinates[0]+self.wingspan,coordinates.coordinates[1]+self.wingspan),
                                             (coordinates.coordinates[0]+self.wingspan,coordinates.coordinates[1]-self.wingspan),
                                             (coordinates.coordinates[0]-self.wingspan,coordinates.coordinates[1]-self.wingspan),
                                             (coordinates.coordinates[0]-self.wingspan,coordinates.coordinates[1]+self.wingspan)])
        
    
    
    
    def move_random(self):
        self.doing_something = self.movement.move
        esta_Fuera = True
        while esta_Fuera:
            self.movement.move_destination_coordinates = [random.randint(0,self.field.width),random.randint(0,self.field.width)]  
            #print("Coordenadas random: ", self.movement.move_destination_coordinates)
            player_area_new_position: Polygon = Polygon([(self.movement.move_destination_coordinates[0]+self.wingspan,self.movement.move_destination_coordinates[1]+self.wingspan),
                                                 (self.movement.move_destination_coordinates[0]+self.wingspan,self.movement.move_destination_coordinates[1]-self.wingspan),
                                                 (self.movement.move_destination_coordinates[0]-self.wingspan,self.movement.move_destination_coordinates[1]-self.wingspan),
                                                 (self.movement.move_destination_coordinates[0]-self.wingspan,self.movement.move_destination_coordinates[1]+self.wingspan)])
        
            if(player_area_new_position.within(self.field.sites.field_site)):
                esta_Fuera = False
                     
    def refresh(self):
        self.action_area = Polygon([(self.coordinates.coordinates[0]+self.wingspan,self.coordinates.coordinates[1]+self.wingspan),
                                             (self.coordinates.coordinates[0]+self.wingspan,self.coordinates.coordinates[1]-self.wingspan),
                                             (self.coordinates.coordinates[0]-self.wingspan,self.coordinates.coordinates[1]-self.wingspan),
                                             (self.coordinates.coordinates[0]-self.wingspan,self.coordinates.coordinates[1]+self.wingspan)])


    def behavior(self):
        if self.doing_something != None:
            
            self.doing_something()
        else: 
            print("Me meto")
            self.move_random()
        self.refresh()
        
        
        

    def __str__(self):
        return (f'{self.name} ({self.number}): {self.coordinates} -> {self.movement}') #- {str.lower(self.role.name)}
    

class Movement():
    def __init__(self,player :Player):
        self.move_destination_coordinates = np.array([0,0])
        self.acceleration = 4
        self.current_direction = np.array([1,0])
        self.destination_direction = np.array([0,0])
        self.current_vel = 0
        self.sprint_speed = 8.71 #m/s
        self.normal_speed = 4.74 #m/s
        self.deceleration = -2
        self.current_deceleration = 0
        self.current_acceleration = self.acceleration
        self.destination_distance = 0
        


        self.player = player

    def __str__(self):
        return (f'velocidad actual: {self.current_vel} | aceleracion: {self.current_acceleration}')
   
    def decelation_to_move(self):
        self.current

    def move_slow(self):
        self.current_acceleration = self.acceleration * (1 - (self.current_vel/self.sprint_speed))
        v0 = self.current_vel
        self.current_vel = self.current_vel + (self.current_acceleration * self.player.time)
        #print("La velocidad: ",self.current_vel, " La aceleracion: ", self.current_acceleration, " Tiempo: ", self.player.time)
        
        
        space = ((v0+self.current_vel)/2)* self.player.time

        #self.current_direction[0] *= space
        #self.current_direction[1] *= space

          
        self.player.coordinates.coordinates = self.player.coordinates.coordinates + (self.current_direction*space) 

    def run(self):
        self.current_acceleration = self.acceleration * (1 - (self.current_vel/self.sprint_speed))
        v0 = self.current_vel
        self.current_vel = self.current_vel + (self.current_acceleration * self.player.time)
        #print("La velocidad: ",self.current_vel, " La aceleracion: ", self.current_acceleration, " Tiempo: ", self.player.time)
        
        
        space = ((v0+self.current_vel)/2)* self.player.time



        #self.current_direction[0] *= space
        #self.current_direction[1] *= space

        if self.destination_distance > space:
            self.player.coordinates.coordinates = self.player.coordinates.coordinates + (self.current_direction*space) 
        else:
            self.player.coordinates.coordinates = self.player.coordinates.coordinates + (self.move_destination_coordinates - self.player.coordinates.coordinates)

        
        #print("Espacio Total Recorrido: ",space, " -> Coordenadas antes: ",coordenadas_antes," Coordenadas Despues: ",self.player.coordinates.coordinates," Lo que me he movido ", self.current_direction)



    

    def move(self):
        
        
        #self.current_direction = [self.move_destination_coordinates[0] - self.player.coordinates.coordinates[0],self.move_destination_coordinates[1] - self.player.coordinates.coordinates[1]] 
        self.current_direction = self.move_destination_coordinates - self.player.coordinates.coordinates
        self.destination_distance = np.linalg.norm(self.current_direction)
        #print("Self MC: ",self.move_destination_coordinates," Player Coor: ", self.player.coordinates.coordinates," current_direction: ", self.current_direction)
        print("Current Direction: ",self.current_direction, " -> norma = ", self.destination_distance)
        if self.destination_distance < 0.1:
            self.player.doing_something = None
            self.current_acceleration = self.acceleration
            self.current_vel = 0

        else:
            

            self.current_direction = self.current_direction/self.destination_distance
            #print("Direccion Normalizada: ", self.current_direction)
            self.run()

        
       
        


class Goalkeeper(Player):
    """Concrete class that defines the goalkeeper's behavior"""

    def __init__(self, name: str, number: int, attributes):
        super().__init__(name, attributes)
        self.position: PlayerRole = PlayerRole.GOALKEEPER

    def make_move(self):
        pass


class Defender(Player):
    """Concrete class that defines the defender's behavior"""

    def __init__(self, name: str, number: int, attributes):
        super().__init__(name, attributes)
        self.position: PlayerRole = PlayerRole.DEFENDER

    def make_move(self):
        pass


class Midfielder(Player):
    """Concrete class that defines the midfielder's behavior"""

    def __init__(self, name: str, number: int, attributes):
        super().__init__(name, attributes)
        self.position: PlayerRole = PlayerRole.MIDFIELDER

    def make_move(self):
        pass


class Forward(Player):
    """Concrete class that defines the forward's behavior"""

    def __init__(self, name: str, number: int, attributes):
        super().__init__(name, attributes)
        self.position: PlayerRole = PlayerRole.FORWARD

    def make_move(self):
        pass
