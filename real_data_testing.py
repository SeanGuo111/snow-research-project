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


def format_iowa_real_data(data: pd.DataFrame):
    """Returns the formatted real_data.\n\nIndex is the year of the START of the winter season; for example, 1947 would represent the winter of 1947-1948."""
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

    # Winter: format is winter of "year-nextyear". Winter_year is the year representing the start of that winter.
    winter_column = pd.Series(dtype="string")
    winter_column = data["date"].apply(date_to_winter)
    data["winter_label"] = winter_column
    data["winter_year"] = data["winter_label"].str.slice(0, 4).astype('int32')


    # Snow -> float64, Precip only where estimated = False
    # "int32" is int, "int64" is long, "int" lets python decide
    data["snow"] = data["snow"].astype('float64')
    data["precip"] = np.where(data["precip_estimated"] == False, data["precip"], np.nan)

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
# First "good" from 7/1/1947
# First full winter from 1947
start_winter = 1947
end_winter = 2020


# Plot Precip
#func.all_precip(breck_data)

# Plot snowfall
#func.all_snowfall(breck_data)

# Max snowfall events for each year, and average
#func.largest_and_average_snowfall_events(breck_data, start_winter, end_winter)

# Average SWR for each year
#func.average_snow_water_ratio(breck_data, start_winter, end_winter)

# Largest x-event average
x = 15
func.x_largest_snowfall_events_average(breck_data, start_winter, end_winter, x)

# Days of snow (threshold for snow to count)
threshold = 0
#func.days_with_snow(breck_data, start_winter, end_winter, threshold)