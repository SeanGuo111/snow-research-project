
from cmath import nan
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from sklearn.linear_model import LinearRegression
import statsmodels.api as sm

def linreg(x_axis, y_axis):
    X = np.array(x_axis).reshape(-1,1)
    y = np.array(y_axis).reshape(-1,1)
    reg = LinearRegression()
    reg.fit(X, y)
    print("The linear model is: Y = {:.5} + {:.5}X".format(reg.intercept_[0], reg.coef_[0][0]))
    plt.plot(x_axis, reg.predict(X), c='blue', linewidth=2)

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


def largest_and_average_snowfall_events(data: pd.DataFrame, start_winter, end_winter):
    """Takes data and graphs the largest snowfall event from each winter.\n\nThe data has to have winter_year and snow columns."""
    # SEE IF THIS CAN BE CLEANED
    years_axis = np.arange(start_winter, end_winter + 1)
    max_axis = []
    average_axis = []

    for y in range(start_winter, end_winter + 1):
        current_winter_data = data[data["winter_year"] == y]
        #years_axis.append(current_winter_data["winter_label"].iloc[0])
        current_winter_snowfall = current_winter_data["snow"]
        
        max = current_winter_snowfall.max()
        average = current_winter_snowfall.replace(0.0, np.nan).mean()

        max_axis.append(max)
        average_axis.append(average)

    plt.plot(years_axis, average_axis, label = "Average Snowfall (in)", color="b")
    plt.scatter(years_axis, max_axis, label = "Max Snowfall (in)", color="r")
    plt.title(f"Snowfall Events from Winters of {start_winter}-{end_winter}")
    plt.xlim(start_winter, end_winter)
    plt.ylim(0, np.max(max_axis) + 1)
    plt.xlabel("Year")
    plt.ylabel("Snowfall (in)")
    plt.fill_between(years_axis, 0, average_axis, color="b", alpha = 0.5)

    plt.legend()
    plt.show()

def x_largest_snowfall_events_average(data: pd.DataFrame, start_winter, end_winter, x):
    """Takes data and graphs the average snowfall of the x largest events from each winter. Fits a line.\n\nThe data has to have winter_year and snow columns, and year index."""
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

    # Fit a line
    linreg(years_axis, average_axis)

    # Testing
    title = f"Average {x}-Largest Snowfall Events from {start_winter}-{end_winter}"
    basic_plot(years_axis, average_axis, "Year", f"Average of {x}-Largest Snowfall Events (in)", title, "r", "o", "")
    plt.xlim(start_winter, end_winter)
    plt.ylim(0, np.max(average_axis) + 1)
    plt.show()

# SWE vs SWR?
def average_snow_water_ratio(data: pd.DataFrame, start_winter, end_winter):
    """Takes data and graphs the bulk average snow-water ratio from each winter.\n\nThe data has to have winter_year, snow, and precip columns."""
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

    title = f"Average Snow Water Ratio from {start_winter}-{end_winter}"
    basic_plot(years_axis, average_axis, "Year", "Average Snow-Water Ratio", title, "y", line_style="-")
    plt.xlim(start_winter, end_winter)
    plt.ylim(bottom=0)
    plt.fill_between(years_axis, 0, average_axis, color="yellow", alpha = 0.5)
    plt.show()

def days_with_snow(data: pd.DataFrame, start_winter, end_winter, threshold):
    """Takes data and graphs the total number of days with snow each year.\n\nThe data has to have year and snow columns."""

    years_axis = np.arange(start_winter, end_winter + 1)
    days_axis = []

    for y in range(start_winter, end_winter + 1):
        current_winter_data = data[data["winter_year"] == y]
        current_winter_snow_days = current_winter_data[current_winter_data["snow"] > threshold]
        days_axis.append(len(current_winter_snow_days))

    title = f"Number of Snow days each Winter from {start_winter}-{end_winter}"
    basic_plot(years_axis, days_axis, "Year", "Number of Snowfall Days", title, "m", "o", "")
    plt.plot(years_axis, days_axis, "mo")
    plt.xlim(start_winter, end_winter)
    plt.ylim(bottom=0)
    plt.show()


