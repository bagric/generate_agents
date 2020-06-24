import respoi_process
import school_poi_process
import generate_agents
import generate_secondary_locations
import convert_poi
import convert_agents

# Only text to modify
file_prefix = "Szeged"

# This file contains the residential locations
#   100x100 cell data
shapefile    = "100100_2019_" + file_prefix
respoi       = file_prefix + "_respoi.json"
schoolcsv    = "schoolpoi_" + file_prefix + ".csv"
schoolpoi    = file_prefix + "_schoolpoi.json"
tempagentin  = file_prefix + "_agents_temp.json"
tempagentout = file_prefix + "_agents_temp_sec.json"
tempstat     = file_prefix + "_stat.txt"
magic        = file_prefix + "_magic_number.json"

agentout    = "agents.json"
locationout = "locations.json"

# respoi_process.process_input_data(file_prefix, shapefile, respoi)
# school_poi_process.process_input_data(file_prefix, schoolcsv, schoolpoi)

generate_agents.generate_agents(respoi, magic, tempagentin, tempstat)
generate_secondary_locations.generate_additional_locations(tempagentin, tempagentout, schoolpoi)

convert_agents.convert_data(tempagentout, agentout)
#convert_poi.convert_data(respoi, schoolpoi, locationout)