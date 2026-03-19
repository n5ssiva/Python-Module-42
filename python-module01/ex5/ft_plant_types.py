#!/usr/bin/env python3
"""Exercise 5: Specialized Plant Types - Inheritance with super()."""


class Plant:
    """Base class for all plants with common features."""

    def __init__(self, name: str, height: int, age: int) -> None:
        """Initialize a plant with basic attributes."""
        self.name: str = name
        self.height: int = height
        self.age: int = age

    def get_info(self) -> str:
        """Return basic plant info."""
        return f"{self.name}: {self.height}cm, {self.age} days"


class Flower(Plant):
    """A flowering plant with color attribute."""

    def __init__(self, name: str, height: int, age: int, color: str) -> None:
        """Initialize a flower with color."""
        super().__init__(name, height, age)
        self.color: str = color

    def bloom(self) -> str:
        """Return a blooming message."""
        return f"{self.name} is blooming beautifully!"

    def get_info(self) -> str:
        """Return flower info with color."""
        return f"{self.name} (Flower): {self.height}cm, {self.age} days, " \
               f"{self.color} color"


class Tree(Plant):
    """A tree with trunk diameter."""

    def __init__(self, name: str, height: int, age: int,
                 trunk_diameter: int) -> None:
        """Initialize a tree with trunk diameter."""
        super().__init__(name, height, age)
        self.trunk_diameter: int = trunk_diameter

    def produce_shade(self) -> str:
        """Calculate and return shade area message."""
        shade_area: int = self.trunk_diameter + (self.height * 56) // 1000
        return f"{self.name} provides {shade_area} square meters of shade"

    def get_info(self) -> str:
        """Return tree info with diameter."""
        return f"{self.name} (Tree): {self.height}cm, {self.age} days, " \
               f"{self.trunk_diameter}cm diameter"


class Vegetable(Plant):
    """A vegetable with harvest season and nutritional value."""

    def __init__(self, name: str, height: int, age: int,
                 harvest_season: str, nutritional_value: str) -> None:
        """Initialize a vegetable with harvest info."""
        super().__init__(name, height, age)
        self.harvest_season: str = harvest_season
        self.nutritional_value: str = nutritional_value

    def get_nutrition(self) -> str:
        """Return nutritional info."""
        return f"{self.name} is rich in {self.nutritional_value}"

    def get_info(self) -> str:
        """Return vegetable info with harvest season."""
        return f"{self.name} (Vegetable): {self.height}cm, {self.age} days, " \
               f"{self.harvest_season} harvest"


def main() -> None:
    """Demonstrate different plant types."""
    print("=== Garden Plant Types ===")

    # Flowers
    rose: Flower = Flower("Rose", 25, 30, "red")
    print(rose.get_info())
    print(rose.bloom())

    # Trees
    oak: Tree = Tree("Oak", 500, 1825, 50)
    print(oak.get_info())
    print(oak.produce_shade())

    # Vegetables
    tomato: Vegetable = Vegetable("Tomato", 80, 90, "summer", "vitamin C")
    print(tomato.get_info())
    print(tomato.get_nutrition())


if __name__ == "__main__":
    main()
