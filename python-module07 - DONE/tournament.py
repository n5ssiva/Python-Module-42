from ex0 import CreatureFactory, FlameFactory, AquaFactory
from ex1 import HealingCreatureFactory, TransformCreatureFactory
from ex2 import (
    BattleStrategy,
    NormalStrategy,
    AggressiveStrategy,
    DefensiveStrategy,
    InvalidStrategyError,
)


def battle(opponents: list[tuple[CreatureFactory, BattleStrategy]]) -> None:
    print("*** Tournament ***")
    print(f"{len(opponents)} opponents involved")

    creatures = [(factory.create_base(), strategy)
                 for factory, strategy in opponents]

    try:
        for i in range(len(creatures)):
            for j in range(i + 1, len(creatures)):
                creature_a, strategy_a = creatures[i]
                creature_b, strategy_b = creatures[j]
                print()
                print("* Battle *")
                print(creature_a.describe())
                print(" vs.")
                print(creature_b.describe())
                print(" now fight!")
                strategy_a.act(creature_a)
                strategy_b.act(creature_b)
    except InvalidStrategyError as e:
        print(f"Battle error, aborting tournament: {e}")


def main() -> None:
    try:
        flame = FlameFactory()
        aqua = AquaFactory()
        healing = HealingCreatureFactory()
        transform = TransformCreatureFactory()

        normal = NormalStrategy()
        aggressive = AggressiveStrategy()
        defensive = DefensiveStrategy()

        print("Tournament 0 (basic)")
        print(" [ (Flameling+Normal), (Healing+Defensive) ]")
        battle([(flame, normal), (healing, defensive)])
        print()

        print("Tournament 1 (error)")
        print(" [ (Flameling+Aggressive), (Healing+Defensive) ]")
        battle([(flame, aggressive), (healing, defensive)])
        print()

        print("Tournament 2 (multiple)")
        print(" [ (Aquabub+Normal), (Healing+Defensive), "
              "(Transform+Aggressive) ]")
        battle([(aqua, normal), (healing, defensive),
                (transform, aggressive)])

    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
