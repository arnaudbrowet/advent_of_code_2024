from utils import read_input
from pathlib import Path

data = read_input(Path('./data/day_02/input.txt'))
# data = '''
# 7 6 4 2 1
# 1 2 7 8 9
# 9 7 6 2 1
# 1 3 2 4 5
# 8 6 4 4 1
# 1 3 6 7 9
# '''

lines = [l.split() for l in data.split('\n') if l]

lines = [[int(k) for k in l]for l in lines]

nb_valid_lines = 0
min_shift = 1
max_shift = 3


def is_valid_line(line):

    dir = line[1] - line[0]
    if (abs(dir) < min_shift or abs(dir) > max_shift):
        return 0

    valid = True
    i = 2
    v = line[1]
    while valid and (i < len(line)):
        new = line[i]
        diff = new-v

        if (diff*dir < 0 or abs(diff) < min_shift or abs(diff) > max_shift):
            valid = False
            break

        v = new
        i += 1

    if (valid):
        return None
    else:
        return i-1


for l in lines:
    invalid_index = is_valid_line(l)

    if invalid_index is None:
        nb_valid_lines += 1


print(f'Part 1 - solution: {nb_valid_lines}')

# Part 2
nb_valid_lines = 0
for l in lines:
    invalid_index = is_valid_line(l)

    if invalid_index is None:
        nb_valid_lines += 1
        continue

    if (invalid_index == 1):
        l_t = l[1:]
        slice_valid = is_valid_line(l_t)
        if slice_valid is None:
            nb_valid_lines += 1
            continue

    l_t = l[0:invalid_index]+l[invalid_index+1:]
    slice_valid = is_valid_line(l_t)
    if slice_valid is None:
        nb_valid_lines += 1
        continue

    l_t = l[0:invalid_index+1]+l[invalid_index+2:]
    slice_valid = is_valid_line(l_t)
    if slice_valid is None:
        nb_valid_lines += 1
        continue


print(f'Part 2 - solution: {nb_valid_lines}')
