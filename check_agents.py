import json
import sys

agents="agents0.json"

with open(agents, 'r') as f:
    people = json.load(f)

for i in people["people"]:
    if i['typeID'] == 6:
        resokay = False
        workokay = False
        for j in i['locations']:
            if j['typeID'] == 2:
                resokay = True
            if j['typeID'] == 4:
                workokay = True
        if not (resokay and workokay):
            print(i)