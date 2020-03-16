from itertools import permutations
from typing import List, Tuple

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


def input_operation(input_value: int, positions: List[int], integers: List[int], pointer: int) -> int:
    integers[positions[0]] = input_value
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


def run_program(pointer: int, integers: List[int], inputs: List[int]) -> Tuple[int, List[int], List[int], list, bool]:
    outputs = []

    instruction = str(integers[pointer])
    op_code = int(instruction[-2:])

    while op_code != 99 and (op_code != 3 or inputs):
        values = get_values(instruction, op_structure.get(op_code)[0], integers, pointer)
        positions = get_positions(op_structure.get(op_code)[0], op_structure.get(op_code)[1], integers, pointer)

        op_functions = {
            1: lambda: addition_operation(values, positions, integers, pointer),
            2: lambda: multiplication_operation(values, positions, integers, pointer),
            3: lambda: input_operation(inputs.pop(0), positions, integers, pointer),
            4: lambda: output_operation(outputs, values, pointer),
            5: lambda: jump_if_true_operation(values, pointer),
            6: lambda: jump_if_false_operation(values, pointer),
            7: lambda: less_than_operation(values, positions, integers, pointer),
            8: lambda: equals_operation(values, positions, integers, pointer)
        }

        pointer = op_functions.get(op_code)()
        instruction = str(integers[pointer])
        op_code = int(instruction[-2:])

    if any(outputs[:-1]):
        print('Error - Non-zero outputs')

    return pointer, integers, inputs, outputs, op_code != 99


def get_max_thruster_signal(integers: List[int]) -> int:
    thruster_signals = []

    for phase_setting_sequence in permutations([0, 1, 2, 3, 4], 5):
        input_signal = 0
        output_signals = []

        for phase_setting in phase_setting_sequence:
            output_signals.append(run_program(0, integers.copy(), [phase_setting, input_signal])[3][-1])
            input_signal = output_signals[-1]
        thruster_signals.append(output_signals[-1])

    return max(thruster_signals)


def get_max_thruster_signal_with_feedback(integers: List[int]) -> int:
    thruster_signals = []

    for phase_setting_sequence in permutations([5, 6, 7, 8, 9], 5):
        states = dict()
        input_signal = 0
        output_signals = []

        for phase_setting in [5, 6, 7, 8, 9]:
            states[phase_setting] = (0, integers.copy(), [phase_setting], [], True)

        while any([state[4] for state in states.values()]):
            for phase_setting in phase_setting_sequence:
                states.get(phase_setting)[2].append(input_signal)
                states[phase_setting] = run_program(states.get(phase_setting)[0], states.get(phase_setting)[1],
                                                    states.get(phase_setting)[2])
                output_signals.append(states.get(phase_setting)[3][-1])
                input_signal = output_signals[-1]

        thruster_signals.append(output_signals[-1])

    return max(thruster_signals)


def part_1(filename: str) -> int:
    with open(filename) as file:
        integers = [int(i) for i in file.read().split(',')]
        return get_max_thruster_signal(integers)


def part_2(filename: str) -> int:
    with open(filename) as file:
        integers = [int(i) for i in file.read().split(',')]
        return get_max_thruster_signal_with_feedback(integers)


print(f"Day 7 (Part 1) - Answer: {part_1('input.txt')}")
print(f"Day 7 (Part 2) - Answer: {part_2('input.txt')}")
