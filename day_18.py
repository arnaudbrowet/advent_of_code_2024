from utils import read_input, pprint, config
from pathlib import Path
import heapq
from utils import orthogonal_shift, is_valid_grid_index

testing = True
config['verbose'] = True
current_file = "day_18"
data_path = Path(f'./data/{current_file}/input.txt')

if not testing:
    data = read_input(data_path)
else:
    data = '''
5,4
4,2
4,5
3,0
2,1
6,3
2,4
1,5
0,6
3,3
2,6
5,1
1,2
5,5
2,5
6,5
1,4
0,4
6,4
1,1
6,1
1,0
0,5
1,6
2,0
'''

positions = [tuple(map(int, reversed(p.split(','))))
             for p in data.split('\n') if p]

grid_size = 70
bytes = 1024
if testing:
    bytes = 12
    grid_size = 6

falled = positions[:bytes]

visited = {}
to_visit = []


def print_grid(pounds):
    for i in range(grid_size+1):
        l = ''
        for j in range(grid_size+1):
            if (i, j) in pounds:
                l += '#'
            else:
                l += '.'

        print(l)


# print_grid(falled)
heapq.heappush(to_visit, (0, (0, 0)))
w = None
found = False
while not found:
    weight, pos = heapq.heappop(to_visit)
    # print(weight, pos)
    if (pos in visited):
        continue

    visited[pos] = weight

    for shift in orthogonal_shift.values():

        np_x, np_y = pos[0] + shift[0], pos[1] + shift[1]
        np = np_x, np_y
        # print(np)
        if np == (grid_size, grid_size):
            w = weight+1
            found = True
            break

        if is_valid_grid_index(np_x, grid_size+1, np_y, grid_size+1) and np not in falled and np not in visited:
            # print('adding',np)
            heapq.heappush(to_visit, (weight+1, np))

    # print(to_visit)
solution = w
print(f'Part 1 - solution: {solution}')

# Part 2

solution = 0
print(f'Part 2 - solution: {solution}')
