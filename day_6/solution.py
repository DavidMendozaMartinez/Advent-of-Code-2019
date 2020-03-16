from collections import defaultdict
from typing import List

direct_orbits_map = defaultdict(str)
orbits_count = defaultdict(int)
path_of_orbits = defaultdict(list)


def calculate_orbits(key: str, orbits: int) -> int:
    count = orbits_count.get(key, calculate_orbits(direct_orbits_map[key], orbits) + 1 if direct_orbits_map[
                                                                                              key] != 'COM' else 1)
    orbits_count[key] = count
    orbits += count
    return orbits


def get_path_of_orbits(key: str) -> List[str]:
    return path_of_orbits.get(key, get_path_of_orbits(direct_orbits_map[key]).copy() + [
        direct_orbits_map[key]] if direct_orbits_map[key] != 'COM' else ['COM']).copy()


def get_min_orbital_transfers(path_origin: List[str], path_destination: List[str]) -> int:
    last_common = [value for value in path_origin if value in path_destination][-1]
    index_last_common = path_origin.index(last_common)

    return len(path_origin[index_last_common + 1:]) + len(path_destination[index_last_common + 1:])


def part_1(filename: str) -> int:
    with open(filename) as file:
        for line in file.read().split('\n'):
            key = line[line.find(')') + 1:]
            value = line[:line.find(')')]
            direct_orbits_map[key] = value

    orbits = 0
    for orbit in direct_orbits_map.keys():
        orbits += calculate_orbits(orbit, 0)

    return orbits


def part_2(filename: str) -> int:
    with open(filename) as file:
        for line in file.read().split('\n'):
            key = line[line.find(')') + 1:]
            value = line[:line.find(')')]
            direct_orbits_map[key] = value

    path_origin = get_path_of_orbits('YOU')
    path_destination = get_path_of_orbits('SAN')
    return get_min_orbital_transfers(path_origin, path_destination)


print(f"Day 6 (Part 1) - Answer: {part_1('input.txt')}")
print(f"Day 6 (Part 2) - Answer: {part_2('input.txt')}")
