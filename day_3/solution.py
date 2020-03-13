from typing import List, Tuple, Set

central_port = (0, 0)


def move(instruction: str, positions: List[Tuple[int, int]]):
    movement = instruction[0]
    distance = int(instruction[1:])

    x = positions[-1][0]
    y = positions[-1][1]

    for i in range(1, distance + 1):
        if movement == 'U':
            positions.append((x, y + i))
        elif movement == 'D':
            positions.append((x, y - i))
        elif movement == 'R':
            positions.append((x + i, y))
        elif movement == 'L':
            positions.append((x - i, y))


def get_wires(filename: str) -> List[List[Tuple[int, int]]]:
    wires = []

    with open(filename) as file:
        for line in file:
            instructions = line.split(',')
            positions = [central_port]

            for instruction in instructions:
                move(instruction, positions)
            wires.append(positions)
    return wires


def get_crosses(wires: List[List[Tuple[int, int]]]) -> Set[Tuple[int, int]]:
    crosses = set.intersection(*[set(wire) for wire in wires])
    crosses.discard(central_port)
    return crosses


def manhattan_distance(point_1: Tuple[int, int], point_2: Tuple[int, int]) -> int:
    return abs(point_2[0] - point_1[0]) + abs(point_2[1] - point_1[1])


def part_1(filename: str) -> int:
    crosses_distances = []

    wires = get_wires(filename)
    crosses = get_crosses(wires)

    for cross in crosses:
        crosses_distances.append(manhattan_distance(central_port, cross))

    return min(crosses_distances)


def part_2(filename: str) -> int:
    crosses_distances = []

    wires = get_wires(filename)
    crosses = get_crosses(wires)

    for cross in crosses:
        crosses_distances.append(sum([wire.index(cross) for wire in wires]))

    return min(crosses_distances)


print(f"Day 3 (Part 1) - Answer: {part_1('input.txt')}")
print(f"Day 3 (Part 2) - Answer: {part_2('input.txt')}")
