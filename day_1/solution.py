import math


def calculate_fuel(value: int) -> int:
    return math.floor(value / 3) - 2


def part_1(filename: str) -> int:
    total_fuel = 0

    with open(filename) as file:
        for mass in file:
            total_fuel += calculate_fuel(int(mass))

    return total_fuel


def part_2(filename: str) -> int:
    total_fuel = 0

    with open(filename) as file:
        for mass in file:
            fuel = calculate_fuel(int(mass))

            while fuel > 0:
                total_fuel += fuel
                fuel = calculate_fuel(fuel)

    return total_fuel


print(f"Day 1 (Part 1) - Answer: {part_1('input.txt')}")
print(f"Day 1 (Part 2) - Answer: {part_2('input.txt')}")
