#!/usr/bin/env python3
"""Exercise 3: Plant Factory - Constructors and initialization."""


class Plant:
    """A plant with proper initialization via constructor."""

    def __init__(self, name: str, height: int, age: int) -> None:
        """Initialize a plant with all its attributes."""
        self.name: str = name
        self.height: int = height
        self.age: int = age

    def display(self) -> str:
        """Return formatted string for display."""
        return f"Created: {self.name} ({self.height}cm, {self.age} days)"


def main() -> None:
    """Create multiple plants using the factory pattern."""
    plants: list[Plant] = [
        Plant("Rose", 25, 30),
        Plant("Oak", 200, 365),
        Plant("Cactus", 5, 90),
        Plant("Sunflower", 80, 45),
        Plant("Fern", 15, 120)
    ]

    print("=== Plant Factory Output ===")
    for plant in plants:
        print(plant.display())
    print(f"Total plants created: {len(plants)}")


if __name__ == "__main__":
    main()
