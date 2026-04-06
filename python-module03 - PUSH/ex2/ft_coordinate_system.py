#!/usr/bin/env python3
"""Exercise 2: Position Tracker - 3D coordinate system."""
import math


def get_player_pos() -> tuple[float, float, float]:
    """Ask user for coordinates until valid input is provided."""
    while True:
        user_input: str = input("Enter new coordinates as floats in "
                                "format 'x,y,z': ")
        try:
            pieces = user_input.split(",")
            if len(pieces) != 3:
                print("Invalid syntax")
                continue
            x = float(pieces[0].strip())
            y = float(pieces[1].strip())
            z = float(pieces[2].strip())
            return (x, y, z)
        except ValueError:
            for p in pieces:
                try:
                    float(p.strip())
                except ValueError:
                    print(f"Error on parameter '{p.strip()}': "
                          f"could not convert string to float: '{p.strip()}'")
                    break


def calculate_distance(pos1: tuple[float, float, float],
                       pos2: tuple[float, float, float]) -> float:
    """Calculate Euclidean distance between two 3D points."""
    x1, y1, z1 = pos1
    x2, y2, z2 = pos2
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2 + (z2 - z1)**2)


def main() -> None:
    """Main function to demonstrate coordinate system."""
    print("=== Game Coordinate System ===")

    print("Get a first set of coordinates")
    pos1: tuple[float, float, float] = get_player_pos()
    print(f"Got a first tuple: {pos1}")
    print(f"It includes: X={pos1[0]}, Y={pos1[1]}, Z={pos1[2]}")

    center: tuple[float, float, float] = (0.0, 0.0, 0.0)
    dist_to_center: float = calculate_distance(center, pos1)
    print(f"Distance to center: {round(dist_to_center, 4)}")

    print("Get a second set of coordinates")
    pos2: tuple[float, float, float] = get_player_pos()

    dist_between: float = calculate_distance(pos1, pos2)
    print(f"Distance between the 2 sets of coordinates: "
          f"{round(dist_between, 4)}")


if __name__ == "__main__":
    main()
