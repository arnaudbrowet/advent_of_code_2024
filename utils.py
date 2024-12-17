def read_input(input_path):
    with open(input_path, 'r') as f:
        input = f.read()
    return input


config = {
    'verbose': False
}


def pprint(*args):
    if config.get('verbose', False):
        print(*args)


orthogonal_shift = {
    'U': [-1, 0],
    'D': [1, 0],
    'L': [0, -1],
    'R': [0, 1],
}


def is_valid_grid_index(row, rows, col, cols):
    return row >= 0 and row < rows and col >= 0 and col < cols
