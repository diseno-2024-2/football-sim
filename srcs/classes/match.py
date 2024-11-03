from typing import List

from team import Team
from ball import Ball


class match():
    """ Class responsible for the simulation of the football match"""

    def __init__(self, teams: List[Team]):
        if len(teams) != 2:
            raise ValueError("A match must have exactly two teams")
        self.teams = teams
        self.ball = Ball()

    def start():
        pass
