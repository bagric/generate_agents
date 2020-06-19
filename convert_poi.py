import json
import sys


def _process_data(filename, data, type):
    with open(filename, 'r') as f:
        d = json.load(f)
    d = d["places"]

    for item in d:
        convert = {
            'ID': item['id'],
            'type': type,
            'coordinates': item['coordinates_alt'],
            'area': item['area'],
            'state': 'ON',
            'capacity': item['capacity'],
            'ageInter': item['ageInter']
        }
        data.append(convert)


def convert_data(respoi, schoolpoi, locationout):
    data = []
    txt = "Converting location files"
    sys.stdout.write('\r' + txt)

    _process_data(respoi, data, 2)
    _process_data(schoolpoi, data, 3)

    adat = {"places": data}
    with open(locationout, 'w') as f:
        json.dump(adat, f, indent="\t")

    print(" - done")