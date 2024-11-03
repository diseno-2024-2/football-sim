from abc import ABC, abstractmethod
from enum import Enum


class PlayerRole(Enum):
    """Enum used to represent the player's role."""
    GOALKEEPER = 1
    DEFENDER = 2
    MIDFIELDER = 3
    FORWARD = 4


class PlayerAttributes():
    """Class containing all relevant player stats."""

    def __init__(self, data):
        # Should read data from the database with player stats and asign it to
        # the corresponding stats. (Define which stats will be used and the
        # data format before implementing)
        pass


class Player(ABC):
    """Abstract class representing a generic player."""

    def __init__(self, name: str, number: int, attributes):
        self.name: str = name
        self.number: int = number
        self.attributes: PlayerAttributes = PlayerAttributes(attributes)
        self.role: PlayerRole = None

    @abstractmethod
    def make_move(self):
        """Abstract method to decide the player's action. """
        pass

    def __str__(self):
        return (f'{self.name} ({self.number}) - {str.lower(self.role.name)}')


class Goalkeeper(Player):
    """Concrete class that defines the goalkeeper's behavior"""

    def __init__(self, name: str, number: int, attributes):
        super().__init__(name, attributes)
        self.position: PlayerRole = PlayerRole.GOALKEEPER

    def make_move(self):
        pass


class Defender(Player):
    """Concrete class that defines the defender's behavior"""

    def __init__(self, name: str, number: int, attributes):
        super().__init__(name, attributes)
        self.position: PlayerRole = PlayerRole.DEFENDER

    def make_move(self):
        pass


class Midfielder(Player):
    """Concrete class that defines the midfielder's behavior"""

    def __init__(self, name: str, number: int, attributes):
        super().__init__(name, attributes)
        self.position: PlayerRole = PlayerRole.MIDFIELDER

    def make_move(self):
        pass


class Forward(Player):
    """Concrete class that defines the forward's behavior"""

    def __init__(self, name: str, number: int, attributes):
        super().__init__(name, attributes)
        self.position: PlayerRole = PlayerRole.FORWARD

    def make_move(self):
        pass
