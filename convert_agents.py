import json

data = []

filename = "Szeged_adat_agentsB.json"
with open(filename, 'r') as f:
    people = json.load(f)

for res in people:
    convert = {
        'age': res['age'],
        'sex': res['sex'],
        'preCond': res['preCond'],
        'state': res['SIRD'],
        'typeID': res['typeID'],
        'locations': []
    }

    for locs in res['locations']:
        loc = {
            'typeID': locs['typeID'],
            'locID': locs['locID']
        }
        convert['locations'].append(loc)

    data.append(convert)


adat = {"people": data}
with open("agents.json", 'w') as f:
    json.dump(adat, f, indent="\t")
