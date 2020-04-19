from math import ceil
from typing import List, Tuple, Dict

reactions = dict()
increments = dict()


def get_reaction_inputs(reaction: str) -> List[Tuple[str, int]]:
    input_chemicals = reaction[:reaction.find('=')].split(',')
    return [(chemical.strip().split(' ')[1], int(chemical.strip().split(' ')[0])) for chemical in input_chemicals]


def get_reaction_output(reaction: str) -> str:
    return reaction[reaction.find('=') + 3:].split(' ')[1]


def get_reaction_output_increment(reaction: str) -> int:
    return int(reaction[reaction.find('=') + 3:].split(' ')[0])


def get_wasted_chemicals(chemical: str, quantity: int, waste: Dict[str, int]) -> int:
    wasted_reused = quantity if waste.get(chemical) >= quantity else waste.get(chemical)
    waste[chemical] = waste.get(chemical) - quantity if waste.get(chemical) > quantity else 0
    return wasted_reused


def get_amount_of_ores(chemical: str, quantity: int, waste: Dict[str, int]) -> int:
    ores = 0
    if chemical != 'ORE':
        quantity -= get_wasted_chemicals(chemical, quantity, waste)
        increment = increments.get(chemical)
        waste[chemical] += 0 if not quantity % increment else increment - (quantity % increment)
        input_chemicals = reactions.get(chemical)

        for input_chemical in input_chemicals:
            ores += get_amount_of_ores(input_chemical[0], input_chemical[1] * ceil(quantity / increment), waste)
    else:
        ores = quantity
    return ores


def get_amount_of_fuel(amount: int, waste: Dict[str, int]) -> int:
    mean = get_amount_of_ores('FUEL', 1, waste.copy())
    fuels = amount / mean
    i = 10

    while fuels != amount / (get_amount_of_ores('FUEL', i, waste.copy()) / i):
        mean = (get_amount_of_ores('FUEL', i, waste.copy()) / i)
        fuels = amount / mean
        i *= 10

    return int(amount / mean)


def part_1(filename: str) -> int:
    waste = dict()
    with open(filename) as file:
        for line in file.read().split('\n'):
            reactions[get_reaction_output(line)] = get_reaction_inputs(line)
            increments[get_reaction_output(line)] = get_reaction_output_increment(line)
            waste[get_reaction_output(line)] = 0

    return get_amount_of_ores('FUEL', 1, waste)


def part_2(filename: str) -> int:
    waste = dict()
    with open(filename) as file:
        for line in file.read().split('\n'):
            reactions[get_reaction_output(line)] = get_reaction_inputs(line)
            increments[get_reaction_output(line)] = get_reaction_output_increment(line)
            waste[get_reaction_output(line)] = 0

    return get_amount_of_fuel(1000000000000, waste)


print(f"Day 14 (Part 1) - Answer: {part_1('input.txt')}")
print(f"Day 14 (Part 2) - Answer: {part_2('input.txt')}")
