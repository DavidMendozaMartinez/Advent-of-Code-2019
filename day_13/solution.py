from copy import deepcopy
from typing import List, Tuple, Dict

from day_9 import solution as int_code


def get_tiles(outputs: List[int]) -> List[List[int]]:
    return [[outputs[i], outputs[i + 1], outputs[i + 2]] for i in range(len(outputs))[::3]]


def get_quantity_of_blocks(tiles: List[List[int]]) -> int:
    return [tile[2] for tile in tiles].count(2)


def get_ball_direction(ball_positions: List[Tuple[int, int]]) -> int:
    return ball_positions[-1][1] - ball_positions[-2][1]


def update_positions(positions: Dict[int, Tuple[int, int]], tiles: List[List[int]]):
    for tile in tiles:
        if tile[2] in (3, 4):
            positions[tile[2]] = (tile[0], tile[1])


def get_next_joystick_position(positions: Dict[int, Tuple[int, int]],
                               state: Tuple[int, int, List[int], List[int], List[int], bool]) -> int:
    ball_position = positions.get(4)

    while ball_position[1] < 21 and state[5]:
        state = int_code.run_program(state[0], state[1], state[2], [0])
        tiles = get_tiles(state[4])
        update_positions(positions, tiles)
        ball_position = positions.get(4)

    return ball_position[0]


def run_game(integers: List[int], tiles: List[List[int]]) -> int:
    positions = dict()
    update_positions(positions, tiles)

    ball_positions = [positions.get(4)]
    joystick_position = positions.get(3)[0]
    next_joystick_position = joystick_position

    integers[0] = 2
    state = (0, 0, integers, [0], [], True)

    while state[5]:
        state = int_code.run_program(state[0], state[1], state[2], state[3])
        tiles = get_tiles(state[4])
        update_positions(positions, tiles)

        joystick_position = positions.get(3)[0]
        ball_position = positions.get(4)
        ball_positions.append(ball_position)
        ball_direction = get_ball_direction(ball_positions)

        if ball_position[1] == 20 and ball_direction == -1:
            next_joystick_position = get_next_joystick_position(deepcopy(positions), deepcopy(state))

        state[3].append((next_joystick_position > joystick_position) - (joystick_position > next_joystick_position))

    return next(tile[2] for tile in tiles if tile[0] == -1 and tile[1] == 0)


def part_1(filename: str) -> int:
    with open(filename) as file:
        integers = [int(i) for i in file.read().split(',')]
        outputs = int_code.run_program(0, 0, integers, [])[4]
        tiles = get_tiles(outputs)
    return get_quantity_of_blocks(tiles)


def part_2(filename: str) -> int:
    with open(filename) as file:
        integers = [int(i) for i in file.read().split(',')]
        outputs = int_code.run_program(0, 0, integers, [])[4]
        tiles = get_tiles(outputs)
    return run_game(integers.copy(), tiles.copy())


print(f"Day 13 (Part 1) - Answer: {part_1('input.txt')}")
print(f"Day 13 (Part 2) - Answer: {part_2('input.txt')}")
