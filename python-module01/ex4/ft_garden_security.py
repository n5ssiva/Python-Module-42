#!/usr/bin/env python3
"""Exercise 4: Garden Security System - Encapsulation and validation."""


class SecurePlant:
    """A plant with protected data and validation."""

    def __init__(self, name: str) -> None:
        """Initialize a secure plant with a name."""
        self._name: str = name
        self._height: int = 0
        self._age: int = 0

    def get_name(self) -> str:
        """Return the plant's name."""
        return self._name

    def get_height(self) -> int:
        """Return the plant's height."""
        return self._height

    def get_age(self) -> int:
        """Return the plant's age."""
        return self._age

    def set_height(self, height: int) -> bool:
        """Set height with validation. Returns True if successful."""
        if height < 0:
            print("Security: Negative height rejected")
            return False
        self._height = height
        return True

    def set_age(self, age: int) -> bool:
        """Set age with validation. Returns True if successful."""
        if age < 0:
            print("Security: Negative age rejected")
            return False
        self._age = age
        return True


def main() -> None:
    """Demonstrate the garden security system."""
    print("=== Garden Security System ===")

    plant: SecurePlant = SecurePlant("Rose")
    print(f"Plant created: {plant.get_name()}")

    # Valid operations
    if plant.set_height(25):
        print(f"Height updated: {plant.get_height()}cm [OK]")

    if plant.set_age(30):
        print(f"Age updated: {plant.get_age()} days [OK]")

    # Invalid operation
    print("Invalid operation attempted: height -5cm [REJECTED]")
    plant.set_height(-5)

    # Show current state
    print(f"Current plant: {plant.get_name()} "
          f"({plant.get_height()}cm, {plant.get_age()} days)")


if __name__ == "__main__":
    main()