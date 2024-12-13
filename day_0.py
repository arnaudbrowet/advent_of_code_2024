from utils import read_input, pprint, config
from pathlib import Path


testing = True
config['verbose']=True
current_file = "day_"
data_path = Path(f'./data/{current_file}/input.txt')

if not testing:
    data = read_input(data_path)
else:
    data = '''
'''

solution = 0
print(f'Part 1 - solution: {solution}')

# Part 2

solution = 0
print(f'Part 2 - solution: {solution}')

