from utils import read_input, pprint, config
from pathlib import Path


testing = False
config['verbose']=False
current_file = "day_06"
data_path = Path(f'./data/{current_file}/input.txt')

if not testing:
    data = read_input(data_path)
else:
    data = '''
....#.....
.........#
..........
..#.......
.......#..
..........
.#..^.....
........#.
#.........
......#...
'''

# parse the map
grid = [list(d) for d in data.split()]
turns= {
    'U':'R',
    'R':'D',
    'D':'L',
    'L': 'U'
}
move={
    'U':[-1, 0],
    'R':[0, 1],
    'D':[1, 0],
    'L':[0, -1],
}
rows = len(grid)
cols=len(grid[0])

[start_row, start_col] = location = [(row, g.index('^')) for row, g in enumerate(grid) if '^' in g][0]

direction = 'U'
visited = [(*location, direction)]

while direction is not None:
    shift = move[direction]
    [new_row, new_col] = new_location = [location[0] + shift[0], location[1] + shift[1]]

    if (new_row <0 or new_row >= rows or new_col<0 or new_col>=cols):
        direction=None
        continue

    if grid[new_row][new_col] == '#':
        direction=turns[direction]
        if (*location,direction) not in visited: visited.append((*location, direction))
        continue

    location = (new_row, new_col)
    if (*location,direction) not in visited: visited.append((*location, direction))

unique_positions = set([(r,c) for [r, c, _] in visited])
solution = len(unique_positions)
print(f'Part 1 - solution: {solution}')

# Part 2
def detect_loop(altered, row, col, direction, previously_visited):
    location = [row, col]
    # direction = start_direction

    visited = set(previously_visited)

    # nb_loops = 0
    while True:
        # nb_loops+=1
        # if (nb_loops>1000):
        #     raise Exception('too many loops')
        
        # print(location, direction)
        if len(visited)>1 and (*location, direction) in visited:
            return True
        visited.add((*location, direction))
        # visited.append((*location, direction))

        shift = move[direction]
        [new_row, new_col] = new_location = (location[0] + shift[0], location[1] + shift[1])
        if (new_row <0 or new_row >= rows or new_col<0 or new_col>=cols):
            # print('going out')
            return False

        if altered[new_row][new_col] == '#':
            # print('turning')
            direction=turns[direction]
            continue
    
        
        # print('moving')
        location = new_location
        


nb_loops = 0
test = set()

## running only position following the path
for v, [row, col, direction] in enumerate(visited[:-1]):
    pprint(f"{v+1}/{len(visited)-1}")
    previously_visited = visited[:v]

    shift = move[direction]
    [next_row, next_col] = (row + shift[0], col + shift[1])

    if grid[next_row][next_col] != '.':
        # not changing the grid
        continue

    if (next_row, next_col) in test:
        # already test - should block the path earlier
        continue

    test.add((next_row, next_col))

    grid[next_row][next_col] = '#'
    is_looping = detect_loop(grid, row, col, direction, previously_visited)
    if is_looping:
        # pprint((start_row, start_col), 'is looping')
        nb_loops+=1

    # testing - start always on the initial position
    # is_looping = detect_loop(grid, start_row, start_col, 'U', [])
    # if is_looping:
    #     # pprint((next_row, next_col), 'is actually looping')
    #     nb_true_loops+=1

    grid[next_row][next_col] = '.'

## Testing - running all possible location
# for row in range(rows):
#     for col in range(cols):
#         # pprint('row/col:', row, col)
#         if grid[row][col]!='.':
#             # pprint('skipped')
#             continue
        
#         grid[row][col] = '#'

#         is_looping = detect_loop(grid, start_row, start_col, 'U', [])

#         if is_looping:
#             pprint((row, col), 'is looping')
#             nb_loops+=1
#         grid[row][col] = '.'
        

solution = nb_loops
print(f'Part 2 - solution: {solution}')
