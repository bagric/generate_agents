import json
import sys


def _process_data(filename, data, type):
    print(filename)
    see = [0 for _ in range(1, 50)]

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
            if "essential" in item.keys():
                essential = item['essential']
            else:
                essential = 0
            convert = {
                'ID': item['id'],
                'type': t,
                'essential': essential,
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
                    'essential': item['essential'],
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
            'type': 3,    ## A school is fixed to 3 in the final location dbs
            'essential': item['essential'],
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
                    'essential': 0,
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
                'essential': 0,
                'coordinates': item['coordinates_alt'],
                'area': item['area'],
                'infectious': infectious,
                'state': 'ON',
                'capacity': item['capacity'],
                'ageInter': item['ageInter']
            }
            data.append(convert)


def cleanse(data):
    print("cleansing")
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
                for key in subd:
                    if key == "type":
                        if pop[key] == 3:
                            break
                        elif subd[key] == 4:
                            break
                    else:
                        if subd[key] != pop[key]:
                            break
                else:
                    output.append(subd)

    return {"places": output}


def convert_data(respoi, schoolpoi, workpoi, ipoi, publicpoi, ohpoi, tempfamlocation, tempschoollocation, locationout, resvisitor_helper):
    data = []
    txt = "Converting location files"
    sys.stdout.write('\r' + txt)

    # Order is important! Interesting poi and its type is the primary type. Only schools can override.
    _process_res_data(respoi, tempfamlocation, data)
    with open(resvisitor_helper, 'w') as f:
        json.dump(data, f, indent="\t")

    _process_data(ohpoi, data, -1)
    _process_sch_data(schoolpoi, tempschoollocation, data)
    _process_data(ipoi, data, -1)
    _process_data(publicpoi, data, -1)
    _process_data(workpoi, data, -1)


    data.append({'ID': 'tourist_box',
                  'type': 15,
                  'coordinates': [120000, 740000],
                  'area': 0,
                  'infectious': 0,
                  'state': 'ON',
                  'capacity': 1000000,
                  'essential': 0,
                  'ageInter': [0, 100]
                  })
    data.append({'ID': 'school_commuter_box',
                  'type': 15,
                  'coordinates': [120000, 740000],
                  'area': 0,
                  'infectious': 0,
                  'state': 'ON',
                  'capacity': 1000000,
                  'essential': 0,
                  'ageInter': [0, 100]
                 })
    data.append({'ID': 'work_commuter_box',
                  'type': 15,
                  'coordinates': [120000, 740000],
                  'area': 0,
                  'infectious': 0,
                  'state': 'ON',
                  'capacity': 1000000,
                  'essential': 0,
                  'ageInter': [0, 100]
                 })
    data.append({'ID': 'work_commuter_box',
                  'type': 15,
                  'coordinates': [120000, 740000],
                  'area': 0,
                  'infectious': 0,
                  'state': 'ON',
                  'capacity': 1000000,
                  'essential': 0,
                  'ageInter': [0, 100]
                 })

    adat = cleanse(data)
    with open(locationout, 'w') as f:
        json.dump(adat, f, indent="\t")

    print(" - done")