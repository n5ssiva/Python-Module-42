#!/usr/bin/env python3
"""Exercise 6: Garden Analytics Platform - Advanced OOP patterns."""


class Plant:
    """Base plant class with common features."""

    def __init__(self, name: str, height: int) -> None:
        """Initialize a basic plant."""
        self.name: str = name
        self.height: int = height

    def grow(self, amount: int = 1) -> None:
        """Increase plant height."""
        self.height += amount

    def get_info(self) -> str:
        """Return plant info."""
        return f"{self.name}: {self.height}cm"


class FloweringPlant(Plant):
    """A plant that can bloom."""

    def __init__(self, name: str, height: int, color: str) -> None:
        """Initialize a flowering plant with color."""
        super().__init__(name, height)
        self.color: str = color
        self.is_blooming: bool = True

    def bloom(self) -> None:
        """Make the plant bloom."""
        self.is_blooming = True

    def get_info(self) -> str:
        """Return flowering plant info."""
        status: str = "blooming" if self.is_blooming else "not blooming"
        return f"{self.name}: {self.height}cm, {self.color} flowers ({status})"


class PrizeFlower(FloweringPlant):
    """A prize-winning flowering plant."""

    def __init__(self, name: str, height: int, color: str,
                 prize_points: int) -> None:
        """Initialize a prize flower."""
        super().__init__(name, height, color)
        self.prize_points: int = prize_points

    def get_info(self) -> str:
        """Return prize flower info."""
        status: str = "blooming" if self.is_blooming else "not blooming"
        return f"{self.name}: {self.height}cm, {self.color} flowers " \
               f"({status}), Prize points: {self.prize_points}"


class GardenManager:
    """Manages multiple gardens with analytics capabilities."""

    garden_count: int = 0

    class GardenStats:
        """Nested helper class for calculating garden statistics."""

        @staticmethod
        def count_plant_types(plants: list[Plant]) -> dict[str, int]:
            """Count different types of plants."""
            regular: int = 0
            flowering: int = 0
            prize: int = 0

            for plant in plants:
                if isinstance(plant, PrizeFlower):
                    prize += 1
                elif isinstance(plant, FloweringPlant):
                    flowering += 1
                else:
                    regular += 1
            return {"regular": regular, "flowering": flowering, "prize": prize}

        @staticmethod
        def calculate_total_height(plants: list[Plant]) -> int:
            """Calculate total height of all plants."""
            total: int = 0
            for plant in plants:
                total += plant.height
            return total

    def __init__(self, owner: str) -> None:
        """Initialize a garden manager for an owner."""
        self.owner: str = owner
        self.plants: list[Plant] = []
        self.plants_added: int = 0
        self.total_growth: int = 0
        GardenManager.garden_count += 1

    def add_plant(self, plant: Plant) -> None:
        """Add a plant to the garden."""
        self.plants.append(plant)
        self.plants_added += 1
        print(f"Added {plant.name} to {self.owner}'s garden")

    def grow_all(self, amount: int = 1) -> None:
        """Make all plants grow."""
        print(f"{self.owner} is helping all plants grow...")
        for plant in self.plants:
            plant.grow(amount)
            self.total_growth += amount
            print(f"{plant.name} grew {amount}cm")

    def get_report(self) -> None:
        """Print a garden report."""
        print(f"=== {self.owner}'s Garden Report ===")
        print("Plants in garden:")
        for plant in self.plants:
            print(f"- {plant.get_info()}")

        print(f"Plants added: {self.plants_added}, "
              f"Total growth: {self.total_growth}cm")

        stats: dict[str, int] = self.GardenStats.count_plant_types(self.plants)
        print(f"Plant types: {stats['regular']} regular, "
              f"{stats['flowering']} flowering, "
              f"{stats['prize']} prize flowers")

    def get_score(self) -> int:
        """Calculate garden score."""
        return self.GardenStats.calculate_total_height(self.plants)

    @classmethod
    def create_garden_network(cls, owners: list[str]) -> list["GardenManager"]:
        """Create multiple gardens at once (class method)."""
        gardens: list[GardenManager] = []
        for owner in owners:
            gardens.append(cls(owner))
        return gardens

    @classmethod
    def get_total_gardens(cls) -> int:
        """Return total number of gardens managed."""
        return cls.garden_count

    @staticmethod
    def validate_height(height: int) -> bool:
        """Validate that height is positive (utility function)."""
        return height > 0


def main() -> None:
    """Demonstrate the garden analytics platform."""
    print("=== Garden Management System Demo ===")

    # Create garden manager
    alice_garden: GardenManager = GardenManager("Alice")
    bob_garden: GardenManager = GardenManager("Bob")

    # Add plants of different types
    oak: Plant = Plant("Oak Tree", 100)
    rose: FloweringPlant = FloweringPlant("Rose", 25, "red")
    sunflower: PrizeFlower = PrizeFlower("Sunflower", 50, "yellow", 10)

    alice_garden.add_plant(oak)
    alice_garden.add_plant(rose)
    alice_garden.add_plant(sunflower)

    # Grow all plants
    alice_garden.grow_all(1)

    # Print report
    alice_garden.get_report()

    # Static method demo
    print(f"Height validation test: "
          f"{GardenManager.validate_height(100)}")

    # Garden scores
    bob_garden.add_plant(Plant("Fern", 30))
    bob_garden.add_plant(FloweringPlant("Tulip", 20, "pink"))
    bob_garden.grow_all(1)

    print(f"Garden scores - Alice: {alice_garden.get_score()}, "
          f"Bob: {bob_garden.get_score()}")

    # Class method demo
    print(f"Total gardens managed: {GardenManager.get_total_gardens()}")


if __name__ == "__main__":
    main()