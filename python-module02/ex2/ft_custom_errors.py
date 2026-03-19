"""Module demonstrating custom exception hierarchies in a garden context."""


class GardenError(Exception):
    """Base class for all garden-related exceptions."""
    pass


class PlantError(GardenError):
    """Exception raised for issues specifically related to plants."""
    pass


class WaterError(GardenError):
    """Exception raised for issues related to irrifation or water levels."""
    pass


def test_custom_errors() -> None:
    """Demonstrate how to raise and catch custom garden exceptions."""
    print("=== Custom Garden Errors Demo ===\n")

    print("Testing PlantError...")
    try:
        raise PlantError("The tomato plant is wilting!")
    except PlantError as e:
        print(f"Caught PlantError: {e}\n")
    print("Testing WaterError...")
    try:
        raise WaterError("Not enough water in the tank!")
    except WaterError as e:
        print(f"Caught WaterError: {e}\n")

    print("Testing catching all garden errors...")
    errors_to_test = [
        PlantError("The tomato plant is wilting!"),
        WaterError("Not enough water in the tank!")
    ]
    for error in errors_to_test:
        try:
            raise error
        except GardenError as e:
            print(f"Caught a garden error : {e}")
    print("\nAll custom error types work correctly!")


if __name__ == "__main__":
    test_custom_errors()
