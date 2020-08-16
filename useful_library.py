import json
import random
import sys
from scipy import spatial
from scipy.spatial import distance

def order_by_place(odata, pindex):
    ndata = sorted(odata, key = lambda x: (x['locations'][pindex]['coordinates'][0], x['locations'][pindex]['coordinates'][1]))
    return ndata

def order_places(odata):
    ndata = sorted(odata, key = lambda x: (x['coordinates'][0], x['coordinates'][1]))
    return ndata

def load_data(filename, index_divide=False):
    '''
    Load a formatted JSON file with the places

    :param filename: Name of the file
    '''
    with open(filename, 'r') as f:
        _places = json.load(f)
        _places = _places["places"]
    temp_places = [v for v in sorted(_places, key=lambda item: item["subtype"])]
    if index_divide:
        base_places = [[] for _ in range(15)]
        for item in temp_places:
            base_places[item["type"]].append(item)
        return base_places
    else:
        return temp_places

def select_random_place(odata, place_type, how_many):
    list_of_places = []
    i = 0
    while i < how_many:
        place = random.choice(odata[place_type])
        rloc = {"typeID": place["type"],
                "locID": place["id"],
                "coordinates": place["coordinates"],
                "coordinates_alt": place["coordinates_alt"]
                }
        if dict(rloc) not in list_of_places:
            list_of_places.append(dict(rloc))
            i = i + 1
    return list_of_places

def create_distance_data(odata):
    ndata = []
    for item in odata:
        ndata.append(item["coordinates"] + item["coordinates_alt"])
    return ndata

def select_closer_places(odata, odata_distance, ref_place, how_many):
    list_of_places = []
    saving_list = []
    ref_vector = ref_place["coordinates"] + ref_place["coordinates_alt"]
    _, index = odata_distance.query(ref_vector)
    if round(how_many/2) + index < len(odata) and index - round(how_many/2) >= 0:
        i = 0
        while i < how_many:
            saving_list.append(index-round(how_many/2)+i)
            i = i + 1
    elif how_many + index < len(odata):
        i = 0
        while i < how_many:
            saving_list.append(index+i)
            i = i + 1
    elif index - how_many >= 0:
        i = 0
        while i < how_many:
            saving_list.append(index-how_many+i)
            i = i + 1
    for saved_place in saving_list:
        rloc = {"typeID": odata[saved_place]["type"],
                "locID": odata[saved_place]["id"],
                "coordinates": odata[saved_place]["coordinates"],
                "coordinates_alt": odata[saved_place]["coordinates_alt"]
                }
        list_of_places.append(dict(rloc))
    return list_of_places

class Switch(dict):
    def __getitem__(self, item):
        for key in self.keys():                   # iterate over the intervals
            if item in key:                       # if the argument is part of that interval
                return super().__getitem__(key)   # return its associated value
        raise KeyError(item)                      # if not in any interval, raise KeyError

def choose_percentage(percent):
    num = random.choice(range(1, 101))
    if num <= percent and num != 0:
        return True
    else:
        return False