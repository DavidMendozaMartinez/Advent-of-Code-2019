def contains_adjacent_digits(password: str) -> bool:
    return any([password[digit] == password[digit + 1] for digit in range(len(password) - 1)])


def contains_two_adjacent_digits(password: str) -> bool:
    return any([password[digit] != password[digit + 1] == password[digit + 2] != password[digit + 3]
                for digit in range(len(password) - 3)]) \
           or password[0] == password[1] and password[1] != password[2] \
           or password[-3] != password[-2] and password[-2] == password[-1]


def never_decrease(password: str) -> bool:
    return all([password[digit] <= password[digit + 1] for digit in range(len(password) - 1)])


def valid_part_1(password: str) -> bool:
    return len(str(password)) == 6 and contains_adjacent_digits(str(password)) and never_decrease(str(password))


def valid_part_2(password: str) -> bool:
    return len(str(password)) == 6 and contains_two_adjacent_digits(str(password)) and never_decrease(str(password))


def part_1(filename: str) -> int:
    with open(filename) as file:
        ranges = [int(number) for number in file.read().split('-')]

    return len([password for password in range(ranges[0], ranges[1] + 1) if valid_part_1("{:06d}".format(password))])


def part_2(filename: str) -> int:
    with open(filename) as file:
        ranges = [int(number) for number in file.read().split('-')]

    return len([password for password in range(ranges[0], ranges[1] + 1) if valid_part_2("{:06d}".format(password))])


print(f"Day 4 (Part 1) - Answer: {part_1('input.txt')}")
print(f"Day 4 (Part 2) - Answer: {part_2('input.txt')}")
