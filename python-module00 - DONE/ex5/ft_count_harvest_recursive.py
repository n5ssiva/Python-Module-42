def ft_count_harvest_recursive(day=1, total=None):
    if total is None:
        total = int(input("Days until harvest: "))
    if day > total:
        print("Harvest time!")
        return
    print("Day", day)
    ft_count_harvest_recursive(day + 1, total)
