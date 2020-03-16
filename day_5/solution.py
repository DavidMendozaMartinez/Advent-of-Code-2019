from typing import List

op_structure = {1: (2, 1), 2: (2, 1), 3: (0, 1), 4: (1, 0), 5: (2, 0), 6: (2, 0), 7: (2, 1), 8: (2, 1)}


def get_values(instruction: str, operation_values: int, integers: List[int], pointer: int) -> List[int]:
    values = []

    for i in range(1, operation_values + 1):
        mode_parameter = int(instruction[-(2 + i)]) if len(instruction) > (i + 1) else 0

        if mode_parameter == 0:
            values.append(integers[integers[pointer + i]])
        elif mode_parameter == 1:
            values.append(integers[pointer + i])

    return values


def get_positions(operation_values: int, operation_positions: int, integers: List[int], pointer: int) -> List[int]:
    positions = []

    for i in range(operation_values + 1, operation_values + operation_positions + 1):
        positions.append(integers[pointer + i])

    return positions


def addition_operation(values: List[int], positions: List[int], integers: List[int], pointer: int) -> int:
    integers[positions[0]] = values[0] + values[1]
    pointer += (sum(op_structure[1]) + 1)
    return pointer


def multiplication_operation(values: List[int], positions: List[int], integers: List[int], pointer: int) -> int:
    integers[positions[0]] = values[0] * values[1]
    pointer += (sum(op_structure[2]) + 1)
    return pointer


def input_operation(system_id: int, positions: List[int], integers: List[int], pointer: int) -> int:
    integers[positions[0]] = int(system_id)
    pointer += (sum(op_structure[3]) + 1)
    return pointer


def output_operation(output_log: List[int], values: List[int], pointer: int) -> int:
    diagnostic_code = values[0]
    output_log.append(diagnostic_code)
    pointer += (sum(op_structure[4]) + 1)
    return pointer


def jump_if_true_operation(values: List[int], pointer: int) -> int:
    return values[1] if values[0] else pointer + (sum(op_structure[5]) + 1)


def jump_if_false_operation(values: List[int], pointer: int) -> int:
    return values[1] if not values[0] else pointer + (sum(op_structure[6]) + 1)


def less_than_operation(values: List[int], positions: List[int], integers: List[int], pointer: int) -> int:
    integers[positions[0]] = int(values[0] < values[1])
    pointer += (sum(op_structure[7]) + 1)
    return pointer


def equals_operation(values: List[int], positions: List[int], integers: List[int], pointer: int) -> int:
    integers[positions[0]] = int(values[0] == values[1])
    pointer += (sum(op_structure[8]) + 1)
    return pointer


def run_program(system_id: int, integers: List[int]) -> int:
    pointer = 0
    output_log = []

    instruction = str(integers[pointer])
    op_code = int(instruction[-2:])

    while op_code != 99:
        values = get_values(instruction, op_structure.get(op_code)[0], integers, pointer)
        positions = get_positions(op_structure.get(op_code)[0], op_structure.get(op_code)[1], integers, pointer)

        op_functions = {
            1: lambda: addition_operation(values, positions, integers, pointer),
            2: lambda: multiplication_operation(values, positions, integers, pointer),
            3: lambda: input_operation(system_id, positions, integers, pointer),
            4: lambda: output_operation(output_log, values, pointer),
            5: lambda: jump_if_true_operation(values, pointer),
            6: lambda: jump_if_false_operation(values, pointer),
            7: lambda: less_than_operation(values, positions, integers, pointer),
            8: lambda: equals_operation(values, positions, integers, pointer)
        }

        pointer = op_functions.get(op_code)()
        instruction = str(integers[pointer])
        op_code = int(instruction[-2:])

    if any(output_log[:-1]):
        print('Error - Non-zero outputs')

    return output_log[-1]


def part_1(filename: str) -> int:
    with open(filename) as file:
        integers = [int(i) for i in file.read().split(',')]
        diagnostic_code = run_program(1, integers)

    return diagnostic_code


def part_2(filename: str) -> int:
    with open(filename) as file:
        integers = [int(i) for i in file.read().split(',')]
        diagnostic_code = run_program(5, integers)

    return diagnostic_code


print(f"Day 5 (Part 1) - Answer: {part_1('input.txt')}")
print(f"Day 5 (Part 2) - Answer: {part_2('input.txt')}")
