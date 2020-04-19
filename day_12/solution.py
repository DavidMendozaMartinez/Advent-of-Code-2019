from itertools import combinations
from math import gcd
from typing import List


def apply_gravity(positions: List[List[int]], velocities: List[List[int]]):
    for pair in combinations(range(len(positions)), 2):
        for dim in range(len(positions[0])):
            dim_1 = positions[pair[0]][dim]
            dim_2 = positions[pair[1]][dim]

            velocities[pair[0]][dim] += (dim_2 > dim_1) - (dim_2 < dim_1)
            velocities[pair[1]][dim] += (dim_1 > dim_2) - (dim_1 < dim_2)


def apply_velocity(positions: List[List[int]], velocities: List[List[int]]):
    for i, velocity in enumerate(velocities):
        for j, dim_velocity in enumerate(velocity):
            positions[i][j] += dim_velocity


def make_simulation(positions: List[List[int]], velocities: List[List[int]], steps: int):
    for _ in range(steps):
        apply_gravity(positions, velocities)
        apply_velocity(positions, velocities)


def calculate_total_energy(positions: List[List[int]], velocities: List[List[int]]) -> int:
    total_energy = 0
    for i in range(len(positions)):
        total_energy += sum(map(abs, positions[i])) * sum(map(abs, velocities[i]))

    return total_energy


def get_lcm(values: List[int]) -> int:
    lcm = 1
    for value in values:
        lcm = abs(lcm * value) // gcd(lcm, value)
    return lcm


def get_steps_to_reach_initial_state(positions: List[List[int]], velocities: List[List[int]]) -> int:
    steps_by_dimension = []

    for dim in range(len(positions[0])):
        dim_positions = [[position[dim]] for position in positions]
        dim_velocities = [[velocity[dim]] for velocity in velocities]

        dim_initial_positions = [dim[:] for dim in dim_positions]
        dim_initial_velocities = [dim[:] for dim in dim_velocities]

        make_simulation(dim_positions, dim_velocities, 1)
        steps = 1

        while dim_initial_positions != dim_positions or dim_initial_velocities != dim_velocities:
            make_simulation(dim_positions, dim_velocities, 1)
            steps += 1

        steps_by_dimension.append(steps)

    return get_lcm(steps_by_dimension)


def part_1(filename: str) -> int:
    positions = []

    with open(filename) as file:
        for line in file:
            dimensions = line.replace('\n', '')[1:-1].split(',')
            positions.append([int(dimension[dimension.index('=') + 1:]) for dimension in dimensions])

    velocities = [[0 for _ in range(len(positions[0]))] for _ in range(len(positions))]
    make_simulation(positions, velocities, 1000)

    return calculate_total_energy(positions, velocities)


def part_2(filename: str) -> int:
    positions = []

    with open(filename) as file:
        for line in file:
            dimensions = line.replace('\n', '')[1:-1].split(',')
            positions.append([int(dimension[dimension.index('=') + 1:]) for dimension in dimensions])

    velocities = [[0 for _ in range(len(positions[0]))] for _ in range(len(positions))]

    return get_steps_to_reach_initial_state(positions, velocities)


print(f"Day 12 (Part 1) - Answer: {part_1('input.txt')}")
print(f"Day 12 (Part 2) - Answer: {part_2('input.txt')}")
