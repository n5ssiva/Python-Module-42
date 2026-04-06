#!/usr/bin/env python3
"""Exercise 4: Inventory system - Player inventory management."""
import sys


def main() -> None:
    print("=== Inventory System Analysis ===")
    if len(sys.argv) == 1:
        print("No arguments provided!")
        return
    inventory: dict[str, int] = {}

    for arg in sys.argv[1:]:
        pieces = arg.split(":")
        if len(pieces) != 2:
            print(f"Error - invalid parameter '{arg}'")
        else:
            item = pieces[0]
            quantity_str = pieces[1]
            try:
                quantity = int(quantity_str)
                if item in inventory:
                    print(f"Redundant item '{item}' - discarding")
                else:
                    inventory[item] = quantity
            except ValueError:
                print(
                    f"Quantity error for '{item}': invalid literal"
                    f" for int() with base 10: '{quantity_str}'"
                )

    if not inventory:
        return

    total = sum(inventory.values())
    print(f"Got inventory: {inventory}")
    print(f"Item list: {list(inventory.keys())}")
    print(f"Total quantity of the {len(inventory)} items: {total}")

    for item, quantity in inventory.items():
        percentage = round((quantity / total) * 100, 1)
        print(f"Item {item} represents {percentage}%")

    most = max(inventory, key=lambda i: inventory[i])
    least = min(inventory, key=lambda i: inventory[i])
    print(f"Item most abundant: {most} with quantity {inventory[most]}")
    print(f"Item least abundant: {least} with quantity {inventory[least]}")

    inventory.update({"magic_item": 1})
    print(f"Updated inventory: {inventory}")


if __name__ == "__main__":
    main()
