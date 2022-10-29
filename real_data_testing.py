from cmath import nan
import data_importing as di

import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
#from sklearn.linear_model

def all_precip(data: pd.DataFrame):
    """Takes data and graphs all precip data.\n\nThe data has to have year and precip columns."""
    exact_precip_data = data[(data["precip_estimated"] == False) ]
    exact_precip = exact_precip_data["precip"]
    years_axis = exact_precip_data["year"]
    
    plt.plot(years_axis, exact_precip, label = "Precip")
    plt.xlabel("Year")
    plt.ylabel("Exact Melted Precip (in)")
    plt.title("All Exact Melted Precip ")
    plt.legend()
    plt.show()


def all_snowfall(data: pd.DataFrame):
    """Takes data and graphs all precip data.\n\nThe data has to have year and snowfall columns."""
    exact_snow = data["snow"]
    exact_snow = exact_snow.replace("M", np.nan)
    years_axis = data["year"]

    plt.plot(years_axis, exact_snow, label = "Snowfall")
    plt.xlabel("Year")
    plt.ylabel("Snowfall (in)")
    plt.title("All Snowfall")
    plt.legend()
    plt.show()


def largest_and_average_snowfall_events(data: pd.DataFrame, start_year, end_year):
    """Takes data and graphs the largest snowfall event from each year.\n\nThe data has to have year and snow columns."""
    # SEE IF THIS CAN BE CLEANED
    # LEGENDS????
    years_axis = np.arange(start_year, end_year + 1)
    max_axis = []
    average_axis = []


    for y in range(start_year, end_year + 1):
        current_year_data = data[data["year"] == y]
        current_year_snowfall = current_year_data["snow"]
        
        max = current_year_snowfall.max()
        average = current_year_snowfall.replace(0.0, np.nan).mean()

        max_axis.append(max)
        average_axis.append(average)

    plt.plot(years_axis, max_axis, "ro")
    plt.ylim(0, np.max(max_axis) + 5)

    plt.xlabel("Year")
    plt.ylabel("Snowfall (in)")
    plt.title(f"Largest Annual Snowfall Events from {start_year}-{end_year}")
    plt.show()

    plt.plot(years_axis, average_axis, "r-")
    plt.xlim(start_year, end_year)
    plt.ylim(0, np.max(average_axis) + 1)
    plt.fill_between(years_axis, 0, average_axis, color="red", alpha = 0.5)
    plt.title(f"Average Snowfall Event Size from {start_year}-{end_year}")
    plt.show()

def x_largest_snowfall_events_average(data: pd.DataFrame, start_year, end_year, x):
    """Takes data and graphs the average snowfall of the x largest events from each year.\n\nThe data has to have year and snow columns, and year index."""
    years_axis = np.arange(start_year, end_year + 1)
    average_axis = []

    for y in range(start_year, end_year + 1):
        current_year_data = data[data["year"] == y]
        current_year_snowfall = current_year_data["snow"]
        max_total = 0

        for i in range(x):
            current_max_index = current_year_snowfall.idxmax() # index is a year so loc. if it was an integer, than it would be iloc.
            max_total += current_year_snowfall.loc[current_max_index]
            current_year_excluded = current_year_snowfall.drop(current_max_index, inplace=False)
            current_year_snowfall = current_year_excluded
        
        average_axis.append(max_total / x)

    plt.plot(years_axis, average_axis, "ro")
    plt.xlim(start_year, end_year)
    plt.ylim(0, np.max(average_axis) + 1)
    plt.xlabel("Year")
    plt.ylabel(f"Average of {x}-Largest Snowfall Events")
    plt.title(f"Average {x}-Largest Snowfall Events from {start_year}-{end_year}")
    plt.show()

# SWE vs SWR?
def average_snow_water_ratio(data: pd.DataFrame, start_year, end_year):
    """Takes data and graphs the bulk average snow-water ratio from each year.\n\nThe data has to have year, snow, and precip columns."""
    years_axis = np.arange(start_year, end_year + 1)
    average_axis = []

    for y in range(start_year, end_year + 1):
        #Setup current year data
        current_year_data = data[data["year"] == y]
        current_year_data["snow"] = current_year_data["snow"].replace("M", np.nan)

        # Conditions
        swr_availability = (current_year_data["snow"] > 0) & (current_year_data["precip"] > 0) & (current_year_data["precip_estimated"] == False) & (current_year_data["highc"] < 2)
        current_year_swr_available = current_year_data[swr_availability]

        # Calculation
        snow_sum_array = np.sum(np.array(current_year_swr_available["snow"]))
        precip_sum_array = np.sum(np.array(current_year_swr_available["precip"]))
        SWR_average_array = snow_sum_array / precip_sum_array
        # try bulk: summing all snow
        if (y == 1982):
            print("s")

        average_axis.append(SWR_average_array)

    plt.plot(years_axis, average_axis, "y-")
    plt.xlim(start_year, end_year)
    plt.xlabel("Year")
    plt.ylabel("Average Snow-Water Ratio")
    plt.fill_between(years_axis, 0, average_axis, color="yellow", alpha = 0.5)
    plt.title(f"Average Snow Water Ratio from {start_year}-{end_year}")
    plt.show()

def days_with_snow(data: pd.DataFrame, start_year, end_year):
    """Takes data and graphs the total number of days with snow each year.\n\nThe data has to have year and snow columns."""

    years_axis = np.arange(start_year, end_year + 1)
    days_axis = []

    for y in range(start_year, end_year + 1):
        current_year_data = data[data["year"] == y]
        current_year_snow_days = current_year_data[current_year_data["snow"] > 0]
        days_axis.append(len(current_year_snow_days))

    plt.plot(years_axis, days_axis, "mo")
    plt.xlim(start_year, end_year)
    plt.ylim(0, 150)
    plt.xlabel("Year")
    plt.ylabel("Number of Snowfall Days")
    #plt.fill_between(years_axis, 0, days_axis, color="purple", alpha = 0.5)
    plt.title(f"Number of Snow days each year from {start_year}-{end_year}")
    plt.show()










# IMPORT DATA ---------------------------------------------------------
data_dict = di.import_all_data()
breck_data = data_dict["breck_data"]
leadville_data = data_dict["leadville_data"]


# DO STUFF -------------------------------------------------------------
# Quick Preparations ---
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

# Do stuff ----------------------------------------------------
# Get data
# precip "cut" from 8/26/1913, snow "cut" from 8/31/1913
# Data "good" from 7/1/1947
# Start from 1948
start_year = 1948
end_year = 2020



# Plot Precip
#all_precip(breck_data)

# Plot snowfall
#all_snowfall(breck_data)

# Max snowfall events for each year, and average
#largest_and_average_snowfall_events(breck_data, start_year, end_year)

# Average SWR for each year
#average_snow_water_ratio(breck_data, start_year, end_year)

# Largest 3 event average
x_largest_snowfall_events_average(breck_data, start_year, end_year, 10)

# Days of snow
days_with_snow(breck_data, start_year, end_year)