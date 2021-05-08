import json
from json import encoder


with open('test2.json', 'r') as handle:
    parsed = json.load(handle)
print(len(parsed))

