import matplotlib.pyplot as plt
from utils import read_input, pprint, config, orthogonal_shift
from pathlib import Path


testing = False
config['verbose'] = True
current_file = "day_12"
data_path = Path(f'./data/{current_file}/input.txt')

if not testing:
    data = read_input(data_path)
else:
    data = '''
RRRRIICCFF
RRRRIICCCF
VVRRRCCFFF
VVRCCCJFFF
VVVVCJJCFE
VVIVCCJJEE
VVIIICJJEE
MIIIIIJJEE
MIIISIJEEE
MMMISSJEEE
'''

    data = '''
KKKKKKKKKKKKKKKK
AAKKKKKFKKKKKKKK
AAAKKFFFKKKKKKKK
AAKKKKFFKKKKKKKK
AAKKKFFKKKKKKKKK
AAKKKFFKFFFKKKKK
FKKKKKKFFFKKKKKK
FKKKKKKFIFKKKKKK
KKKKKKKFEEKKKKKK
KKKKKEEEEEEKKKKK
KKKKEEEEEKKKKKKK
    '''

grid = {(i, j): v for i, d in enumerate(
    data.split()) if d for j, v in enumerate(d)}


border_shift = {
    'U': [(-.5, -.5), (-.5, .5)],
    'D': [(.5, .5), (.5, -.5)],
    'L': [(.5, -.5), (-.5, -.5)],
    'R': [(-.5, .5), (.5, .5)],
}


def print_borders(borders):
    for b in borders:
        plt.plot([b[0][0], b[1][0]], [b[0][1], b[1][1]])
        # break


def find_region(pos, letter, grid):
    region = set([pos])
    visit = set([pos])

    borders = []
    while len(visit) > 0:
        (x, y) = visit.pop()

        for dir, (shift_x, shift_y) in orthogonal_shift.items():
            # break
            (nx, ny) = (x+shift_x, y+shift_y)

            neighbour_in_region = (nx, ny) in grid and grid[(nx, ny)] == letter
            if (nx, ny) not in region:
                if neighbour_in_region:
                    visit.add((nx, ny))
                else:
                    [(b1r, b1c), (b2r, b2c)] = border_shift[dir]
                    s = (x+b1r, y+b1c)
                    u = (x+b2r, y+b2c)
                    p = (s, u)  # if dir in ['U', 'L'] else (u,s)
                    borders.append(p)
                    # perimeter += 1

        # if len(t) > 0:
        #     pprint((x, y), '-', len(t), 'borders:', t)

        region.add((x, y))

    return (len(borders), len(region), region, borders)


def map_borders(borders):
    border_map = {s: (e, (s[0]-e[0], s[1]-e[1])) for (s, e) in borders}
    return border_map


def find_loop(borders):
    border_map = map_borders(borders)
    b = borders[0]
    p, e = b
    visited = {
        p: e
    }
    while e not in visited:
        ne, d = border_map[e]
        visited[e] = ne
        e = ne

    ne = visited[e]
    loop = [(e, ne)]
    while ne != e:
        p = visited[ne]
        loop.append((ne, p))
        ne = p

    for b in loop:
        borders.pop(borders.index(b))

    return loop, borders


def loop_length(loop):
    loop_map = map_borders(loop)
    p0 = next(iter(loop_map))
    (e, d0) = loop_map[p0]
    d = d0
    nb_borders = 1
    # visited = 0
    while e != p0:
        # print(e, d)
        # visited += 1
        # print('visited', visited, '/', len(border_map))
        (ne, nd) = loop_map[e]

        if nd != d:
            nb_borders += 1
        e = ne
        d = nd
    if d == d0:
        nb_borders -= 1
    return nb_borders


def collapse_borders(borders):
    total_loop = 0
    while len(borders) > 0:
        [loop, borders] = find_loop(borders)
        total_loop += loop_length(loop)

    return total_loop


sol = 0
sol2 = 0
while grid.keys():
    pos = next(iter(grid))
    letter = grid[pos]

    (perimeter, area, region, borders) = find_region(pos, letter, grid)
    sol += perimeter*area

    nb_borders = collapse_borders(borders)

    sol2 += nb_borders*area

    for pos in region:
        del grid[pos]


solution = sol
print(f'Part 1 - solution: {solution}')

# Part 2

solution = sol2
print(f'Part 2 - solution: {solution}')
