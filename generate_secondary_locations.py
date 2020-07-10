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


def findoccupation(schools, workplaces, locs, typeID):
    distan = 10000
    loc_id = -1
    if typeID > 4:
        if typeID == 6:
            i = 0
            for wp in workplaces:
                temp_d = distance.cityblock(wp["coordinates"] + wp["coordinates_alt"],
                                            locs["coordinates"] + locs["coordinates_alt"])
                if temp_d < distan:
                    distan = temp_d
                    loc_id = i
                    rloc = {"typeID": workplaces[loc_id]["type"],
                            "locID": workplaces[loc_id]["id"],
                            "coordinates": workplaces[loc_id]["coordinates"],
                            "coordinates_alt": workplaces[loc_id]["coordinates_alt"]
                            }
                    workplaces[loc_id]["capacity"] = workplaces[loc_id]["capacity"] - 1
                    if workplaces[loc_id]["capacity"] < 1:
                        del workplaces[loc_id]
                    return rloc
                i = i + 1
            if len(workplaces) < 1:
                return None
        else:
            return None
    else:
        snum = school_switch(typeID)
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


def generate_occupation(sfn, wfn, agents):
    sc_data = load_schooldata(sfn)
    wp_data = load_schooldata(wfn)
    for agent in agents:
        ifhasoccupation = findoccupation(sc_data, wp_data, agent["locations"][0], agent['typeID'])
        if ifhasoccupation != None:
            #if 4 < ifhasoccupation["typeID"] < 7:
            #    agent['typeID'] = 7
            #if 6 < ifhasoccupation["typeID"] < 9 or ifhasoccupation["typeID"] == 12 or ifhasoccupation["typeID"] == 14:
            #    random.choice([6, 7])
            if ifhasoccupation["typeID"] == 13:
                agent['typeID'] = 7
            agent['locations'].append(dict(ifhasoccupation))
        elif agent['typeID'] > 4:
            agent['typeID'] = 8


def generate_additional_locations(agentsfilein, agentsfileout, schools, workplaces):
    sys.stdout.write("Loading agents")
    with open(agentsfilein, 'r') as f:
        person = json.load(f)
    sys.stdout.write(" - done. Adding schools/workplaces")

    generate_occupation(schools, workplaces, person)

    sys.stdout.write(" - done. Saving")
    with open(agentsfileout, 'w') as f:
        json.dump(person, f, indent="\t")
    print(" - done.")