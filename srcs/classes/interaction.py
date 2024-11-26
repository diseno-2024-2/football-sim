from shapely.geometry import Polygon
import numpy as np
from classes.player import Player
from classes.utils import Math
from classes.ball import Ball
from classes.field import Field
from typing import List
import random


class Interaction:
    """
    Clase para crear y mostrar una ventana interactiva con un polígono y una línea en Pygame.
    """

    def __init__(self, playerList: List[Player], ball: Ball, field: Field):
        # Inicializar Pygame
        self.player_list = playerList
        self.ball: Ball = ball
        self.field: Field = field

        self.jugadorescuandosehizoelpase = []
        self.candidatosanteriores = []
        self.candidatosanteriorescontrol = []

        self.clock = 0
        self.timepoint = -1
        self.time = 0

    def resolverconflictos(self):
        self.sehapasadoelbalon()
        self.disputadebalondividido()
        self.controlarbalon()
        self.balonsehaidofuerae()
        self.losjugadorespuedenvolveraatraparla()

    def sehapasadoelbalon(self):
        if self.ball.hasidopasada:
            # print("Ha sido pasada")
            self.jugadorescuandosehizoelpase = []
            # print("Ha sido pasada")
            for player in self.player_list:
                if player.action_area.intersects(self.ball.action_area):
                    self.jugadorescuandosehizoelpase.append(player)
            self.ball.hasidopasada = False

    def losjugadorespuedenvolveraatraparla(self):
        # print("Time:  ", self.time - self.timepoint)
        if self.timepoint > 0 and self.time - self.timepoint > 0.5:
            # print("Ya pueden los jugadores inhabilitados")
            self.jugadorescuandosehizoelpase = []
            self.candidatosanteriores = []

    def disputadebalondividido(self):
        if self.ball.id_passed == -1:
            candidatos: List[Player] = []
            for player in self.player_list:
                if player.action_area.intersects(self.ball.action_area) and self.ball.id_passed != player.id and player not in self.candidatosanteriores:
                    candidatos.append(player)

            # Sustituir el siguiente codigo por el de disputa entre los jugadores 2 a 2
            if len(candidatos) > 0:
                # print('candidatos en disputadebalondividido:')
                # for i in candidatos:
                #     print(i)
                self.timepoint = self.time
                # print("Disputa del Balón Dividido")
                elegido = random.randint(0, len(candidatos)-1)

                # print("Cojo el valon: id del ultimo que la paso ",self.ball.id_passed," id del elegido ",elegido)
                candidatos[elegido].tengoelbalon = True
                candidatos[elegido].doing_something = None
                self.ball.alguienlotiene = True
                self.player_list[0].field.equipo_con_balon = candidatos[elegido].id_equipo

                self.candidatosanteriores = candidatos
                self.jugadorescuandosehizoelpase = []
                # print("Balon interceptado disputadebalondividido")

    '''Para simular los controles lo hacemos de la siguiente manera: 
            1. Obtenemos el vector del Jugador -> Pelota.
            2. Lo normalizamos.
            4. Lo rotamos en angulo aleatorio entre [-45º,45º]
            5. La fuerza será medida según el control del jugador aunque por ahora será aleatoria. 10 N 
    '''

    def controlarbalon(self):
        if self.ball.id_passed != -1:
            candidatos: List[Player] = []
            for player in self.player_list:
                if player.action_area.intersects(self.ball.action_area) and player not in self.jugadorescuandosehizoelpase + self.candidatosanteriores:
                    candidatos.append(player)

            if len(candidatos) > 0:  # control
                # print("Disputa del control de balón")
                # print('candidatos en controlarbalon:')
                # for i in candidatos:
                #     print(i)
                elegido = random.randint(0, len(candidatos)-1)
                # print("Balon interceptado controlarbalon")
                # print("Cojo el valon: id del ultimo que la paso ",self.ball.id_passed," id del elegido ",elegido)

                vjugador_pelota = Math.vector(
                    candidatos[elegido].coordinates.coordinates, self.ball.coordinates.coordinates)
                norma = np.linalg.norm(vjugador_pelota)
                if (norma != 0):
                    vjugador_pelota = vjugador_pelota / \
                        np.linalg.norm(vjugador_pelota)
                    angulo_de_rotacion = random.randint(0, 90)-45
                    vrotado = Math.rotarvector(
                        vjugador_pelota, angulo_de_rotacion)
                    self.ball.catch(3, vrotado)
                    self.ball.hasidopasada = False
                    self.ball.alguienlotiene = False
                    candidatos[elegido].tengoelbalon = False

                else:
                    # print(f"candidato elegido = {candidatos[elegido].id_equipo}, {
                    #       candidatos[elegido].id}")
                    self.ball.alguienlotiene = True
                    candidatos[elegido].tengoelbalon = True
                    self.player_list[0].field.equipo_con_balon = candidatos[elegido].id_equipo

                self.candidatosanteriorescontrol = candidatos

         # print("Ya no hay PASE")

    def balonsehaidofuerae(self):
        if (not (self.ball.action_area.within(self.field.sites.field_site))):
            self.ball.stop()
            self.ball.coordinates.coordinates[0] = self.field.center_x
            self.ball.coordinates.coordinates[1] = self.field.center_y
