from utils import read_input
from pathlib import Path
from collections import Counter

data = read_input(Path('./data/day_01/input.txt'))

lines = [l.split() for l in data.split('\n') if l]

# Part 1
left = sorted([int(l[0])for l in lines])
right = sorted([int(l[1]) for l in lines])

diff = [abs(y-x) for x, y in zip(left, right)]

solution = sum(diff)
print(f'Part 1 - solution: {solution}')

# Part 2
# left_count = Counter(left)
right_count = Counter(right)

counts = [l*right_count[l] for l in left]
solution2 = sum(counts)
print(f'Part 2 - solution: {solution2}')
