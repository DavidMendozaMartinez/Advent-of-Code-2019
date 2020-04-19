from typing import List, Dict, Tuple

from day_9 import solution as int_code


def turn_robot(current_direction: str, output_direction: int) -> str:
    directions = ['<', '^', '>', 'v']
    index = (directions.index(current_direction) + (1 if output_direction else -1)) % len(directions)
    return directions[index]


def move_robot(position: Tuple[int, int], direction: str) -> Tuple[int, int]:
    movements = {'<': (-1, 0), '^': (0, 1), '>': (1, 0), 'v': (0, -1)}
    x = position[0] + movements.get(direction)[0]
    y = position[1] + movements.get(direction)[1]
    return x, y


def get_panels(integers: List[int], initial_color: int) -> Dict[Tuple[int, int], int]:
    panels = {(0, 0): initial_color}
    current_position = (0, 0)
    current_direction = '^'

    state = (0, 0, integers, [panels.get(current_position, 0)], [], True)

    while state[5]:
        state = int_code.run_program(state[0], state[1], state[2], state[3])
        panels[current_position] = state[4][-2]
        current_direction = turn_robot(current_direction, state[4][-1])
        current_position = move_robot(current_position, current_direction)
        state[3].append(panels.get(current_position, 0))

    return panels


def paint_registration_identifier(panels: Dict[Tuple[int, int], int]) -> str:
    colors = {0: '█', 1: '▒'}
    drawing = ''
    x_values = [panel[0] for panel in panels.keys()]
    y_values = [panel[1] for panel in panels.keys()]

    for y in range(min(y_values), max(y_values) + 1)[::-1]:
        for x in range(min(x_values), max(x_values) + 1):
            drawing += colors.get(panels.get((x, y), 0))
        drawing += '\n'

    return drawing


def part_1(filename: str) -> int:
    with open(filename) as file:
        integers = [int(i) for i in file.read().split(',')]
        panels = get_panels(integers, 0)
    return len(panels.keys())


def part_2(filename: str) -> str:
    with open(filename) as file:
        integers = [int(i) for i in file.read().split(',')]
        panels = get_panels(integers, 1)
        registration_identifier = paint_registration_identifier(panels)
    return registration_identifier


print(f"Day 11 (Part 1) - Answer: {part_1('input.txt')}")
print(f"Day 11 (Part 2) - Answer:\n{part_2('input.txt')}")
