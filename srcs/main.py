# from classes.field import Field
# from classes.player import Player
# from classes.utils import Coordinates
# from time import sleep
# from classes.screen import Screen

import pymongo


def main():
    client = pymongo.MongoClient("mongodb://root:example@localhost:27017/")
    db = client["simulation"]
    collection = db["player"]
    print(collection.count_documents({}))
    # time = 1
    # field = Field()
    # player = Player("Jugador", 1, Coordinates(0, 0), field, time)
    # screen = Screen([player], field, 960, 480)

    # while True:
    #     screen.visualice()
    #     player.behavior()
    #     sleep(0.1)
    #     print(player)


if __name__ == '__main__':
    main()
