import useful_library
import json
import sys
from collections import OrderedDict

# Only text to modify
file_prefix = "Szeged"

# This file contains the residential locations
#   100x100 cell data

workpoi      = file_prefix + "_workpoi_old.json"
nworkpoi     = file_prefix + "_workpoi.json"

def location_type_standardizer(w_data):
    nw_data = []
    for item in w_data:
        if item['type'] != 4:
            item['type'] = 4
        places = item
        nw_data.append(places)
    adat = {"area": file_prefix, "places": nw_data}
    with open(nworkpoi, 'w') as f:
        json.dump(adat, f, indent="\t")

w_data = json.load(open(workpoi), object_pairs_hook=OrderedDict)
w_data = w_data["places"]
location_type_standardizer(w_data)