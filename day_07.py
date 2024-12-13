from utils import read_input, pprint, config
from pathlib import Path
import re

testing = False
config['verbose']=False
current_file = "day_07"
data_path = Path(f'./data/{current_file}/input.txt')

if not testing:
    data = read_input(data_path)
else:
    data = '''
190: 10 19
3267: 81 40 27
83: 17 5
156: 15 6
7290: 6 8 6 15
161011: 16 10 13
192: 17 8 14
21037: 9 7 18 13
292: 11 6 16 20
'''

equations = [eq for eq in data.split('\n') if eq]

def find_eq(values):
    if len(values)==1:
        return [f"{values[0]}"]
    return [ 
        eq+f"+{values[-1]})"for eq in find_eq( values[:-1])
    ] + [ 
        eq+f"*{values[-1]})" for eq in find_eq( values[:-1])
    ] 


def find_exhaustive(num, values):
    equations_string = ['('*(len(values)-1) + eq for eq in find_eq(values)]
    results = [eval(eq) for eq in equations_string]
    try:
        return equations_string[results.index(num)]
    except:
        return None
    

def find_match(search_value, total, sequence, operations=''):
    if total > search_value : 
        # pprint('total above search value', total, search_value)
        return None
    if total == search_value:
        if len(sequence)==0: return operations
        # pprint('total reached, but more values to come', total, sequence)
        # return None
    
    if len(sequence) ==0: 
        # pprint('sequence is empty', total, search_value)
        return None

    # pprint('Current total:', total, 'Searching', search_value)
    # pprint('Testing sequence', operations+'+')
    sigma = find_match(search_value, total+sequence[0], sequence[1:], operations+'+')
    if sigma is not None: return sigma

    # pprint('Current total:', total, '. Searching', search_value)
    # pprint('Testing sequence', operations+'*')
    product = find_match(search_value, total*sequence[0], sequence[1:], operations+'*')
    return product


def reverse_search(total, sequence, part2=False):
    if total<0:
        return False
    if total==0 and len(sequence)>0:
        return False
    if len(sequence)==0:
        return total == 0
    
    v = sequence[-1]
    sub = sequence[:-1]

    additional = False
    if part2:
        if f"{total}".endswith(f"{v}"):
            additional = reverse_search(
                int((total-v)/10**(len(f"{v}"))),
                sequence[:-1],
                part2
            )

    if total%v == 0 :
        return reverse_search(int(total/v), sub, part2) or reverse_search(total-v, sub, part2) or additional
    return reverse_search(total-v, sub, part2) or additional


total = 0
total_p2 = 0

for i, eq in enumerate(equations):
    # pprint(eq)
    [sol, *values] = re.findall(r"(\d+)", eq)
    values = [int(v) for v in values]
    operations = find_match(int(sol), values[0], values[1:])

    is_valid = reverse_search(int(sol), values)
    total += int(sol) if is_valid else 0
    
    is_valid_p2 = is_valid if is_valid else reverse_search(int(sol), values, True)
    total_p2 += int(sol) if is_valid_p2 else 0
    

solution = total
print(f'Part 1 - solution: {solution}')

# Part 2
solution = total_p2
print(f'Part 2 - solution: {solution}')

