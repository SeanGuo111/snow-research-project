
from cmath import nan
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from sklearn.linear_model import LinearRegression
import statsmodels.api as sm

# UTILITY ------------------------------------------------------------------------------------------------------------------
def get_start_end_winter_years(station):
    """Returns start and end winter for a given station. First and last years clipped."""
    start_winter = station["winter_year"].iloc[0] + 1
    end_winter = station["winter_year"].iloc[len(station)-1] - 1
    return start_winter, end_winter

def linreg(x_axis, y_axis, title, color):
    """Fits on a line from x and y axises, name, and color. Plots and displays equation and relevant statistics. Returns a dictionary of p-value and slope."""
    X = np.array(x_axis).reshape(-1,1)
    y = np.array(y_axis).reshape(-1,1)
    reg = LinearRegression()
    reg.fit(X, y)

    print()
    print(f"---{title}---")
    print("The linear model is: Y = {:.5} + {:.5}X".format(reg.intercept_[0], reg.coef_[0][0]))
    slope_over_timeframe = reg.coef_[0][0] * (len(y) - 1)
    print(f"The slope over the timeframe is {slope_over_timeframe}")
    plt.plot(x_axis, reg.predict(X), c=color, linewidth=2)

    X2 = sm.add_constant(X)
    est = sm.OLS(y, X2).fit()
    print(est.summary())

    dict = {}
    dict["p-value"] = np.round(est.pvalues[1], 4)
    dict["total change"] = np.round(slope_over_timeframe, 4)
    return dict


def basic_plot(x_axis, y_axis, x_label=None, y_label=None, title=None, color=None, marker=None, line_style=None):
    """Returns a basic graph. Does not include features such as x/y lims and shading."""
    plt.plot(x_axis, y_axis, label = y_label, color = color, marker = marker, ls = line_style)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.title(title)

# FUNCTIONS ------------------------------------------------------------------------------------------------------------------

# "ALL" FUNCTIONS, CHECK DAYS ------------------------------------------------------------------------------------------------------------------
def all_functions(data: pd.DataFrame, start_winter, end_winter, x = 10, percentage = 20, swr_include_estimated_precip = True, check_and_all = False):

    """Call all functions."""
    """Default x-largest-snowfall: 10"""
    """Default percentage-largest snowfall: 20%"""
    """Default swr inclusion of estimated precip"""

    if check_and_all:
        check_days(data)
        all_precip(data)
        all_snowfall(data)

    average_temperature(data, start_winter, end_winter)
    largest_and_average_snowfall_events(data, start_winter, end_winter)

    x_largest_snowfall_events_average(data, start_winter, end_winter, x)
    percentage_largest_snowfall_events_average(data, start_winter, end_winter, percentage)
    season_total_snow_water_ratio(data, start_winter, end_winter, swr_include_estimated_precip)
    average_days_with_snow(data, start_winter, end_winter)


def check_days(data: pd.DataFrame):
    """Checks that the data includes all days. Printed number should be close to 365.25"""
    first_year = data.iloc[0]["year"]
    last_year = data.iloc[len(data) - 1]["year"]
    print(len(data) / (last_year - first_year + 1))

    years_axis = np.arange(first_year, last_year + 1)
    days_axis = []
    for year in range(first_year, last_year + 1):
        days_axis.append(len(data[data["year"] == year]))

    plt.scatter(years_axis, days_axis)
    plt.show()

def all_temp(data: pd.DataFrame):
    """Takes data and graphs all average precip data.\n\nThe data has to have year and precip columns."""
    exact_temp = (data["lowc"] + data["highc"]) / 2
    years_axis = data["winter_year"]
    
    station_name = data["station_name"].iloc[0]
    title = f"{station_name}: All Average Temp" 
    basic_plot(years_axis, exact_temp, "Year", "Average Temp (in)", title)
    plt.show()

def all_precip(data: pd.DataFrame):
    """Takes data and graphs all precip data.\n\nThe data has to have year and precip columns."""
    exact_precip = data["precip"]
    years_axis = data["winter_year"]
    
    station_name = data["station_name"].iloc[0]
    title = f"{station_name}: All Melted Precip" 
    basic_plot(years_axis, exact_precip, "Year", "Melted Precip (in)", title)
    plt.show()


def all_snowfall(data: pd.DataFrame, show: bool = True, start_winter = None, end_winter = None):
    """Takes data and graphs all precip data.\n\nThe data has to have year and snowfall columns."""
    exact_snow = data["snow"]
    years_axis = data["winter_year"]

    station_name = data["station_name"].iloc[0]
    title = f"{station_name}: All Snowfall" 
    basic_plot(years_axis, exact_snow, "Year", "Snow (in)", title)

    if show:
        plt.show()

# ANALYSIS FUNCTIONS ------------------------------------------------------------------------------------------------------------------

def average_temperature(data: pd.DataFrame, start_winter, end_winter, show: bool = True):
    """Takes data and graphs the average, average temperature from each winter.\n\nThe data has to have winter_year, highc, and lowc columns.\n\n Sets up graph, but shows only if show set to true."""
    years_axis = np.arange(start_winter, end_winter + 1)
    average_axis = []

    for y in range(start_winter, end_winter + 1):
        
        current_winter_data = data[data["winter_year"] == y]
        current_winter_lows = current_winter_data["lowc"]
        current_winter_highs = current_winter_data["highc"]        

        average_temp_by_day = (current_winter_lows + current_winter_highs) / 2
        average_temp_winter = np.average(average_temp_by_day)

        average_axis.append(average_temp_winter)
    
    station_name = data["station_name"].iloc[0]
    title = f"{station_name}: Average Temperature from Winters of {start_winter}-{end_winter}"
    dict = linreg(years_axis, average_axis, title, "green")
    
    basic_plot(years_axis, average_axis, "Year", "Average Temperature (C)", title, "purple", "o", line_style="")
    plt.xlim(start_winter, end_winter)
    plt.ylim(np.min(average_axis) - 2, np.max(average_axis) + 2)
    
    if show:
        plt.show()

    return dict


def largest_and_average_snowfall_events(data: pd.DataFrame, start_winter, end_winter):
    """Takes data and graphs the largest snowfall event from each winter.\n\nThe data has to have winter_year and snow columns."""
    # SEE IF THIS CAN BE CLEANED
    years_axis = np.arange(start_winter, end_winter + 1)
    largest_axis = []
    average_axis = []

    for y in range(start_winter, end_winter + 1):
        current_winter_data = data[data["winter_year"] == y]
        current_winter_snowfall = current_winter_data["snow"]
        
        max = current_winter_snowfall.max()
        average = current_winter_snowfall.replace(0.0, np.nan).mean()

        largest_axis.append(max)
        average_axis.append(average)
    
    station_name = data["station_name"].iloc[0]
    title = f"{station_name}: Average Snowfall Events from Winters of {start_winter}-{end_winter}" 
    dict_average = linreg(years_axis, average_axis, title, "green")
    basic_plot(years_axis, average_axis, "Year", "Average Snowfall (in)", title, "b", "o", line_style="")
    plt.xlim(start_winter, end_winter)
    plt.ylim(0, np.max(average_axis) + 1)
    plt.figtext(0.65, 0.20, f"p-value: {dict_average['p-value']}")
    plt.figtext(0.65, 0.15, f"total change: {dict_average['total change']}")
    plt.show()
    
    station_name = data["station_name"].iloc[0]
    title = f"{station_name}: Largest Snowfall Events from Winters of {start_winter}-{end_winter}"
    dict_largest = linreg(years_axis, largest_axis, title, "blue")
    basic_plot(years_axis, largest_axis, "Year", "Largest Snowfall (in)", title, "r", "o", line_style="")
    plt.xlim(start_winter, end_winter)
    plt.ylim(0, np.max(largest_axis) + 1)
    plt.figtext(0.65, 0.20, f"p-value: {dict_largest['p-value']}")
    plt.figtext(0.65, 0.15, f"total change: {dict_largest['total change']}")

    plt.show()

    return dict_largest, dict_average


def x_largest_snowfall_events_average(data: pd.DataFrame, start_winter, end_winter, x):
    """Takes data and graphs the average snowfall of the x largest events from each winter. Fits a line.\n\nThe data has to have winter_year and snow columns."""
    years_axis = np.arange(start_winter, end_winter + 1)
    average_axis = []

    for y in range(start_winter, end_winter + 1):
        current_winter_data = data[data["winter_year"] == y]
        current_winter_snowfall = current_winter_data["snow"]
        max_total = 0

        for i in range(x):
            current_max_index = current_winter_snowfall.idxmax() # index is a label (year) so loc. if it was an integer, than it would be iloc.
            max_total += current_winter_snowfall.loc[current_max_index]
            current_winter_excluded = current_winter_snowfall.drop(current_max_index, inplace=False)
            current_winter_snowfall = current_winter_excluded
        
        average_axis.append(max_total / x)

 
    # Testing
    station_name = data["station_name"].iloc[0]
    title = f"{station_name}: Average {x}-Largest Snowfall Events from {start_winter}-{end_winter}"
    dict = linreg(years_axis, average_axis, title, "blue")
    basic_plot(years_axis, average_axis, "Year", f"Average of {x}-Largest Snowfall Events (in)", title, "r", "o", "")
    plt.xlim(start_winter, end_winter)
    plt.ylim(0, np.max(average_axis) + 1)
    plt.figtext(0.65, 0.20, f"p-value: {dict['p-value']}")
    plt.figtext(0.65, 0.15, f"total change: {dict['total change']}")
    plt.show()

    return dict


def percentage_largest_snowfall_events_average(data: pd.DataFrame, start_winter, end_winter, percentage):
    """Takes data and graphs the average snowfall for a percentile of largest events for that winter. Fits a line.\n\nThe data has to have winter_year and snow columns."""
    years_axis = np.arange(start_winter, end_winter + 1)
    average_axis = []

    for y in range(start_winter, end_winter + 1):
        current_winter_data = data[data["winter_year"] == y]
        current_winter_snowfall = current_winter_data["snow"]

        snow_days_length = len(current_winter_snowfall[current_winter_snowfall > 0])
        amount_highest_winters = (int) (np.floor(snow_days_length * (percentage / 100)))
       
        max_total = 0

        for i in range(amount_highest_winters):
            current_max_index = current_winter_snowfall.idxmax() # index is a label (year) so loc. if it was an integer, than it would be iloc.
            max_total += current_winter_snowfall.loc[current_max_index]
            current_winter_excluded = current_winter_snowfall.drop(current_max_index, inplace=False)
            current_winter_snowfall = current_winter_excluded
        
        average_axis.append(max_total / amount_highest_winters)

 
    # Testing
    station_name = data["station_name"].iloc[0]
    title = f"{station_name}: Average Top {percentage}% Snowfall Events from {start_winter}-{end_winter}"
    dict = linreg(years_axis, average_axis, title, "blue")
    basic_plot(years_axis, average_axis, "Year", f"Average of {percentage}%-Largest Snowfall Events (in)", title, "r", "o", "")
    plt.xlim(start_winter, end_winter)
    plt.ylim(0, np.max(average_axis) + 1)
    plt.figtext(0.65, 0.20, f"p-value: {dict['p-value']}")
    plt.figtext(0.65, 0.15, f"total change: {dict['total change']}")
    plt.show()

    return dict


def season_total_snow_water_ratio(data: pd.DataFrame, start_winter, end_winter, include_estimated_precip: bool = True):
    """Takes data and graphs the season total (bulk) snow-water ratio from each winter.\n\nThe data has to have winter_year, snow, and precip columns."""
    years_axis = np.arange(start_winter, end_winter + 1)
    average_axis = []

    for y in range(start_winter, end_winter + 1):
        #Setup current year data
        current_winter_data = data[data["winter_year"] == y]

        # Conditions
        swr_availability = (current_winter_data["snow"] > 0) & (current_winter_data["precip"] > 0) & (current_winter_data["highc"] < 2)
        if not include_estimated_precip:
            swr_availability = (current_winter_data["snow"] > 0) & (current_winter_data["precip"] > 0) & (current_winter_data["highc"] < 2) & (current_winter_data["precip_estimated"] == False)
        current_winter_swr_available = current_winter_data[swr_availability]

        # Calculation
        snow_sum = np.sum(np.array(current_winter_swr_available["snow"]))
        precip_sum = np.sum(np.array(current_winter_swr_available["precip"]))
        SWR_average = snow_sum / precip_sum

        average_axis.append(SWR_average)

    station_name = data["station_name"].iloc[0]
    title = f"{station_name}: Season Total Snow Water Ratio from {start_winter}-{end_winter}"
    dict = linreg(years_axis, average_axis, title, "purple")
    basic_plot(years_axis, average_axis, "Year", "Season Total Snow-Water Ratio", title, "y", "o", line_style="")
    plt.xlim(start_winter, end_winter)
    plt.ylim(bottom=0)
    plt.figtext(0.65, 0.20, f"p-value: {dict['p-value']}")
    plt.figtext(0.65, 0.15, f"total change: {dict['total change']}")
    plt.show()
        
    return dict


def average_days_with_snow(data: pd.DataFrame, start_winter, end_winter):
    """Takes data and graphs the total number of days with snow each year.\n\nThe data has to have year and snow columns."""

    years_axis = np.arange(start_winter, end_winter + 1)
    days_axis = []

    for y in range(start_winter, end_winter + 1):
        current_winter_data = data[data["winter_year"] == y]
        current_winter_snow_days = current_winter_data[current_winter_data["snow"] > 0]
        days_axis.append(len(current_winter_snow_days))

    station_name = data["station_name"].iloc[0]
    title = f"{station_name}: Number of Snow days each Winter from {start_winter}-{end_winter}"
    dict = linreg(years_axis, days_axis, title, "green")
    basic_plot(years_axis, days_axis, "Year", "Number of Snowfall Days", title, "cornflowerblue", "o", "")
    plt.figtext(0.65, 0.20, f"p-value: {dict['p-value']}")
    plt.figtext(0.65, 0.15, f"total change: {dict['total change']}")
    plt.xlim(start_winter, end_winter)
    plt.ylim(bottom=0)
    plt.show()

    return dict

