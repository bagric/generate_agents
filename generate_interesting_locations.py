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
    base_iplaces = [v for v in sorted(_interestingp, key=lambda item: item["subtype"])]
    evening_schedule = [v for v in base_iplaces if 4 < v["type"] < 7]
    activity = [v for v in base_iplaces if 6 < v["type"] < 9]
    recreational_weekend_schedule = [v for v in base_iplaces if 8 < v["type"] < 11]
    nicer_places = [v for v in base_iplaces if v["type"] == 13]
    health_places = [v for v in base_iplaces if v["type"] == 12 or v["type"] == 14]
    return evening_schedule, activity, recreational_weekend_schedule, nicer_places, health_places

def generate_evs(i_data, persontype):
    if persontype > 4:
        place = random.choice(i_data)
        rloc = {"typeID": place["type"],
                "locID": place["id"],
                "coordinates": place["coordinates"],
                "coordinates_alt": place["coordinates_alt"]
                }
        return rloc
    else:
        return None

def generate_act(i_data, persontype):
    if persontype > 2:
        list_of_places = []
        i = 0
        while i < 1*persontype:
            place = random.choice(i_data)
            rloc = {"typeID": place["type"],
                    "locID": place["id"],
                    "coordinates": place["coordinates"],
                    "coordinates_alt": place["coordinates_alt"]
                    }
            if dict(rloc) not in list_of_places:
                list_of_places.append(dict(rloc))
                i = i + 1
        return list_of_places
    else:
        return None

def generate_rws(i_data):
    place = random.choice(i_data)
    rloc = {"typeID": place["type"],
            "locID": place["id"],
            "coordinates": place["coordinates"],
            "coordinates_alt": place["coordinates_alt"]
            }
    return rloc

def generate_nice(i_data, persontype):
    if persontype > 3:
        list_of_places = []
        i = 0
        while i < 1*persontype:
            place = random.choice(i_data)
            rloc = {"typeID": place["type"],
                    "locID": place["id"],
                    "coordinates": place["coordinates"],
                    "coordinates_alt": place["coordinates_alt"]
                    }
            if dict(rloc) not in list_of_places:
                list_of_places.append(dict(rloc))
                i = i + 1
        return list_of_places
    else:
        return None

def generate_health(i_data):
    place = random.choice(i_data)
    rloc = {"typeID": place["type"],
            "locID": place["id"],
            "coordinates": place["coordinates"],
            "coordinates_alt": place["coordinates_alt"]
            }
    return rloc

def generate_ilocation(ifn, agents):
    evening_schedule, activity, recreational_weekend_schedule, nicer_places, health_places = load_idata(ifn)
    for agent in agents:
        ifeveningschedule = generate_evs(evening_schedule, agent['typeID'])
        if ifeveningschedule != None:
            agent['locations'].append(dict(ifeveningschedule))
        ifactivity = generate_act(activity, agent['typeID'])
        if ifactivity != None:
            agent['locations'] = agent['locations'] + ifactivity
        agent['locations'].append(dict(generate_rws(recreational_weekend_schedule)))
        ifnice = generate_nice(nicer_places, agent['typeID'])
        if ifnice != None:
            agent['locations'] = agent['locations'] + ifnice
        agent['locations'].append(dict(generate_health(health_places)))


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