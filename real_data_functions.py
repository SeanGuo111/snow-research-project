
from cmath import nan
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

def basic_plot(x_axis, y_axis, x_label=None, y_label=None, title=None, color=None, marker=None, line_style=None):
    """Returns a basic graph. Does not include features such as x/y lims and shading. Legend label is the same as the y label."""
    plt.plot(x_axis, y_axis, label = y_label, color = color, marker = marker, ls = line_style)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.title(title)
    plt.legend()

def all_precip(data: pd.DataFrame):
    """Takes data and graphs all precip data.\n\nThe data has to have year and precip columns."""
    exact_precip = data["precip"]
    years_axis = data["year"]
    
    basic_plot(years_axis, exact_precip, "Year", "Exact Melted Precip (in)", "All Exact Melted Precip")
    plt.show()


def all_snowfall(data: pd.DataFrame):
    """Takes data and graphs all precip data.\n\nThe data has to have year and snowfall columns."""
    exact_snow = data["snow"]
    years_axis = data["year"]

    basic_plot(years_axis, exact_snow, "Year", "Snow (in)", "All Snowfall")
    plt.show()


def largest_and_average_snowfall_events(data: pd.DataFrame, start_year, end_year):
    """Takes data and graphs the largest snowfall event from each year.\n\nThe data has to have year and snow columns."""
    # SEE IF THIS CAN BE CLEANED
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

    plt.plot(years_axis, average_axis, label = "Average Snowfall (in)", color = "r")
    plt.scatter(years_axis, max_axis, label = "Max Snowfall (in)", color="r")
    plt.title("Max and Average Snowfall Events")
    plt.xlim(start_year, end_year)
    plt.ylim(0, np.max(max_axis) + 1)
    plt.fill_between(years_axis, 0, average_axis, color="r", alpha = 0.5)
    plt.legend()
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

    title = f"Average {x}-Largest Snowfall Events from {start_year}-{end_year}"
    basic_plot(years_axis, average_axis, "Year", f"Average of {x}-Largest Snowfall Events", title, "r", "o", "")
    plt.xlim(start_year, end_year)
    plt.ylim(0, np.max(average_axis) + 1)
    plt.show()

# SWE vs SWR?
def average_snow_water_ratio(data: pd.DataFrame, start_year, end_year):
    """Takes data and graphs the bulk average snow-water ratio from each year.\n\nThe data has to have year, snow, and precip columns."""
    years_axis = np.arange(start_year, end_year + 1)
    average_axis = []

    for y in range(start_year, end_year + 1):
        #Setup current year data
        current_year_data = data[data["year"] == y]

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

    title = f"Average Snow Water Ratio from {start_year}-{end_year}"
    basic_plot(years_axis, average_axis, "Year", "Average Snow-Water Ratio", title, "y", line_style="-")
    plt.xlim(start_year, end_year)
    plt.fill_between(years_axis, 0, average_axis, color="yellow", alpha = 0.5)
    plt.show()

def days_with_snow(data: pd.DataFrame, start_year, end_year):
    """Takes data and graphs the total number of days with snow each year.\n\nThe data has to have year and snow columns."""

    years_axis = np.arange(start_year, end_year + 1)
    days_axis = []

    for y in range(start_year, end_year + 1):
        current_year_data = data[data["year"] == y]
        current_year_snow_days = current_year_data[current_year_data["snow"] > 0]
        days_axis.append(len(current_year_snow_days))

    title = f"Number of Snow days each year from {start_year}-{end_year}"
    basic_plot(years_axis, days_axis, "Year", "Number of Snowfall Days", title, "m", "o", "")
    plt.plot(years_axis, days_axis, "mo")
    plt.xlim(start_year, end_year)
    plt.ylim(0, 150)
    plt.show()


