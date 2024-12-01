from shapely.geometry import Polygon,LineString
import numpy as np
from classes.player import Player
from classes.utils import Math
from classes.ball import Ball
from classes.field import Field
from classes.field import Evento
from typing import List
import random
from classes.team import Team
import math

class Interaction:
    """
    Clase para crear y mostrar una ventana interactiva con un polígono y una línea en Pygame.
    """

    def __init__(self,playerList: List[Player],ball: Ball,field: Field,team1: Team,team2:Team):
        # Inicializar Pygame
        self.player_list = playerList
        self.ball: Ball = ball
        self.field: Field = field
        self.team1: Team = team1
        self.team2: Team = team2 
        self.jugadorescuandosehizoelpase = []
        self.candidatosanteriores = []
        self.candidatosanteriorescontrol = []

        self.clock = 0
        self.timepoint= -1
        self.time = 0

    def resolverconflictos(self):
        self.sehapasadoelbalon()
        self.disputadebalondividido()
        self.controlarbalon()
        self.balonsehaidofuerae()
        self.losjugadorespuedenvolveraatraparla()


    def sehapasadoelbalon(self):
        if self.ball.hasidopasada:
            #print("Ha sido pasada")
            self.jugadorescuandosehizoelpase = []
            #print("Ha sido pasada")
            for player in self.player_list:
                    if player.action_area.intersects(self.ball.action_area) and self.field.equipo_con_balon != player.id_equipo: 
                        self.jugadorescuandosehizoelpase.append(player)
            self.ball.hasidopasada = False

    def losjugadorespuedenvolveraatraparla(self):
        #print("Time:  ",self.time - self.timepoint)
        if self.timepoint > 0 and self.time - self.timepoint > 1:
            #print("Ya pueden los jugadores inhabilitados")
            self.jugadorescuandosehizoelpase = [] 
            self.candidatosanteriores = []


           

    def disputadebalondividido(self):
        if self.field.evento_actual != Evento.PASE_LARGO:
            if self.ball.id_passed == -1:
                    candidatos: List[Player] = []
                    for player in self.player_list:
                        if player.action_area.intersects(self.ball.action_area) and self.ball.id_passed != player.id and player not in self.candidatosanteriores:
                            candidatos.append(player)

                # Sustituir el siguiente codigo por el de disputa entre los jugadores 2 a 2
                    if len(candidatos) > 0:
                        self.timepoint = self.time
                        #print("Disputa del Balón Dividido")
                        elegido = random.randint(0,len(candidatos)-1)
                        
                        #print("Cojo el valon: id del ultimo que la paso ",self.ball.id_passed," id del elegido ",elegido)
                        candidatos[elegido].tengoelbalon = True
                        candidatos[elegido].doing_something = None
                        self.ball.alguienlotiene = True
                        self.player_list[0].field.equipo_con_balon = candidatos[elegido].id_equipo

                        self.candidatosanteriores = candidatos 
                        self.jugadorescuandosehizoelpase = []
                    
                
                


    '''Para simular los controles lo hacemos de la siguiente manera: 
            1. Obtenemos el vector del Jugador -> Pelota.
            2. Lo normalizamos.
            4. Lo rotamos en angulo aleatorio entre [-45º,45º]
            5. La fuerza será medida según el control del jugador aunque por ahora será aleatoria. 10 N 
    '''



    def controlarbalon(self):
        if self.field.evento_actual != Evento.PASE_LARGO:
            if self.ball.id_passed != -1 and not(self.ball.alguienlotiene):
                    candidatos: List[Player] = []
                    for player in self.player_list:
                        if player.action_area.intersects(self.ball.action_area) and player not in self.jugadorescuandosehizoelpase + self.candidatosanteriores:
                            candidatos.append(player)

                    if len(candidatos) > 0: #control
                        #print("Disputa del control de balón")
                        elegido = random.randint(0,len(candidatos)-1)
                        #print("Cojo el valon: id del ultimo que la paso ",self.ball.id_passed," id del elegido ",elegido)
                        
                        vjugador_pelota = Math.vector(candidatos[elegido].coordinates.coordinates,self.ball.coordinates.coordinates)
                        norma = np.linalg.norm(vjugador_pelota)
                        if(norma != 0):
                            vjugador_pelota = vjugador_pelota/np.linalg.norm(vjugador_pelota)
                            angulo_de_rotacion = random.randint(0,90)-45
                            vrotado = Math.rotarvector(vjugador_pelota,angulo_de_rotacion)
                            self.ball.catch(3,vrotado)
                            self.ball.hasidopasada = False
                            self.ball.alguienlotiene = False
                            candidatos[elegido].tengoelbalon = False
                            
                        else:
                            self.ball.alguienlotiene = True
                            candidatos[elegido].tengoelbalon = True
                            self.player_list[0].field.equipo_con_balon = candidatos[elegido].id_equipo

                        
                        self.candidatosanteriorescontrol = candidatos
        else: 
            if self.field.ball.movement.coordenada_aerea <= 1.8: # Hay que incorporarlo a bajo dependiendo de la altura de los jugadores
                    candidatos: List[Player] = []
                    for player in self.player_list:
                        if player.action_area.intersects(self.ball.action_area) and player not in self.jugadorescuandosehizoelpase + self.candidatosanteriores:
                            candidatos.append(player)

                    if len(candidatos) > 0: #control
                        #print("Disputa del control de balón PASE LARGO")
                        elegido = random.randint(0,len(candidatos)-1)
                        #print("Cojo el valon: id del ultimo que la paso ",self.ball.id_passed," id del elegido ",elegido)
                        
                        vjugador_pelota = self.ball.movement.direction_pase
                        norma = np.linalg.norm(vjugador_pelota)
                        if(norma != 0):
                            vjugador_pelota = vjugador_pelota/np.linalg.norm(vjugador_pelota)
                            angulo_de_rotacion = random.randint(0,90)-45
                            vrotado = Math.rotarvector(vjugador_pelota,angulo_de_rotacion)
                            fuerza_rebote = (self.ball.masa * math.sqrt((self.ball.movement.current_vel**2) + (self.ball.movement.current_vel_y_pase_largo)))
                            #print("FUERZA DE REBOTE = ", fuerza_rebote)
                            #self.ball.catch_pass_largo(fuerza_rebote,vrotado)
                            self.ball.hasidopasada = False
                            self.ball.alguienlotiene = False
                            candidatos[elegido].tengoelbalon = False
                            self.field.evento_actual = None
                            
                        else:
                            self.ball.alguienlotiene = True
                            candidatos[elegido].tengoelbalon = True
                            self.player_list[0].field.equipo_con_balon = candidatos[elegido].id_equipo

                        
          
                    
                    

               
    def eliminarposesionbalon(self):
        for i in range(len(self.player_list)):
           self.player_list[i].tengoelbalon = False 



    def balonsehaidofuerae(self):
        if(self.ball.coordinates.coordinates[0] < 0):
            if(self.ball.coordinates.coordinates[1] > self.field.center_y):
                self.ball.coordinates.coordinates[0] = 0
                self.ball.coordinates.coordinates[1] = self.field.height
                self.field.evento_actual = Evento(Evento.CORNER)
                self.field.equipo_con_balon = (self.field.equipo_con_balon+1)%2
                self.eliminarposesionbalon()
                self.team1.posicioneseventoactualizadas = False
                self.team2.posicioneseventoactualizadas = False
                print("CORNER | EQUIPO CON POSESIÓN: ", self.field.equipo_con_balon)
                self.ball.stop()
            else:
                self.ball.coordinates.coordinates[0] = 0
                self.ball.coordinates.coordinates[1] = 0
                self.field.evento_actual = Evento(Evento.CORNER)
                self.team1.posicioneseventoactualizadas = False
                self.team2.posicioneseventoactualizadas = False
                self.field.equipo_con_balon = (self.field.equipo_con_balon+1)%2
                print("CORNER | EQUIPO CON POSESIÓN: ", self.field.equipo_con_balon)
                self.eliminarposesionbalon()
                self.ball.stop()
        else: 
            if(self.ball.coordinates.coordinates[0] > self.field.width):
                if(self.ball.coordinates.coordinates[1] > self.field.center_y):
                    self.ball.coordinates.coordinates[0] = self.field.width
                    self.ball.coordinates.coordinates[1] = self.field.height
                    self.field.equipo_con_balon = (self.field.equipo_con_balon+1)%2
                    print("CORNER | EQUIPO CON POSESIÓN: ", self.field.equipo_con_balon)
                    self.team1.posicioneseventoactualizadas = False
                    self.team2.posicioneseventoactualizadas = False
                    print("LA PELOTA HA SALIDO")
                    self.eliminarposesionbalon()
                    self.ball.stop()
                else:
                    self.ball.coordinates.coordinates[0] = self.field.width
                    self.ball.coordinates.coordinates[1] = 0
                    self.field.equipo_con_balon = (self.field.equipo_con_balon+1)%2
                    print("CORNER | EQUIPO CON POSESIÓN: ", self.field.equipo_con_balon)
                    self.team1.posicioneseventoactualizadas = False
                    self.team2.posicioneseventoactualizadas = False
                    print("LA PELOTA HA SALIDO")
                    self.eliminarposesionbalon()
                    self.ball.stop()
            else: 
                if(self.ball.coordinates.coordinates[1] > self.field.height):
                    self.ball.coordinates.coordinates[1] = self.field.height
                    self.field.equipo_con_balon = (self.field.equipo_con_balon+1)%2
                    self.field.evento_actual = Evento(Evento.FUERA)
                    print("FUERA | EQUIPO CON POSESIÓN: ", self.field.equipo_con_balon)
                    self.team1.posicioneseventoactualizadas = False
                    self.team2.posicioneseventoactualizadas = False
                    self.eliminarposesionbalon()
                    self.ball.stop()
                else:
                    if(self.ball.coordinates.coordinates[1] < 0):
                        self.ball.coordinates.coordinates[1] = 0
                        self.field.evento_actual = Evento(Evento.FUERA)
                        self.field.equipo_con_balon = (self.field.equipo_con_balon+1)%2
                        print("FUERA | EQUIPO CON POSESIÓN: ", self.field.equipo_con_balon)
                        self.team1.posicioneseventoactualizadas = False
                        self.team2.posicioneseventoactualizadas = False
                        self.eliminarposesionbalon()
                        self.ball.stop()
        

        

        

        


        
        

