from typing import List

wide = 25
tall = 6
colors = {0: '█', 1: '▒'}


def get_layers(pixels: List[int]) -> List[List[int]]:
    return [pixels[i:i + wide * tall] for i in range(0, len(pixels), wide * tall)]


def get_layer_with_fewest_0_digits(layers: List[List[int]]) -> List[int]:
    return min(layers, key=lambda k: k.count(0))


def decode_image(layers: List[List[int]]) -> str:
    image = ''
    final_pixels = ['' for _ in range(wide * tall)]

    for layer in layers:
        for i in range(len(layer)):
            if not final_pixels[i] and layer[i] != 2:
                final_pixels[i] = colors.get(layer[i])

    for row in range(tall):
        image += ''.join(final_pixels[row * wide: (row * wide) + wide]) + '\n'
    return image


def part_1(filename: str) -> int:
    with open(filename) as file:
        pixels = [int(i) for i in file.read()]
        layer = get_layer_with_fewest_0_digits(get_layers(pixels))
        result = layer.count(1) * layer.count(2)
    return result


def part_2(filename: str) -> str:
    with open(filename) as file:
        pixels = [int(i) for i in file.read()]
        layers = get_layers(pixels)
        image = decode_image(layers)
    return image


print(f"Day 8 (Part 1) - Answer: {part_1('input.txt')}")
print(f"Day 8 (Part 2) - Answer:\n{part_2('input.txt')}")
