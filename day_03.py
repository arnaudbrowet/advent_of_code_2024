from utils import read_input
from pathlib import Path
import re

data = read_input(Path('./data/day_03/input.txt'))

matches = re.findall("mul\(([\d]{1,3}),([\d]{1,3})\)", data)

mul = [int(l[0])*int(l[1])for l in matches]
solution = sum(mul)

print(f'Part 1 - solution: {solution}')


matches = re.findall("mul\([\d]{1,3},[\d]{1,3}\)|do\(\)|don't\(\)", data)

do = True
s = 0
for l in matches:
    if do:
        if l == 'don\'t()':
            do = False
        elif l.startswith('mul'):
            f = re.match('mul\(([\d]{1,3}),([\d]{1,3})\)', l).groups(0)
            s += int(f[0])*int(f[1])
    else:
        if l == 'do()':
            do = True

solution = s

print(f'Part 2 - solution: {solution}')
