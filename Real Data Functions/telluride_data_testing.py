import data_preparing as dp
import real_data_functions as func

# IMPORT DATA ---------------------------------------------------------
telluride_data = dp.import_from_source("Telluride RD.txt")

# PREPARE DATA ---------------------------------------------------------
telluride_data = dp.format_iowa_real_data(telluride_data, include_estimated_M_temp=True, include_estimated_M_precip=True)
telluride_data["station_name"][:] = "Telluride"
print(telluride_data)

# DO STUFF ----------------------------------------------------
# Gap until 6/1/1911
# First full winter year: 1912
# Another gap from 12/1/2008
# Last full winter year: 2008
start_winter = 1913
end_winter = 2022 

func.all_functions(telluride_data, start_winter, end_winter, check_and_all=False)