import numpy as np
from enum import Enum
from typing import List

from classes.utils import Coordinates
from classes.player import Player
from classes.ball import Ball
from classes.utils import Math
from classes.field import Evento
from classes.player import TeamInformation
from classes.field import Field


class TeamFormation(Enum):
    """Enum used to represent the team's formation."""
    pass


class Team():
    """Class representing a team inside a match."""

    def __init__(self, id: int, players, collection, field, color):
        self.color = color
        self.id = id
        self.lado = self.id + 1
        self.players = []
        self.substitutes = []
        self.substitutions_made: int = 0
        self.formation: TeamFormation = None
        self.field: Field = field
        self.posicionesinciales: List[np.array] = []
        self.posicioneseventoactualizadas = False
        self.ball: Ball = self.field.ball
        self.teaminformation: TeamInformation = TeamInformation()
        starters = players['starting']
        subs = players['substitutes']
        for id, p in enumerate(starters):
            self.players.append(
                Player(  # Cambiar
                    collection.find_one({"_id": p['id']}),
                    p['role'],
                    Coordinates(0, 0),
                    field,
                    self.color,
                    1,  # time
                    id
                )
            )
        for id, p in enumerate(subs):
            self.substitutes.append(
                Player(
                    collection.find_one({"_id": p['id']}),
                    None,
                    Coordinates(0, 0),
                    field,
                    self.color,
                    1,  # Time
                    id
                )
            )
        self.teaminformation.balon_pasado_a_jugador = self.players[0]
        self.inicializarposiciones()

    def set_player_info(self, rival):
        self.rivales = rival.players
        for i in self.players:
            i.id_equipo = id
            i.info_equipo = self.teaminformation
            for x in range(len(self.players)):
                if self.players[x].id != i.id:
                    i.companieros.append(self.players[x])
            i.rivales = self.rivales.copy()

    def actualizarposiciones(self):
        if (self.id == 1):
            cantidadasumar = (self.ball.coordinates.coordinates[0] - 16.5)/2
        else:
            cantidadasumar = - (self.field.width -
                                self.ball.coordinates.coordinates[0] - 16.5)/2

        for pos in range(1, len(self.players)):
            self.players[pos].posicion_formacion.coordinates[0] = self.posicionesinciales[pos][0] + cantidadasumar

        if not (self.posicioneseventoactualizadas):

            if self.field.evento_actual == Evento.FUERA or self.field.evento_actual == Evento.CORNER:
                self.posicioneseventoactualizadas = True
                for pos in range(0, len(self.players)):
                    self.players[pos].coordinates.coordinates[0] = self.players[pos].posicion_formacion.coordinates[0]
                    self.players[pos].coordinates.coordinates[1] = self.players[pos].posicion_formacion.coordinates[1]
                if self.field.equipo_con_balon == self.id:
                    print("ACTUALIZANDO POSICIONES EQUIPO CON POSESIÓN: ",
                          self.field.equipo_con_balon)
                    jugadorquesaca = np.array([Math.distancia(self.players[pos].posicion_formacion.coordinates,
                                              self.ball.coordinates.coordinates) for pos in range(0, len(self.players))]).argmin()
                    self.players[jugadorquesaca].coordinates.coordinates[0] = self.ball.coordinates.coordinates[0]
                    self.players[jugadorquesaca].coordinates.coordinates[1] = self.ball.coordinates.coordinates[1]
                    print("ID DEL JUGADOR QUE SACA: ", jugadorquesaca)
                    self.players[jugadorquesaca].tengoelbalon = True

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

    def __str__(self):
        string = ''
        string += "Starting players:\n"
        for p in self.players:
            string += f'{str(p)}\n'
        string += "\nSubstitutes:\n"
        for p in self.substitutes:
            string += f'{str(p)}\n'
        return (string)

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
