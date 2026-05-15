from collections.abc import Callable


def spell_combiner(spell1: Callable, spell2: Callable) -> Callable:
    def combined(target: str, power: int) -> tuple:
        return (spell1(target, power), spell2(target, power))
    return combined


def power_amplifier(base_spell: Callable, multiplier: int) -> Callable:
    def amplified(target: str, power: int) -> str:
        return base_spell(target, power * multiplier)
    return amplified


def conditional_caster(condition: Callable, spell: Callable) -> Callable:
    def maybe_cast(target: str, power: int) -> str:
        if condition(target, power):
            return spell(target, power)
        return "Spell fizzled"
    return maybe_cast


def spell_sequence(spells: list[Callable]) -> Callable:
    def cast_all(target: str, power: int) -> list:
        return [s(target, power) for s in spells]
    return cast_all


def fireball(target: str, power: int) -> str:
    return f"Fireball hits {target} for {power} damage"


def heal(target: str, power: int) -> str:
    return f"Heal restores {target} for {power} HP"


def shield(target: str, power: int) -> str:
    return f"Shield protects {target} with {power} armor"


def main() -> None:
    print("Testing spell combiner...")
    combined = spell_combiner(fireball, heal)
    result = combined("Dragon", 10)
    print(f"Combined spell result: {result[0]}, {result[1]}")
    print()

    print("Testing power amplifier...")
    mega_fireball = power_amplifier(fireball, 3)
    print(f"Original: {fireball('Goblin', 10)}")
    print(f"Amplified: {mega_fireball('Goblin', 10)}")
    print()

    print("Testing conditional caster...")
    only_strong = conditional_caster(
        lambda t, p: p >= 50,
        fireball,
    )
    print(only_strong("Dragon", 75))
    print(only_strong("Goblin", 10))
    print()

    print("Testing spell sequence...")
    sequence = spell_sequence([fireball, heal, shield])
    results = sequence("Knight", 20)
    for r in results:
        print(r)


if __name__ == "__main__":
    main()
