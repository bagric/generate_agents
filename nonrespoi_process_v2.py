import csv
import json
import sys

def pick_csv(inputcsv, pref="", oldh=False):
    data = []
    oldhome = 0
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
            if oldh:
                oldhome = int(row[6])
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
                      'ageDistribution': [0, 0, 0, 0, oldhome]
                      }
            data.append(places)
    return data

def pick_csvnew(inputcsv, pref=""):
    data_1 = []
    data_2 = []
    with open(inputcsv, encoding="UTF-8") as csvfile:
        cfile = csv.reader(csvfile, dialect='excel', delimiter=";")
        skip = True
        for row in cfile:
            if skip:
                skip = False
                continue

            row[3] = float(row[3].replace(",", "."))
            row[4] = float(row[4].replace(",", "."))
            row[7] = float(row[7].replace(",", "."))
            places = {
                    'id': row[6],
                    'risk': row[7],
                    'subtype': pref + row[0],
                    'coordinates': [row[4], row[3]],
                    'coordinates_alt': [int(row[2]), int(row[1])],
                    'area': 0,
                    'stat': 'ON',
                    'essential': int(row[8]),
                    'ageDistribution': [0, 0, 0, 0, 0],

                    'type': int(row[9]),
                    'capacity': int(row[10]),
                    'ageInter': [int(row[11]), int(row[12])]
                }
            data_1.append(places)

            places = places.copy()
            places["type"] = int(row[13])
            places["capacity"] = int(row[14])
            places["ageInter"] = [int(row[15]), int(row[16])]

            data_2.append(places)

    return data_1, data_2


def dump_json(prefix, poifile, data):
    adat = {"area": prefix, "places": data}
    with open(poifile, 'w') as f:
        json.dump(adat, f, indent="\t")


def process_schools_workplaces(teach, work):
    data = teach
    for wp in work:
        if wp["capacity"] != 0:
            wp["type"] = 4
            data.append(wp)
    return data

def process_intpoit(intpoi):
    for ip in intpoi:
        ip["subtype"] = "int_" + ip["subtype"]

def process_input_data(prefix, schoolncsv, combinedcsv, ohcsv, schoolpoi, workpoi, ipoi, ohpoi):
    txt = "Processing non residential poi files"
    sys.stdout.write('\r' + txt)

    scraw_teach, scraw_student = pick_csvnew(schoolncsv)
    combr_work, combr_interest = pick_csvnew(combinedcsv)
    process_intpoit(combr_interest)

    ohraw = pick_csv(ohcsv, "oh_")

    dump_json(prefix, schoolpoi, scraw_student)
    dump_json(prefix, workpoi, process_schools_workplaces(scraw_teach, combr_work))
    dump_json(prefix, ipoi, combr_interest)
    dump_json(prefix, ohpoi, ohraw)

    print(" - file saved")