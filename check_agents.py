import json
import sys

agents="agents0.json"

with open(agents, 'r') as f:
    people = json.load(f)

for i in people["people"]:
    if i['typeID'] == 5:
        print(i)