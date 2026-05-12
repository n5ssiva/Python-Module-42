from abc import ABC, abstractmethod


class Creature(ABC):

    def __init__(self, name: str, ctype: str) -> None:
        self.name = name
        self.ctype = ctype

    def describe(self) -> str:
        return f"{self.name} is a {self.ctype} type Creature"

    @abstractmethod
    def attack(self) -> str:
        pass
