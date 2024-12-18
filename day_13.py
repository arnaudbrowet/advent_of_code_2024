from utils import read_input, pprint, config
from pathlib import Path
import re

testing = False
config['verbose'] = False
current_file = "day_13"
data_path = Path(f'./data/{current_file}/input.txt')

if not testing:
    data = read_input(data_path)
else:
    data = '''
Button A: X+94, Y+34
Button B: X+22, Y+67
Prize: X=8400, Y=5400

Button A: X+26, Y+66
Button B: X+67, Y+21
Prize: X=12748, Y=12176

Button A: X+17, Y+86
Button B: X+84, Y+37
Prize: X=7870, Y=6450

Button A: X+69, Y+23
Button B: X+27, Y+71
Prize: X=18641, Y=10279
'''

machines = data.split('\n\n')

configurations = [[d for d in m.split('\n') if d] for m in machines]


def find_solutions(A, B, P):
    Ax, Ay = A
    Bx, By = B
    Px, Py = P
    sol = None
    for ka in range(101):
        s = Px - Ax*ka
        if s % Bx != 0:
            continue
        kb = int(s/Bx)

        if Ay*ka + By*kb != Py:
            continue

        cost = 3*ka + kb
        if sol is None or sol[2] > cost:
            sol = (ka, kb, cost)

    return sol


def find_equation_solution(A, B, P):
    Ax, Ay = A
    Bx, By = B
    Px, Py = P

    d = 1-(Ax*By)/(Bx*Ay)
    s = (Px/Bx - (Ax*Py)/(Bx*Ay))

    r = s/d

    kb = int(round(s/d))
    ka = int(round((Px - kb*Bx) / Ax))

    # check
    ppx = Ax*ka + Bx*kb
    ppy = Ay*ka + By*kb
    if ppx != Px or ppy != Py:
        return None
    return (ka, kb, 3*ka+kb)


P2_shift = 10000000000000
total = 0
total2 = 0
for i, c in enumerate(configurations):
    s = re.search(r"Button A: X\+(\d+), Y\+(\d+)", c[0])
    A_X, A_Y = (int(v) for v in s.groups())

    s = re.search(r"Button B: X\+(\d+), Y\+(\d+)", c[1])
    B_X, B_Y = (int(v) for v in s.groups())

    s = re.search(r"Prize: X=(\d+), Y=(\d+)", c[2])
    P_X, P_Y = (int(v) for v in s.groups())

    A = (A_X, A_Y)
    B = (B_X, B_Y)
    P = (P_X, P_Y)

    # sol = find_solutions((A_X, A_Y), (B_X, B_Y), (P_X, P_Y))
    sol = find_equation_solution(A, B, P)
    if sol is not None:
        total += sol[2]

    P = (P_X + P2_shift, P_Y+P2_shift)
    sol2 = find_equation_solution(A, B, P)
    if sol2 is not None:
        pprint('find solution for ', i+1, sol2)
        total2 += sol2[2]

solution = total
print(f'Part 1 - solution: {solution}')

# Part 2

solution = total2
print(f'Part 2 - solution: {solution}')
