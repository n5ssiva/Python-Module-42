def ft_seed_inventory(seed_type: str, quantity: int, unit: str) -> None:
    name = seed_type.capitalize()
    if unit == "packets":
        print(name, "seeds:", quantity, unit, "available")
    elif unit == "grams":
        print(name, "seeds:", quantity, unit, "total")
    elif unit == "area":
        print(name, "seeds:", "covers", quantity, "square meters")
    else:
        print("Unknown unit type")
