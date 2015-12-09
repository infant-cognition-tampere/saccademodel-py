import json
import os

base = os.path.dirname(os.path.realpath(__file__))

def loader(name):
    '''
    Parameter
        name
            filename without .json
    '''
    filename = os.path.join(base, name + '.json')
    with open(filename, 'r') as jsonfile:
        r = json.load(jsonfile)
        return r
