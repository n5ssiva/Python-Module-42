"""Module for validating plant health parameters by raising custom ValueErrors."""


def check_plant_health(plant_name: str, water: int, sunlight: int) -> str:
    """
    Validate plant parameters and raise errors if conditions are not met.

    Args:
        plant_name (str): Name of the plant.
        water (int): Water level (1-10).
        sunlight (int): Sunlight hours (2-12).

    Returns:
        str: A success message if all checks pass.
    """
    if not plant_name:
        raise ValueError("Plant name cannot be empty!")
    
    if water > 10:
        raise ValueError(f"Water level {water} is too high (max 10)")
    if water < 1:
        raise ValueError(f"Water level {water} is too low (min 1)")
        
    if sunlight < 2:
        raise ValueError(f"Sunlight hours {sunlight} is too low (min 2)")
    if sunlight > 12:
        raise ValueError(f"Sunlight hours {sunlight} is too high (max 12)")

    return f"Plant '{plant_name}' is healthy!"


def test_plant_checks() -> None:
    """Run test cases to demonstrate error raising and handling."""
    print("=== Garden Plant Health Checker ===\n")

    # 1. Good values
    print("Testing good values...")
    try:
        result = check_plant_health("tomato", 5, 8)
        print(result)
    except ValueError as e:
        print(f"Error: {e}")

    # 2. Empty name
    print("\nTesting empty plant name...")
    try:
        check_plant_health("", 5, 5)
    except ValueError as e:
        print(f"Error: {e}")

    # 3. Bad water level
    print("\nTesting bad water level...")
    try:
        check_plant_health("tomato", 15, 5)
    except ValueError as e:
        print(f"Error: {e}")

    # 4. Bad sunlight hours
    print("\nTesting bad sunlight hours...")
    try:
        check_plant_health("tomato", 5, 0)
    except ValueError as e:
        print(f"Error: {e}")

    print("\nAll error raising tests completed!")


if __name__ == "__main__":
    test_plant_checks()