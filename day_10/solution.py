import math
from typing import List, Tuple, Dict


def get_asteroids_coordinates(asteroids_map: List[List[int]]) -> List[Tuple[int, int]]:
    asteroids_coordinates = []
    for i, row in enumerate(asteroids_map):
        for j, column in enumerate(row):
            if column == '#':
                asteroids_coordinates.append((j, i))
    return asteroids_coordinates


def get_module(point_1: Tuple[int, int], point_2: Tuple[int, int]) -> float:
    return math.sqrt(math.pow(point_2[0] - point_1[0], 2) + math.pow(point_2[1] - point_1[1], 2))


def get_angle(point_1: Tuple[int, int], point_2: Tuple[int, int]) -> float:
    vector = (point_2[0] - point_1[0], point_2[1] - point_1[1])
    return math.degrees(math.atan2(vector[1], vector[0]))


def get_number_visible_asteroids(coordinates: Tuple[int, int], asteroids_coordinates: List[Tuple[int, int]]) -> int:
    asteroids_with_direct_sight = 0
    angles = []

    for asteroid_coordinates in asteroids_coordinates:
        if asteroid_coordinates != coordinates:
            angle = get_angle(coordinates, asteroid_coordinates)
            if angle not in angles:
                angles.append(angle)
                asteroids_with_direct_sight += 1
    return asteroids_with_direct_sight


def get_max_number_visible_asteroids(asteroids_coordinates: List[Tuple[int, int]]) -> int:
    return max([get_number_visible_asteroids(asteroid, asteroids_coordinates) for asteroid in asteroids_coordinates])


def get_monitoring_station_coordinates(asteroids_coordinates: List[Tuple[int, int]]) -> Tuple[int, int]:
    number_visible_asteroids_by_coordinates = {asteroid: get_number_visible_asteroids(asteroid, asteroids_coordinates)
                                               for asteroid in asteroids_coordinates}
    return max(number_visible_asteroids_by_coordinates, key=number_visible_asteroids_by_coordinates.get)


def get_visible_asteroids_map(coordinates: Tuple[int, int], asteroids_coordinates: List[Tuple[int, int]]) \
        -> Dict[float, Tuple[int, int]]:
    visible_asteroid_map = dict()

    for asteroid_coordinates in asteroids_coordinates:
        if asteroid_coordinates != coordinates:
            angle = get_angle(coordinates, asteroid_coordinates) + 90
            angle += (360 if angle < 0 else 0)
            module = get_module(coordinates, asteroid_coordinates)
            if angle not in visible_asteroid_map or get_module(coordinates, visible_asteroid_map[angle]) > module:
                visible_asteroid_map[angle] = asteroid_coordinates

    return visible_asteroid_map


def sort_visible_asteroid_map_by_angle(visible_asteroid_map: Dict[float, Tuple[int, int]]) \
        -> Dict[float, Tuple[int, int]]:
    return {k: v for k, v in sorted(visible_asteroid_map.items())}


def get_vaporized_asteroids(monitoring_station: Tuple[int, int], asteroids_coordinates: List[Tuple[int, int]]) \
        -> List[Tuple[int, int]]:
    vaporized_asteroids = []
    visible_asteroids_map = get_visible_asteroids_map(monitoring_station, asteroids_coordinates)
    sorted_visible_asteroids_map = sort_visible_asteroid_map_by_angle(visible_asteroids_map)

    while len(asteroids_coordinates) != 1:
        for asteroid in sorted_visible_asteroids_map.values():
            asteroids_coordinates.remove(asteroid)
            vaporized_asteroids.append(asteroid)

        visible_asteroids_map = get_visible_asteroids_map(monitoring_station, asteroids_coordinates)
        sorted_visible_asteroids_map = sort_visible_asteroid_map_by_angle(visible_asteroids_map)

    return vaporized_asteroids


def part_1(filename: str) -> int:
    asteroids_map = []
    with open(filename) as file:
        for line in file:
            asteroids_map.append(list(line.replace('\n', '')))
    asteroids_coordinates = get_asteroids_coordinates(asteroids_map)

    return get_max_number_visible_asteroids(asteroids_coordinates)


def part_2(filename: str) -> int:
    asteroids_map = []
    with open(filename) as file:
        for line in file:
            asteroids_map.append(list(line.replace('\n', '')))
    asteroids_coordinates = get_asteroids_coordinates(asteroids_map)
    monitoring_station = get_monitoring_station_coordinates(asteroids_coordinates)
    vaporized_asteroids = get_vaporized_asteroids(monitoring_station, asteroids_coordinates.copy())

    return vaporized_asteroids[199][0] * 100 + vaporized_asteroids[199][1]


print(f"Day 10 (Part 1) - Answer: {part_1('input.txt')}")
print(f"Day 10 (Part 2) - Answer: {part_2('input.txt')}")
