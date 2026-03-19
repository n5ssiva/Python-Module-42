#!/usr/bin/env python3
"""Exercise 1: Garden Data Organizer - Introduction to classes."""


class Plant:
    """A blueprint for any plant with its basic attributes."""

    def __init__(self, name: str, height: int, age: int) -> None:
        """Initialize a plant with name, height, and age."""
        self.name: str = name
        self.height: int = height
        self.age: int = age


def main() -> None:
    """Create and display multiple plants."""
    plants: list[Plant] = [
        Plant("Rose", 25, 30),
        Plant("Sunflower", 80, 45),
        Plant("Cactus", 15, 120)
    ]

    print("=== Garden Plant Registry ===")
    for plant in plants:
        print(f"{plant.name}: {plant.height}cm, {plant.age} days old")


if __name__ == "__main__":
    main()
