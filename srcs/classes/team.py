from enum import Enum
from typing import List

from player import Player


class TeamFormation(Enum):
    """Enum used to represent the team's formation."""
    pass


class Team():
    """Class representing a team inside a match."""

    def __init__(self, playerList: List[Player]):
        # players and their respective position need to be extracted from
        # data
        
        
        self.players: List[Player] = playerList# Should contain 11 players
        self.bench_players: List[Player] = None  # Should contain 12 players
        self.substitutions_made: int = 0
        self.formation: TeamFormation = None

    def sub_player(player_out, player_in):
        pass
