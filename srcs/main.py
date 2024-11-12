from classes.field import Field
from classes.player import Player
from classes.utils import Coordinates
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from time import sleep 
from classes.screen import Screen

def main():
    time = 1
    field = Field()
    player = Player("Jugador",1,Coordinates(0,0),field,time)
    screen = Screen([player],field,960,480)

    while True:
        screen.visualice()
        player.behavior()
        sleep(0.1)
        print(player)
        
        pass
   
        
   


if __name__ == '__main__':
    main()