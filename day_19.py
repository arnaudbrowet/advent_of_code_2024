from utils import read_input, pprint, config
from pathlib import Path


testing = False
config['verbose'] = True
current_file = "day_19"
data_path = Path(f'./data/{current_file}/input.txt')

if not testing:
    data = read_input(data_path)
else:
    data = '''
r, wr, b, g, bwu, rb, gb, br

brwrr
bggr
gbbr
rrbgbr
ubwu
bwurrg
brgr
bbrgwb
'''

towel_list, pattern_list = data.split('\n\n')
towels = [t.strip() for t in towel_list.split(',') if t]
patterns = pattern_list.split()

found = {}


def find_towels(pattern: str) -> int:
    if pattern in found:
        return found[pattern]

    valid_towels = [towel for towel in towels if pattern.startswith(towel)]
    if len(valid_towels) == 0:
        found[pattern] = 0
        return found[pattern]

    s = 0
    for towel in valid_towels:
        new_pattern = pattern[len(towel):]
        if len(new_pattern) == 0:
            # found[pattern] = 1
            s += 1
        else:
            sub = find_towels(new_pattern)
            # found[pattern] = sub
            s += sub

    found[pattern] = s
    return found[pattern]


solvable = [find_towels(t) for t in patterns]
s = sum([s > 0 for s in solvable])

solution = s
print(f'Part 1 - solution: {solution}')

# Part 2
s = sum(solvable)
solution = s
print(f'Part 2 - solution: {solution}')
