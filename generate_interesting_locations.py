import json
import random
import sys
import useful_library
from scipy import spatial
#from scipy.spatial import distance

'''
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
'''

def generate_ilocation(ifn, agents):
    i_data = useful_library.load_data(ifn, True)
    i_distance_data = [[] for _ in range(len(i_data))]
    i = 0
    while i < len(i_data):
        i_data[i] = useful_library.order_places(i_data[i])
        if len(i_data[i]) > 1:
            i_distance_data[i] = spatial.KDTree(useful_library.create_distance_data(i_data[i]))
        else:
            i_distance_data[i] = useful_library.create_distance_data(i_data[i])
        i = i + 1
    for agent in agents:
        if agent['typeID'] == 1:
            agent['locations'] = agent['locations'] + useful_library.select_random_place(i_data, 10, 3)
            agent['locations'] = agent['locations'] + useful_library.select_random_place(i_data, 12, 1)
            agent['locations'] = agent['locations'] + useful_library.select_random_place(i_data, 14, 1)
        elif 1 < agent['typeID'] < 4:
            agent['locations'] = agent['locations'] + useful_library.select_closer_places(i_data[8], i_distance_data[8], agent['locations'][0], 2)
            if len(agent['locations']) > 2:
                agent['locations'] = agent['locations'] + useful_library.select_closer_places(i_data[8], i_distance_data[8], agent['locations'][1], 1)
            agent['locations'] = agent['locations'] + useful_library.select_random_place(i_data, 12, 1)
            agent['locations'] = agent['locations'] + useful_library.select_random_place(i_data, 14, 1)
        elif agent['typeID'] == 4:
            agent['locations'] = agent['locations'] + useful_library.select_random_place(i_data, 6, 3)
            agent['locations'] = agent['locations'] + useful_library.select_closer_places(i_data[7], i_distance_data[7], agent['locations'][0], 2)
            if len(agent['locations']) > 2:
                agent['locations'] = agent['locations'] + useful_library.select_closer_places(i_data[7], i_distance_data[7], agent['locations'][1], 1)
            agent['locations'] = agent['locations'] + useful_library.select_closer_places(i_data[8], i_distance_data[8], agent['locations'][0], 2)
            if len(agent['locations']) > 2:
                agent['locations'] = agent['locations'] + useful_library.select_closer_places(i_data[8], i_distance_data[8], agent['locations'][1], 1)
            agent['locations'] = agent['locations'] + useful_library.select_random_place(i_data, 9, 3)
            agent['locations'] = agent['locations'] + useful_library.select_random_place(i_data, 10, 3)
            agent['locations'] = agent['locations'] + useful_library.select_random_place(i_data, 12, 1)
            agent['locations'] = agent['locations'] + useful_library.select_random_place(i_data, 14, 1)
        elif 4 < agent['typeID'] <= 9:  # Add tourists as well
            agent['locations'] = agent['locations'] + useful_library.select_random_place(i_data, 5, 3)
            agent['locations'] = agent['locations'] + useful_library.select_random_place(i_data, 6, 3)
            agent['locations'] = agent['locations'] + useful_library.select_closer_places(i_data[7], i_distance_data[7], agent['locations'][0], 2)
            if len(agent['locations']) > 2:
                agent['locations'] = agent['locations'] + useful_library.select_closer_places(i_data[7], i_distance_data[7], agent['locations'][1], 1)
            agent['locations'] = agent['locations'] + useful_library.select_closer_places(i_data[8], i_distance_data[8], agent['locations'][0], 2)
            if len(agent['locations']) > 2:
                agent['locations'] = agent['locations'] + useful_library.select_closer_places(i_data[8], i_distance_data[8], agent['locations'][1], 1)
            agent['locations'] = agent['locations'] + useful_library.select_random_place(i_data, 9, 3)
            agent['locations'] = agent['locations'] + useful_library.select_random_place(i_data, 10, 3)
            agent['locations'] = agent['locations'] + useful_library.select_random_place(i_data, 12, 1)
            agent['locations'] = agent['locations'] + useful_library.select_random_place(i_data, 14, 1)

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