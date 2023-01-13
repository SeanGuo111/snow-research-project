
from cmath import nan
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from sklearn.linear_model import LinearRegression
import statsmodels.api as sm

#%% UTILITY FUNCTIONS------------------------------------------------------------------------------------------------------------------
def get_start_end_winter_years(station, start_winter = None, end_winter = None):
    """Returns start and end winter for a given station. If given start and end winters, then those are simply returned."""
    """Otherwise, the second and second-to-last winter years are chosen from the dataset and returned."""
    if (start_winter == None):
        start_winter = station["winter_year"].iloc[0] + 1
    if (end_winter == None):
        end_winter = station["winter_year"].iloc[len(station)-1] - 1
    return start_winter, end_winter

def remove_nan_zero_years(x_axis, y_axis):
    """Creates removes x and y values nan/0 years."""
    array_valid = ~(np.isnan(y_axis) | np.where(y_axis == 0, True, False))
    x_axis = x_axis[array_valid]
    y_axis = y_axis[array_valid]

    return x_axis, y_axis

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
    start_year_linreg_point = (reg.coef_[0][0] * X[0]) + reg.intercept_[0]
    percentage_over_timeframe = 100 * (slope_over_timeframe / start_year_linreg_point)[0]
    print(f"The total change over the timeframe is {slope_over_timeframe}")
    print(f"The percentage change over the timeframe is {percentage_over_timeframe}")

    plt.plot(x_axis, reg.predict(X), c=color, linewidth=2)

    X2 = sm.add_constant(X)
    est = sm.OLS(y, X2).fit()
    print(est.summary())

    dict = {}
    dict['p-value'] = np.round(est.pvalues[1], 3)
    dict['total_change'] = np.round(slope_over_timeframe, 2)
    dict['percentage_change'] = np.round(percentage_over_timeframe, 2)
    return dict


def basic_plot(x_axis, y_axis, x_label=None, y_label=None, title=None, color=None, marker=None, line_style=None):
    """Returns a basic graph. Does not include features such as x/y lims and shading."""
    plt.plot(x_axis, y_axis, label = y_label, color = color, marker = marker, ls = line_style)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.title(title)

# FUNCTIONS ------------------------------------------------------------------------------------------------------------------

#%% "ALL" FUNCTIONS, CHECK DAYS ------------------------------------------------------------------------------------------------------------------
def all_functions(data: pd.DataFrame, start_winter=None, end_winter=None, x:int = 10, percentage:int = 20, swr_include_estimated_precip:bool = True, threshold:float = 10, check_and_all = False):

    """Call all functions."""
    """If start/end winters are not given, then they are inferred in the child function from the second and second-to-last year."""
    """Default x-largest-snowfall: 10"""
    """Default percentage-largest snowfall: 20%"""
    """Default swr inclusion of estimated precip"""

    if check_and_all:
        check_days(data, start_winter, end_winter)
        all_temp(data, start_winter, end_winter)
        all_precip(data, start_winter, end_winter)
        all_snowfall(data, start_winter, end_winter)

    average_temperature(data, start_winter, end_winter)
    average_snowfall_events(data, start_winter, end_winter)
    largest_snowfall_events(data, start_winter, end_winter)

    x_largest_snowfall_events_average(data, start_winter, end_winter, x)
    percentage_largest_snowfall_events_average(data, start_winter, end_winter, percentage)
    season_total_swr(data, start_winter, end_winter, swr_include_estimated_precip)
    number_days_with_snow(data, start_winter, end_winter, threshold)


def check_days(data: pd.DataFrame, start_winter=None, end_winter=None, show: bool = True):
    """Checks that the data includes all days. Printed number should be close to 365.25"""
    """Still, excluding the first and last winter year."""
    start_winter, end_winter = get_start_end_winter_years(data, start_winter, end_winter)
    subsetted_data = data[(data["year"] >= start_winter) & (data["year"] <= end_winter)]
    print(len(subsetted_data) / (end_winter - start_winter + 1))

    years_axis = np.arange(start_winter, end_winter + 1)
    days_axis = np.array([])
    for year in range(start_winter, end_winter + 1):
        days_axis = np.append(days_axis, len(data[data["year"] == year]))

    station_name = data["station_name"].iloc[0]
    plt.title(f"{station_name}: Day Count Check")
    plt.scatter(years_axis, days_axis)

    if show: 
        plt.show()


def all_temp(data: pd.DataFrame, start_winter=None, end_winter=None, show: bool = True):
    """Takes data and graphs all average precip data.\n\nThe data has to have year and precip columns."""
    exact_temp = (data["lowc"] + data["highc"]) / 2
    years_axis = data["winter_year"]
    
    station_name = data["station_name"].iloc[0]
    title = f"{station_name}: All Average Temp" 
    basic_plot(years_axis, exact_temp, "Year", "Temp (C)", title)
    
    if start_winter != None:
        plt.xlim(left=start_winter)
    if end_winter != None:
        plt.xlim(right=end_winter)
    
    if show:
        plt.show()

def all_precip(data: pd.DataFrame, start_winter=None, end_winter=None, show: bool = True):
    """Takes data and graphs all precip data.\n\nThe data has to have year and precip columns."""
    exact_precip = data["precip"]
    years_axis = data["winter_year"]
    
    station_name = data["station_name"].iloc[0]
    title = f"{station_name}: All Melted Precip" 
    basic_plot(years_axis, exact_precip, "Year", "Melted Precip (in)", title)
    
    if start_winter != None:
        plt.xlim(left=start_winter)
    if end_winter != None:
        plt.xlim(right=end_winter)

    if show: 
        plt.show()


def all_snowfall(data: pd.DataFrame, start_winter = None, end_winter = None, show: bool = True):
    """Takes data and graphs all precip data.\n\nThe data has to have year and snowfall columns."""
    exact_snow = data["snow"]
    years_axis = data["winter_year"]

    station_name = data["station_name"].iloc[0]
    title = f"{station_name}: All Snowfall" 
    basic_plot(years_axis, exact_snow, "Year", "Snow (in)", title)

    if start_winter != None:
        plt.xlim(left=start_winter)
    if end_winter != None:
        plt.xlim(right=end_winter)

    if show:
        plt.show()

#%% ANALYSIS FUNCTIONS ------------------------------------------------------------------------------------------------------------------

def average_temperature(data: pd.DataFrame, start_winter=None, end_winter=None, show: bool = True, figtext:bool=True):
    """Takes data and graphs the average, average temperature from each winter.\n\nThe data has to have winter_year, highc, and lowc columns.\n\n Sets up graph, but shows only if show set to true."""
    start_winter, end_winter = get_start_end_winter_years(data, start_winter, end_winter)
    years_axis = np.arange(start_winter, end_winter + 1)
    average_axis = np.array([])

    for y in range(start_winter, end_winter + 1):
        
        current_winter_data = data[data["winter_year"] == y]
        current_winter_lows = current_winter_data["lowc"]
        current_winter_highs = current_winter_data["highc"]        

        average_temp_by_day = (current_winter_lows + current_winter_highs) / 2
        average_temp_winter = np.average(average_temp_by_day)

        average_axis = np.append(average_axis, average_temp_winter)
    
    years_axis, average_axis = remove_nan_zero_years(years_axis, average_axis)
    station_name = data["station_name"].iloc[0]
    title = f"{station_name}: Average Temperature from Winters of {start_winter}-{end_winter}"
    dict = linreg(years_axis, average_axis, title, "green")
    
    basic_plot(years_axis, average_axis, "Year", "Average Temp (C)", title, "purple", "o", line_style="")
    plt.xlim(start_winter, end_winter)
    plt.ylim(np.min(average_axis) - 2, np.max(average_axis) + 2)
    
    if figtext:
        plt.figtext(0.65, 0.20, f"p-value: {dict['p-value']}")
        plt.figtext(0.65, 0.15, f"total change: {dict['total_change']}")
    if show:
        plt.show()

    return dict


def largest_snowfall_events(data: pd.DataFrame, start_winter=None, end_winter=None, show: bool=True, figtext:bool=True):
    """Takes data and graphs the largest snowfall event from each winter.\n\nThe data has to have winter_year and snow columns. Start/end winter can be None."""
    start_winter, end_winter = get_start_end_winter_years(data, start_winter, end_winter)
    years_axis = np.arange(start_winter, end_winter + 1)
    largest_axis = np.array([])

    for y in range(start_winter, end_winter + 1):
        current_winter_data = data[data["winter_year"] == y]
        current_winter_snowfall = current_winter_data["snow"]
        
        largest = current_winter_snowfall.max()
        largest_axis = np.append(largest_axis, largest)
    
    years_axis, largest_axis = remove_nan_zero_years(years_axis, largest_axis)
    station_name = data["station_name"].iloc[0]
    title = f"{station_name}: Largest Snowfall Events from Winters of {start_winter}-{end_winter}"
    dict = linreg(years_axis, largest_axis, title, "blue")
    
    basic_plot(years_axis, largest_axis, "Year", "Largest Snowfall (in)", title, "r", "o", line_style="")
    plt.xlim(start_winter, end_winter)
    plt.ylim(0, np.max(largest_axis) + 1)
    
    if figtext:
        plt.figtext(0.65, 0.20, f"p-value: {dict['p-value']}")
        plt.figtext(0.65, 0.15, f"total change: {dict['total_change']}")
    if show:
        plt.show()

    return dict

def total_snowfall(data: pd.DataFrame, start_winter=None, end_winter=None, show:bool=True, figtext:bool=True):
    """Takes data and graphs the total amount of snowfall each year.\n\nThe data has to have year and snow columns."""
    start_winter, end_winter = get_start_end_winter_years(data, start_winter, end_winter)
    years_axis = np.arange(start_winter, end_winter + 1)
    totals_axis = np.array([])

    for y in range(start_winter, end_winter + 1):
        current_winter_data = data[data["winter_year"] == y]
        current_winter_snowfall = current_winter_data["snow"]
        
        total = np.sum(current_winter_snowfall)
        totals_axis = np.append(totals_axis, total)

    years_axis, totals_axis = remove_nan_zero_years(years_axis, totals_axis)
    station_name = data["station_name"].iloc[0]
    
    title = f"{station_name}: Total Snowfall each Winter from {start_winter}-{end_winter}"
    
    dict = linreg(years_axis, totals_axis, title, "black")
    
    basic_plot(years_axis, totals_axis, "Year", "Snowfall (in)", title, "orange", "o", "")
    plt.xlim(start_winter, end_winter)
    plt.ylim(bottom=0)
    
    if figtext:
        plt.figtext(0.65, 0.20, f"p-value: {dict['p-value']}")
        plt.figtext(0.65, 0.15, f"total change: {dict['total_change']}")
    if show:
        plt.show()

    return dict

def average_snowfall_events(data: pd.DataFrame, start_winter=None, end_winter=None, show: bool=True, figtext:bool=True):
    """Takes data and graphs the average snowfall event from each winter.\n\nThe data has to have winter_year and snow columns. Start/end winter can be None."""
    # SEE IF THIS CAN BE CLEANED
    start_winter, end_winter = get_start_end_winter_years(data, start_winter, end_winter)
    years_axis = np.arange(start_winter, end_winter + 1)
    average_axis = np.array([])

    for y in range(start_winter, end_winter + 1):
        current_winter_data = data[data["winter_year"] == y]
        current_winter_snowfall = current_winter_data["snow"]
        
        average = current_winter_snowfall.replace(0.0, np.nan).mean()
        average_axis = np.append(average_axis, average)
    
    years_axis, average_axis = remove_nan_zero_years(years_axis, average_axis)
    station_name = data["station_name"].iloc[0]
    title = f"{station_name}: Average Snowfall Events from Winters of {start_winter}-{end_winter}" 
    dict = linreg(years_axis, average_axis, title, "green")
    
    basic_plot(years_axis, average_axis, "Year", "Average Snowfall (in)", title, "b", "o", line_style="")
    plt.xlim(start_winter, end_winter)
    plt.ylim(0, np.max(average_axis) + 1)
    
    if figtext:
        plt.figtext(0.65, 0.20, f"p-value: {dict['p-value']}")
        plt.figtext(0.65, 0.15, f"total change: {dict['total_change']}")
    if show:
        plt.show()

    return dict


def x_largest_snowfall_events_average(data: pd.DataFrame, start_winter=None, end_winter=None, x:int=10, show:bool=True, figtext:bool=True):
    """Takes data and graphs the average snowfall of the x largest events from each winter. Fits a line.\n\nThe data has to have winter_year and snow columns."""
    start_winter, end_winter = get_start_end_winter_years(data, start_winter, end_winter)
    years_axis = np.arange(start_winter, end_winter + 1)
    average_axis = np.array([])

    for y in range(start_winter, end_winter + 1):
        current_winter_data = data[data["winter_year"] == y]
        current_winter_snowfall = current_winter_data["snow"]
        max_total = 0

        for i in range(x):
            if ((current_winter_snowfall == 0).all() or current_winter_snowfall.isnull().all()):
                max_total = np.nan
                break

            current_max_index = current_winter_snowfall.idxmax() # index is a label (year) so loc. if it was an integer, than it would be iloc.
            max_total += current_winter_snowfall.loc[current_max_index]
            current_winter_excluded = current_winter_snowfall.drop(current_max_index, inplace=False)
            current_winter_snowfall = current_winter_excluded
        
        if not np.isnan(max_total):
            average_axis = np.append(average_axis, (max_total / x))
        else:
            average_axis = np.append(average_axis, np.nan)

    years_axis, average_axis = remove_nan_zero_years(years_axis, average_axis)
    station_name = data["station_name"].iloc[0]
    title = f"{station_name}: Average {x}-Largest Snowfall Events from {start_winter}-{end_winter}"
    dict = linreg(years_axis, average_axis, title, "blue")

    basic_plot(years_axis, average_axis, "Year", f"Snowfall (in)", title, "r", "o", "")
    plt.xlim(start_winter, end_winter)
    plt.ylim(0, np.max(average_axis) + 1)
    
    if figtext:
        plt.figtext(0.65, 0.20, f"p-value: {dict['p-value']}")
        plt.figtext(0.65, 0.15, f"total change: {dict['total_change']}")
    if show:
        plt.show()

    return dict


def percentage_largest_snowfall_events_average(data: pd.DataFrame, start_winter=None, end_winter=None, percentage:int=20, show:bool=True, figtext:bool=True):
    """Takes data and graphs the average snowfall for a percentile of largest events for that winter. Fits a line.\n\nThe data has to have winter_year and snow columns."""
    """In the case that the percentage is too selective, andn there are not enough events to make an accurate percentage, the single largest event is used."""
    """Ex. if the chosen percentage is 20%, and there are 4 snow events that year, then the largest of the 4 is chosen for that year"""
    
    start_winter, end_winter = get_start_end_winter_years(data, start_winter, end_winter)
    years_axis = np.arange(start_winter, end_winter + 1)
    average_axis = np.array([])
    
    for y in range(start_winter, end_winter + 1):
        current_winter_data = data[data["winter_year"] == y]
        current_winter_snowfall = current_winter_data["snow"]

        snow_days_length = len(current_winter_snowfall[current_winter_snowfall > 0])
        if (snow_days_length == 0):
            average_axis = np.append(average_axis, np.nan)
            continue
        amount_highest_winters = (int) (np.ceil(snow_days_length * (percentage / 100)))
        
       
        max_total = 0

        for i in range(amount_highest_winters):
            current_max_index = current_winter_snowfall.idxmax() # index is a label (year) so loc. if it was an integer, than it would be iloc.
            max_total += current_winter_snowfall.loc[current_max_index]
            current_winter_excluded = current_winter_snowfall.drop(current_max_index, inplace=False)
            current_winter_snowfall = current_winter_excluded
        
        average_axis = np.append(average_axis, (max_total / amount_highest_winters))

    years_axis, average_axis = remove_nan_zero_years(years_axis, average_axis)
    station_name = data["station_name"].iloc[0]
    title = f"{station_name}: Average Top {percentage}% Snowfall Events from {start_winter}-{end_winter}"
    dict = linreg(years_axis, average_axis, title, "blue")

    basic_plot(years_axis, average_axis, "Year", f"Snowfall (in)", title, "r", "o", "")
    plt.xlim(start_winter, end_winter)
    plt.ylim(0, np.max(average_axis) + 1)
    
    if figtext:
        plt.figtext(0.65, 0.20, f"p-value: {dict['p-value']}")
        plt.figtext(0.65, 0.15, f"total change: {dict['total_change']}")
    if show:
        plt.show()

    return dict


def season_total_swr(data: pd.DataFrame, start_winter=None, end_winter=None, include_estimated_precip: bool = True, show:bool=True, figtext:bool=True):
    """Takes data and graphs the season total (bulk) snow-water ratio from each winter.\n\nThe data has to have winter_year, snow, and precip columns."""
    start_winter, end_winter = get_start_end_winter_years(data, start_winter, end_winter)
    years_axis = np.arange(start_winter, end_winter + 1)
    average_axis = np.array([])

    for y in range(start_winter, end_winter + 1):
        #Setup current year data
        current_winter_data = data[data["winter_year"] == y]

        # Conditions
        swr_availability = (current_winter_data["snow"] > 0) & (current_winter_data["precip"] > 0) & (current_winter_data["highc"] < 2)
        if not include_estimated_precip:
            swr_availability = (current_winter_data["snow"] > 0) & (current_winter_data["precip"] > 0) & (current_winter_data["highc"] < 2) & (current_winter_data["precip_estimated"] == False)
        current_winter_swr_available = current_winter_data[swr_availability]
        
        if (len(current_winter_swr_available) == 0):
            average_axis = np.append(average_axis, np.nan)
            continue

        # Calculation
        snow_sum = np.sum(np.array(current_winter_swr_available["snow"]))
        precip_sum = np.sum(np.array(current_winter_swr_available["precip"]))
        SWR_average = snow_sum / precip_sum

        average_axis = np.append(average_axis, SWR_average)

    years_axis, average_axis = remove_nan_zero_years(years_axis, average_axis)
    station_name = data["station_name"].iloc[0]
    title = f"{station_name}: Season Total Snow Water Ratio from {start_winter}-{end_winter}"
    dict = linreg(years_axis, average_axis, title, "purple")

    basic_plot(years_axis, average_axis, "Year", "SWR", title, "y", "o", line_style="")
    plt.xlim(start_winter, end_winter)
    plt.ylim(bottom=0)
    if figtext:
        plt.figtext(0.65, 0.20, f"p-value: {dict['p-value']}")
        plt.figtext(0.65, 0.15, f"total change: {dict['total_change']}")
    if show:
        plt.show()
        
    return dict


def number_days_with_snow(data: pd.DataFrame, start_winter=None, end_winter=None, threshold:float=0, show:bool=True, figtext:bool=True):
    """Takes data and graphs the total number of days with snow each year.\n\nThe data has to have year and snow columns."""
    start_winter, end_winter = get_start_end_winter_years(data, start_winter, end_winter)
    years_axis = np.arange(start_winter, end_winter + 1)
    days_axis = np.array([])

    for y in range(start_winter, end_winter + 1):
        current_winter_data = data[data["winter_year"] == y]
        current_winter_snow_days = current_winter_data[current_winter_data["snow"] > threshold]
        
        days_axis = np.append(days_axis, len(current_winter_snow_days))

    years_axis, days_axis = remove_nan_zero_years(years_axis, days_axis)
    station_name = data["station_name"].iloc[0]
    if threshold == 0:
        title = f"{station_name}: Number of Measureable Snow Events each Winter from {start_winter}-{end_winter}"
    else:
        title = f"{station_name}: Number of Snow Events Over {threshold} in. each Winter from {start_winter}-{end_winter}"
    dict = linreg(years_axis, days_axis, title, "green")
    
    basic_plot(years_axis, days_axis, "Year", "# Events", title, "cornflowerblue", "o", "")
    plt.xlim(start_winter, end_winter)
    plt.ylim(bottom=0)
    
    if figtext:
        plt.figtext(0.65, 0.20, f"p-value: {dict['p-value']}")
        plt.figtext(0.65, 0.15, f"total change: {dict['total_change']}")
    if show:
        plt.show()

    return dict



