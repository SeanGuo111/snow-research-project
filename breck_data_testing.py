from datetime import date, datetime
from xml.sax.handler import DTDHandler
from xmlrpc.client import DateTime
import data_importing as di
import real_data_functions as func

from cmath import nan
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
#from sklearn.linear_model

def date_to_winter(date: datetime):
    current_year = date.year
    if (date.month <= 6):
        return f"{current_year - 1}-{current_year}"
    else:
        return f"{current_year}-{current_year + 1}"


def format_iowa_real_data(data: pd.DataFrame, include_estimated_temp: bool = False, include_estimated_precip: bool = False):
    """Returns the formatted real_data. Disregards all data less than 0.01 as inaccuracy. \n\nIndex is the year of the END of the winter season; for example, 1948 would represent the winter of 1947-1948."""
    data.replace({"M": np.nan}, inplace=True)

    # Station correct dtypes
    data["station"]: pd.Series = data["station"].astype("string")
    data["station_name"]: pd.Series = data["station_name"].astype("string")

    # Date, Year, Month, correct dtypes. Date to index, not dropped.
    data["day"] = pd.to_datetime(data["day"])
    data.rename({"day": "date"}, axis="columns", inplace=True)
    data.set_index("date", drop=False, inplace=True)
    data["year"] = data["date"].dt.year.astype('int32')
    data["month"] = data["date"].dt.month.astype('int32')

    # Winter: format is winter of "year-nextyear". Winter_year is the year representing the END of that winter.
    winter_column = pd.Series(dtype="string")
    winter_column = data["date"].apply(date_to_winter)
    data["winter_label"] = winter_column
    data["winter_year"] = data["winter_label"].str.slice(5, 10).astype('int32')


    # Snow -> float64
    # "int32" is int, "int64" is long, "int" lets python decide
    data["snow"] = data["snow"].astype('float64')

    # Replace less than 0.01 with nothing, Temps and Precip only where estimated = False
    data["snow"] = np.where((data["snow"] > 0) & (data["snow"] < 0.01), np.nan, data["snow"])
    data["precip"] = np.where((data["precip"] > 0) & (data["precip"] < 0.01), np.nan, data["precip"])

    if not include_estimated_precip:
        data["precip"] = np.where(data["precip_estimated"] == True, np.nan, data["precip"])

    if not include_estimated_temp:
        data["highc"] = np.where(data["temp_estimated"] == True, np.nan, data["highc"])
        data["lowc"] = np.where(data["temp_estimated"] == True, np.nan, data["lowc"])

    return data

# IMPORT DATA ---------------------------------------------------------
data_dict = di.import_all_data()
breck_data = data_dict["breck_data"]

# PREPARE DATA ---------------------------------------------------------
breck_data = format_iowa_real_data(breck_data, include_estimated_temp=True)
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
#func.largest_and_average_snowfall_events(breck_data, start_winter, end_winter)

# Average SWR for each year
#func.season_total_snow_water_ratio(breck_data, start_winter, end_winter)

# Largest x-event average
x = 10
#func.x_largest_snowfall_events_average(breck_data, start_winter, end_winter, x)

# Percentile event average
max_percentile = 20
#func.percentile_largest_snowfall_events_average(breck_data, start_winter, end_winter, max_percentile)

# Days of snow (threshold for snow to count)
#func.days_with_snow(breck_data, start_winter, end_winter)