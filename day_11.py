from utils import read_input, pprint, config
from pathlib import Path


testing = True
config['verbose'] = True
current_file = "day_11"
data_path = Path(f'./data/{current_file}/input.txt')

if not testing:
    data = read_input(data_path)
else:
    data = '''
125 17
'''

line = [int(d) for d in data.split() if d]


def split_stone(value):
    str_value = f"{value}"
    if value == 0:
        return [1]
    elif len(str_value) % 2 == 0:
        mid = int(len(str_value)/2)
        return [
            int(str_value[0:mid]),
            int(str_value[mid:]),
        ]
    else:
        return [value*2024]


class stone:
    def __init__(self, value, next_stone):
        self.value = value
        self.next = next_stone

    def __repr__(self):
        return f"Stone {self.value}"

    def __str__(self):
        return f"{self.value}"

    def blink(self):
        current_next = self.next

        values = split_stone(self.value)
        self.value = values[0]

        if len(values) > 1:
            new_stone = stone(values[1], current_next)
            self.next = new_stone

        return current_next


def print_stones(stone):
    v = [str(stone)]
    while stone.next:
        stone = stone.next
        v.append(str(stone))
    print(v)


def count_stones(s):
    nb = 0
    while s:
        nb += 1
        s = s.next
    return nb


current_stone = None
for v in reversed(line):
    current_stone = stone(v, current_stone)

nb_blinks = 25
starting_stone = current_stone
for step in range(nb_blinks):
    s = starting_stone
    while s is not None:
        s = s.blink()

    # if config['verbose']:
    #     print_stones(starting_stone)

solution = count_stones(starting_stone)
print(f'Part 1 - solution: {solution}')

# Part 2

stone_life = {}


def path_length(value, length):
    ex = stone_life.get((value, length), None)
    if ex:
        return ex

    if length == 0:
        stone_life[(value, length)] = 1
    else:
        values = split_stone(value)
        stone_life[(value, length)] = sum(
            [path_length(v, length-1) for v in values])

    return stone_life[(value, length)]


# part 1 bis
s = sum([path_length(d, 25) for d in line])
print(f'Part 1 bis - solution: {s}')
# nb_blinks = 75
# starting_stone = current_stone
# for step in range(nb_blinks):
#     print(f"{step}/{nb_blinks}")
#     s = starting_stone
#     while s is not None:
#         s = s.blink()


solution = sum([path_length(d, 75) for d in line])
print(f'Part 2 - solution: {solution}')
