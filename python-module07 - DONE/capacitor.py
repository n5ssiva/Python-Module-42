from ex0 import CreatureFactory
from ex1 import (
    HealingCreatureFactory,
    TransformCreatureFactory,
    HealCapability,
    TransformCapability,
)


def test_healing_family(factory: CreatureFactory) -> None:
    print("Testing Creature with healing capability")
    base = factory.create_base()
    print(" base:")
    print(base.describe())
    print(base.attack())
    if isinstance(base, HealCapability):
        print(base.heal())

    evolved = factory.create_evolved()
    print(" evolved:")
    print(evolved.describe())
    print(evolved.attack())
    if isinstance(evolved, HealCapability):
        print(evolved.heal())


def test_transform_family(factory: CreatureFactory) -> None:
    print("Testing Creature with transform capability")
    base = factory.create_base()
    print(" base:")
    print(base.describe())
    print(base.attack())
    if isinstance(base, TransformCapability):
        print(base.transform())
        print(base.attack())
        print(base.revert())

    evolved = factory.create_evolved()
    print(" evolved:")
    print(evolved.describe())
    print(evolved.attack())
    if isinstance(evolved, TransformCapability):
        print(evolved.transform())
        print(evolved.attack())
        print(evolved.revert())


def main() -> None:
    try:
        test_healing_family(HealingCreatureFactory())
        print()
        test_transform_family(TransformCreatureFactory())
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
