def read_input(input_path):
    with open(input_path, 'r') as f:
        input = f.read()
    return input

config = {
    'verbose':False
}

def pprint(*args):
    if config.get('verbose', False):
        print(*args)