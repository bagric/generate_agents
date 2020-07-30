import json
import sys


def _process_data(filename, data, type):
    with open(filename, 'r') as f:
        d = json.load(f)
    d = d["places"]

    for item in d:
        if type == -1:
            t = item['type']
        else:
            t = type
        infectious = 0 if t == 1 else 1
        convert = {
            'ID': item['id'],
            'type': t,
            'coordinates': item['coordinates_alt'],
            'area': item['area'],
            'infectious': infectious,
            'state': 'ON',
            'capacity': item['capacity'],
            'ageInter': item['ageInter']
        }
        data.append(convert)


def convert_data(respoi, schoolpoi, workpoi, ipoi, publicpoi, locationout):
    data = []
    txt = "Converting location files"
    sys.stdout.write('\r' + txt)

    _process_data(respoi, data, 2)
    _process_data(schoolpoi, data, 3)
    _process_data(workpoi, data, -1)
    _process_data(ipoi, data, -1)
    _process_data(publicpoi, data, -1)

    adat = {"places": data}
    with open(locationout, 'w') as f:
        json.dump(adat, f, indent="\t")

    print(" - done")