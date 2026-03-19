"""Module demonstrating the mandatory execution of the finally block."""


def water_plants(plant_list: list) -> None:
    """
    Simulate watering plants and ensure the system is closed properly.

    Args:
        plant_list (list): A list of plant names to water.
    """
    try:
        print("Opening watering system")
        for plant in plant_list:
            if plant is None:
                raise ValueError("Cannot water None - invalid plant!")
            # Note: lowercase in screenshot for plant names
            print(f"Watering {plant.lower()}")
    except ValueError as e:
        print(f"Error: {e}")
        # Le return ici empêche d'atteindre le print final, 
        # mais le bloc 'finally' s'exécutera QUAND MÊME avant de sortir.
        return
    finally:
        print("Closing watering system (cleanup)")
    
    print("Watering completed successfully!")


def test_watering_system() -> None:
    """Run tests to demonstrate the try/except/finally flow."""
    # Titre avec un saut de ligne après
    print("=== Garden Watering System ===\n")

    print("Testing normal watering...")
    water_plants(["tomato", "lettuce", "carrots"])

    # Saut de ligne avant le test en erreur
    print("\nTesting with error...")
    water_plants(["tomato", None])

    # Saut de ligne avant le message final
    print("\nCleanup always happens, even with errors!")


if __name__ == "__main__":
    test_watering_system()