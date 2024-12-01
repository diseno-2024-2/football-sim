from classes.field import Field
from classes.player import Player
from classes.utils import Coordinates
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from time import sleep
from classes.screen import Screen
from classes.ball import Ball
from classes.interaction import Interaction
from classes.team import Team
import random


def main():
    time = 0.01
    field = Field()
    n_jugadores_por_equipo = 11
    jugadoresequipo1 = []
    jugadoresequipo2 = []
    color1 = (255, 0, 0)
    color2 = (0, 0, 255)

    field.ball = ball = Ball(time)
    for i in range(0,n_jugadores_por_equipo):
        jugadoresequipo1.append(Player("Jugador"+str(i),i,Coordinates(random.randint(0,field.width),random.randint(0,field.height)),field,color1,time))
    for i in range(0,n_jugadores_por_equipo):
        jugadoresequipo2.append(Player("Jugador"+str(i),i,Coordinates(random.randint(0,field.width),random.randint(0,field.height)),field,color2,time))    
    field.ball.campo = field
    equipo1 = Team(0,jugadoresequipo1,jugadoresequipo2,field,1)
    equipo2 = Team(1,jugadoresequipo2,jugadoresequipo1,field,2)


    screen = Screen(jugadoresequipo1+jugadoresequipo2,ball,field,1080,720,time)
    interaction = Interaction(jugadoresequipo1+jugadoresequipo2,ball,field,equipo1,equipo2)

    segundos = 0.1
    minutos = -1
    while minutos < 90:
        screen.visualice()
        equipo1.decision()
        equipo2.decision()
        ball.behaviour()
        equipo1.behaviour()
        equipo2.behaviour()
        interaction.resolverconflictos()
        interaction.time += time
        equipo1.actualizarposiciones()
        equipo2.actualizarposiciones()
        screen.time = interaction.time
        screen.minutos = minutos
        screen.segundos = segundos.__round__(2)
        
        segundos += time
        if int(segundos) % 61 == 0:
            minutos += 1
            segundos = 1.0


if __name__ == '__main__':
    main()
