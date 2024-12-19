from utils import read_input, pprint, config
from pathlib import Path
import re

testing = False
config['verbose'] = True
current_file = "day_14"
data_path = Path(f'./data/{current_file}/input.txt')

if not testing:
    cols = 101
    rows = 103
    data = read_input(data_path)
else:
    cols = 11
    rows = 7
    data = '''
p=0,4 v=3,-3
p=6,3 v=-1,-3
p=10,3 v=-1,2
p=2,0 v=2,-1
p=0,0 v=1,3
p=3,0 v=-2,-2
p=7,6 v=-1,-3
p=3,0 v=-1,-2
p=9,3 v=2,3
p=7,3 v=-1,2
p=2,4 v=2,-3
p=9,5 v=-3,-3
'''

robots = [[(int(v)) for v in re.search(
    r'p=(-{0,1}\d+),(-{0,1}\d+) v=(-{0,1}\d+),(-{0,1}\d+)', d).groups()] for d in data.split('\n') if d]


def move(p, v, step, rows, cols):
    end_pos = (p[0] + step*v[0]) % cols,  (p[1]+step*v[1]) % rows
    midRow = (rows-1)/2
    midCol = (cols-1)/2

    if end_pos[0] == midCol or end_pos[1] == midRow:
        return None

    # print(end_pos)
    return (end_pos[0] > midCol) + 2*(end_pos[1] > midRow)


end_positions = [move((px, py), (vx, vy), 100, rows, cols)
                 for px, py, vx, vy in robots]


quad = {
    0: 0,
    1: 0,
    2: 0,
    3: 0
}
for p in end_positions:
    if p is not None:
        quad[p] += 1


solution = quad[0]*quad[1]*quad[2]*quad[3]
print(f'Part 1 - solution: {solution}')

# Part 2


def print_robots(robots):
    pos = [(robot[0], robot[1]) for robot in robots]

    l = []
    for row in range(rows):
        line = ''
        for col in range(cols):
            if (col, row) in pos:
                line += '*'
            else:
                line += ' '
        print(line)
        # l.append(line)
        # if '*'*line_count in line:
        #     has_line = True

    # if has_line:
    #     [print(line) for line in l]
    #     print('\n--\n')
    # return has_line


def move_robots(robot): return (
    (robot[0]+robot[2]) % cols, (robot[1]+robot[3]) % rows, robot[2], robot[3])


def find_largest_cc(robot):
    pos = {(x, y) for x, y, _, _ in robot}

    cc = []
    while len(pos):
        # create a connected component
        p = pos.pop()
        to_visit = {p}
        cc.append({p})

        while len(to_visit):
            np = to_visit.pop()
            for r in range(-1, 2):
                for c in range(-1, 2):
                    ngbh = (np[0] + r, np[1]+c)
                    if ngbh in pos:
                        to_visit.add(ngbh)
                        cc[-1].add(ngbh)
                        pos.remove(ngbh)

    return max([
        len(c) for c in cc
    ])


# print_robots(robots, line_count)
r = robots

for m in range(100000):
    # print(m)
    r = [move_robots(k) for k in r]

    cc_size = find_largest_cc(r)
    if cc_size > 100:
        print(m+1)
        print_robots(r)
        break
    # break
    # has_line = print_robots(r, line_count)
    # if has_line:
    #     print('***Found')
    # # print('\n\n')

solution = m+1
print(f'Part 2 - solution: {solution}')
