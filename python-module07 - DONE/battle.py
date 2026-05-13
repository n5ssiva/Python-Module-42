from ex0 import FlameFactory, AquaFactory, CreatureFactory


def test_factory(factory: CreatureFactory) -> None:
    print("Testing factory")
    base = factory.create_base()
    print(base.describe())
    print(base.attack())
    evolved = factory.create_evolved()
    print(evolved.describe())
    print(evolved.attack())


def battle(factory_a: CreatureFactory, factory_b: CreatureFactory) -> None:
    print("Testing battle")
    a = factory_a.create_base()
    b = factory_b.create_base()
    print(a.describe())
    print("vs.")
    print(b.describe())
    print("fight!")
    print(a.attack())
    print(b.attack())


def main() -> None:
    try:
        flame_factory = FlameFactory()
        aqua_factory = AquaFactory()

        test_factory(flame_factory)
        print()
        test_factory(aqua_factory)
        print()
        battle(flame_factory, aqua_factory)
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
