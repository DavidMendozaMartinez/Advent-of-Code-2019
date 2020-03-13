from typing import List


def restore_program(integers: List[int], noun: int, verb: int) -> List[int]:
    integers[1] = noun
    integers[2] = verb
    return integers


def run_program(integers: List[int]) -> List[int]:
    pointer = 0
    op_code = integers[pointer]

    while op_code != 99:
        input_1 = integers[integers[pointer + 1]]
        input_2 = integers[integers[pointer + 2]]
        output_position = integers[pointer + 3]

        if op_code == 1:
            integers[output_position] = input_1 + input_2
        elif op_code == 2:
            integers[output_position] = input_1 * input_2

        pointer += 4
        op_code = integers[pointer]

    return integers


def part_1(filename: str) -> int:
    with open(filename) as file:
        integers = [int(i) for i in file.read().split(',')]
        restored_integers = restore_program(integers.copy(), 12, 2)
        final_integers = run_program(restored_integers)

    return final_integers[0]


def part_2(filename: str) -> int:
    with open(filename) as file:
        integers = [int(i) for i in file.read().split(',')]
        nouns = [i for i in range(100)]
        verbs = [i for i in range(100)]

        for noun in nouns:
            for verb in verbs:
                restored_integers = restore_program(integers.copy(), noun, verb)
                final_integers = run_program(restored_integers)

                if final_integers[0] == 19690720:
                    break
            else:
                continue
            break

    return 100 * noun + verb


print(f"Day 2 (Part 1) - Answer: {part_1('input.txt')}")
print(f"Day 2 (Part 2) - Answer: {part_2('input.txt')}")
