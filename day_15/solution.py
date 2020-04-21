from typing import List, Tuple, Dict

from day_9 import solution as int_code

initial_position = (0, 0)
routes_to_oxygen_system = []
map_status = {0: '#', 1: '.', 2: 'O'}


def get_position_by_command(position: Tuple[int, int], command: int) -> Tuple[int, int]:
    commands = {1: (0, 1), 2: (0, -1), 3: (-1, 0), 4: (1, 0)}
    return position[0] + commands.get(command)[0], position[1] + commands.get(command)[1]


def get_next_position_status(integers: List[int], command: int) -> int:
    return int_code.run_program(0, 0, integers.copy(), [command])[4][0]


def get_next_integers(integers: List[int], command: int) -> List[int]:
    return int_code.run_program(0, 0, integers.copy(), [command])[2]


def get_oxygen_system_position_from_area_map(area_map: Dict[Tuple[int, int], str]) -> Tuple[int, int]:
    return list(area_map.keys())[list(area_map.values()).index(map_status[2])]


def set_routes_to_oxygen_system(routes: List[List[Tuple[int, int]]], area_map: Dict[Tuple[int, int], str]):
    oxygen_system_position = get_oxygen_system_position_from_area_map(area_map)
    for route in routes:
        if oxygen_system_position in route:
            routes_to_oxygen_system.append(route)


def get_valid_adjacent_positions(position: Tuple[int, int], area_map: Dict[Tuple[int, int], str]) \
        -> List[Tuple[int, int]]:
    adjacent_sums = [(0, 1), (0, -1), (-1, 0), (1, 0)]
    valid_positions = list()

    for adjacent_sum in adjacent_sums:
        adjacent_position = (position[0] + adjacent_sum[0], position[1] + adjacent_sum[1])
        if adjacent_position in area_map and area_map[adjacent_position] == map_status[1]:
            valid_positions.append(adjacent_position)
    return valid_positions


def get_new_routes(route: List[Tuple[int, int]], integers_by_position: Dict[Tuple[int, int], List[int]],
                   area_map: Dict[Tuple[int, int], str]) -> List[List[Tuple[int, int]]]:
    new_routes = []
    position = route[-1]

    for command in range(1, 5):
        next_position = get_position_by_command(position, command)
        next_position_status = get_next_position_status(integers_by_position[position], command)

        if next_position not in route:
            area_map[next_position] = map_status.get(next_position_status)

            if next_position_status != 0:
                integers_by_position[next_position] = get_next_integers(integers_by_position[position], command)
                new_routes.append(route + [next_position])
    return new_routes


def complete_area_map(integers: List[int], area_map: Dict[Tuple[int, int], str]):
    routes = [[initial_position]]
    integers_by_position = {initial_position: integers}
    area_map_is_completed = False

    while not area_map_is_completed:
        active_routes = []
        for route in routes.copy():
            new_routes = get_new_routes(route, integers_by_position, area_map)
            routes += new_routes
            routes.remove(route)
            route_status = bool(new_routes)

            if route_status:
                active_routes += new_routes

            if not routes_to_oxygen_system and map_status[2] in area_map.values():
                set_routes_to_oxygen_system(routes, area_map)

        area_map_is_completed = not bool(active_routes)


def get_fewest_movements_to_oxygen_system(area_map: Dict[Tuple[int, int], str]) -> int:
    oxygen_system_position = get_oxygen_system_position_from_area_map(area_map)
    return min([route.index(oxygen_system_position) for route in routes_to_oxygen_system])


def time_to_fill_with_oxygen(area_map: Dict[Tuple[int, int], str]) -> int:
    minutes = 0
    oxygen_system_position = get_oxygen_system_position_from_area_map(area_map)
    positions_to_oxygenate = get_valid_adjacent_positions(oxygen_system_position, area_map)

    while map_status[1] in area_map.values():
        for position in positions_to_oxygenate.copy():
            area_map[position] = map_status[2]
            positions_to_oxygenate.remove(position)
            positions_to_oxygenate += get_valid_adjacent_positions(position, area_map)
        minutes += 1
    return minutes


def part_1(filename: str) -> int:
    with open(filename) as file:
        integers = [int(i) for i in file.read().split(',')]
        area_map = {initial_position: map_status[1]}
        complete_area_map(integers, area_map)
    return get_fewest_movements_to_oxygen_system(area_map)


def part_2(filename: str) -> int:
    with open(filename) as file:
        integers = [int(i) for i in file.read().split(',')]
        area_map = {initial_position: map_status[1]}
        complete_area_map(integers, area_map)
    return time_to_fill_with_oxygen(area_map)


print(f"Day 15 (Part 1) - Answer: {part_1('input.txt')}")
print(f"Day 15 (Part 2) - Answer: {part_2('input.txt')}")
