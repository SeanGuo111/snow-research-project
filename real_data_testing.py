import data_importing as di
import real_data_functions as func

from cmath import nan
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
#from sklearn.linear_model

def format_iowa_real_data(data: pd.DataFrame):
    """Returns the formatted real_data.\n -Makes day of type datetime64 and the index, keeps day as column.\n """
    # Station correct dtypes
    data["station"]: pd.Series = data["station"].astype("string")
    data["station_name"]: pd.Series = data["station_name"].astype("string")

    # Day, Year, Month correct dtypes. Day -> Index
    data["day"] = pd.to_datetime(data["day"])
    data.set_index("day", drop=False, inplace=True)
    data["year"] = data["day"].dt.year.astype('int32')
    data["month"] = data["day"].dt.month.astype('int32')

    # Snow -> int64, Ms -> nan, Precip -> Nan where estimated
    # "int32" is int, "int64" is long, "int" lets python decide
    data["snow"] = data["snow"].replace("M", np.nan).astype('float64')
    data["precip"].mask(data["precip_estimated"] == True, nan, inplace=True)
    # Also works: data["precip"] = np.where(data["precip_estimated"] == True, nan, data["precip"])

    return data

# IMPORT DATA ---------------------------------------------------------
data_dict = di.import_all_data()
breck_data = data_dict["breck_data"]
leadville_data = data_dict["leadville_data"]


# PREPARE DATA ---------------------------------------------------------
breck_data = format_iowa_real_data(breck_data)
leadville_data = format_iowa_real_data(leadville_data)

print(breck_data)

# DO STUFF ----------------------------------------------------
# precip "cut" from 8/26/1913, snow "cut" from 8/31/1913
# Data "good" from 7/1/1947
# Start from 1948
start_year = 1948
end_year = 2020


# Plot Precip
func.all_precip(breck_data)

# Plot snowfall
func.all_snowfall(breck_data)

# Max snowfall events for each year, and average
func.largest_and_average_snowfall_events(breck_data, start_year, end_year)

# Average SWR for each year
func.average_snow_water_ratio(breck_data, start_year, end_year)

# Largest 3 event average
func.x_largest_snowfall_events_average(breck_data, start_year, end_year, 10)

# Days of snow
func.days_with_snow(breck_data, start_year, end_year)