import json
import pymongo

from classes.interaction import Interaction
from classes.ball import Ball
from classes.screen import Screen
from classes.team import Team
from classes.field import Field


def main():
    client = pymongo.MongoClient("mongodb://root:example@localhost:27017/")
    db = client["simulation"]
    collection = db["player"]

    time = 0.01
    field = Field()
    field.ball = ball = Ball(time)
    field.ball.campo = field

    equipo1, equipo2 = get_teams(collection, field)
    equipo1.set_player_info(equipo2)
    equipo2.set_player_info(equipo1)
    print(f'TEAM 1:\n{equipo1}\n')
    print(f'TEAM 2:\n{equipo2}')

    screen = Screen(equipo1.players + equipo2.players,
                    ball, field, 1080, 720, time)
    interaction = Interaction(
        equipo1.players + equipo2.players, ball, field, equipo1, equipo2)

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


def get_teams(collection, field):
    team1 = None
    team2 = None
    color1 = (255, 0, 0)
    color2 = (0, 0, 255)
    with open('teams.json', 'r') as file:
        data = json.load(file)
        t1 = data['team1']
        team1 = Team(0, t1, collection, field, color1)
        t2 = data['team2']
        team2 = Team(1, t2, collection, field, color2)
    return team1, team2


if __name__ == '__main__':
    main()
