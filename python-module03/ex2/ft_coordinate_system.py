import math


def parse_coordinates(coord_string):
    try:
        pieces = coord_string.split(",")
        return (int(pieces[0]), int(pieces[1]), int(pieces[2]))
    except ValueError as e:
        print(f"Error parsing coordinates: {e}")
        print(f"Error details - Type: {type(e).__name__}, Args: {e.args}\n")
        return None


def calculate_distance(pos1, pos2):
    x1, y1, z1 = pos1
    x2, y2, z2 = pos2
    distance = math.sqrt((x2-x1)**2 + (y2-y1)**2 + (z2-z1)**2)
    return distance


if __name__ == "__main__":
    print("=== Game Coordinate System ===")
    pos0 = parse_coordinates("10,20,5")
    print(f"Position created: {pos0}")
    pos1 = parse_coordinates("0,0,0")
    print(f"Distance between {pos1} and {pos0}: "
          f"{calculate_distance(pos1, pos0):.2f}\n")
    pos2 = parse_coordinates("3,4,0")
    print('Parsing coordinates: "3,4,0"')
    print(f"Parsed position: {pos2}")
    print(f"Distance between {pos1} and {pos2}: "
          f"{calculate_distance(pos1, pos2)}\n")
    print('Parsing invalid coordinates: "abc,def,ghi"')
    parse_coordinates("abc,def,ghi")
    print("Unpacking demonstration:")
    x, y, z = pos2
    print(f"Player at x={x}, y={y}, z={z}")
    print(f"Coordinates = X={x}, Y={y}, Z={z}")
