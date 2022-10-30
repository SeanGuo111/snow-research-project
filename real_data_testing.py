import data_importing as di
import real_data_functions as func

from cmath import nan
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
#from sklearn.linear_model



# IMPORT DATA ---------------------------------------------------------
data_dict = di.import_all_data()
breck_data = data_dict["breck_data"]
leadville_data = data_dict["leadville_data"]


# IMPORT DATA ---------------------------------------------------------
breck_data.set_index("day", drop=False, inplace=True)
leadville_data.set_index("day", drop=False, inplace=True)

# Breck preparations ---
# Set year column
breck_data['year'] = breck_data['day'].str.slice(0, 4)
breck_data['year'] = breck_data['year'].astype('int32')
# Missing Snow -> Nan
breck_data["snow"] = breck_data["snow"].replace("M", np.nan)
# Correct types
breck_data["snow"] = breck_data["snow"].astype('float32')
breck_data["precip"] = breck_data["precip"].astype('float32')

print(breck_data)

# DO STUFF ----------------------------------------------------
# precip "cut" from 8/26/1913, snow "cut" from 8/31/1913
# Data "good" from 7/1/1947
# Start from 1948
start_year = 1948
end_year = 2020


# Plot Precip
#func.all_precip(breck_data)

# Plot snowfall
#func.all_snowfall(breck_data)

# Max snowfall events for each year, and average
#func.largest_and_average_snowfall_events(breck_data, start_year, end_year)

# Average SWR for each year
func.average_snow_water_ratio(breck_data, start_year, end_year)

# Largest 3 event average
func.x_largest_snowfall_events_average(breck_data, start_year, end_year, 10)

# Days of snow
func.days_with_snow(breck_data, start_year, end_year)