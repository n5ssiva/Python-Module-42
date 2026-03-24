"""Agricultural data validation pipeline for temperature readings."""


def check_temperature(temp_str: str) -> int | None:
    """Validate temperature for plants (0-40°C)."""
    try:
        temperature = int(temp_str)
        if temperature < 0:
            print(f"Error: {temperature}°C is too cold for plants (min 0°C)")
            return None
        if temperature > 40:
            print(f"Error: {temperature}°C is too hot for plants (max 40°C)")
            return None
        print(f"Temperature {temperature}°C is perfect for plants!")
        return temperature
    except ValueError:
        print(f"Error: '{temp_str}' is not a valid number")
        return None


def test_temperature_input() -> None:
    """Test check_temperature with various inputs."""
    print("=== Garden Temperature Checker ===")
    print("\nTesting temperature: 25")
    check_temperature("25")
    print("\nTesting temperature: abc")
    check_temperature("abc")
    print("\nTesting temperature: 100")
    check_temperature("100")
    print("\nTesting temperature: -50")
    check_temperature("-50")
    print("\nAll tests completed - program didn't crash!")


if __name__ == "__main__":
    test_temperature_input()
