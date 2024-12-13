from utils import read_input
from pathlib import Path

data = read_input(Path('./data/day_04/input.txt'))

# data = '''
# MMMSXXMASM
# MSAMXMSMSA
# AMXSXMAAMM
# MSAMASMSMX
# XMASAMXAMM
# XXAMMXXAMA
# SMSMSASXSS
# SAXAMASAAA
# MAMMMXMMMM
# MXMXAXMASX
# '''

letters = [list(l) for l in data.split('\n') if l]

rows = len(letters)
cols = len(letters[0])

directions = {
    'U': [0, -1],
    'D': [0, 1],
    'L': [-1, 0],
    'R': [1, 0],
    'UR': [1, -1],
    'UL': [-1, -1],
    'DL': [-1, 1],
    'DR': [1, 1],
}


def get_letter(row, col):
    if (col < 0 or col >= cols):
        return '.'
    if (row < 0 or row >= cols):
        return '.'
    return letters[row][col]


def findword(row, col):
    s = 0
    for dir, vec in directions.items():
        word = ''.join([
            get_letter(row+vec[0]*i, col+vec[1]*i) for i in range(4)
        ])
        if word == 'XMAS':
            s += 1

    return s


t = 0
for i in range(rows):
    for j in range(cols):

        t += findword(i, j)

solution = t
print(f'Part 1 - solution: {solution}')


# Part 2

def findcross(row, col):
    # s = 0
    word1 = ''.join([
        get_letter(row+directions['UR'][0], col+directions['UR'][1]),
        get_letter(row, col),
        get_letter(row+directions['DL'][0], col+directions['DL'][1]),
    ])
    word2 = ''.join([
        get_letter(row+directions['DR'][0], col+directions['DR'][1]),
        get_letter(row, col),
        get_letter(row+directions['UL'][0], col+directions['UL'][1]),
    ])

    # word3 = ''.join([
    #     get_letter(row+directions['D'][0], col+directions['D'][1]),
    #     get_letter(row, col),
    #     get_letter(row+directions['U'][0], col+directions['U'][1]),
    # ])
    # word4 = ''.join([
    #     get_letter(row+directions['R'][0], col+directions['R'][1]),
    #     get_letter(row, col),
    #     get_letter(row+directions['L'][0], col+directions['L'][1]),
    # ])

    is1 = (word1 == 'MAS' or word1 == 'SAM')
    is2 = (word2 == 'MAS' or word2 == 'SAM')
    # is3 = (word3 == 'MAS' or word3 == 'SAM')
    # is4 = (word4 == 'MAS' or word4 == 'SAM')

    return is1+is2
    # return is1+is2+is3+is4


t = 0
for i in range(rows):
    for j in range(cols):

        nb_cross = findcross(i, j)
        if nb_cross > 1:
            t += 1
            # print(i,j)

solution = t
print(f'Part 2 - solution: {solution}')

row = 1
col = 13
