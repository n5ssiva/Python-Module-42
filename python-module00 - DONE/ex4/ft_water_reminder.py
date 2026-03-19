def ft_water_reminder():
    watering_time = int(input("Days since last watering: "))
    if watering_time > 2:
        print("Water the plants!")
    else:
        print("Plants are fine")
