import respoi_process
import school_poi_process
import work_poi_process
import intersting_poi_process
import generate_agents
import generate_secondary_locations
import generate_interesting_locations
import generate_public_locations
import generate_commuters
import convert_poi
import convert_agents
import sys

# Only text to modify
file_prefix = "Szeged"
#file_prefix = "szeged_kaposvar_jaras"

# This file contains the residential locations
#   100x100 cell data
shapefile    = "100100_2019_" + file_prefix
respoi       = file_prefix + "_respoi.json"
schoolcsv    = "schoolpoi_" + file_prefix + ".csv"
schoolpoi    = file_prefix + "_schoolpoi.json"
workcsv      = "workpoi_" + file_prefix + ".csv"
workpoi      = file_prefix + "_workpoi.json"
icsv         = "interestingpoi_" + file_prefix + ".csv"
ipoi         = file_prefix + "_interestingpoi.json"
publiccsv    = "publicpoi" + file_prefix + ".csv"
publicpoi    = file_prefix + "_publicpoi.json"
#publicpoi    = "Szeged_publicpoi.json"
tempagentin  = file_prefix + "_agents_temp.json"
tempagentout = file_prefix + "_agents_temp_sec.json"
tempstat     = file_prefix + "_stat.txt"
magic        = file_prefix + "_magic_number.json"
#magic        = "Szeged_magic_number.json"
illness      = file_prefix + "_illness_number.json"
#illness      = "Szeged_illness_number.json"
comcsv       = file_prefix + "_commuters.csv"
comscsv      = file_prefix + "_commuter_students.csv"

tempfamlocation = file_prefix + "_famlocation_helper.json"

#agentout    = "agents.json"
#locationout = "locations.json"

def main(argv):
    if len(argv) > 1:
        # processsing csv files and creating needed json files (usually run only a few times when needed)
        respoi_process.process_input_data(file_prefix, shapefile, respoi)
        school_poi_process.process_input_data(file_prefix, schoolcsv, schoolpoi)
        work_poi_process.process_input_data(file_prefix, workcsv, workpoi)
        intersting_poi_process.process_input_data(file_prefix, icsv, ipoi)
    # default data generating when files are ready to be used
    for i in range(int(argv[0])):
        agentout = "agents"+str(i)+".json"
        locationout = "locations"+str(i)+".json"
        generate_agents.generate_agents(respoi, magic, illness, tempagentin, tempstat, comcsv, comscsv, tempfamlocation)
        generate_secondary_locations.generate_additional_locations(tempagentin, tempagentout, schoolpoi, workpoi)
        generate_public_locations.generate_additional_locations(tempagentout, tempagentin, publicpoi)
        generate_interesting_locations.generate_additional_locations(tempagentin, tempagentout, ipoi)
        convert_poi.convert_data(respoi, schoolpoi, workpoi, ipoi, publicpoi, tempfamlocation, locationout)
        convert_agents.convert_data(tempagentout, agentout)

if __name__ == "__main__":
   main(sys.argv[1:])