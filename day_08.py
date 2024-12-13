from utils import read_input, pprint, config
from pathlib import Path


testing = False
config['verbose'] = False
current_file = "day_08"
data_path = Path(f'./data/{current_file}/input.txt')

if not testing:
    data = read_input(data_path)
else:
    data = '''
............
........0...
.....0......
.......0....
....0.......
......A.....
............
............
........A...
.........A..
............
............
'''

grid=[d for d in data.split("\n") if d]

rows=len(grid)
cols=len(grid[0])

antennas = [ (col, (r,c)) for r, row in enumerate(grid) for c, col in enumerate(row) if col!="." ]

signals = {}
for signal, location in antennas:
    signals[signal] = signals.get(signal,[])+[location]


# Part 1
def detect(antenna, others, locations):
    [row, col] = antenna

    for other in others:
        # break
        [other_row, other_col] = other
        row_shift = row - other_row
        col_shift = col - other_col

        new_pos = (row + row_shift, col + col_shift)
        is_invalid_pos = new_pos[0]<0 or new_pos[0]>=rows or new_pos[1]<0 or new_pos[1]>=cols
        if not is_invalid_pos:
            locations.add(new_pos)

        new_pos = (other_row - row_shift, other_col - col_shift)
        is_invalid_pos = new_pos[0]<0 or new_pos[0]>=rows or new_pos[1]<0 or new_pos[1]>=cols
        if not is_invalid_pos:
            locations.add(new_pos)
            


locations = set()
for signal in signals.values():
    # break
    for i in range(len(signal)-1):
        # break
        antenna = signal[i]
        others = signal[i+1:]
        detect(antenna, others, locations)

solution = len(locations)
print(f'Part 1 - solution: {solution}')

# Part 2

def detect_multiple(antenna, others, locations):
    [row, col] = antenna

    for other in others:
        # break
        [other_row, other_col] = other
        row_shift = row - other_row
        col_shift = col - other_col

        k=-1
        while True:
            k+=1
            new_pos = (row + k * row_shift, col + k * col_shift)
            is_invalid_pos = new_pos[0]<0 or new_pos[0]>=rows or new_pos[1]<0 or new_pos[1]>=cols
            if not is_invalid_pos:
                locations.add(new_pos)
            else:
                break

        k=-1
        while True:
            k+=1
            new_pos = (other_row - k * row_shift, other_col - k * col_shift)
            is_invalid_pos = new_pos[0]<0 or new_pos[0]>=rows or new_pos[1]<0 or new_pos[1]>=cols
            if not is_invalid_pos:
                locations.add(new_pos)
            else:
                break

multiple_locations = set()
for signal in signals.values():
    # break
    for i in range(len(signal)-1):
        # break
        antenna = signal[i]
        others = signal[i+1:]
        detect_multiple(antenna, others, multiple_locations)

solution = len(multiple_locations)

print(f'Part 2 - solution: {solution}')


