import json
import sys


def _process_data(filename, data, type):
    print(filename)
    see = [0 for _ in range(1,16)]

    with open(filename, 'r') as f:
        d = json.load(f)
    d = d["places"]

    for item in d:
        if type == -1:
            t = item['type']
        else:
            t = type
        infectious = 0 if t == 1 else 1
        if not any(act_loc['ID'] == item['id'] for act_loc in data):
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
        see[t] = see[t] + 1

    print(see)

def _process_sch_data(filename, tempschoollocation, data):
    with open(filename, 'r') as f:
        d = json.load(f)
    d = d["places"]

    with open(tempschoollocation, 'r') as f:
        tfl = json.load(f)

    cnt = 0
    for item in d:
        t = 3
        infectious = 1
        if item['id'] in tfl:
            for multip in tfl[item['id']]['codes']:
                convert = {
                    'ID': multip + "_" + item['id'],
                    'type': 33,
                    'coordinates': item['coordinates_alt'],
                    'area': item['area'],
                    'infectious': infectious,
                    'state': 'ON',
                    'capacity': item['capacity'],
                    'ageInter': item['ageInter']
                }
                data.append(convert)
        # Entire school is stored as well
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

def _process_res_data(filename, tempfamlocation, data):
    with open(filename, 'r') as f:
        d = json.load(f)
    d = d["places"]
    cnt = 0

    with open(tempfamlocation, 'r') as f:
        tfl = json.load(f)

    for item in d:
        t = 2
        infectious = 1
        if item['id'] in tfl:
            for multip in tfl[item['id']]:
                convert = {
                    'ID': multip + item['id'],
                    'type': t,
                    'coordinates': item['coordinates_alt'],
                    'area': item['area'],
                    'infectious': infectious,
                    'state': 'ON',
                    'capacity': item['capacity'],
                    'ageInter': item['ageInter']
                }
                data.append(convert)
        else:
            cnt = cnt + 1
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


def cleanse(data):
    ou = dict()
    for d in data:
        if d['ID'] in ou.keys():
            ou[d['ID']].append(d)
        else:
            ou[d['ID']] = [d]
    output = []
    for dk in ou:
        d = ou[dk]
        pop = d[0]
        output.append(pop)
        if len(d) > 1:
            for subd in d:
                shared_items = {k: pop[k] for k in pop if k in subd and subd[k] == pop[k]}
                if len(shared_items) != len(pop):
                    output.append(subd)

    return {"places": output}


def convert_data(respoi, schoolpoi, workpoi, ipoi, publicpoi, ohpoi, tempfamlocation, tempschoollocation, locationout):
    data = []
    txt = "Converting location files"
    sys.stdout.write('\r' + txt)

    _process_res_data(respoi, tempfamlocation, data)
    _process_sch_data(schoolpoi, tempschoollocation, data)
    _process_data(ipoi, data, -1)
    _process_data(publicpoi, data, -1)
    _process_data(workpoi, data, -1)
    _process_data(ohpoi, data, -1)
    

    data.append({'ID': 'tourist_box',
                  'type': 15,
                  'coordinates': [120000, 740000],
                  'area': 0,
                  'infectious': 0,
                  'state': 'ON',
                  'capacity': 1000000,
                  'ageInter': [0, 100]
                  })
    data.append({'ID': 'school_commuter_box',
                  'type': 15,
                  'coordinates': [120000, 740000],
                  'area': 0,
                  'infectious': 0,
                  'state': 'ON',
                  'capacity': 1000000,
                  'ageInter': [0, 100]
                 })
    data.append({'ID': 'work_commuter_box',
                  'type': 15,
                  'coordinates': [120000, 740000],
                  'area': 0,
                  'infectious': 0,
                  'state': 'ON',
                  'capacity': 1000000,
                  'ageInter': [0, 100]
                 })
    data.append({'ID': 'work_commuter_box',
                  'type': 15,
                  'coordinates': [120000, 740000],
                  'area': 0,
                  'infectious': 0,
                  'state': 'ON',
                  'capacity': 1000000,
                  'ageInter': [0, 100]
                 })

    adat = cleanse(data)
    with open(locationout, 'w') as f:
        json.dump(adat, f, indent="\t")

    print(" - done")