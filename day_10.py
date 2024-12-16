from utils import read_input, pprint, config
from pathlib import Path


testing = False
config['verbose'] = True
current_file = "day_10"
data_path = Path(f'./data/{current_file}/input.txt')

if not testing:
    data = read_input(data_path)
else:
    data = '''
89010123
78121874
87430965
96549874
45678903
32019012
01329801
10456732
'''

grid = [[int(k) for k in d] for d in data.split() if d]
rows = len(grid)
cols = len(grid[0])


def is_valid(row, col):
    return row >= 0 and row < rows and col >= 0 and col < cols


def find_paths(row, col, grid):
    path = {(row, col, 0)}
    explored = set()
    found = set()
    while len(path) > 0:
        (r, c, h) = path.pop()

        for [sr, sc] in [[-1, 0], [1, 0], [0, -1], [0, 1]]:
            (nr, nc) = (r+sr, c+sc)
            if is_valid(nr, nc):
                nh = grid[nr][nc]
                if nh == h+1:
                    if (nr, nc, nh) in explored:
                        continue
                    explored.add((nr, nc, nh))
                    if nh == 9:
                        found.add((nr, nc))
                    else:
                        path.add((nr, nc, nh))

    return len(found)


paths = {}
for row in range(rows):
    for col in range(cols):
        if grid[row][col] == 0:
            paths[(row, col)] = find_paths(row, col, grid)

solution = sum(paths.values())
print(f'Part 1 - solution: {solution}')

# Part 2


def find_ratings(row, col, grid):
    path = [(row, col, 0)]
    # explored = set()
    found = []
    while len(path) > 0:
        (r, c, h) = path.pop()

        for [sr, sc] in [[-1, 0], [1, 0], [0, -1], [0, 1]]:
            (nr, nc) = (r+sr, c+sc)
            if is_valid(nr, nc):
                nh = grid[nr][nc]
                if nh == h+1:
                    # explored.add((nr, nc, nh))
                    if nh == 9:
                        found.append((nr, nc))
                    else:
                        path.append((nr, nc, nh))

    return len(found)


ratings = {}
for row in range(rows):
    for col in range(cols):
        if grid[row][col] == 0:
            ratings[(row, col)] = find_ratings(row, col, grid)

solution = sum(ratings.values())
print(f'Part 2 - solution: {solution}')
