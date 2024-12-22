from utils import read_input, pprint, config
from pathlib import Path
import re

testing = False
config['verbose'] = True
current_file = "day_17"
data_path = Path(f'./data/{current_file}/input.txt')

if not testing:
    data = read_input(data_path)
else:
    data = '''
Register A: 2024
Register B: 0
Register C: 0

Program: 0,3,5,4,3,0
'''
#     data = '''
# Register A: 2024
# Register B: 0
# Register C: 0

# Program: 0,1,5,4,3,0
# '''

A, B, C, program = re.search(
    r'Register A: (\d+)\nRegister B: (\d+)\nRegister C: (\d+)\n\nProgram: (.+)', data).groups()


class Register:
    def __init__(self, A, B, C):
        self.A = int(A)
        self.B = int(B)
        self.C = int(C)
        self.pointer = 0
        self.output = []

    def __repr__(self):
        return f"A: {self.A} - B: {self.B} - C: {self.C}"


register = Register(A, B, C)

codes = [int(s) for s in program.split(',')]

instructions = [[codes[2*i], codes[2*i+1]]for i in range(len(codes)//2)]
# pointer = 0

# output = []


def combo(op, register):
    if op <= 3:
        return op
    if op == 4:
        return register.A
    if op == 5:
        return register.B
    if op == 6:
        return register.C
    if op == 7:
        raise Exception('invalid combo')


def div_p2(x, y):
    return x >> y


def adv(op, register):
    register.A = div_p2(register.A, combo(op, register))
    register.pointer += 1
    return register


def bxl(op, register):
    register.B = register.B ^ op
    register.pointer += 1
    return register


def bst(op, register):
    register.B = combo(op, register) % 8
    register.pointer += 1
    return register


def jnz(op, register):
    if register.A == 0:
        register.pointer += 1
        return register
    if op % 2 != 0:
        raise Exception('invalid jump', op)
    register.pointer = op // 2
    return register


def bxc(op, register):
    register.B = register.B ^ register.C
    register.pointer += 1
    return register


def out(op, register):
    register.output.append(combo(op, register) % 8)
    register.pointer += 1
    return register


def bdv(op, register):
    register.B = div_p2(register.A, combo(op, register))
    register.pointer += 1
    return register


def cdv(op, register):
    register.C = div_p2(register.A, combo(op, register))
    register.pointer += 1
    return register


operations = {
    0: adv,
    1: bxl,
    2: bst,
    3: jnz,
    4: bxc,
    5: out,
    6: bdv,
    7: cdv,
}

if testing:
    r = Register(0, 0, 0)
    r.C = 9
    ins = 2
    op = 6
    p, r = operations[ins](op, 0, r)
    assert (r.B == 1)

    x = 64324
    y = 3
    assert (x//(2**y) == div_p2(x, y))

    r.B = 29
    ins, op = 1, 7
    operations[ins](op, 0, r)
    assert (r.B == 26)

    r.B = 2024
    r.C = 43690
    ins, op = 4, 0
    operations[ins](op, 0, r)
    assert (r.B == 44354)


def run(register):
    while register.pointer < len(instructions):
        ins, op = instructions[register.pointer]
        # print(ins, op)
        register = operations[ins](op, register)
        # print(register)

    # return register


run(register)
solution = ','.join([f"{o}" for o in register.output])
print(f'Part 1 - solution: {solution}')


# Part 2

def search_output(current_values, searching_value):
    sol = []

    a = sum([b << (3*(i+1))for i, b in enumerate(current_values)])

    for i in range(8):
        reg = Register(a+i, B, C)
        run(reg)
        # print(reg.output)
        if reg.output[0] == searching_value:
            sol.append(
                [i] + current_values
            )
    return sol


bit_values = [[]]

for ind in range(len(codes)):
    # break
    to_find = codes[-1-ind]

    new_bit_values = []

    for v in bit_values:
        # break
        current_values = v
        searching_value = to_find
        sol = search_output(current_values, searching_value)
        if len(sol) > 0:
            new_bit_values += [s for s in sol if s[-1] != 0]

    bit_values = new_bit_values
    # break

# check and find minimum
a_opt = None
for bit_value in bit_values:
    a = sum([b << (3*(i))for i, b in enumerate(bit_value)])
    register = Register(a, B, C)
    run(register)
    if register.output == codes:
        if a_opt is None or a_opt > a:
            a_opt = a

    # print(register.output)
solution = a_opt
print(f'Part 2 - solution: {solution}')
