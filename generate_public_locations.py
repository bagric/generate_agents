import json
import random
import sys
import useful_library
from scipy import spatial

def generate_plocation(pfn, agents):
    p_data = useful_library.load_data(pfn, True)
    p_data = useful_library.order_places(p_data[1])
    p_distance_data = spatial.KDTree(useful_library.create_distance_data(p_data))

    iter = 0
    for agent in agents:
        iter = iter+1
        if iter % 250 == 0:
            txt = "Loading agents - done. Adding public places " + '{:6.2f}'.format(100.0*(iter/len(agents))) + "%"
            sys.stdout.write('\r' + txt)

        if len(agent['locations']) > 0:
            agent['locations'] = agent['locations'] + \
                useful_library.select_closer_places(p_data, p_distance_data, agent['locations'][0], 1)

def generate_additional_locations(agentsfilein, agentsfileout, pplaces):
    sys.stdout.write("Loading agents")
    with open(agentsfilein, 'r') as f:
        person = json.load(f)

    generate_plocation(pplaces, person)

    sys.stdout.write("\rLoading agents - done. Adding public places 100% - done. Saving")
    with open(agentsfileout, 'w') as f:
        json.dump(person, f, indent="\t")
    print(" - done.")