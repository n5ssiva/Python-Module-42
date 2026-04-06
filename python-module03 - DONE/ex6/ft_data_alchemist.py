#!/usr/bin/env python3
"""Exercise 6: List & Dictionary - Comprehensible list."""

import random

players = ['Alice', 'bob', 'Charlie', 'dylan',
           'Emma', 'Gregory', 'john', 'kevin', 'Liam']


def main() -> None:
    all_capitalize = [player.capitalize() for player in players]
    only_capitalize = [player for player in players if player[0].isupper()]

    print("=== Game Data Alchemist ===\n")
    print(f"Initial list of players: {players}")
    print(f"New list with all names capitalized: {all_capitalize}")
    print(f"New list of capitalized names only: {only_capitalize}\n")

    score_dict = {player: random.randint(0, 1000) for player in all_capitalize}

    print(f"Score dict: {score_dict}")

    average = sum(score_dict.values()) / len(score_dict)

    print(f"Score average is: {round(average, 2)}")

    high_score_dict = {player: score
                       for player, score in score_dict.items()
                       if score > average}

    print(f"High scores: {high_score_dict}")


if __name__ == "__main__":
    main()
