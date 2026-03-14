import json

def read_json (path):
    with open (path) as f:
        return json.load (f)
    
def make_odd(x):
    return x if x % 2 != 0 else x - 1