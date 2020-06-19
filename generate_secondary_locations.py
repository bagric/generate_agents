import json
import random
import sys

from scipy.spatial import distance


class Switch(dict):
    def __getitem__(self, item):
        for key in self.keys():                   # iterate over the intervals
            if item in key:                       # if the argument is part of that interval
                return super().__getitem__(key)   # return its associated value
        raise KeyError(item)


def load_schooldata(filename):
    '''
    Load a formatted JSON file with the location of schools

    :param filename: Name of the file
    '''
    with open(filename, 'r') as f:
        _schools = json.load(f)
        _schools = _schools["places"]
    return [v for v in sorted(_schools, key=lambda item: item["subtype"])]


def school_switch(i):
    switcher = {
        1: "bölcsőde",  # Infant
        2: "óvoda",  # Kindergarden student
        3: "általános iskola",  # Elemntary school student
        4: random.choice(["gimnázium", "szakközépiskola"])  # Highschool student
    }
    return switcher.get(i, "más")


def findschool(schools, locs, typeID):
    if typeID > 4:
        return None
    snum = school_switch(typeID)
    distan = 10000
    loc_id = -1
    i = 0
    for sch in schools:
        if sch["subtype"] == snum:
            temp_d = distance.cityblock(sch["coordinates"] + sch["coordinates_alt"],
                                        locs["coordinates"] + locs["coordinates_alt"])
            if temp_d < distan:
                distan = temp_d
                loc_id = i
        i = i + 1
    if loc_id == -1:
        return None
    else:
        rloc = {"typeID": schools[loc_id]["type"],
                "locID": schools[loc_id]["id"],
                "coordinates": schools[loc_id]["coordinates"],
                "coordinates_alt": schools[loc_id]["coordinates_alt"]
                }
        schools[loc_id]["capacity"] = schools[loc_id]["capacity"] - 1
        if schools[loc_id]["capacity"] < 1:
            del schools[loc_id]
        return rloc


def generate_schools(filename, agents):
    sc_data = load_schooldata(filename)
    for agent in agents:
        ifschool = findschool(sc_data, agent["locations"][0], agent['typeID'])
        if ifschool != None:
            agent['locations'].append(dict(ifschool))


def generate_additional_locations(agentsfile, schools):
    sys.stdout.write("Loading agents")
    with open(agentsfile, 'r') as f:
        person = json.load(f)
    sys.stdout.write(" - done. Adding schools")

    generate_schools(schools, person)

    sys.stdout.write(" - done. Saving")
    with open(agentsfile, 'w') as f:
        json.dump(person, f, indent="\t")
    print(" - done.")