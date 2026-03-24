"""Custom exception classes for garden-related errors."""


class GardenError(Exception):
    """Base exception for garden problems."""
    pass


class PlantError(GardenError):
    """Exception for plant-related issues."""
    pass


class WaterError(GardenError):
    """Exception for water/irrigation issues."""
    pass


def test_custom_errors() -> None:
    """Demonstrate custom garden exceptions."""
    print("=== Custom Garden Errors Demo ===")
    print()
    print("Testing PlantError...")
    try:
        raise PlantError("The tomato plant is wilting!")
    except PlantError as e:
        print(f"Caught PlantError: {e}")
    print()
    print("Testing WaterError...")
    try:
        raise WaterError("Not enough water in the tank!")
    except WaterError as e:
        print(f"Caught WaterError: {e}")
    print()
    print("Testing catching all garden errors...")
    errors_to_test = [
        PlantError("The tomato plant is wilting!"),
        WaterError("Not enough water in the tank!")
    ]
    for error in errors_to_test:
        try:
            raise error
        except GardenError as e:
            print(f"Caught a garden error: {e}")
    print()
    print("All custom error types work correctly!")


if __name__ == "__main__":
    test_custom_errors()
