from utils import read_input, pprint, config
from pathlib import Path


testing = False
config['verbose'] = False
current_file = "day_15"
data_path = Path(f'./data/{current_file}/input.txt')

if not testing:
    data = read_input(data_path)
else:
    data = '''
##########
#..O..O.O#
#......O.#
#.OO..O.O#
#..O@..O.#
#O#..O...#
#O..O..O.#
#.OO.O.OO#
#....O...#
##########

<vv>^<v^>v>^vv^v>v<>v^v<v<^vv<<<^><<><>>v<vvv<>^v^>^<<<><<v<<<v^vv^v>^
vvv<<^>^v^^><<>>><>^<<><^vv^^<>vvv<>><^^v>^>vv<>v<<<<v<^v>^<^^>>>^<v<v
><>vv>v^v^<>><>>>><^^>vv>v<^^^>>v^v^<^^>v^^>v^<^v>v<>>v^v^<v>v^^<^^vv<
<<v<^>>^^^^>>>v^<>vvv^><v<<<>^^^vv^<vvv>^>v<^^^^v<>^>vvvv><>>v^<<^^^^^
^><^><>>><>^^<<^^v>>><^<v>^<vv>>v>>>^v><>^v><<<<v>>v<v<v>vvv>^<><<>^><
^>><>^v<><^vvv<^^<><v<<<<<><^v<<<><<<^^<v<^^^><^>>^<v^><<<^>>^v<v^v<v^
>^>>^v>vv>^<<^v<>><<><<v<<v><>v<^vv<<<>^^v^>^^>>><<^v>>v^v><^^>>^<>vv^
<><^^>^^^<><vvvvv^v<v<<>^v<v>v<<^><<><<><<<^^<<<^<<>><<><^^^>^^<>^>v<>
^^>vv<^v^v<vv>^<><v<^v>^^^>>>^^vvv^>vvv<>>>^<^>>>>>^<<^v>^vvv<>^<><<v>
v^^>>><<^^<>>^v^<v^vv<>v^<<>^<^v^v><^<<<><<^<v><v<>vv>>v><v^<vv<>v^<<^
'''
#     data = '''
# #######
# #...#.#
# #.....#
# #..OO@#
# #..O..#
# #.....#
# #######

# <vv<<^^<<^^
# '''

[grid_string, move_string] = data.split('\n\n')


bot = None
grid = {}
sg = grid_string.split()
nbRows = len(sg)
nbCols = len(sg[0])
for row, r in enumerate(sg):
    if not r:
        continue
    for col, s in enumerate(r):
        pos = (row, col)
        if s == '@':
            bot = pos
        grid[pos] = s


def print_grid(grid):
    for r in range(nbRows):
        l = ''
        for c in range(nbCols):
            l += grid[(r, c)]
        pprint(l)


moves = ''.join(move_string.split('\n'))

move_map = {
    '<': (0, -1),
    'v': (1, 0),
    '^': (-1, 0),
    '>': (0, 1),
}


def move_block(grid, pos, shift):

    new_pos = pos[0] + shift[0], pos[1] + shift[1]
    sym = grid[pos]

    if grid[new_pos] == '#':
        return False, grid, pos

    if grid[new_pos] == '.':
        grid[new_pos] = sym
        grid[pos] = "."
        return True, grid, new_pos

    # new pos contains a o
    has_moved, grid, _ = move_block(grid, new_pos, shift)
    if has_moved:
        grid[new_pos] = sym
        grid[pos] = "."
        return True, grid, new_pos

    return False, grid, pos


for move in moves:
    # break
    shift = move_map[move]
    moved, grid, bot = move_block(grid, bot, shift)
    # pprint('move', move)
    # pprint_grid(grid)
    # pprint()

s = 0
for pos, sym in grid.items():
    if sym == "O":
        s += 100*pos[0]+pos[1]


solution = s
print(f'Part 1 - solution: {solution}')

# Part 2


class Box():
    def __init__(self, pos):
        self.left = pos
        self.right = (pos[0], pos[1]+1)

    def __str__(self):
        return f"{self.left}-{self.right}"

    def __repr__(self):
        return f"{self.left}-{self.right}"

    def new_pos(self, dir):
        shift = move_map[dir]
        new_left = self.left[0] + shift[0], self.left[1] + shift[1]
        new_right = self.right[0] + shift[0], self.right[1] + shift[1]
        return new_left, new_right

    def nghb(self, grid, dir):
        new_left, new_right = self.new_pos(dir)

        left_element = grid[new_left]
        right_element = grid[new_right]

        n = [
            False if left_element == "#" else None,
            False if right_element == "#" else None,
        ]
        if left_element not in ['.', '#']:
            n[0] = None if left_element == self else left_element
        if right_element not in ['.', '#']:
            n[1] = None if right_element == self else right_element

        return n

    def apply_move(self, grid, dir):
        new_left, new_right = self.new_pos(dir)

        grid[self.left] = '.'
        grid[self.right] = '.'
        grid[new_left] = self
        grid[new_right] = self
        self.left = new_left
        self.right = new_right

    def move(self, grid, dir):

        new_left, new_right = self.new_pos(dir)

        if grid[new_left] == '#' or grid[new_right] == '#':
            return False, grid

        if (
            grid[new_left] == '.' or grid[new_left] == self
        ) and (
            grid[new_right] == '.' or grid[new_right] == self
        ):
            self.apply_move(grid, dir)
            return True, grid
        else:
            # we hit another box
            nghb_levels = [set(self.nghb(grid, dir))]
            if False in nghb_levels:
                return False, grid

            pprint('level1', nghb_levels)
            # detect all neighbours
            while True:
                new_nghb = set()
                for n in nghb_levels[-1]:
                    if n is None:
                        continue
                    pprint('start_element', n)
                    cur = n.nghb(grid, dir)
                    pprint('Box', n, 'neighbours:')
                    pprint(cur)
                    if False in cur:
                        return False, grid

                    for c in cur:
                        new_nghb.add(c)

                if len(new_nghb) <= 0:
                    break
                nghb_levels.append(new_nghb)

            # no false returned => all can move
            while len(nghb_levels):
                level = nghb_levels.pop()
                for n in level:
                    if n is None:
                        continue
                    n.apply_move(grid, dir)

            self.apply_move(grid, dir)
            return True, grid


def move_bot(grid, pos, shift, dir):

    new_pos = pos[0] + shift[0], pos[1] + shift[1]
    sym = grid[pos]

    if grid[new_pos] == '#':
        return False, grid, pos

    if grid[new_pos] == '.':
        grid[new_pos] = sym
        grid[pos] = "."
        return True, grid, new_pos

    # new pos contains a box
    box = grid[new_pos]
    # self = box
    has_moved, grid = box.move(grid, dir)
    if has_moved:
        grid[new_pos] = sym
        grid[pos] = "."
        return True, grid, new_pos

    return False, grid, pos


def print_box_grid(grid):
    for r in range(nbRows):
        l = ''
        for c in range(nbCols):
            el = grid[(r, c)]
            if el in [".", "@", '#']:
                l += el
            else:
                # in a box
                if (r, c) == el.left:
                    l += '['
                else:
                    l += ']'
        pprint(l)


bot = None
grid = {}
sg = grid_string.split()
nbRows = len(sg)
nbCols = 2*len(sg[0])
allBoxes = []
for row, r in enumerate(sg):
    if not r:
        continue
    for col, s in enumerate(r):
        pos1 = (row, 2*col)
        pos2 = (row, 2*col+1)
        if s == '@':
            bot = pos1
            grid[pos1] = s
            grid[pos2] = '.'
        elif s == '.':
            grid[pos1] = s
            grid[pos2] = s
        elif s == '#':
            grid[pos1] = s
            grid[pos2] = s
        elif s == 'O':
            b = Box(pos1)
            grid[pos1] = b
            grid[pos2] = b
            allBoxes.append(b)
        else:
            print('** element', s)
            raise Exception('unknown grid element')


print_box_grid(grid)

for i, move in enumerate(moves):
    # if (i == 156):
    #     break
    shift = move_map[move]
    # pos=bot
    # dir=move
    pprint('move', i, ':', move)

    moved, grid, bot = move_bot(grid, bot, shift, move)

    print_box_grid(grid)
    pprint()

print_box_grid(grid)

s = 0
for b in allBoxes:
    s += 100*b.left[0] + b.left[1]


solution = s
print(f'Part 2 - solution: {solution}')
