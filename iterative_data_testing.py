import data_preparing as dp
import real_data_functions as func
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
import numpy as np

# %% Grid Utility Functions -----------------------------------------------------------------------------------------------
def adjust_grid(grid_title):
    """Adjusts subplot grid to a 3x4 graph layout. Takes a overarching grid title as a parameter."""
    fig, axs = plt.subplots(2,3) # ndarray if one of two subplots() parameters > 1
    axs = axs.flatten() # Flatten 2D to 1D for plt.sca() later to work
    plt.subplots_adjust(hspace=0.5, wspace=0.5)
    plt.suptitle(grid_title)
    
    return fig, axs

def get_grid_title(title, start_winter, end_winter):
    date_str = ""
    if (start_winter != None and end_winter != None):
        date_str = f" from Winters of {start_winter}-{end_winter}"
    return title + date_str


# %% One by One Functions -----------------------------------------------------------------------------------------------
def one_by_one_func_allf(data_dict, station_names, given_function, start_winter = None, end_winter = None):
    for current_station_name in station_names:
        current_station = data_dict[current_station_name]
        given_function(current_station, start_winter, end_winter)

def one_by_one_temp_precip_snowfall(data_dict, station_names, start_winter = None, end_winter = None):
    for current_station_name in station_names:
        current_station = data_dict[current_station_name]

        func.check_days(current_station, start_winter, end_winter)
        func.all_temp(current_station, start_winter, end_winter)
        func.all_precip(current_station, start_winter, end_winter)
        func.all_snowfall(current_station, start_winter, end_winter)

def one_by_one_all_functions(data_dict, station_names, start_winter = None, end_winter = None):
    for current_station_name in station_names:
        current_station = data_dict[current_station_name]
        func.all_functions(current_station, start_winter, end_winter)

    
# %% Grid Functions -----------------------------------------------------------------------------------------------
def grid_func_allf(data_dict, station_names, given_function, grid_title, start_winter = None, end_winter = None):
    grid_title = get_grid_title(grid_title, start_winter, end_winter)
    fig, axs = adjust_grid(grid_title)
    graph_counter = 0

    for current_station_name in station_names:
        current_station = data_dict[current_station_name]
        
        current_axes = axs[graph_counter]
        plt.sca(current_axes)
        given_function(current_station, start_winter, end_winter, show=False)
        plt.title(current_station_name)

        graph_counter += 1

    plt.show()

def grid_func_analysis(data_dict, station_names, given_function, grid_title, start_winter = None, end_winter = None):
    grid_title = get_grid_title(grid_title, start_winter, end_winter)
    fig, axs = adjust_grid(grid_title)
    graph_counter = 0

    for current_station_name in station_names:
        current_station = data_dict[current_station_name]
        
        current_axes = axs[graph_counter]
        plt.sca(current_axes)
        dict = given_function(current_station, start_winter=start_winter, end_winter=end_winter, show=False, figtext=False)
        plt.title(current_station_name)
        plt.text(0.3,0.08, f"p={dict['p-value']}; tc={dict['total change']}", horizontalalignment='center', verticalalignment='center', transform=current_axes.transAxes)

        graph_counter += 1

    plt.show()

def grid_all_temp_precip_snowfall(data_dict, station_names, start_winter = None, end_winter = None):
    grid_func_allf(data_dict, station_names, func.check_days, f"Day Count Check", start_winter, end_winter)
    grid_func_allf(data_dict, station_names, func.all_temp, f"All Temperature Data of {len(data_dict)} Colorado Stations", start_winter, end_winter)
    grid_func_allf(data_dict, station_names, func.all_precip, f"All Precip Data of {len(data_dict)} Colorado Stations", start_winter, end_winter)
    grid_func_allf(data_dict, station_names, func.all_snowfall, f"All Snowfall Data of {len(data_dict)} Colorado Stations", start_winter, end_winter)


def grid_average_temperature(data_dict, station_names, start_winter = None, end_winter = None):
    grid_func_analysis(data_dict, station_names, func.average_temperature, f"Average Temperature Data of {len(data_dict)} Colorado Stations", start_winter, end_winter)

# IMPLEMENT average/largest, x and % largest, and snow days for grids
# IMPLEMENT checkdays abstraction

def grid_season_total_swr(data_dict, station_names, start_winter = None, end_winter = None):
    grid_func_analysis(data_dict, station_names, func.season_total_snow_water_ratio, f"Season Total SWR of {len(data_dict)} Colorado Stations", start_winter, end_winter)

#%% Code Running
return_value = dp.import_all_rd()
all_station_names = return_value["station_names"] #12 stations
all_data = return_value["data"]
map_station_names = ["Colorado - Colorado Drainage Basin Climate Division","TELLURIDE 4WNW","HERMIT 7 ESE","WOLF CREEK PASS 1 E","RUXTON PARK"] #5 stations on 1960-1993
map_data = {}
for name in map_station_names:
    map_data[name] = all_data[name]



start_winter = 1960
end_winter = 1993

grid_all_temp_precip_snowfall(map_data, map_station_names, start_winter, end_winter)
grid_average_temperature(map_data, map_station_names, start_winter, end_winter)
grid_season_total_swr(map_data, map_station_names, start_winter, end_winter)
