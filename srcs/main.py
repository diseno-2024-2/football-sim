# from classes.field import Field
# from classes.player import Player
# from classes.utils import Coordinates
# from time import sleep
# from classes.screen import Screen
from classes.team import Team

import pymongo
import json


def main():
    client = pymongo.MongoClient("mongodb://root:example@localhost:27017/")
    db = client["simulation"]
    collection = db["player"]
    team1, team2 = get_teams(collection)
    print(f'TEAM 1:\n{team1}\n')
    print(f'TEAM 2:\n{team2}')

    # time = 1
    # field = Field()
    # player = Player("Jugador", 1, Coordinates(0, 0), field, time)
    # screen = Screen([player], field, 960, 480)

    # while True:
    #     screen.visualice()
    #     player.behavior()
    #     sleep(0.1)
    #     print(player)


def get_teams(collection):
    team1 = None
    team2 = None
    with open('teams.json', 'r') as file:
        data = json.load(file)
        t1 = data['team1']
        team1 = Team(t1, collection)
        t2 = data['team2']
        team2 = Team(t2, collection)
    return team1, team2


if __name__ == '__main__':
    main()
