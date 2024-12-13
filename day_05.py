from utils import read_input
from pathlib import Path
import math

data = read_input(Path('./data/day_05/input.txt'))

data = '''
47|53
97|13
97|61
97|47
75|29
61|13
75|53
29|13
97|29
53|29
61|53
97|53
61|29
47|13
75|47
97|75
47|61
75|61
47|29
75|13
53|13

75,47,61,53,29
97,61,53,29,13
75,29,13
75,97,47,61,53
61,13,29
97,13,75,29,47
'''

[orders, pages] = data.split('\n\n')

orders = [[int(i) for i in o.split('|')] for o in orders.split('\n') if o]

page_next = {}
for o in orders:
    page_next[o[0]] = page_next.get(o[0], []) + [o[1]]

pages = [[int(n) for n in p.split(',')]for p in pages.split('\n') if p]


def is_valid_page(page):
    # print("page", page)
    if len(page) <= 1:
        return True

    p = page[0]
    # print('check for ', p)
    for n in page[1:]:
        # print("next", n)
        follow = page_next.get(n, [])
        # print('follow of', n, ":",follow)
        if p in follow:
            # print('invalid')
            return False
    return is_valid_page(page[1:])


mid_page = [page[math.floor(len(page)/2)]
            for page in pages if is_valid_page(page)]

solution = sum(mid_page)
print(f'Part 1 - solution: {solution}')
