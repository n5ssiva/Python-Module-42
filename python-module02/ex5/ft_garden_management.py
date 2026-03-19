# -*- coding: utf-8 -*-
"""Final module integrating all error handling techniques in a Garden Manager."""


# --- Étape 1 : Récupération des exceptions de l'Ex 2 ---
class GardenError(Exception):
    """Base class for all garden errors."""
    pass


class PlantError(GardenError):
    """Errors related specifically to plants."""
    pass


# --- Étape 2 : La Classe GardenManager ---
class GardenManager:
    """Class to manage garden operations with robust error handling."""

    def __init__(self):
        self.plants = []

    def add_plant(self, name: str):
        """Add a plant or raise PlantError if name is empty."""
        if not name:
            raise PlantError("Plant name cannot be empty!")
        self.plants.append(name)
        print(f"Added {name} successfully")

    def water_plants(self):
        """Simulate watering with mandatory cleanup (Ex 3)."""
        try:
            print("Opening watering system")
            for plant in self.plants:
                # Format spécifique du screenshot: "Watering name - success"
                print(f"Watering {plant} - success")
        finally:
            print("Closing watering system (cleanup)")

    def check_plant_health(self, name: str, water: int, sun: int):
        """Validate health and raise ValueError if out of bounds (Ex 4)."""
        if water > 10:
            raise ValueError(f"Water level {water} is too high (max 10)")
        print(f"{name}: healthy (water: {water}, sun: {sun})")


# --- Étape 3 : La fonction de test (Le scénario du screenshot) ---
def test_garden_management():
    """Demonstrate all error handling techniques integrated."""
    manager = GardenManager()
    print("=== Garden Management System ===\n")

    # 1. Ajout de plantes
    print("Adding plants to garden...")
    try:
        manager.add_plant("tomato")
        manager.add_plant("lettuce")
        manager.add_plant("")  # Provoque une erreur
    except PlantError as e:
        print(f"Error adding plant: {e}")

    # 2. Arrosage
    print("\nWatering plants...")
    manager.water_plants()

    # 3. Vérification de santé
    print("\nChecking plant health...")
    try:
        manager.check_plant_health("tomato", 5, 8)
        manager.check_plant_health("lettuce", 15, 5)  # Provoque une erreur
    except ValueError as e:
        print(f"Error checking lettuce: {e}")

    # 4. Récupération d'erreur (Error Recovery)
    print("\nTesting error recovery...")
    try:
        # Simulation d'une erreur générale de jardin
        raise GardenError("Not enough water in tank")
    except GardenError as e:
        print(f"Caught GardenError: {e}")
        print("System recovered and continuing...")

    print("\nGarden management system test complete!")


if __name__ == "__main__":
    test_garden_management()