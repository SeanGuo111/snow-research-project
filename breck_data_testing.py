from datetime import date, datetime
from xml.sax.handler import DTDHandler
from xmlrpc.client import DateTime
import data_preparing as dp
import real_data_functions as func

from cmath import nan
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
#from sklearn.linear_model


# IMPORT DATA ---------------------------------------------------------
data_dict = dp.import_all_data()
breck_data = data_dict["breck_data"]

# PREPARE DATA ---------------------------------------------------------
breck_data = dp.format_iowa_real_data(breck_data, include_estimated_M_temp=True, include_estimated_M_precip=False)
print(breck_data)

# DO STUFF ----------------------------------------------------
# precip "cut" from 8/26/1913, snow "cut" from 8/31/1913
# First "good" from 7/1/1947
# First full winter from 1948
start_winter = 1948
end_winter = 2020


# Plot Precip
#func.all_precip(breck_data)

# Plot snowfall
#func.all_snowfall(breck_data)

# Plot average temperature
func.average_temperature(breck_data, start_winter, end_winter)

# Largest and average snowfall events for each year
func.largest_and_average_snowfall_events(breck_data, start_winter, end_winter)

# Average SWR for each year
func.season_total_snow_water_ratio(breck_data, start_winter, end_winter)

# Largest x-event average
x = 10
func.x_largest_snowfall_events_average(breck_data, start_winter, end_winter, x)

# Percentile event average
max_percentile = 20
func.percentile_largest_snowfall_events_average(breck_data, start_winter, end_winter, max_percentile)

# Days of snow (threshold for snow to count)
func.days_with_snow(breck_data, start_winter, end_winter)