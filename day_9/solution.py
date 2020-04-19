from typing import List, Tuple

TEST_MODE = 1
SENSOR_BOOST_MODE = 2

op_structure = {1: (2, 1), 2: (2, 1), 3: (0, 1), 4: (1, 0), 5: (2, 0), 6: (2, 0), 7: (2, 1), 8: (2, 1), 9: (1, 0)}


def get_values(instruction: str, operation_values: int, integers: List[int], pointer: int,
               relative_base: int) -> List[int]:
    values = []

    for i in range(1, operation_values + 1):
        mode_parameter = int(instruction[-(2 + i)]) if len(instruction) > (i + 1) else 0

        if mode_parameter == 0:
            check_memory(integers, [integers[pointer + i]])
            values.append(integers[integers[pointer + i]])
        elif mode_parameter == 1:
            values.append(integers[pointer + i])
        elif mode_parameter == 2:
            check_memory(integers, [integers[pointer + i] + relative_base])
            values.append(integers[integers[pointer + i] + relative_base])

    return values


def get_positions(instruction: str, operation_values: int, operation_positions: int, integers: List[int], pointer: int,
                  relative_base: int) -> List[int]:
    positions = []

    for i in range(operation_values + 1, operation_values + operation_positions + 1):
        mode_parameter = int(instruction[-(2 + i)]) if len(instruction) > (i + 1) else 0

        if mode_parameter == 0:
            check_memory(integers, [integers[pointer + i]])
            positions.append(integers[pointer + i])
        elif mode_parameter == 2:
            check_memory(integers, [integers[pointer + i] + relative_base])
            positions.append(integers[pointer + i] + relative_base)

    return positions


def addition_operation(values: List[int], positions: List[int], integers: List[int]):
    integers[positions[0]] = values[0] + values[1]


def multiplication_operation(values: List[int], positions: List[int], integers: List[int]):
    integers[positions[0]] = values[0] * values[1]


def input_operation(input_value: int, positions: List[int], integers: List[int]):
    integers[positions[0]] = input_value


def output_operation(output_log: List[int], values: List[int]):
    diagnostic_code = values[0]
    output_log.append(diagnostic_code)


def jump_if_true_operation(values: List[int], pointer: int) -> int:
    return values[1] if values[0] else pointer + (sum(op_structure[5]) + 1)


def jump_if_false_operation(values: List[int], pointer: int) -> int:
    return values[1] if not values[0] else pointer + (sum(op_structure[6]) + 1)


def less_than_operation(values: List[int], positions: List[int], integers: List[int]):
    integers[positions[0]] = int(values[0] < values[1])


def equals_operation(values: List[int], positions: List[int], integers: List[int]):
    integers[positions[0]] = int(values[0] == values[1])


def adjusts_relative_base(relative_base: int, values: List[int]) -> int:
    return relative_base + values[0]


def update_int_code(op_code: int, integers: List[int], inputs: List[int], outputs: List[int], values: List[int],
                    positions: List[int]):
    int_code_operations = {
        1: lambda: addition_operation(values, positions, integers),
        2: lambda: multiplication_operation(values, positions, integers),
        3: lambda: input_operation(inputs.pop(0), positions, integers),
        4: lambda: output_operation(outputs, values),
        7: lambda: less_than_operation(values, positions, integers),
        8: lambda: equals_operation(values, positions, integers),
    }
    int_code_operations.get(op_code)() if op_code in int_code_operations else None


def update_pointer(op_code: int, pointer: int, values: List[int]) -> int:
    pointer_op = {
        5: lambda: jump_if_true_operation(values, pointer),
        6: lambda: jump_if_false_operation(values, pointer),
    }
    return pointer_op.get(op_code)() if op_code in pointer_op else pointer + sum(op_structure[op_code]) + 1


def update_relative_base(op_code: int, relative_base: int, values: List[int]) -> int:
    relative_base_op = {
        9: lambda: adjusts_relative_base(relative_base, values)
    }
    return relative_base_op.get(op_code)() if op_code in relative_base_op else relative_base


def check_memory(integers: List[int], positions: List[int]):
    for position in positions:
        if position > len(integers) - 1:
            increase_memory(integers, position)


def increase_memory(integers: List[int], required_position: int):
    integers += [0 for _ in range(required_position - len(integers) + 1)]


def run_program(pointer: int, relative_base: int, integers: List[int], inputs: List[int]) \
        -> Tuple[int, int, List[int], List[int], List[int], bool]:
    outputs = []

    instruction = str(integers[pointer])
    op_code = int(instruction[-2:])

    while op_code != 99 and (op_code != 3 or inputs):
        values = get_values(instruction, op_structure.get(op_code)[0], integers, pointer, relative_base)
        positions = get_positions(instruction, op_structure.get(op_code)[0], op_structure.get(op_code)[1], integers,
                                  pointer, relative_base)

        update_int_code(op_code, integers, inputs, outputs, values, positions)
        pointer = update_pointer(op_code, pointer, values)
        relative_base = update_relative_base(op_code, relative_base, values)

        instruction = str(integers[pointer])
        op_code = int(instruction[-2:])

    return pointer, relative_base, integers, inputs, outputs, op_code != 99


def part_1(filename: str) -> int:
    with open(filename) as file:
        integers = [int(i) for i in file.read().split(',')]
        diagnostic_code = run_program(0, 0, integers, [TEST_MODE])[4][-1]

    return diagnostic_code


def part_2(filename: str) -> int:
    with open(filename) as file:
        integers = [int(i) for i in file.read().split(',')]
        diagnostic_code = run_program(0, 0, integers, [SENSOR_BOOST_MODE])[4][-1]

    return diagnostic_code


if __name__ == '__main__':
    print(f"Day 9 (Part 1) - Answer: {part_1('input.txt')}")
    print(f"Day 9 (Part 2) - Answer: {part_2('input.txt')}")
