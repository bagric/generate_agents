import json
import random
import sys
import useful_library
from scipy import spatial

def generate_plocation(pfn, agents):
    p_data = useful_library.load_data(pfn, True)
    p_data = useful_library.order_places(p_data[1])
    p_distance_data = spatial.KDTree(useful_library.create_distance_data(p_data))
    for agent in agents:
        if len(agent['locations']) > 0:
            agent['locations'] = agent['locations'] + \
                useful_library.select_closer_places(p_data, p_distance_data, agent['locations'][0], 1)

def generate_additional_locations(agentsfilein, agentsfileout, pplaces):
    sys.stdout.write("Loading agents")
    with open(agentsfilein, 'r') as f:
        person = json.load(f)
    sys.stdout.write(" - done. Adding public places")

    generate_plocation(pplaces, person)

    sys.stdout.write(" - done. Saving")
    with open(agentsfileout, 'w') as f:
        json.dump(person, f, indent="\t")
    print(" - done.")