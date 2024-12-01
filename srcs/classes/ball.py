import numpy as np
import random
import math
from classes.utils import Coordinates
from shapely.geometry import Polygon
from classes.utils import Math



class Ball():
    def __init__(self, time):
        self.alguienlotiene = False
        self.coordinates: Coordinates = Coordinates(40,40)

        self.long_pass_coordinates: np.array = np.array([1.3,1.3])
        self.radius: float =  0.48# Change later to apropiate value
        self.time = time
        self.force = 0
        self.id_passed = -1
        
        self.tiempo_contacto = 0.5
        self.masa = 0.420
        self.doing_something = None
        self.action_area: Polygon = Polygon([(self.coordinates.coordinates[0]+self.radius,self.coordinates.coordinates[1]+self.radius),
                                             (self.coordinates.coordinates[0]+self.radius,self.coordinates.coordinates[1]-self.radius),
                                             (self.coordinates.coordinates[0]-self.radius,self.coordinates.coordinates[1]-self.radius),
                                             (self.coordinates.coordinates[0]-self.radius,self.coordinates.coordinates[1]+self.radius)])
        self.hasidopasada = False
        self.campo = None
        self.movement = Movement(self)
        
        
        

        

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

    def run_with_ball(self,coordinates:np.ndarray):
        #print("run_with_ball: ",coordinates)
        self.doing_something = None
        self.movement.current_vel = 0
        self.id_passed = -1
        self.coordinates.coordinates[0] = float(coordinates[0])
        self.coordinates.coordinates[1] = float(coordinates[1])
        self.alguienlotiene = True 
        self.refresh()
        #print("Coordenadas de la Pelota = ",self.coordinates.coordinates)

    def pase_largo(self,direction,force,id,distancia,coordinates):

        """Realiza un pase largo."""    
        self.alguienlotiene = False

        self.long_pass_coordinates = coordinates
        
        # Calcular velocidad inicial a partir de la fuerza aplicada
        self.movement.current_vel = (force * self.tiempo_contacto) / self.masa
        norma = np.linalg.norm(direction)
        if norma > 0:
            self.movement.direction_pase = direction / norma

        # Asumimos un ángulo de lanzamiento (45° para optimizar alcance)
        angle = math.radians(45)  # Ángulo en radianes
        v0 = self.movement.current_vel
        
        self.movement.current_vel_y_pase_largo = self.movement.current_vel * math.sin(angle)
        self.movement.current_vel = self.movement.current_vel * math.cos(angle)

        # Tiempo total de vuelo para un lanzamiento parabólico
        
        # Distancia máxima alcanzable con la fuerza aplicada
        
        
        # Espacio recorrido por iteración
        self.movement.espacioporiteracionpaselargo = self.movement.current_vel * self.time
        self.movement.paselargo = []
        # Configurar la acción
        self.doing_something = self.movement.movimiendome_por_encima
        self.id_passed = id
        self.hasidopasada = True
    



    def pass_ball(self,direction,force,id):
        self.alguienlotiene = False
        self.movement.current_vel = (force * self.tiempo_contacto / self.masa)
        #print("Velocidad Inicial del Pase: ",self.movement.current_vel)
        norma = np.linalg.norm(direction)
        if norma > 0:
            self.movement.direction_pase = direction/norma
        self.doing_something = self.movement.move
        self.id_passed = id
        self.hasidopasada = True
        
        #print("Inicio del pase: ", self.id_passed)


    def catch(self,forcerebote,direction):
        if not(self.alguienlotiene):
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

    def catch_pass_largo(self,forcerebote,direction):
        
        self.alguienlotiene = False
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
        self.acceleration_frenado = -Math.gravedad * ball.masa
        self.direction_pase = np.array([0,0])
        self.current_vel = 0
        self.current_vel_x_pase_largo:float = 0
        self.current_vel_y_pase_largo:float = 0
        self.ball= ball
        self.timepaselargo: float = -1
        self.espacioporiteracionpaselargo: float = -1
        self.coordenada_aerea = 0
        self.paselargo = []

    def movimiendome_por_encima(self):
        #print("MOVIENDOME POR ENCIMA: vel =",self.current_vel, " tiempo restante = " , self.timepaselargo, " Distancia respecto al suelo", self.coordenada_aerea)
        

        self.ball.coordinates.coordinates += self.direction_pase * (self.current_vel * self.ball.time)
        self.coordenada_aerea += (self.current_vel_y_pase_largo * self.ball.time) - ((Math.gravedad * (self.ball.time**2)/2))
        self.current_vel_y_pase_largo -= Math.gravedad * self.ball.time

        if(self.coordenada_aerea <= 0):
            self.timepaselargo = -1
            self.ball.doing_something = None
            self.coordenada_aerea = 0
            self.ball.campo.evento_actual = None # Debería dejar de ser un evento de pase largo cuando se hayan resuelto

        
        
    
    def caerse(self):
        delta_x = self.paselargo.pop()
        self.ball.coordinates.coordinates += self.direction_pase * delta_x

        if len(self.paselargo) == 0:
            self.timepaselargo = -1
            self.ball.doing_something = None
            self.coordenada_aerea = 0
            self.ball.campo.evento_actual = None # Debería dejar de ser un evento de pase largo cuando se hayan resuelto

        
    
    def move(self):
        
        v0 = self.current_vel

        self.current_vel = self.current_vel + (self.acceleration_frenado * self.ball.time)

        space = ((v0+self.current_vel)/2)* self.ball.time

        if(self.current_vel < 0):
            self.ball.stop()

        self.ball.coordinates.coordinates = self.ball.coordinates.coordinates + (self.direction_pase*space)

        


    def __str__(self):
        return (f'velocidad actual: {self.current_vel} | aceleracion: {self.current_acceleration}')


    


