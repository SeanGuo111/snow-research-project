
from cmath import nan
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from sklearn.linear_model import LinearRegression
import statsmodels.api as sm

# UTILITY ------------------------------------------------------------------------------------------------------------------
def linreg(x_axis, y_axis, title, color):
    """Fits on a line from x and y axises, name, and color. Plots and displays equation and relevant statistics."""
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
    est = sm.OLS(y, X2)
    est2 = est.fit()
    print(est2.summary())


def basic_plot(x_axis, y_axis, x_label=None, y_label=None, title=None, color=None, marker=None, line_style=None):
    """Returns a basic graph. Does not include features such as x/y lims and shading. Legend label is the same as the y label."""
    plt.plot(x_axis, y_axis, label = y_label, color = color, marker = marker, ls = line_style)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.title(title)
    plt.legend()

# FUNCTIONS ------------------------------------------------------------------------------------------------------------------
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

def average_temperature(data: pd.DataFrame, start_winter, end_winter):
    """Takes data and graphs the average, average temperature from each winter.\n\nThe data has to have winter_year, highc, and lowc columns."""
    years_axis = np.arange(start_winter, end_winter + 1)
    average_axis = []

    for y in range(start_winter, end_winter + 1):
        if (y == 2020):
            print("sdf")
        current_winter_data = data[data["winter_year"] == y]
        current_winter_lows = current_winter_data["lowc"]
        current_winter_highs = current_winter_data["highc"]
        

        average_temp_by_day = (current_winter_lows + current_winter_highs) / 2
        average_temp_winter = np.average(average_temp_by_day)

        average_axis.append(average_temp_winter)
    
    title = f"Average Temperature from Winters of {start_winter}-{end_winter}"
    linreg(years_axis, average_axis, title, "green")
    basic_plot(years_axis, average_axis, "Year", "Average Temperature (C)", title, "purple", "o", line_style="")
    plt.xlim(start_winter, end_winter)
    plt.ylim(0, np.max(average_axis) + 1)
    plt.show()

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
    
    title = f"Average Snowfall Events from Winters of {start_winter}-{end_winter}"
    linreg(years_axis, average_axis, title, "green")
    basic_plot(years_axis, average_axis, "Year", "Average Snowfall (in)", title, "b", "o", line_style="")
    plt.xlim(start_winter, end_winter)
    plt.ylim(0, np.max(average_axis) + 1)
    plt.show()
    
    title = f"Largest Snowfall Events from Winters of {start_winter}-{end_winter}"
    linreg(years_axis, largest_axis, title, "blue")
    basic_plot(years_axis, largest_axis, "Year", "Largest Snowfall (in)", title, "r", "o", line_style="")
    plt.xlim(start_winter, end_winter)
    plt.ylim(0, np.max(largest_axis) + 1)
    plt.show()

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
    title = f"Average {x}-Largest Snowfall Events from {start_winter}-{end_winter}"
    linreg(years_axis, average_axis, title, "blue")
    basic_plot(years_axis, average_axis, "Year", f"Average of {x}-Largest Snowfall Events (in)", title, "r", "o", "")
    plt.xlim(start_winter, end_winter)
    plt.ylim(0, np.max(average_axis) + 1)
    plt.show()

def percentile_largest_snowfall_events_average(data: pd.DataFrame, start_winter, end_winter, percentile):
    """Takes data and graphs the average snowfall for a percentile of largest events for that winter. Fits a line.\n\nThe data has to have winter_year and snow columns."""
    years_axis = np.arange(start_winter, end_winter + 1)
    average_axis = []

    for y in range(start_winter, end_winter + 1):
        current_winter_data = data[data["winter_year"] == y]
        current_winter_snowfall = current_winter_data["snow"]

        snow_days_length = len(current_winter_snowfall[current_winter_snowfall > 0])
        amount_highest_winters = (int) (np.floor(snow_days_length * (percentile / 100)))
       
        max_total = 0

        for i in range(amount_highest_winters):
            current_max_index = current_winter_snowfall.idxmax() # index is a label (year) so loc. if it was an integer, than it would be iloc.
            max_total += current_winter_snowfall.loc[current_max_index]
            current_winter_excluded = current_winter_snowfall.drop(current_max_index, inplace=False)
            current_winter_snowfall = current_winter_excluded
        
        average_axis.append(max_total / amount_highest_winters)

 
    # Testing
    title = f"Average {percentile}th-Percentile Snowfall Events from {start_winter}-{end_winter}"
    linreg(years_axis, average_axis, title, "blue")
    basic_plot(years_axis, average_axis, "Year", f"Average of {percentile}%-Largest Snowfall Events (in)", title, "r", "o", "")
    plt.xlim(start_winter, end_winter)
    plt.ylim(0, np.max(average_axis) + 1)
    plt.show()


def season_total_snow_water_ratio(data: pd.DataFrame, start_winter, end_winter):
    """Takes data and graphs the season total (bulk) snow-water ratio from each winter.\n\nThe data has to have winter_year, snow, and precip columns."""
    years_axis = np.arange(start_winter, end_winter + 1)
    average_axis = []

    for y in range(start_winter, end_winter + 1):
        #Setup current year data
        current_winter_data = data[data["winter_year"] == y]

        # Conditions
        swr_availability = (current_winter_data["snow"] > 0) & (current_winter_data["precip"] > 0) & (current_winter_data["precip_estimated"] == False) & (current_winter_data["highc"] < 2)
        current_winter_swr_available = current_winter_data[swr_availability]

        # Calculation
        snow_sum = np.sum(np.array(current_winter_swr_available["snow"]))
        precip_sum = np.sum(np.array(current_winter_swr_available["precip"]))
        SWR_average = snow_sum / precip_sum

        average_axis.append(SWR_average)

    title = f"Season Total Snow Water Ratio from {start_winter}-{end_winter}"
    linreg(years_axis, average_axis, title, "purple")
    basic_plot(years_axis, average_axis, "Year", "Season Total Snow-Water Ratio", title, "y", "o", line_style="")
    plt.xlim(start_winter, end_winter)
    plt.ylim(bottom=0)
    #plt.fill_between(years_axis, 0, average_axis, color="yellow", alpha = 0.5)
    plt.show()

def days_with_snow(data: pd.DataFrame, start_winter, end_winter):
    """Takes data and graphs the total number of days with snow each year.\n\nThe data has to have year and snow columns."""

    years_axis = np.arange(start_winter, end_winter + 1)
    days_axis = []

    for y in range(start_winter, end_winter + 1):
        current_winter_data = data[data["winter_year"] == y]
        current_winter_snow_days = current_winter_data[current_winter_data["snow"] > 0]
        days_axis.append(len(current_winter_snow_days))

    title = f"Number of Snow days each Winter from {start_winter}-{end_winter}"
    linreg(years_axis, days_axis, title, "green")
    basic_plot(years_axis, days_axis, "Year", "Number of Snowfall Days", title, "cornflowerblue", "o", "")
    plt.xlim(start_winter, end_winter)
    plt.ylim(bottom=0)
    plt.show()


