from enum import Enum

from player import Player


class TeamFormation(Enum):
    """Enum used to represent the team's formation."""
    pass


class Team():
    """Class representing a team inside a match."""

    def __init__(self, data):
        # players and their respective position need to be extracted from
        # data
        self.players: Player[11] = None
        self.bench_players: Player[12] = None
        self.substitutions_made: int = 0
        self.formation: TeamFormation = None

    def sub_player(player_out, player_in):
        pass
