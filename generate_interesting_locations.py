import json
import random
import sys

from scipy.spatial import distance

def load_idata(filename):
    '''
    Load a formatted JSON file with the location of interesting places

    :param filename: Name of the file
    '''
    with open(filename, 'r') as f:
        _interestingp = json.load(f)
        _interestingp = _interestingp["places"]
    temp_iplaces = [v for v in sorted(_interestingp, key=lambda item: item["subtype"])]
    base_iplaces = [[] for _ in range(15)]
    for iitem in temp_iplaces:
        base_iplaces[iitem["type"]].append(iitem)
    return base_iplaces

def select_random_place(i_data, place_type, how_many):
    list_of_places = []
    i = 0
    while i < how_many:
        place = random.choice(i_data[place_type])
        rloc = {"typeID": place["type"],
                "locID": place["id"],
                "coordinates": place["coordinates"],
                "coordinates_alt": place["coordinates_alt"]
                }
        if dict(rloc) not in list_of_places:
            list_of_places.append(dict(rloc))
            i = i + 1
    return list_of_places

def select_closer_places(i_data, agent, place_type, how_many):
    list_of_places = []
    saving_list = []
    random_stop = random.randint(int(len(i_data[place_type])/2), len(i_data[place_type]))
    i = 0
    for iplace in i_data[place_type]:
        temp_res = distance.cityblock(iplace["coordinates"] + iplace["coordinates_alt"],
                                    agent['locations'][0]["coordinates"] + agent['locations'][0]["coordinates_alt"])
        temp_work = temp_res + 1
        if agent['typeID'] > 1 and len(agent['locations']) > 1:
            temp_work = distance.cityblock(iplace["coordinates"] + iplace["coordinates_alt"],
                                        agent['locations'][1]["coordinates"] + agent['locations'][1]["coordinates_alt"])
        if len(saving_list) < how_many:
            saving_list.append([i, temp_res if temp_res < temp_work else temp_work])
        else:
            saving_list.sort(key = lambda x: x[1])
            j = 0
            for saved_place in saving_list:
                if temp_res < saved_place[1] or temp_work < saved_place[1]:
                    saving_list[j] = [i, temp_res if temp_res < temp_work else temp_work]
                j = j + 1
        if i == random_stop:
            break
        i = i + 1
    for saved_place in saving_list:
        rloc = {"typeID": i_data[place_type][saved_place[0]]["type"],
                "locID": i_data[place_type][saved_place[0]]["id"],
                "coordinates": i_data[place_type][saved_place[0]]["coordinates"],
                "coordinates_alt": i_data[place_type][saved_place[0]]["coordinates_alt"]
                }
        list_of_places.append(dict(rloc))
    return list_of_places

def generate_ilocation(ifn, agents):
    i_data = load_idata(ifn)
    for agent in agents:
        if agent['typeID'] == 1:
            agent['locations'] = agent['locations'] + select_random_place(i_data, 10, 3)
            agent['locations'] = agent['locations'] + select_random_place(i_data, 12, 1)
            agent['locations'] = agent['locations'] + select_random_place(i_data, 14, 1)
        elif 1 < agent['typeID'] < 4:
            agent['locations'] = agent['locations'] + select_closer_places(i_data, agent, 8, 2)
            agent['locations'] = agent['locations'] + select_random_place(i_data, 12, 1)
            agent['locations'] = agent['locations'] + select_random_place(i_data, 14, 1)
        elif agent['typeID'] == 4:
            agent['locations'] = agent['locations'] + select_random_place(i_data, 6, 3)
            agent['locations'] = agent['locations'] + select_closer_places(i_data, agent, 7, 2)
            agent['locations'] = agent['locations'] + select_closer_places(i_data, agent, 8, 2)
            agent['locations'] = agent['locations'] + select_random_place(i_data, 9, 3)
            agent['locations'] = agent['locations'] + select_random_place(i_data, 10, 3)
            agent['locations'] = agent['locations'] + select_random_place(i_data, 12, 1)
            agent['locations'] = agent['locations'] + select_random_place(i_data, 14, 1)
        elif 4 < agent['typeID'] < 9:
            agent['locations'] = agent['locations'] + select_random_place(i_data, 5, 3)
            agent['locations'] = agent['locations'] + select_random_place(i_data, 6, 3)
            agent['locations'] = agent['locations'] + select_closer_places(i_data, agent, 7, 2)
            agent['locations'] = agent['locations'] + select_closer_places(i_data, agent, 8, 2)
            agent['locations'] = agent['locations'] + select_random_place(i_data, 9, 3)
            agent['locations'] = agent['locations'] + select_random_place(i_data, 10, 3)
            agent['locations'] = agent['locations'] + select_random_place(i_data, 12, 1)
            agent['locations'] = agent['locations'] + select_random_place(i_data, 14, 1)

def generate_additional_locations(agentsfilein, agentsfileout, iplaces):
    sys.stdout.write("Loading agents")
    with open(agentsfilein, 'r') as f:
        person = json.load(f)
    sys.stdout.write(" - done. Adding interesting places")

    generate_ilocation(iplaces, person)

    sys.stdout.write(" - done. Saving")
    with open(agentsfileout, 'w') as f:
        json.dump(person, f, indent="\t")
    print(" - done.")