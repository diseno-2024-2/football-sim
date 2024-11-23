from enum import Enum
# from player import Player


class TeamFormation(Enum):
    """Enum used to represent the team's formation."""
    pass


class Team():
    """Class representing a team inside a match."""

    def __init__(self, players, collection):
        self.players = []
        self.substitutes = []
        self.substitutions_made: int = 0
        self.formation: TeamFormation = None

        starters = players['starting']
        subs = players['substitutes']
        for p in starters:
            self.players.append(
                # Wrap arround player constructor later `Player(*)`
                collection.find_one({"_id": p['id']})
            )
        for p in subs:
            self.substitutes.append(
                # Wrap arround player constructor later `Player(*)`
                collection.find_one({"_id": p['id']})
            )

    def __str__(self):
        return (f'Starting: {self.players}\n\nSubs: {self.substitutes}')

    def sub_player(player_out, player_in):
        pass
