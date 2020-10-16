import csv
import json
import sys

def pick_csv(inputcsv, pref=""):
    data = []
    datadict = {}
    with open(inputcsv, encoding="UTF-8") as csvfile:
        cfile = csv.reader(csvfile, dialect='excel', delimiter=";")
        skip = True
        for row in cfile:
            if skip:
                skip = False
                continue
            row[4] = float(row[4].replace(",", "."))
            row[5] = float(row[5].replace(",", "."))
            row[11] = float(row[11].replace(",", "."))
            places = {'id': row[7],
                      'type': int(row[0]),
                      'subtype': pref + row[1],
                      'coordinates': [row[5], row[4]],
                      'coordinates_alt': [int(row[3]), int(row[2])],
                      'area': 0,
                      'stat': 'ON',
                      'capacity': int(row[6]),
                      'ageInter': [int(row[9]), int(row[10])],
                      'risk': row[11],
                      'ageDistribution': [0, 0, 0, 0, 0]
                      }
            data.append(places)
    return data


def dump_json(prefix, poifile, data):
    adat = {"area": prefix, "places": data}
    with open(poifile, 'w') as f:
        json.dump(adat, f, indent="\t")


def process_input_data(prefix, schoolcsv, workcsv, icsv, schoolpoi, workpoi, ipoi):
    txt = "Processing non residential poi files"
    sys.stdout.write('\r' + txt)

    scraw = pick_csv(schoolcsv)
    woraw = pick_csv(workcsv)
    inraw = pick_csv(icsv, "int_")

    dump_json(prefix, schoolpoi, scraw)
    dump_json(prefix, workpoi, woraw)
    dump_json(prefix, ipoi, inraw)

    print(" - file saved")