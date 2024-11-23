from classes.utils import Coordinates
from classes.player import Player

from enum import Enum


class TeamFormation(Enum):
    """Enum used to represent the team's formation."""
    pass


class Team():
    """Class representing a team inside a match."""

    def __init__(self, players, collection, field):
        self.players = []
        self.substitutes = []
        self.substitutions_made: int = 0
        self.formation: TeamFormation = None

        starters = players['starting']
        subs = players['substitutes']
        for p in starters:
            self.players.append(
                Player(
                    collection.find_one({"_id": p['id']}),
                    p['role'],
                    Coordinates(0, 0),
                    field,
                    1  # Time
                )
            )
        for p in subs:
            self.substitutes.append(
                Player(
                    collection.find_one({"_id": p['id']}),
                    None,
                    Coordinates(0, 0),
                    field,
                    1  # Time
                )
            )

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
