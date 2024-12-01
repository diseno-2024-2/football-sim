from enum import Enum
from shapely.geometry import Polygon, Point
from shapely import LineString
import math
import random
import numpy as np
from typing import List

from classes.field import Evento
from classes.utils import Coordinates
from classes.utils import Math
from classes.field import Field


class PlayerRole(Enum):
    """Enum used to represent the player's role."""
    GK = 1
    RB = 2
    LB = 3
    CB = 4
    CDM = 5
    CM = 6
    RM = 7
    LM = 8
    CAM = 9
    CF = 10
    ST = 11
    LW = 12
    RW = 13


class Probabilidades():
    pesos_decision_alternativas_equipo_perdiendo: np.array = np.array([
                                                                      0.41, 0.32, 0.27])
    pesos_decision_alternativas_equipo_ganando: np.array = np.array([
                                                                    0.37, 0.21, 0.42])

    def probabilidad_de_marcar_gol(jugador: 'Player', portero: 'Player'):
        return random.randint(50, 100)


class Alternativa():
    def __init__(self, player: "Player", tipo: 'AlternativaType', distancia_adversario: float, distancia_porteria: float, probilidad_de_marcar_gol: float = 0.0, movecoordinates: np.array = None, alternativas: List["Alternativa"] = None):
        self.player = player
        self.distancia_adversario = distancia_adversario
        self.distancia_porteria = distancia_porteria
        self.alternativas = alternativas or []  # Asegura que siempre sea una lista
        self.movecoordinates: np.array = movecoordinates
        self.probabilidad_de_marcar_gol: float = probilidad_de_marcar_gol
        self.tipo = tipo

    def vectorizar(self):
        return np.array([self.probabilidad_de_marcar_gol, self.distancia_porteria, self.distancia_adversario])

    def __str__(self):
        return (f'Jugador {self.player.id} - dis.ad {self.distancia_adversario} - dis.por {self.distancia_porteria} - num.alt {len(self.alternativas)}')


class AlternativaType(Enum):
    PASS = 1
    MOVE = 2
    LONG_PASS = 3
    SHOT = 4


position_map = {
    "GK": PlayerRole.GK,
    "RB": PlayerRole.RB,
    "LB": PlayerRole.LB,
    "CB": PlayerRole.CB,
    "CDM": PlayerRole.CDM,
    "CM": PlayerRole.CM,
    "RM": PlayerRole.RM,
    "LM": PlayerRole.LM,
    "CAM": PlayerRole.CAM,
    "CF": PlayerRole.CF,
    "ST": PlayerRole.ST,
    "LW": PlayerRole.LW,
    "RW": PlayerRole.RW
}


class Player():
    """Abstract class representing a generic player."""


    def __init__(self, data, role, coordinates: Coordinates, field: Field, color, time: float, id: int):
        self.data = data
        self.role = position_map.get(role)
        self.coordinates = coordinates
        self.posicion_formacion = Coordinates(
            coordinates.coordinates[0], coordinates.coordinates[1])
        self.id = data['_id']
        self.id_equipo = 0
    # def __init__(self, name: str, number: int, coordinates: Coordinates, field: Field, color, time: float):

        self.field: Field = field
        self.time = time
        # wingspan = math.sqrt(math.pow(self.wingspan,2)+ math.pow(self.wingspan,2))
        self.movement: Movement = Movement(self)
        self.doing_something = None
        self.wingspan = 1  # 1.7
        self.action_area: Polygon = Polygon([(coordinates.coordinates[0]+self.wingspan, coordinates.coordinates[1]+self.wingspan),
                                             (coordinates.coordinates[0]+self.wingspan,
                                              coordinates.coordinates[1]-self.wingspan),
                                             (coordinates.coordinates[0]-self.wingspan,
                                              coordinates.coordinates[1]-self.wingspan),
                                             (coordinates.coordinates[0]-self.wingspan, coordinates.coordinates[1]+self.wingspan)])
        self.tengoelbalon = False
        self.color_inicial = color
        self.color = color
        self.fuerza_pase_corto = 10
        self.fuerza_maxima_pase_largo = 20
        self.distancia_maxima_pase_largo = math.pow(
            (self.fuerza_maxima_pase_largo * self.field.ball.tiempo_contacto / self.field.ball.masa), 2)/(9.8)
        self.distancia_maxima_pase = math.pow((self.fuerza_pase_corto * self.field.ball.tiempo_contacto /
                                              self.field.ball.masa), 2)/(-2 * (self.field.ball.movement.acceleration_frenado))
        self.companieros: List[Player] = []
        self.rivales: List[Player] = []
        self.regiondelcampoasignada: Polygon = None
        self.info_equipo: TeamInformation = None
        self.jugadores_rivales_en_mi_zona: List[np.array] = []
        self.soycandidato = False
        self.quemostrar = True

        self.fuicandidato: float = 0.0

        if self.id_equipo == 1:
            self.coordenadas_porteria_rival = [
                self.field.width, self.field.center_y]
        else:
            self.coordenadas_porteria_rival = [0, self.field.center_y]

    def poligono_en_posicion(self,coordinates):
        return Polygon([(coordinates[0]+self.wingspan,coordinates[1]+self.wingspan),
                                             (coordinates[0]+self.wingspan,coordinates[1]-self.wingspan),
                                             (coordinates[0]-self.wingspan,coordinates[1]-self.wingspan),
                                             (coordinates[0]-self.wingspan,coordinates[1]+self.wingspan)])
    def alternativadetiro(self):
        if(Math.distancia(self.coordinates.coordinates,self.coordenadas_porteria_rival) < 30):
            return [Alternativa(self,AlternativaType.SHOT, np.array([Math.distancia(self.coordinates.coordinates,ri.coordinates.coordinates) for ri in self.rivales]).min() ,Math.distancia(self.coordinates.coordinates,self.coordenadas_porteria_rival),probilidad_de_marcar_gol= 50)]

    def alternativasdemovimiento(self,posibilidades = 32):
        #print("Miro posibilidades de movimiento")
        posibilidades = 32
        grados_iteracion = 360.0/posibilidades
        vincial =  np.array([0.0,1.0])  * self.movement.distancia_maxima_de_movimiento_por_iteracion()
        alternativas = []
        for i in range(posibilidades):
            vrotado = Math.rotarvector(vincial,grados_iteracion * i)
            #print("Vrotado: ",vrotado)
            nointersecta = True
            poligono:Polygon = self.poligono_en_posicion(self.coordinates.coordinates + vrotado)
            if poligono.within(self.field.sites.field_site):
                for r in  self.rivales:
                    if poligono.intersects(r.action_area):
                        nointersecta = False
                        break
                for c in  self.companieros:
                    if poligono.intersects(c.action_area):
                        nointersecta = False
                        break
                if nointersecta:
                    alternativas.append(Alternativa(self,AlternativaType.MOVE, np.array([Math.distancia(self.coordinates.coordinates + vrotado,ri.coordinates.coordinates) for ri in self.rivales]).min() ,Math.distancia(self.coordinates.coordinates + vrotado,self.coordenadas_porteria_rival),movecoordinates=self.coordinates.coordinates + (vrotado*10000)))
        return alternativas


    def alternativas_de_paselargo(self,jugadoresvetados:List[int] = []):
        altenativas = []

        for id in range(len(self.companieros)):
            if self.companieros[id].id not in jugadoresvetados and Math.distancia(self.companieros[id].coordinates.coordinates,self.coordinates.coordinates) < self.distancia_maxima_pase_largo:                              
                altenativas.append(Alternativa(self.companieros[id],AlternativaType.LONG_PASS, np.array([Math.distancia(self.companieros[id].coordinates.coordinates,ri.coordinates.coordinates) for ri in self.rivales]).min() ,Math.distancia(self.companieros[id].coordinates.coordinates,self.companieros[id].coordenadas_porteria_rival)))
        return altenativas

    def estaenmipoligonodevoronoi(self,coordinates: np.array):
        distancias = [Math.distancia(coordinates,self.posicion_formacion.coordinates)]

        for companiero in self.companieros:
            distancias.append(Math.distancia(coordinates,companiero.posicion_formacion.coordinates))

        return np.array(distancias).argmin() == 0

    def estoyenmipoligonodevoronoi(self):
        distancias = [Math.distancia(
            self.coordinates.coordinates, self.posicion_formacion.coordinates)]

        for companiero in self.companieros:
            distancias.append(Math.distancia(
                self.coordinates.coordinates, companiero.posicion_formacion.coordinates))

        return np.array(distancias).argmin() == 0

    def posformacioneinicial(self, x, y):
        self.posicion_formacion = Coordinates(x, y)
        self.coordinates = Coordinates(x, y)
        return self.coordinates.coordinates.copy()

    def haylineadepase_inicial(self, companiero: 'Player'):

        for vertice_pelota in self.field.ball.action_area.exterior.coords:

            for vertice_companiero in companiero.action_area.exterior.coords:

                linea = LineString(
                    [Point(vertice_pelota), Point(vertice_companiero)])

                for rival in self.rivales:
                    if linea.intersects(rival.action_area):
                        return False

        return True

    def alternativas_de_pase_disponibles_iluminarcandidatos(self, jugadoresvetados: List[int] = []):
        altenativas = []

        for id in range(len(self.companieros)):
            if self.companieros[id].id not in jugadoresvetados and Math.distancia(self.companieros[id].coordinates.coordinates, self.coordinates.coordinates) < self.distancia_maxima_pase:
                disponible = self.haylineadepase_inicial(self.companieros[id])
                if disponible == True:
                    if self.quemostrar:
                        self.companieros[id].soycandidato = True
                    altenativas.append(Alternativa(self.companieros[id], AlternativaType.PASS, np.array([Math.distancia(self.companieros[id].coordinates.coordinates, ri.coordinates.coordinates) for ri in self.rivales]).min(
                    ), Math.distancia(self.companieros[id].coordinates.coordinates, self.companieros[id].coordenadas_porteria_rival)))

        return altenativas

    def alternativas_de_pase_disponibles(self, jugadoresvetados: List[int] = []):
        altenativas = []
        for id in range(len(self.companieros)):
            if self.companieros[id].id not in jugadoresvetados and Math.distancia(self.companieros[id].coordinates.coordinates, self.coordinates.coordinates) < self.distancia_maxima_pase:
                linea = LineString([Point(self.companieros[id].coordinates.coordinates), Point(
                    self.coordinates.coordinates)])
                disponible = True
                for rival in self.rivales:
                    if linea.intersects(rival.action_area):
                        disponible = False
                        break
                if disponible == True:
                    altenativas.append(Alternativa(self.companieros[id], AlternativaType.PASS, np.array([Math.distancia(self.companieros[id].coordinates.coordinates, ri.coordinates.coordinates) for ri in self.rivales]).min(
                    ), Math.distancia(self.companieros[id].coordinates.coordinates, self.companieros[id].coordenadas_porteria_rival)))

        return altenativas

    def lineas_de_pase_disponibles(self):
        candidatos = []

        for id in range(len(self.companieros)):
            if Math.distancia(self.companieros[id].coordinates.coordinates, self.coordinates.coordinates) < self.distancia_maxima_pase:
                linea = LineString([Point(self.companieros[id].coordinates.coordinates), Point(
                    self.coordinates.coordinates)])
                disponible = True
                for rival in self.rivales:
                    if linea.intersects(rival.action_area):
                        disponible = False
                        break
                if disponible == True:
                    candidatos.append(self.companieros[id])

        return candidatos

    def pasar_balon_random(self):
        #print("Comienzo a pasarlo")
        arbol: List[Alternativa] = arbol_alternativas(self,10)
        #representar_arbol_alternativas(arbol)
        self.field.evento_actual = None
        if(len(arbol) > 0):
            elegido = eligealternativa(arbol)
            if arbol[elegido].tipo == AlternativaType.PASS:
                #print("Paso el balon")
                direccion = arbol[elegido].player.coordinates.coordinates - self.coordinates.coordinates  
                self.info_equipo.balon_pasado_a = arbol[elegido].player.id
                self.info_equipo.balon_pasado_a_jugador = arbol[elegido].player
                self.tengoelbalon = False
                self.doing_something = self.field.ball.pass_ball(direccion,self.fuerza_pase_corto,self.id)
            else:
                if arbol[elegido].tipo == AlternativaType.MOVE:
                    #print("Me muevo con el balon")
                    self.movement.move_destination_coordinates = arbol[elegido].movecoordinates
                    self.tengoelbalon = True
                    self.movement.move()
                else: 
                     if arbol[elegido].tipo == AlternativaType.LONG_PASS:
                        #print("REALIZO PASE LARGO")
                        # Calcular dirección y distancia
                        coordenadas = self.field.manterencampo(arbol[elegido].player.coordinates.coordinates)
                        direccion = coordenadas - self.field.ball.coordinates.coordinates
                        distancia = Math.distancia(coordenadas, self.field.ball.coordinates.coordinates)
                        #distancia = ((3.14 * distancia/2) + (math.sqrt(math.pow(distancia,2)/2) * 2) / 2)#Teniendo en cuenta el eje y y el x
                        #distancia = 2 * math.pow(distancia,2)/math.sqrt(2)
                        #print("DISTANCIA", distancia)
                        # Configurar información del equipo y balón
                        self.info_equipo.balon_pasado_a = arbol[elegido].player.id
                        self.info_equipo.balon_pasado_a_jugador = arbol[elegido].player
                        self.tengoelbalon = False
                        self.field.evento_actual = Evento.PASE_LARGO
                        arbol[elegido].player.soycandidato = True
                        fuerza = self.field.ball.masa * math.sqrt(distancia * Math.gravedad)/ self.field.ball.tiempo_contacto
                        # Ejecutar el pase
                        self.doing_something = self.field.ball.pase_largo(
                            direccion, fuerza, self.id, distancia, coordenadas
                        )
        else:
            elegido = random.randint(4, len(self.companieros)-3)
            self.info_equipo.balon_pasado_a = self.companieros[elegido].id
            direccion = self.companieros[elegido].coordinates.coordinates - \
                self.coordinates.coordinates
            self.field.ball.pass_ball(
                direccion, self.fuerza_pase_corto, self.id)
            self.tengoelbalon = False

    def cubre(self):

        if len(self.jugadores_rivales_en_mi_zona) > 0:
            # print("Jugador ",self.id, " estoy cubriendo")
            # Miro cual de los rivales esta a menos distancia de la pelota, a ese cubro
            id = Math.menordistancia(
                self.jugadores_rivales_en_mi_zona, self.field.ball.coordinates.coordinates)

            vetorcubrir = Math.vector(
                self.jugadores_rivales_en_mi_zona[id], self.field.ball.coordinates.coordinates)

            norma = np.linalg.norm(vetorcubrir)

            if norma != 0:
                vectorcubrir = vetorcubrir/norma
                self.movement.move_destination_coordinates = self.jugadores_rivales_en_mi_zona[id] + vectorcubrir

                self.movement.move()

    def move_to_ball_sin_tocarla(self):
        vector = Math.vector(self.field.ball.coordinates.coordinates,self.coordinates.coordinates)
        norma = np.linalg.norm(vector)
        vector = vector/norma
        self.movement.move_destination_coordinates = self.field.ball.coordinates.coordinates + (vector * 20)
        self.movement.move()

    def move_to_ball(self):
        self.movement.move_destination_coordinates = self.field.ball.coordinates.coordinates
        self.movement.move()

    def move_to_player_pass(self):
        self.movement.move_destination_coordinates = self.info_equipo.balon_pasado_a_jugador.coordinates.coordinates
        self.movement.move()

    def move_to_player_pass_largo(self):
        self.movement.move_destination_coordinates = self.field.ball.long_pass_coordinates
        self.movement.move()

    def move_to_form_position(self):
        self.movement.move_destination_coordinates = self.posicion_formacion.coordinates
        self.movement.move()

    def controlbalon(self):
        # if(self.tengoelbalon):
        #     self.field.ball.coordinates.coordinates[0] = self.coordinates.coordinates[0]
        #     self.field.ball.coordinates.coordinates[1] = self.coordinates.coordinates[1]
        pass

    def move_random(self):
        self.doing_something = self.movement.move
        esta_Fuera = True
        while esta_Fuera:
            self.movement.move_destination_coordinates = [random.randint(
                0, self.field.width), random.randint(0, self.field.width)]
            # print("Coordenadas random: ", self.movement.move_destination_coordinates)
            player_area_new_position: Polygon = Polygon([(self.movement.move_destination_coordinates[0]+self.wingspan, self.movement.move_destination_coordinates[1]+self.wingspan),
                                                         (self.movement.move_destination_coordinates[0]+self.wingspan,
                                                          self.movement.move_destination_coordinates[1]-self.wingspan),
                                                         (self.movement.move_destination_coordinates[0]-self.wingspan,
                                                          self.movement.move_destination_coordinates[1]-self.wingspan),
                                                         (self.movement.move_destination_coordinates[0]-self.wingspan, self.movement.move_destination_coordinates[1]+self.wingspan)])

            if (player_area_new_position.within(self.field.sites.field_site)):
                esta_Fuera = False

    def refresh(self):
        self.action_area = Polygon([(self.coordinates.coordinates[0]+self.wingspan, self.coordinates.coordinates[1]+self.wingspan),
                                    (self.coordinates.coordinates[0]+self.wingspan,
                                     self.coordinates.coordinates[1]-self.wingspan),
                                    (self.coordinates.coordinates[0]-self.wingspan,
                                     self.coordinates.coordinates[1]-self.wingspan),
                                    (self.coordinates.coordinates[0]-self.wingspan, self.coordinates.coordinates[1]+self.wingspan)])

    def comportamiento_estandar(self):
        if self.doing_something == None:
            if not (self.tengoelbalon):
                # print("No tengo el balón")
                if self.info_equipo.id_mas_cerca_del_balon == self.id or self.info_equipo.balon_en_la_zona_de == self.id or (self.info_equipo.balon_pasado_a == self.id and self.field.equipo_con_balon == self.id_equipo):
                    self.doing_something = self.move_to_ball
                else:
                    if self.field.equipo_con_balon != self.id_equipo:
                        if len(self.jugadores_rivales_en_mi_zona) > 0:
                            self.doing_something = self.cubre
                        else:
                            self.doing_something = self.move_to_form_position
                    else:
                        if self.field.equipo_con_balon == self.id_equipo and self.field.ball.id_passed != -1 and Math.distancia(self.coordinates.coordinates, self.info_equipo.balon_pasado_a_jugador.coordinates.coordinates) < self.info_equipo.balon_pasado_a_jugador.distancia_maxima_pase:

                            if self.estoyenmipoligonodevoronoi():

                                if not (self.quemostrar):
                                    self.soycandidato = True
                                self.doing_something = self.move_to_player_pass
                            else:
                                self.doing_something = self.move_to_form_position
                        else:
                            self.doing_something = self.move_to_form_position
            else:
                # print("Tengo el balon")
                self.doing_something = self.pasar_balon_random
        else: 
            if not(self.tengoelbalon):
                if self.info_equipo.id_mas_cerca_del_balon == self.id or self.info_equipo.balon_en_la_zona_de == self.id or (self.info_equipo.balon_pasado_a == self.id and self.field.equipo_con_balon == self.id_equipo):
                        self.doing_something = self.move_to_ball
                else:
                    self.doing_something = None
                    self.decision()
            else:
                self.doing_something = self.pasar_balon_random

    def comportamiento_fuera(self):
        if self.doing_something == None:
            if self.field.equipo_con_balon != self.id_equipo:
                if len(self.jugadores_rivales_en_mi_zona) > 0:
                    self.doing_something = self.cubre
            else: 
                if self.field.equipo_con_balon == self.id_equipo and self.field.ball.id_passed == -1 and Math.distancia(self.coordinates.coordinates,self.info_equipo.balon_pasado_a_jugador.coordinates.coordinates) < self.info_equipo.balon_pasado_a_jugador.distancia_maxima_pase:
                    if self.estoyenmipoligonodevoronoi():
                        if not(self.quemostrar):
                            self.soycandidato = True
                        self.doing_something = self.move_to_ball_sin_tocarla
        else: 
            if self.field.equipo_con_balon == self.id_equipo:
                if (self.tengoelbalon):
                    #print("TENGO EL BALON")
                    self.doing_something = self.pasar_balon_random 
                else:
                    if not(self.estoyenmipoligonodevoronoi()) :
                        self.doing_something = self.move_to_form_position       
                    else:
                        self.doing_something = self.move_to_ball_sin_tocarla
            else: 
                self.doing_something = self.cubre

    def comportamiento_pase_largo(self):
        if self.field.equipo_con_balon == self.id_equipo:
            if self.info_equipo.balon_pasado_a == self.id:
                #print("Me muevo para el pase largo")
                self.soycandidato = True
                self.doing_something = self.move_to_player_pass_largo
            else: 
                if self.estoyenmipoligonodevoronoi():
                    self.doing_something = self.move_to_player_pass 
                else: 
                    self.doing_something = self.move_to_form_position
        else:
            if self.estaenmipoligonodevoronoi(self.field.ball.long_pass_coordinates):
                self.doing_something = self.move_to_player_pass
            else:
                if len(self.jugadores_rivales_en_mi_zona) > 0:
                    self.doing_something = self.cubre
                else: 
                    self.doing_something = self.move_to_form_position

    def decision(self):
        if self.field.evento_actual == None:
            self.comportamiento_estandar()
        else:
            if self.field.evento_actual == Evento.FUERA or self.field.evento_actual == Evento.CORNER:
                self.comportamiento_fuera()
            else: 
                if self.field.evento_actual == Evento.PASE_LARGO:
                    self.comportamiento_pase_largo()


    def refresh(self):
        self.action_area = Polygon([(self.coordinates.coordinates[0]+self.wingspan, self.coordinates.coordinates[1]+self.wingspan),
                                    (self.coordinates.coordinates[0]+self.wingspan,
                                     self.coordinates.coordinates[1]-self.wingspan),
                                    (self.coordinates.coordinates[0]-self.wingspan,
                                     self.coordinates.coordinates[1]-self.wingspan),
                                    (self.coordinates.coordinates[0]-self.wingspan, self.coordinates.coordinates[1]+self.wingspan)])

    def behavior(self):
        if self.doing_something != None:
            self.doing_something()

        self.refresh()

    def __str__(self):
        # - {str.lower(self.role.name)}
        return (f'{self.data['nickname']}: {self.coordinates} -> {self.movement}')


def altenativas_recursivo(alternativa: Alternativa, profundidad, jugadoresvetados: List[int] = []):
    if profundidad >= 0:
        alternativa.alternativas = alternativa.player.alternativas_de_pase_disponibles(jugadoresvetados)  
        if profundidad <= 4:
            jugadoresvetados.append(alternativa.player.id)
        for i in range(len(alternativa.alternativas)):
            altenativas_recursivo(
                alternativa.alternativas[i], profundidad - 1,)


def arbol_alternativas(player: Player,profundidad:int):
    altenativas =  player.alternativasdemovimiento() + player.alternativas_de_pase_disponibles_iluminarcandidatos() + player.alternativas_de_paselargo()
    for i in range(len(altenativas)): 
        altenativas_recursivo(altenativas[i],profundidad)
    return altenativas


def representar_arbol_alternativas(alternativas: List[Alternativa], profundidad=0):

    if (alternativas != None):
        for alternativa in alternativas:
            representar_arbol_alternativas(alternativa.alternativas,profundidad+1)
def eligealternativa(altenativas: List[Alternativa]):
    media,idsele = eligealtenativa_recursivo(altenativas)

    return idsele

def eligealtenativa_recursivo(alternativas: List[Alternativa],sumatorio:np.array = np.array([0.0,0.0,0.0]),profundidad:float = 0.0):
    if alternativas == None or len(alternativas) == 0:
        return (Math.media_geometrica_ponderada(sumatorio/profundidad,Probabilidades.pesos_decision_alternativas_equipo_perdiendo),0)
    else:
        resultados = []
        for id in range(len(alternativas)):
            media,idseleccionada = eligealtenativa_recursivo(alternativas[id].alternativas,sumatorio + alternativas[id].vectorizar(),profundidad + 1)
            resultados.append(media)

        posmaximo = np.array(resultados).argmax()

        return resultados[posmaximo], posmaximo


class TeamInformation():
    def __init__(self):
        self.id_mas_cerca_del_balon = -1
        self.balon_en_la_zona_de = -1
        self.balon_pasado_a = -1
        self.balon_pasado_a_jugador: Player = None

        pass


class Movement():
    def __init__(self, player: Player):
        self.move_destination_coordinates = np.array([0, 0])
        self.acceleration = 4
        self.current_direction = np.array([1, 0])
        self.destination_direction = np.array([0, 0])
        self.current_vel = 0
        #self.sprint_speed = 8.71 #m/s
        self.sprint_speed =  4.71# 8.71
        self.normal_speed = 4.74 #m/s
        self.current_deceleration = 0
        self.current_acceleration = self.acceleration
        self.destination_distance = 0
        self.maximum_acceleration_braking = -12
        self.braking_distance = 0
        self.player = player

    def __str__(self):
        return (f'velocidad actual: {self.current_vel} | aceleracion: {self.current_acceleration}')

    def distancia_maxima_de_movimiento_por_iteracion(self):
        current_acceleration = self.acceleration * (1 - (self.current_vel/self.sprint_speed))
        #tiemporestante = (-self.current_vel + math.sqrt(math.pow(self.current_vel, 2) + (2 * self.current_acceleration * self.destination_distance))) / self.current_acceleration

        v0 = self.current_vel

        current_vel = self.current_vel + (current_acceleration * self.player.time)
        current_acceleration = self.acceleration * (1 - (current_vel/self.sprint_speed))
        current_vel = current_vel + (current_acceleration * self.player.time)

        space = ((v0+current_vel)/2) * self.player.time

        return space

    def runwithball(self):
        self.current_acceleration = self.acceleration * (1 - (self.current_vel/self.sprint_speed))
        #tiemporestante = (-self.current_vel + math.sqrt(math.pow(self.current_vel, 2) + (2 * self.current_acceleration * self.destination_distance))) / self.current_acceleration

        v0:float = self.current_vel
        #print("Velocidad anterior = ", v0)
        self.current_vel = self.current_vel + (self.current_acceleration * self.player.time)
        #print("Velocidad = ", self.current_vel)
        if(self.current_vel < 0):
            self.current_acceleration = self.acceleration * (1 - (self.current_vel/self.sprint_speed))
            self.current_vel = self.current_vel + (self.current_acceleration * self.player.time)

        space = ((v0+self.current_vel)/2)* self.player.time

        #print("Me muevo: ",space," con el balon")

        if self.destination_distance > space:
            #print("Coordenadas Jugador ANTES= ", self.player.coordinates.coordinates)
            self.player.coordinates.coordinates = self.player.coordinates.coordinates + (self.current_direction*space) 
            #print("Coordenadas Jugador = ", self.player.coordinates.coordinates)
            self.player.field.ball.run_with_ball(self.player.coordinates.coordinates)
            self.player.field.ball.stop()
        else:
            #print("ME METO")
            self.player.coordinates.coordinates = self.player.coordinates.coordinates + (self.move_destination_coordinates - self.player.coordinates.coordinates)
            #print("Coordenadas Jugador = ", self.player.coordinates.coordinates)
            self.player.field.ball.run_with_ball(self.player.coordinates.coordinates)
            self.current_vel = 0
            self.player.field.ball.stop()

    def run(self):

        self.current_acceleration = self.acceleration * \
            (1 - (self.current_vel/self.sprint_speed))

        # tiemporestante = (-self.current_vel + math.sqrt(math.pow(self.current_vel, 2) + (2 * self.current_acceleration * self.destination_distance))) / self.current_acceleration

        distancia_maxima_frenado = (
            math.pow(self.current_vel, 2)/(2*(-self.maximum_acceleration_braking)))

        aceleracion_necesaria = - \
            math.pow(self.current_vel, 2)/(2*self.destination_distance)

       # print("Tiempo Restante Para LLegar: ",tiemporestante, " Distancia Máxima de Frenado:  ", distancia_maxima_frenado, " Aceleracion Necesaria: ", aceleracion_necesaria)

        if (distancia_maxima_frenado > self.destination_distance and (self.destination_distance > 0.1)):
            if (aceleracion_necesaria < self.current_acceleration):
                if aceleracion_necesaria < self.maximum_acceleration_braking:
                    self.current_acceleration = self.maximum_acceleration_braking
                else:
                    self.current_acceleration = aceleracion_necesaria

        v0 = self.current_vel

        self.current_vel = self.current_vel + (self.current_acceleration * self.player.time)
        if(self.current_vel < 0):
            self.current_acceleration = self.acceleration * (1 - (self.current_vel/self.sprint_speed))
            self.current_vel = self.current_vel + (self.current_acceleration * self.player.time)

        space = ((v0+self.current_vel)/2) * self.player.time

        if self.destination_distance > space:
            self.player.coordinates.coordinates = self.player.coordinates.coordinates + (self.current_direction*space) 
            #self.player.field.ball.coordinates.coordinates = self.player.coordinates.coordinates.copy()
        else:
            self.player.coordinates.coordinates = self.player.coordinates.coordinates + (self.move_destination_coordinates - self.player.coordinates.coordinates)
            #self.player.field.ball.coordinates.coordinates = self.player.coordinates.coordinates.copy()
            #self.current_vel = 0

    def stop(self):
        v0 = self.current_vel

        self.current_vel = self.current_vel + \
            (self.maximum_acceleration_braking * self.player.time)

        if (self.current_vel < 0):
            self.player.doing_something = None

        space = ((v0+self.current_vel)/2) * self.player.time

        if self.destination_distance > space:
            self.player.coordinates.coordinates = self.player.coordinates.coordinates + \
                (self.current_direction*space)

    def move(self):

        # self.current_direction = [self.move_destination_coordinates[0] - self.player.coordinates.coordinates[0],self.move_destination_coordinates[1] - self.player.coordinates.coordinates[1]]
        self.current_direction = self.move_destination_coordinates - \
            self.player.coordinates.coordinates
        self.destination_distance = np.linalg.norm(self.current_direction)
        #print("Self MC: ",self.move_destination_coordinates," Player Coor: ", self.player.coordinates.coordinates," current_direction: ", self.current_direction)
        #print("Current Direction: ",self.current_direction, " -> norma = ", self.destination_distance)
        #print(self.destination_distance)

        if self.destination_distance == 0:
                # if self.player.tengoelbalon: 
                #     #print("Me meto NOOOOOOOOOO")
                self.player.doing_something = None
                self.current_acceleration = self.acceleration
                self.current_vel = 0

        else:

            self.current_direction = self.current_direction/self.destination_distance
            #print("Direccion Normalizada: ", self.current_direction)
            if self.player.field.equipo_con_balon == self.player.id_equipo and self.player.tengoelbalon: 
                #print("Me voy a mover con balon esta distancia: ", self.destination_distance)

                self.runwithball()
            else:
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
