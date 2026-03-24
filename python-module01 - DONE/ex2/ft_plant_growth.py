#!/usr/bin/env python3
"""Exercise 2: Plant Growth Simulator - Methods on classes."""


class Plant:
    """A plant that can grow and age over time."""

    def __init__(self, name: str, height: int, age: int) -> None:
        """Initialize a plant with name, height, and age."""
        self.name: str = name
        self.height: int = height
        self.age: int = age

    def grow(self, amount: int = 1) -> None:
        """Increase the plant's height by a given amount."""
        self.height += amount

    def age_plant(self, days: int = 1) -> None:
        """Increase the plant's age by a given number of days."""
        self.age += days

    def get_info(self) -> str:
        """Return a string with the current plant status."""
        return f"{self.name}: {self.height}cm, {self.age} days old"


def main() -> None:
    """Simulate plant growth over a week."""
    rose: Plant = Plant("Rose", 25, 30)
    initial_height: int = rose.height

    print("=== Day 1 ===")
    print(rose.get_info())

    for _ in range(6):
        rose.grow(1)
        rose.age_plant(1)

    print("=== Day 7 ===")
    print(rose.get_info())
    print(f"Growth this week: +{rose.height - initial_height}cm")


if __name__ == "__main__":
    main()
