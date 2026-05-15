def artifact_sorter(artifacts: list[dict]) -> list[dict]:
    return sorted(artifacts, key=lambda a: a["power"], reverse=True)


def power_filter(mages: list[dict], min_power: int) -> list[dict]:
    return list(filter(lambda m: m["power"] >= min_power, mages))


def spell_transformer(spells: list[str]) -> list[str]:
    return list(map(lambda s: f"* {s} *", spells))


def mage_stats(mages: list[dict]) -> dict:
    if not mages:
        return {"max_power": 0, "min_power": 0, "avg_power": 0.0}
    max_p = max(mages, key=lambda m: m["power"])["power"]
    min_p = min(mages, key=lambda m: m["power"])["power"]
    avg_p = round(sum(map(lambda m: m["power"], mages)) / len(mages), 2)
    return {"max_power": max_p, "min_power": min_p, "avg_power": avg_p}


def main() -> None:
    artifacts = [
        {"name": "Crystal Orb", "power": 85, "type": "scrying"},
        {"name": "Fire Staff", "power": 92, "type": "offensive"},
        {"name": "Shield Amulet", "power": 70, "type": "defensive"},
    ]
    mages = [
        {"name": "Alex", "power": 80, "element": "fire"},
        {"name": "Jordan", "power": 95, "element": "ice"},
        {"name": "Riley", "power": 60, "element": "earth"},
    ]
    spells = ["fireball", "heal", "shield"]

    print("Testing artifact sorter...")
    sorted_artifacts = artifact_sorter(artifacts)
    print(f"{sorted_artifacts[0]['name']} ({sorted_artifacts[0]['power']} "
          f"power) comes before {sorted_artifacts[1]['name']} "
          f"({sorted_artifacts[1]['power']} power)")
    print()

    print("Testing power filter...")
    strong_mages = power_filter(mages, 75)
    for m in strong_mages:
        print(f"{m['name']} ({m['power']} power)")
    print()

    print("Testing spell transformer...")
    transformed = spell_transformer(spells)
    print(" ".join(transformed))
    print()

    print("Testing mage stats...")
    stats = mage_stats(mages)
    print(f"Max power: {stats['max_power']}")
    print(f"Min power: {stats['min_power']}")
    print(f"Avg power: {stats['avg_power']}")


if __name__ == "__main__":
    main()
