import json
import sys


def convert_data(genagent, agentsout):
    data = []

    with open(genagent, 'r') as f:
        people = json.load(f)

    iter = 0

    for res in people:
        iter = iter + 1
        if iter % 10:
            txt = "Converting agent records " + '{:6.2f}'.format(100.0*iter/len(people)) + "%"
            sys.stdout.write('\r' + txt)

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

    sys.stdout.write(" - done. Saving")
    adat = {"people": data}
    with open(agentsout, 'w') as f:
        json.dump(adat, f, indent="\t")

    print(" - done")