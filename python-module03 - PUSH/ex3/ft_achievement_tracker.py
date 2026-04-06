#!/usr/bin/env python3
"""Exercise 3: Achievement Hunter - Set operations for achievement tracking."""
import random


def gen_player_achievements() -> set[str]:
    """Generate random set of achievements for a player."""
    all_achievements = [
        'Crafting Genius', 'World Savior', 'Master Explorer',
        'Collector Supreme', 'Untouchable', 'Boss Slayer',
        'Strategist', 'Speed Runner', 'Survivor', 'Treasure Hunter',
        'First Steps', 'Sharp Mind', 'Unstoppable', 'Hidden Path Finder'
    ]
    rand = random.randint(4, 8)
    return set(random.sample(all_achievements, rand))


def main() -> None:
    """Main function to demonstrate set operations."""
    print("=== Achievement Tracker System ===\n")

    players = ['Alice', 'Bob', 'Charlie', 'Dylan']
    achievements: dict[str, set[str]] = {}
    for player in players:
        achievements[player] = gen_player_achievements()

    for player, achv in achievements.items():
        print(f"Player {player}: {achv}")

    all_achievements: set[str] = set()
    for val in achievements.values():
        all_achievements |= val
    print(f"\nAll distinct achievements: {all_achievements}\n")

    all_sets = list(achievements.values())
    common: set[str] = set(all_sets[0])
    for s in all_sets[1:]:
        common &= s
    print(f"Common achievements: {common}\n")

    for player, achv in achievements.items():
        others: set[str] = set()
        for other_player, other_achv in achievements.items():
            if other_player != player:
                others |= other_achv
        only_this_player = achv - others
        print(f"Only {player} has: {only_this_player}")
    print()

    for player, achv in achievements.items():
        missing = all_achievements - achv
        print(f"{player} is missing: {missing}")


if __name__ == "__main__":
    main()
