import json

data = []

filename = "Szeged_adat_new.json"
with open(filename, 'r') as f:
    residents = json.load(f)
residents = residents["places"]

for res in residents:
    convert = {
        'ID': res['id'],
        'type': 2,
        'coordinates': res['coordinates_alt'],
        'area': res['area'],
        'state': 'ON',
        'capacity': res['capacity'],
        'ageInter': res['ageInter']
    }
    data.append(convert)

filename = "Szeged_adat_school_poi.json"
with open(filename, 'r') as f:
    schools = json.load(f)
schools = schools["places"]

for res in schools:
    convert = {
        'ID': res['id'],
        'type': 3,
        'coordinates': res['coordinates_alt'],
        'area': res['area'],
        'state': 'ON',
        'capacity': res['capacity'],
        'ageInter': res['ageInter']
    }
    data.append(convert)

adat = {"places": data}
with open("locations.json", 'w') as f:
    json.dump(adat, f, indent="\t")
