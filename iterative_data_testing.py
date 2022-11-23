import data_preparing as dp
import real_data_functions as func
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
import numpy as np

import cartopy.crs as ccrs
import cartopy.io.shapereader as shpreader
import shapely.geometry as sgeom
import matplotlib.patches as mpatches

# %% Grid Utility Functions -----------------------------------------------------------------------------------------------
def adjust_grid(grid_title, station_names):
    """Adjusts subplot grid to a 2x3 or 3x4 graph layout. Takes a overarching grid title as a parameter."""
    fig, axs = None, None
    if len(station_names) <= 6:
        fig, axs = plt.subplots(2,3) # ndarray if one of two subplots() parameters > 1
    else:
        fig, axs = plt.subplots(3,4)
    
    axs = axs.flatten() # Flatten 2D to 1D for plt.sca() later to work
    plt.subplots_adjust(hspace=0.5, wspace=0.5)
    plt.suptitle(grid_title)
    
    return fig, axs

def get_grid_title(title, start_winter, end_winter):
    date_str = ""
    if (start_winter != None and end_winter != None):
        date_str = f": Winters of {start_winter}-{end_winter}"
    return title + date_str


# %% 1b1 and grid generalization functions -----------------------------------------------------------------------------------------------
def one_by_one_func(data_dict, station_names, given_function, start_winter = None, end_winter = None):
    for current_station_name in station_names:
        current_station = data_dict[current_station_name]
        given_function(current_station, start_winter, end_winter)
        # By default figtext is shown, allowing for polymorphism of allf and analysis functions.


def one_by_one_func_analysis_parametered(data_dict, station_names, given_function, given_parameter, start_winter = None, end_winter = None):
    """Allows for parameter adjustment of precip_estimated (swr), x (x-largest), and percentage (percentage-largest)"""
    for current_station_name in station_names:
        current_station = data_dict[current_station_name]
        given_function(current_station, start_winter, end_winter, given_parameter)


def grid_func_allf(data_dict, station_names, given_function, grid_title, start_winter = None, end_winter = None):
    grid_title = get_grid_title(grid_title, start_winter, end_winter)
    fig, axs = adjust_grid(grid_title, station_names)
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
    fig, axs = adjust_grid(grid_title, station_names)
    graph_counter = 0

    for current_station_name in station_names:
        current_station = data_dict[current_station_name]
        
        current_axes = axs[graph_counter]
        plt.sca(current_axes)
        dict = given_function(current_station, start_winter=start_winter, end_winter=end_winter, show=False, figtext=False)
        plt.title(current_station_name)
        plt.text(0.3,0.08, f"p={dict['p-value']}; tc={dict['total_change']}", horizontalalignment='center', verticalalignment='center', transform=current_axes.transAxes)

        graph_counter += 1

    plt.show()


def grid_func_analysis_parametered(data_dict, station_names, given_function, given_parameter, grid_title, start_winter = None, end_winter = None):
    """Allows for parameter adjustment of precip_estimated (swr), x (x-largest), and percentage (percentage-largest)"""
    grid_title = get_grid_title(grid_title, start_winter, end_winter)
    fig, axs = adjust_grid(grid_title, station_names)
    graph_counter = 0

    for current_station_name in station_names:
        current_station = data_dict[current_station_name]
        
        current_axes = axs[graph_counter]
        plt.sca(current_axes)
        dict = given_function(current_station, start_winter, end_winter, given_parameter, show=False, figtext=False)
        plt.title(current_station_name)
        plt.text(0.3,0.08, f"p={dict['p-value']}; tc={dict['total_change']}", horizontalalignment='center', verticalalignment='center', transform=current_axes.transAxes)

        graph_counter += 1

    plt.show()

# %% True Iterative Functions -----------------------------------------------------------------------------------------------

def iterative_check_days_temp_precip_snowfall(type, data_dict, station_names, start_winter = None, end_winter = None):
    """Type determines whether or not the display the information as one by one graphs, or a grid of graphs. Enter '1b1' or 'grid'."""
    if type == "1b1":
        one_by_one_func(data_dict, station_names, func.check_days, start_winter, end_winter)
        one_by_one_func(data_dict, station_names, func.all_temp, start_winter, end_winter)
        one_by_one_func(data_dict, station_names, func.all_precip, start_winter, end_winter)
        one_by_one_func(data_dict, station_names, func.all_snowfall, start_winter, end_winter)
    elif type == "grid":
        grid_func_allf(data_dict, station_names, func.check_days, f"Day Count Check", start_winter, end_winter)
        grid_func_allf(data_dict, station_names, func.all_temp, f"All Temperature Data of {len(data_dict)} Colorado Stations", start_winter, end_winter)
        grid_func_allf(data_dict, station_names, func.all_precip, f"All Precip Data of {len(data_dict)} Colorado Stations", start_winter, end_winter)
        grid_func_allf(data_dict, station_names, func.all_snowfall, f"All Snowfall Data of {len(data_dict)} Colorado Stations", start_winter, end_winter)
    else:
        print("Invalid type.")


def iterative_average_temperature(type, data_dict, station_names, start_winter = None, end_winter = None):
    if type == "1b1":
        one_by_one_func(data_dict, station_names, func.average_temperature, start_winter, end_winter)
    elif type == "grid":
        grid_func_analysis(data_dict, station_names, func.average_temperature, f"Average Temperature Data of {len(data_dict)} Colorado Stations", start_winter, end_winter)
    else:
        print("Invalid type.")


def iterative_largest_snowfall_events(type, data_dict, station_names, start_winter = None, end_winter = None):
    if type == "1b1":
        one_by_one_func(data_dict, station_names, func.largest_snowfall_events, start_winter, end_winter)
    elif type == "grid":
        grid_func_analysis(data_dict, station_names, func.largest_snowfall_events, f"Largest Snowfall Event Data of {len(data_dict)} Colorado Stations", start_winter, end_winter)
    else:
        print("Invalid type.")


def iterative_average_snowfall_events(type, data_dict, station_names, start_winter = None, end_winter = None):
    if type == "1b1":
        one_by_one_func(data_dict, station_names, func.average_snowfall_events, start_winter, end_winter)
    elif type == "grid":
        grid_func_analysis(data_dict, station_names, func.average_snowfall_events, f"Average Snowfall Event Data of {len(data_dict)} Colorado Stations", start_winter, end_winter)
    else:
        print("Invalid type.")


def iterative_x_largest_snowfall_events_average(type, data_dict, station_names, start_winter = None, end_winter = None, x: int = 10):
    if type == "1b1":
        one_by_one_func_analysis_parametered(data_dict, station_names, func.x_largest_snowfall_events_average, x, start_winter, end_winter)
    elif type == "grid":
        grid_func_analysis_parametered(data_dict, station_names, func.x_largest_snowfall_events_average, x, f"Average {x}-Largest Snowfall Events of {len(data_dict)} Colorado Stations", start_winter, end_winter)
    else:
        print("Invalid type.")


def iterative_percentage_largest_snowfall_events_average(type, data_dict, station_names, start_winter = None, end_winter = None, percentage: int = 20):
    if type == "1b1":
        one_by_one_func_analysis_parametered(data_dict, station_names, func.percentage_largest_snowfall_events_average, percentage, start_winter, end_winter)
    elif type == "grid":
        grid_func_analysis_parametered(data_dict, station_names, func.percentage_largest_snowfall_events_average, percentage, f"Average Top {percentage}% Snowfall Events of {len(data_dict)} Colorado Stations", start_winter, end_winter)
    else:
        print("Invalid type.")


def iterative_season_total_swr(type, data_dict, station_names, start_winter = None, end_winter = None, include_estimated_precip: bool = True):
    if type == "1b1":
        one_by_one_func_analysis_parametered(data_dict, station_names, func.season_total_swr, include_estimated_precip, start_winter, end_winter)
    elif type == "grid":
        grid_func_analysis_parametered(data_dict, station_names, func.season_total_swr, include_estimated_precip, f"Season Total Snow Water Ratio of {len(data_dict)} Colorado Stations", start_winter, end_winter)
    else:
        print("Invalid type.")


def iterative_average_days_with_snow(type, data_dict, station_names, start_winter = None, end_winter = None):
    if type == "1b1":
        one_by_one_func(data_dict, station_names, func.average_days_with_snow, start_winter, end_winter)
    elif type == "grid":
        grid_func_analysis(data_dict, station_names, func.average_days_with_snow, f"Number of Snow days each Winter of {len(data_dict)} Colorado Stations", start_winter, end_winter)
    else:
        print("Invalid type.")


def iterative_all_functions(type, data_dict, station_names, start_winter=None, end_winter=None, include_estimated_precip: bool = True, x: int = 10, percentage: int = 20, check_and_all = False):
    if check_and_all:
        iterative_check_days_temp_precip_snowfall(type, data_dict, station_names, start_winter, end_winter)
        
    iterative_average_temperature(type, data_dict, station_names, start_winter, end_winter)
    iterative_largest_snowfall_events(type, data_dict, station_names, start_winter, end_winter)
    iterative_average_snowfall_events(type, data_dict, station_names, start_winter, end_winter)

    iterative_x_largest_snowfall_events_average(type, data_dict, station_names, start_winter, end_winter, x)
    iterative_percentage_largest_snowfall_events_average(type, data_dict, station_names, start_winter, end_winter, percentage)
    iterative_season_total_swr(type, data_dict, station_names, start_winter, end_winter, include_estimated_precip)
    iterative_average_days_with_snow(type, data_dict, station_names, start_winter, end_winter)


def one_by_one_all_functions_grouped_by_station(data_dict, station_names, start_winter = None, end_winter = None):
    """Note: whereas all the other 1by1 functions display the same analytics in a row, this function displays the same stations in a row."""
    one_by_one_func(data_dict, station_names, func.all_functions, start_winter, end_winter)



#%% Map Function

def plot_map(data_dict, station_names, title, given_function, given_parameter=None, start_winter=None, end_winter=None):
    """Plots a map of Colorado for the given stations. Given parameter is x for x-largest, percentage for percentage-largest, and include-estimated-precip for swr"""
    
    fig = plt.figure(figsize=(20,10))

    # GET STATION INFORMATION ------------------------
    points: pd.DataFrame = pd.DataFrame(columns=["name", "lon", "lat", "p-value", "total_change"])
    for current_station_name in station_names:
        current_station = data_dict[current_station_name]
        returned_dict = {}
        if given_parameter==None:
             returned_dict = given_function(current_station, start_winter, end_winter, show=False, figtext=False)
        else:
             returned_dict = given_function(current_station, start_winter, end_winter, given_parameter, show=False, figtext=False)
        
        p_value: float = returned_dict['p-value']
        total_change: float = returned_dict['total_change']
        lon: float = current_station["lon"].iloc[0]
        lat: float = current_station["lat"].iloc[0]

        new_point = {"name": current_station_name, "lon": lon, "lat": lat, "p-value": p_value, "total_change": total_change}
        points.loc[len(points.index)] = new_point

    fig.clf()

    # MAP SETUP ------------------------
    # Lambert Conformal vs Plate Carree?
    ax = fig.add_axes([0, 0, 1, 1], projection=ccrs.PlateCarree(), frameon=False) # Sets background (projection type)
    ax.set_extent([-110, -100.6, 36, 41.7], ccrs.PlateCarree()) # Sets US map
    shapename = 'admin_1_states_provinces_lakes'
    ax.natural_earth_shp(name=shapename, resolution='110m', category='cultural', facecolor= (0.9375, 0.9375, 0.859375), edgecolor='black')
    #ax.add_raster()
    fig.suptitle(get_grid_title(title, start_winter, end_winter))

    
    # POINT PLOTTING -----------------------
    marker_sizes = np.where(points["p-value"] < 0.05, 100, 60)
    
    greatest_tc = np.ceil(np.max(np.abs(points["total_change"])))
    norm = mpl.colors.Normalize(vmin=-greatest_tc, vmax=greatest_tc)
    plt.scatter(x = points["lon"], y = points["lat"], transform=ccrs.PlateCarree(), s=marker_sizes, c=points["total_change"], norm=norm, cmap="seismic", marker='o', linewidths=0.5, edgecolors='black')
    
    ax = plt.gca()
    cbar = plt.colorbar(orientation="vertical", pad=0.01)
    plt.show()


    

#%% Code Running
return_value = dp.import_all_rd()
all_station_names = return_value["station_names"] #12 stations
all_data = return_value["data"]
map_station_names = ["Colorado - Colorado Drainage Basin Climate Division","TELLURIDE 4WNW","HERMIT 7 ESE","WOLF CREEK PASS 1 E","RUXTON PARK"] #5 stations on 1960-1993
map_data = {} # has to be a dict with keys and values
for name in map_station_names:
    map_data[name] = all_data[name]

start_winter = 1960
end_winter = 1993

plot_map(all_data, all_station_names, f"Average Temperature Data of {len(all_station_names)} Colorado Stations", func.average_temperature)
#iterative_all_functions("grid", map_data, map_station_names, start_winter, end_winter)
#one_by_one_all_functions_grouped_by_station(map_data, map_station_names, start_winter, end_winter)

