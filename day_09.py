from utils import read_input, pprint, config
from pathlib import Path


testing = False
config['verbose'] = True
current_file = "day_09"
data_path = Path(f'./data/{current_file}/input.txt')

if not testing:
    data = read_input(data_path)
else:
    data = '''
2333133121414131402
'''

# parse the sequence
sequence = [{"value": int(i/2) if (i % 2 == 0) else '.', "length": int(l)}
            for i, l in enumerate(list(data.strip()))]


def trim_sequence(seq):
    while len(seq) > 0 and (seq[-1]['value'] == '.' or seq[-1]['length'] == 0):
        seq.pop()
    while len(seq) > 0 and seq[0]['length'] == 0:
        seq.pop(0)


trim_sequence(sequence)
sorted_sequence = []
while len(sequence) > 0:
    if sequence[0]['value'] != '.':
        sorted_sequence.append(sequence[0]['value'])
        sequence[0]['length'] -= 1
    else:
        sorted_sequence.append(sequence[-1]['value'])
        sequence[-1]['length'] -= 1
        sequence[0]['length'] -= 1
    trim_sequence(sequence)
    # pprint(sequence)
    # pprint(sorted_sequence)


solution = sum([i*k for i, k in enumerate(sorted_sequence)])
print(f'Part 1 - solution: {solution}')

# Part 2

solution = 0
print(f'Part 2 - solution: {solution}')
