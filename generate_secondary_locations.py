import json
import random
import sys
import math
import useful_library

from scipy.spatial import distance

unschooled_counter = [0] * 4

class Switch(dict):
    def __getitem__(self, item):
        for key in self.keys():                   # iterate over the intervals
            if item in key:                       # if the argument is part of that interval
                return super().__getitem__(key)   # return its associated value
        raise KeyError(item)

def chunkIt(seq, num):
    avg = len(seq) / float(num)
    out = []
    last = 0.0

    while last < len(seq):
        out.append(seq[int(last):int(last + avg)])
        last += avg

    return out

def school_switch(i):
    switcher = {
        1: "bölcsőde",  # Infant
        2: "óvoda",  # Kindergarden student
        3: "általános iskola",  # Elemntary school student
        4: random.choice(["gimnázium", "szakközépiskola"])  # Highschool student
    }
    return switcher.get(i, "más")

def find_class(i):
    switcher = {
        7: 0, # first grader etc.
        8: 1,
        9: 2,
        10: 3,
        11: 4,
        12: 5,
        13: 6,
        14: 7,
        15: 0,
        16: 1,
        17: 2,
        18: 3
    }
    return switcher.get(i, "más")

def class_switch(i):
    switcher = {
        0: "a",
        1: "b",
        2: "c",
        3: "d",
        4: "e",
        5: "f",
        6: "g",
        7: "h",
        8: "i",
        9: "j",
        10: "k",
        11: "l",
        12: "m",
        13: "n",
        14: "o",
        15: "p",
        16: "q"
    }
    return switcher.get(i, "más")

def findoccupation(schools, workplaces, agent, sc_class_data):
    locs = agent['locations'][0]
    typeID = agent['typeID']
    age = agent['age']
    distan = 1000000
    loc_id = -1
    if 4 < typeID < 9:
        if typeID == 6:
            i = 0
            for wp in workplaces:
                temp_d = distance.cityblock(wp["coordinates"] + wp["coordinates_alt"],
                                            locs["coordinates"] + locs["coordinates_alt"])
                if temp_d < distan:
                    distan = temp_d
                    loc_id = i
                    rloc = {"typeID": wp["type"],
                            "locID": wp["id"],
                            "coordinates": wp["coordinates"],
                            "coordinates_alt": wp["coordinates_alt"]
                            }
                    wp["capacity"] = wp["capacity"] - 1
                    if wp["capacity"] < 1:
                        workplaces.remove(wp)
                    return rloc
            if len(workplaces) < 1:
                return None
        else:
            return None
    # babies left out as requested
    elif 1 < typeID <= 4:
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
            if snum == "általános iskola" or snum == "gimnázium" or snum == "szakközépiskola":
                '''schools[loc_id]["classes"][find_class(age)][0] = schools[loc_id]["classes"][find_class(age)][0] + 1
                if schools[loc_id]["classes"][find_class(age)][0] % 18 == 0 and schools[loc_id]["classes"][find_class(age)][0] != 18:
                    schools[loc_id]["classes"][find_class(age)][1] = schools[loc_id]["classes"][find_class(age)][1] + 1'''
                #schools[loc_id]["classes"][find_class(age)] = schools[loc_id]["classes"][find_class(age)] + 1
                sc_class_data[schools[loc_id]["id"]]["classes"][int(find_class(age))].append(agent)
            if schools[loc_id]["capacity"] == 0:
                # changed to go over capacity as requested
                for i in range(len(schools)):
                    if schools[i]["subtype"] == snum and schools[i]["id"] != schools[loc_id]["id"]:
                        del schools[loc_id]
                        break
            return rloc

def generate_occupation(sfn, wfn, agents):
    sc_data = useful_library.load_data(sfn)
    sc_class_data = {}
    for school in sc_data:
        if school["subtype"] == "általános iskola":
            sc_class_data[school["id"]] = {}
            sc_class_data[school["id"]]["classes"] = []
            for i in range(8):
                a = []
                sc_class_data[school["id"]]["classes"].append(a)
        if school["subtype"] == "gimnázium" or school["subtype"] == "szakközépiskola":
            sc_class_data[school["id"]] = {}
            sc_class_data[school["id"]]["classes"] = []
            for i in range(4):
                a = []
                sc_class_data[school["id"]]["classes"].append(a)
    wp_data = useful_library.load_data(wfn)

    iter = 0
    for agent in agents:
        iter = iter+1
        if iter % 250 == 0:
            txt = "Loading agents - done. Adding schools/workplaces " + '{:6.2f}'.format(100.0*(iter/len(agents))) + "%"
            sys.stdout.write('\r' + txt)

        if agent['age'] < 70:
            ifhasoccupation = findoccupation(sc_data, wp_data, agent, sc_class_data)
            if ifhasoccupation is not None and len(ifhasoccupation) > 0:
                # if 4 < ifhasoccupation["typeID"] < 7:
                #    agent['typeID'] = 7
                # if 6 < ifhasoccupation["typeID"] < 9 or ifhasoccupation["typeID"] == 12 or ifhasoccupation["typeID"] == 14:
                #    random.choice([6, 7])
                if ifhasoccupation['typeID'] == 13:
                    agent['typeID'] = 7
                agent['locations'].append(dict(ifhasoccupation))
            else:
                if 5 <= agent['typeID'] < 9:
                    agent['typeID'] = 8
                elif 1 < agent['typeID'] <= 4:
                    unschooled_counter[agent['typeID'] - 1] = unschooled_counter[agent['typeID'] - 1] + 1
                    agent['typeID'] = 1
                    agent['age'] = random.choice([0, 1])
        else:
            agent['typeID'] = 8
    for school in sc_class_data:
        cnt = 0
        sc_class_data[school]["codes"] = []
        for sch in sc_class_data[school]["classes"]:
            cnt = cnt + 1
            num_helper = math.floor(len(sch)/18)
            if num_helper > 1:
                cur_classes = chunkIt(sch, num_helper)
                for i in range(len(cur_classes)):
                    class_code = str(cnt) + class_switch(i)
                    sc_class_data[school]["codes"].append(class_code)
                    for act_student in cur_classes[i]:
                        act_student['locations'][1]['locID'] = class_code + act_student['locations'][1]['locID']
            else:
                class_code = str(cnt) + "a"
                sc_class_data[school]["codes"].append(class_code)
                for act_student in sch:
                        act_student['locations'][1]['locID'] = class_code + act_student['locations'][1]['locID']
    return sc_class_data


def generate_additional_locations(agentsfilein, agentsfileout, schools, workplaces, tempschoollocation=None):
    sys.stdout.write("Loading agents")
    with open(agentsfilein, 'r') as f:
        person = json.load(f)

    schools = generate_occupation(schools, workplaces, person)
    # print(unschooled_counter)
    sys.stdout.write("\rLoading agents - done. Adding schools/workplaces 100% - done. Saving")
    with open(agentsfileout, 'w') as f:
        json.dump(person, f, indent="\t")
    # save schools with classes
    with open(tempschoollocation, 'w') as f:
        json.dump(schools, f, indent="\t")
    print(" - done.")