from classes.field import Field
from classes.player import Player
from classes.ball import Ball
from time import sleep
from classes.screen import Screen


def main():
    time = 1
    field = Field()
    player = Player("Jugador", 1, field=field, time=time)
    ball = Ball(field)
    screen = Screen([player], ball, field, 960, 480)

    while True:
        screen.visualize()
        ball.move()
        player.behavior()
        sleep(0.1)
        print(player)


if __name__ == '__main__':
    main()
