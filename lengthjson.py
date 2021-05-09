import json
from json import encoder


with open('tournaments.json', 'r') as handle:
    parsed = json.load(handle)
print(len(parsed))

