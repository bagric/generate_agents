import csv
import json
import sys


def process_input_data(prefix, icsv, ipoifile):
    data = []
    txt = "Processing interesting poi file"
    sys.stdout.write('\r' + txt)

    with open(icsv, encoding="UTF-8") as csvfile:
        cfile = csv.reader(csvfile, dialect='excel', delimiter=";")
        skip = True
        for row in cfile:
            if skip:
                skip = False
                continue
            row[4] = float(row[4].replace(",", "."))
            row[5] = float(row[5].replace(",", "."))
            places = {'id': row[7],
                      'type': int(row[0]),
                      'subtype': "int_" + row[1],
                      'coordinates': [row[5], row[4]],
                      'coordinates_alt': [int(row[3]), int(row[2])],
                      'area': 0,
                      'stat': 'ON',
                      'capacity': int(row[6]),
                      'ageInter': [int(row[8]), int(row[9])],
                      'ageDistribution': [0, 0, 0, 0, 0]
                      }
            data.append(places)

    adat = {"area": prefix, "places": data}
    with open(ipoifile, 'w') as f:
        json.dump(adat, f, indent="\t")

    print(" - file saved")
