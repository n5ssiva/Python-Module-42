"""Garden management system integrating all error handling techniques."""


class GardenError(Exception):
    """Base exception for garden problems."""
    pass


class PlantError(GardenError):
    """Exception for plant-related issues."""
    pass


class GardenManager:
    """Manage garden operations with robust error handling."""

    def __init__(self) -> None:
        self.plants: list[str] = []

    def add_plant(self, name: str) -> None:
        """Add a plant or raise PlantError if name is empty."""
        if not name:
            raise PlantError("Plant name cannot be empty!")
        self.plants.append(name)
        print(f"Added {name} successfully")

    def water_plants(self) -> None:
        """Water all plants with cleanup in finally block."""
        try:
            print("Opening watering system")
            for plant in self.plants:
                print(f"Watering {plant} - success")
        finally:
            print("Closing watering system (cleanup)")

    def check_plant_health(self, name: str, water: int, sun: int) -> None:
        """Validate plant health and raise ValueError if invalid."""
        if water > 10:
            raise ValueError(f"Water level {water} is too high (max 10)")
        print(f"{name}: healthy (water: {water}, sun: {sun})")


def test_garden_management() -> None:
    """Demonstrate all error handling techniques."""
    manager = GardenManager()
    print("=== Garden Management System ===")
    print()
    print("Adding plants to garden...")
    try:
        manager.add_plant("tomato")
        manager.add_plant("lettuce")
        manager.add_plant("")
    except PlantError as e:
        print(f"Error adding plant: {e}")
    print()
    print("Watering plants...")
    manager.water_plants()
    print()
    print("Checking plant health...")
    try:
        manager.check_plant_health("tomato", 5, 8)
        manager.check_plant_health("lettuce", 15, 5)
    except ValueError as e:
        print(f"Error checking lettuce: {e}")
    print()
    print("Testing error recovery...")
    try:
        raise GardenError("Not enough water in tank")
    except GardenError as e:
        print(f"Caught GardenError: {e}")
        print("System recovered and continuing...")
    print()
    print("Garden management system test complete!")


if __name__ == "__main__":
    test_garden_management()
