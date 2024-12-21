from utils import read_input, pprint, config
from pathlib import Path
import heapq

testing = False
config['verbose'] = False
current_file = "day_16"
data_path = Path(f'./data/{current_file}/input.txt')

if not testing:
    data = read_input(data_path)
else:
    data = '''
###############
#.......#....E#
#.#.###.#.###.#
#.....#.#...#.#
#.###.#####.#.#
#.#.#.......#.#
#.#.#####.###.#
#...........#.#
###.#.#####.#.#
#...#.....#.#.#
#.#.#.###.#.#.#
#.....#...#.#.#
#.###.#.#.#.#.#
#S..#.....#...#
###############
'''
    data = '''
#################
#...#...#...#..E#
#.#.#.#.#.#.#.#.#
#.#.#.#...#...#.#
#.#.#.#.###.#.#.#
#...#.#.#.....#.#
#.#.#.#.#.#####.#
#.#...#.#.#.....#
#.#.#####.#.###.#
#.#.#.......#...#
#.#.###.#####.###
#.#.#...#.....#.#
#.#.#.#####.###.#
#.#.#.........#.#
#.#.#.#########.#
#S#.............#
#################
# '''

move_map = {
    '<': (0, -1),
    'v': (1, 0),
    '^': (-1, 0),
    '>': (0, 1),
}
turns = {
    'left': {
        '<': 'v',
        'v': '>',
        '^': '<',
        '>': '^',
    },
    'right': {
        '<': '^',
        'v': '<',
        '^': '>',
        '>': 'v',
    }
}
grid = {}
dir = '>'


def turn(dir, right=False):
    turn_map = turns['right'] if right else turns['left']
    return turn_map[dir]


for r, row in enumerate(data.split()):
    if not row:
        continue
    for c, col in enumerate(list(row)):
        if col == 'S':
            startPos = (r, c)
        if col == 'E':
            endPos = (r, c)
        grid[(r, c)] = col


def get_new_pos(pos, dir):
    shift = move_map[dir]
    new_pos = pos[0] + shift[0], pos[1]+shift[1]
    return new_pos


def follow_path(path, dir, weight, grid):

    pos = path[-1]
    new_pos = get_new_pos(pos, dir)

    if grid[new_pos] != '.':
        return False

    new_path = [p for p in path] + [new_pos]
    weight += 1

    while True:
        if new_pos == endPos:
            return new_path, dir, weight

        # test neighbours
        new_nghb = []
        add_pos_dir = get_new_pos(new_pos, dir)
        if add_pos_dir not in new_path and grid[add_pos_dir] != '#':
            new_nghb.append((add_pos_dir, 1, dir))

        left = turn(dir)
        add_pos_left = get_new_pos(new_pos, left)
        if add_pos_left not in new_path and grid[add_pos_left] != '#':
            new_nghb.append((add_pos_left, 1000+1, left))

        right = turn(dir, True)
        add_pos_right = get_new_pos(new_pos, right)
        if add_pos_right not in new_path and grid[add_pos_right] != '#':
            new_nghb.append((add_pos_right, 1000+1, right))

        if len(new_nghb) == 0:
            # dead end
            pprint(new_pos, "=> dead end")
            return False
        if len(new_nghb) > 1:
            pprint(new_pos, "=> choice")
            return new_path, dir, weight

        new_pos, add_weight, dir = new_nghb[0]
        weight += add_weight
        new_path += [new_pos]


paths = [(0, [startPos], dir)]
heapq.heapify(paths)

found = False
found_weight = None
found_paths = []
visited = {}

while found_weight is None or weight <= found_weight:
    weight, path, dir = heapq.heappop(paths)

    pos = path[-1]

    if pos == endPos:
        # pprint(path, weight)
        if found_weight is None:
            found_weight = weight
            found_paths.append([p for p in path])
        elif weight == found_weight:
            found_paths.append([p for p in path])

        continue
    if (pos, dir) in visited and weight > visited[(pos, dir)]:
        continue

    pprint(weight, path, dir)
    res = follow_path(path, dir, weight, grid)
    if res:
        new_path, new_dir, new_weight = res
        visited[(pos, dir)] = new_weight
        heapq.heappush(paths, (new_weight, new_path, new_dir))

    left = turn(dir)
    res = follow_path(path, left, weight+1000, grid)
    if res:
        new_path, new_dir, new_weight = res
        visited[(pos, dir)] = new_weight
        heapq.heappush(paths, (new_weight, new_path, new_dir))

    right = turn(dir, True)
    res = follow_path(path, right, weight+1000, grid)
    if res:
        new_path, new_dir, new_weight = res

        visited[(pos, dir)] = new_weight
        heapq.heappush(paths, (new_weight, new_path, new_dir))


tiles = set()
[tiles.add(tile) for p in found_paths for tile in p]

solution = found_weight
print(f'Part 1 - solution: {solution}')

# Part 2
solution = len(tiles)
print(f'Part 2 - solution: {solution}')
