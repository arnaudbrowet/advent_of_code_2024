from utils import read_input, pprint, config
from pathlib import Path


testing = False
config['verbose'] = True
current_file = "day_"
data_path = Path(f'./data/{current_file}/input.txt')

if not testing:
    data = read_input(data_path)
else:
    data = '''
125 17
'''

line = [int(d) for d in data.split() if d]


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
        str_value = f"{self.value}"
        if self.value == 0:
            self.value = 1
        elif len(str_value) % 2 == 0:
            mid = int(len(str_value)/2)
            self.value = int(str_value[0:mid])
            new_stone = stone(int(str_value[mid:]), current_next)
            self.next = new_stone
        else:
            self.value *= 2024

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

solution = 0
print(f'Part 2 - solution: {solution}')
