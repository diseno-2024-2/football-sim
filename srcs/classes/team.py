from enum import Enum
from typing import List

from classes.player import Player
from classes.player import TeamInformation
from classes.field import Field
import numpy as np
from shapely.geometry import Polygon, LineString
from shapely.geometry import Point
from classes.utils import Coordinates
from scipy.spatial import Voronoi
from shapely.geometry import Polygon, Point
from shapely.ops import clip_by_rect
from classes.ball import Ball
from classes.utils import Math


class TeamFormation(Enum):
    """Enum used to represent the team's formation."""
    pass


class Team():
    """Class representing a team inside a match."""

    def inicializarposiciones(self):
        if (self.id == 1):
            partesx = ((self.field.width)/2)/5
            # Portero
            self.posicionesinciales.append(
                self.players[0].posformacioneinicial(0, self.field.center_y))

            # Defensas
            # print("Altura: ", self.field.height)
            partesy = (self.field.height/4)
            y = partesy/2
            self.posicionesinciales.append(
                self.players[1].posformacioneinicial(partesx*1, (partesy * 0)+y))
            self.posicionesinciales.append(
                self.players[2].posformacioneinicial(partesx*1, (partesy * 1)+y))
            self.posicionesinciales.append(
                self.players[3].posformacioneinicial(partesx*1, (partesy * 2)+y))
            self.posicionesinciales.append(
                self.players[4].posformacioneinicial(partesx*1, (partesy * 3)+y))
            # Centrocampistas
            self.posicionesinciales.append(
                self.players[5].posformacioneinicial(partesx*2, self.field.center_y))

            partesy = (self.field.height/2)
            y = partesy/2
            self.posicionesinciales.append(
                self.players[6].posformacioneinicial(partesx*3, (partesy * 0)+y))
            self.posicionesinciales.append(
                self.players[7].posformacioneinicial(partesx*3, (partesy * 1)+y))

            self.posicionesinciales.append(
                self.players[8].posformacioneinicial(partesx*4, self.field.center_y))

            # Delanteros

            partesy = (self.field.height/2)
            y = partesy/2
            self.posicionesinciales.append(
                self.players[9].posformacioneinicial(partesx*5, (partesy * 0)+y))
            self.posicionesinciales.append(
                self.players[10].posformacioneinicial(partesx*5, (partesy * 1)+y))

        else:
            partesx = ((self.field.width)/2)/5
            # Portero
            self.posicionesinciales.append(self.players[0].posformacioneinicial(
                self.field.width, self.field.center_y))

            # Defensas
            # print("Altura: ", self.field.height)
            partesy = (self.field.height/4)
            y = partesy/2
            self.posicionesinciales.append(self.players[1].posformacioneinicial(
                self.field.width - (partesx*1), (partesy * 0)+y))
            self.posicionesinciales.append(self.players[2].posformacioneinicial(
                self.field.width - (partesx*1), (partesy * 1)+y))
            self.posicionesinciales.append(self.players[3].posformacioneinicial(
                self.field.width - (partesx*1), (partesy * 2)+y))
            self.posicionesinciales.append(self.players[4].posformacioneinicial(
                self.field.width - (partesx*1), (partesy * 3)+y))
            # Centrocampistas
            self.posicionesinciales.append(self.players[5].posformacioneinicial(
                self.field.width - (partesx*2), self.field.center_y))

            partesy = (self.field.height/2)
            y = partesy/2
            self.posicionesinciales.append(self.players[6].posformacioneinicial(
                self.field.width - (partesx*3), (partesy * 0)+y))
            self.posicionesinciales.append(self.players[7].posformacioneinicial(
                self.field.width - (partesx*3), (partesy * 1)+y))

            self.posicionesinciales.append(self.players[8].posformacioneinicial(
                self.field.width - (partesx*4), self.field.center_y))

            # Delanteros

            partesy = (self.field.height/2)
            y = partesy/2
            self.posicionesinciales.append(self.players[9].posformacioneinicial(
                self.field.width - (partesx*5), (partesy * 0)+y))
            self.posicionesinciales.append(self.players[10].posformacioneinicial(
                self.field.width - (partesx*5), (partesy * 1)+y))

    def __init__(self, id: int, playerList: List[Player], rivales: List[Player], field: Field, lado: int):
        # players and their respective position need to be extracted from
        # data
        self.id = id

        self.players: List[Player] = playerList  # Should contain 11 players
        self.bench_players: List[Player] = None  # Should contain 12 players
        self.substitutions_made: int = 0
        self.formation: TeamFormation = None
        self.lado = lado
        self.field: Field = field
        self.posicionesinciales: List[np.array] = []
        self.ball: Ball = self.field.ball
        self.inicializarposiciones()
        self.teaminformation: TeamInformation = TeamInformation()
        self.teaminformation.balon_pasado_a_jugador = self.players[0]
        self.rivales: List[Player] = rivales
        for i in self.players:
            i.id_equipo = id
            i.info_equipo = self.teaminformation
            for x in range(len(self.players)):
                if self.players[x].id != i.id:
                    i.companieros.append(self.players[x])

            i.rivales = rivales.copy()

    def actualizarposiciones(self):
        if (self.id == 1):
            cantidadasumar = (self.ball.coordinates.coordinates[0] - 16.5)/2
        else:
            cantidadasumar = - (self.field.width -
                                self.ball.coordinates.coordinates[0] - 16.5)/2

        for pos in range(1, len(self.players)):
            self.players[pos].posicion_formacion.coordinates[0] = self.posicionesinciales[pos][0] + cantidadasumar

    def jugadormascercanobalon(self):
        idjugador: int = -1
        mindist: float = 900.0
        for player in self.players:
            dist = Math.distancia(
                player.posicion_formacion.coordinates, self.ball.coordinates.coordinates)
            if mindist > dist:
                mindist = dist
                idjugador = player.id

        self.teaminformation.balon_en_la_zona_de = idjugador

        idjugador: int = -1
        mindist: float = 900.0

        for player in self.players:
            dist = Math.distancia(
                player.coordinates.coordinates, self.ball.coordinates.coordinates)
            if mindist > dist:
                mindist = dist
                idjugador = player.id

        self.teaminformation.id_mas_cerca_del_balon = idjugador

    def jugadores_rivales_en_cada_zona(self):

        for player in self.players:
            # print("Zona ", player.id, ": ",len(player.jugadores_rivales_en_mi_zona))
            player.jugadores_rivales_en_mi_zona = []

        for rival in self.rivales:
            idjugador: int = -1
            mindist: float = 900.0
            for player in range(len(self.players)):
                dist = Math.distancia(
                    self.players[player].posicion_formacion.coordinates, rival.coordinates.coordinates)
                if mindist > dist:
                    mindist = dist
                    idjugador = player

            self.players[idjugador].jugadores_rivales_en_mi_zona.append(
                rival.coordinates.coordinates)

    def sub_player(player_out, player_in):
        pass

    def decision(self):
        self.jugadormascercanobalon()
        self.jugadores_rivales_en_cada_zona()
        for player in self.players:
            player.decision()

    def behaviour(self):
        for player in self.players:
            player.behavior()
