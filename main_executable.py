import respoi_process
import school_poi_process
import work_poi_process
import intersting_poi_process
import generate_agents
import generate_secondary_locations
import generate_interesting_locations
import convert_poi
import convert_agents
import sys

# Only text to modify
file_prefix = "Szeged"

# This file contains the residential locations
#   100x100 cell data
shapefile    = "100100_2019_" + file_prefix
respoi       = file_prefix + "_respoi.json"
schoolcsv    = "schoolpoi_" + file_prefix + ".csv"
schoolpoi    = file_prefix + "_schoolpoi.json"
workcsv      = "workpoi_" + file_prefix + ".csv"
workpoi      = file_prefix + "_workpoi.json"
icsv         = "interestingpoi" + file_prefix + ".csv"
ipoi         = file_prefix + "_interestingpoi.json"
tempagentin  = file_prefix + "_agents_temp.json"
tempagentout = file_prefix + "_agents_temp_sec.json"
tempstat     = file_prefix + "_stat.txt"
magic        = file_prefix + "_magic_number.json"

agentout    = "agents.json"
locationout = "locations.json"

def main(argv):
    if len(argv)<1:
        # processsing csv files and creating needed json files (usually run only a few times when needed)
        respoi_process.process_input_data(file_prefix, shapefile, respoi)
        school_poi_process.process_input_data(file_prefix, schoolcsv, schoolpoi)
        work_poi_process.process_input_data(file_prefix, workcsv, workpoi)
        intersting_poi_process.process_input_data(file_prefix, icsv, ipoi)
        #convert_poi.convert_data(respoi, schoolpoi, workpoi, ipoi, locationout)
    # default data generating when files are ready to be used
    generate_agents.generate_agents(respoi, magic, tempagentin, tempstat)
    generate_secondary_locations.generate_additional_locations(tempagentin, tempagentout, schoolpoi, workpoi)
    generate_interesting_locations.generate_additional_locations(tempagentout, tempagentin, ipoi)
    convert_agents.convert_data(tempagentin, agentout)
    convert_poi.convert_data(respoi, schoolpoi, workpoi, ipoi, locationout)

if __name__ == "__main__":
   main(sys.argv[1:])