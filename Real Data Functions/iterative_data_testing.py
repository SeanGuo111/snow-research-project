import data_preparing as dp
import real_data_functions as func
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np


import cartopy
import cartopy.crs as ccrs
import rasterio
from PIL import Image
import cartopy.io.shapereader as shpreader
from affine import Affine



# %% Grid Utility Functions -----------------------------------------------------------------------------------------------
def adjust_grid(grid_title, station_names):
    """Adjusts subplot grid to a 2x3 or 3x4 graph layout. Takes a overarching grid title as a parameter."""
    fig, axs = None, None
    if len(station_names) <= 3:
        fig, axs = plt.subplots(3,1, figsize=(6, 15)) # ndarray if one of two subplots() parameters > 1
    else:
        fig, axs = plt.subplots(3,4)
    
    axs = axs.flatten() # Flatten 2D to 1D for plt.sca() later to work
    plt.subplots_adjust(hspace=0.5, wspace=0.5)
    plt.suptitle(grid_title)
    
    return fig, axs

def get_grid_title(title, start_winter, end_winter, subplot=False):
    date_str = ""
    if subplot:
        date_str = f": {start_winter}-{end_winter}"
        return title + date_str
    
    if (start_winter != None or end_winter != None):
        start_winter_str = (start_winter or "")
        end_winter_str = (end_winter or "")
        
        if subplot:
            date_str = f": {start_winter_str}--{end_winter_str}"
        else:
            date_str = f": Winters {start_winter_str}--{end_winter_str}"
    
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
        start_winter_current, end_winter_current = func.get_start_end_winter_years(current_station, start_winter, end_winter)
        plt.title(get_grid_title(current_station_name, start_winter_current, end_winter_current, True))

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
        start_winter_current, end_winter_current = func.get_start_end_winter_years(current_station, start_winter, end_winter)
        plt.title(get_grid_title(current_station_name, start_winter_current, end_winter_current, True))
        text = f"p={dict['p-value']}; total change={dict['total_change']}; % change={dict['percentage_change']}"
        #text = f"p={dict['p-value']}; total change={dict['total_change']}"
        plt.text(0.4,0.08, text, horizontalalignment='center', verticalalignment='center', transform=current_axes.transAxes)

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
        start_winter_current, end_winter_current = func.get_start_end_winter_years(current_station, start_winter, end_winter)
        plt.title(get_grid_title(current_station_name, start_winter_current, end_winter_current, True))
        text = f"p={dict['p-value']}; total change={dict['total_change']}; % change={dict['percentage_change']}"
        #text = f"p={dict['p-value']}; total change={dict['total_change']}"
        plt.text(0.4,0.08, text, horizontalalignment='center', verticalalignment='center', transform=current_axes.transAxes)
        
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
        grid_func_allf(data_dict, station_names, func.all_temp, f"All Temperature Data", start_winter, end_winter)
        grid_func_allf(data_dict, station_names, func.all_precip, f"All Precip Data", start_winter, end_winter)
        grid_func_allf(data_dict, station_names, func.all_snowfall, f"All Snowfall Data", start_winter, end_winter)
    else:
        print("Invalid type.")


def iterative_average_temperature(type, data_dict, station_names, start_winter = None, end_winter = None):
    if type == "1b1":
        one_by_one_func(data_dict, station_names, func.average_temperature, start_winter, end_winter)
    elif type == "grid":
        grid_func_analysis(data_dict, station_names, func.average_temperature, f"Average Temperature of each Winter", start_winter, end_winter)
    else:
        print("Invalid type.")


def iterative_largest_snowfall_events(type, data_dict, station_names, start_winter = None, end_winter = None):
    if type == "1b1":
        one_by_one_func(data_dict, station_names, func.largest_snowfall_events, start_winter, end_winter)
    elif type == "grid":
        grid_func_analysis(data_dict, station_names, func.largest_snowfall_events, f"Largest Snowfall Event Size of each Winter", start_winter, end_winter)
    else:
        print("Invalid type.")

def iterative_total_snowfall(type, data_dict, station_names, start_winter = None, end_winter = None):
    if type == "1b1":
        one_by_one_func(data_dict, station_names, func.total_snowfall, start_winter, end_winter)
    elif type == "grid":
        grid_func_analysis(data_dict, station_names, func.total_snowfall, f"Total Snowfall of each Winter", start_winter, end_winter)
    else:
        print("Invalid type.")

def iterative_average_snowfall_events(type, data_dict, station_names, start_winter = None, end_winter = None):
    if type == "1b1":
        one_by_one_func(data_dict, station_names, func.average_snowfall_events, start_winter, end_winter)
    elif type == "grid":
        grid_func_analysis(data_dict, station_names, func.average_snowfall_events, f"Average Snowfall Event Size of each Winter", start_winter, end_winter)
    else:
        print("Invalid type.")


def iterative_x_largest_snowfall_events_average(type, data_dict, station_names, start_winter = None, end_winter = None, x: int = 10):
    if type == "1b1":
        one_by_one_func_analysis_parametered(data_dict, station_names, func.x_largest_snowfall_events_average, x, start_winter, end_winter)
    elif type == "grid":
        grid_func_analysis_parametered(data_dict, station_names, func.x_largest_snowfall_events_average, x, f"Average of {x}-Largest Snowfall Event Sizes each Winter", start_winter, end_winter)
    else:
        print("Invalid type.")


def iterative_percentage_largest_snowfall_events_average(type, data_dict, station_names, start_winter = None, end_winter = None, percentage: int = 20):
    if type == "1b1":
        one_by_one_func_analysis_parametered(data_dict, station_names, func.percentage_largest_snowfall_events_average, percentage, start_winter, end_winter)
    elif type == "grid":
        grid_func_analysis_parametered(data_dict, station_names, func.percentage_largest_snowfall_events_average, percentage, f"Average of Top {percentage}% Snowfall Events each Winter", start_winter, end_winter)
    else:
        print("Invalid type.")


def iterative_season_total_swr(type, data_dict, station_names, start_winter = None, end_winter = None, include_estimated_precip: bool = True):
    if type == "1b1":
        one_by_one_func_analysis_parametered(data_dict, station_names, func.season_total_swr, include_estimated_precip, start_winter, end_winter)
    elif type == "grid":
        grid_func_analysis_parametered(data_dict, station_names, func.season_total_swr, include_estimated_precip, f"Season Total Snow Water Ratio of each Winter", start_winter, end_winter)
    else:
        print("Invalid type.")


def iterative_number_days_with_snow(type, data_dict, station_names, start_winter = None, end_winter = None, threshold: float = 0):
    if type == "1b1":
        one_by_one_func(data_dict, station_names, func.number_days_with_snow, start_winter, end_winter)
    elif type == "grid":
        title = ""
        if threshold == 0:
            title = f"Number of Measurable Snow Events each Winter"
        else:
            title = f"Number of Snow Events Over {threshold} in. each Winter"
        grid_func_analysis_parametered(data_dict, station_names, func.number_days_with_snow, threshold, title, start_winter, end_winter)
    else:
        print("Invalid type.")


def iterative_all_functions(type, data_dict, station_names, start_winter=None, end_winter=None, 
                            include_estimated_precip: bool = True, x: int = 10, percentage: int = 20, threshold: float = 0, check_and_all = False):
    if check_and_all:
        iterative_check_days_temp_precip_snowfall(type, data_dict, station_names, start_winter, end_winter)
        
    iterative_average_temperature(type, data_dict, station_names, start_winter, end_winter)
    iterative_largest_snowfall_events(type, data_dict, station_names, start_winter, end_winter)
    iterative_total_snowfall(type, data_dict, station_names, start_winter, end_winter)
    iterative_average_snowfall_events(type, data_dict, station_names, start_winter, end_winter)

    iterative_x_largest_snowfall_events_average(type, data_dict, station_names, start_winter, end_winter, x)
    iterative_percentage_largest_snowfall_events_average(type, data_dict, station_names, start_winter, end_winter, percentage)
    iterative_season_total_swr(type, data_dict, station_names, start_winter, end_winter, include_estimated_precip)
    iterative_number_days_with_snow(type, data_dict, station_names, start_winter, end_winter, threshold)


def one_by_one_all_functions_grouped_by_station(data_dict, station_names, start_winter = None, end_winter = None):
    """Note: whereas all the other 1by1 functions display the same analytics in a row, this function displays the same stations in a row."""
    one_by_one_func(data_dict, station_names, func.all_functions, start_winter, end_winter)



#%% Map Function

def plot_map(data_dict, station_names, title, given_function, given_parameter=None, start_winter=None, end_winter=None):
    """Plots a map of Colorado for the given stations. Given parameter is x for x-largest, percentage for percentage-largest, and include-estimated-precip for swr"""
    """You must include start and end winter parameters for maps."""

    fig = plt.figure()

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
    extent = [-110, -100.6, 36, 41.7]
    ax.set_extent(extent, ccrs.PlateCarree()) # Sets US map
    
    shapename = 'admin_1_states_provinces_lakes'
    feature = cartopy.feature.NaturalEarthFeature(name=shapename, scale='110m', category='cultural', facecolor= (0.9375, 0.9375, 0.859375), edgecolor='black')
    ax.add_feature(feature)

    fig.suptitle(get_grid_title(title, start_winter, end_winter))

    
    # POINT PLOTTING -----------------------
    marker_sizes = np.where(points["p-value"] < 0.05, 120, 60)
    
    greatest_tc = np.ceil(np.max(np.abs(points["total_change"])))
    norm = mpl.colors.Normalize(vmin=-greatest_tc, vmax=greatest_tc)
    plt.scatter(x = points["lon"], y = points["lat"], transform=ccrs.PlateCarree(), s=marker_sizes, c=points["total_change"], norm=norm, cmap="seismic", marker='o', linewidths=0.5, edgecolors='black')
    
    cbar = plt.colorbar(orientation="vertical", shrink=0.75)
    plt.show()


def plot_raster():

    raster_path = "C:\\Users\\swguo\\VSCode Projects\\Snow Research\\US Physical Features\\CONUS-Natural-Color-Relief-Hydro\\CONUS_Natural_Color_Relief_Hydro.tif"
    im = Image.open(raster_path)


    fig = plt.figure()
    projection_aa = ccrs.AlbersEqualArea(central_longitude=-96, central_latitude=23, standard_parallels=(29.5, 45.5))
    ax = fig.add_axes([0, 0, 1, 1], projection=projection_aa, frameon=True) # Sets background (projection type)

    #extent_ax = [-109.046667, -102.046667, 37, 41]
    #ax.set_extent(extent_ax, ccrs.Geodetic())

    #extent_trans = projection_aa.transform_points(ccrs.Geodetic(), np.array([-109.046667, -102.046667]), np.array([37, 41]))
    #extent_img = (extent_trans[0][0], extent_trans[1][0], extent_trans[0][1], extent_trans[1][1])

    shapename = 'admin_1_states_provinces_lakes'
    states_shp = shpreader.natural_earth(resolution='110m',
                                          category='cultural', name=shapename)
    ax.add_geometries(shpreader.Reader(states_shp).geometries(), ccrs.PlateCarree())

    
    im = im.crop((3000, 2000, 6000, 8000))
    image = ax.imshow(im, origin='upper', transform=projection_aa)
    
    #plt.xlim(-10.046667, -10200.046667)
    #plt.ylim(37, 10000)

    

    
    
    plt.show()

#%% Code Running

def prepare_telluride_hermit(map_data):
    #Cutoff telluride years: >= 1912
    telluride_data = map_data["TELLURIDE 4WNW"]
    telluride_data = telluride_data[telluride_data["winter_year"] >= 1912]
    #Filter hermit 1993-2000
    hermit_data = map_data["HERMIT 7 ESE"]
    hermit_data["snow"] = np.where(((hermit_data["winter_year"] >= 1993) & (hermit_data["winter_year"] <= 2000)) | (hermit_data["winter_year"] == 2017), np.nan, hermit_data["snow"])

    return telluride_data, hermit_data

return_value = dp.import_all_rd(False, False, True)
# all_data = return_value["all_data"]["all_station_dict"] #48 stations
# all_station_names = return_value["all_data"]["all_station_names"] #48 stations

# sane_data = return_value["sane_data"]["sane_station_dict"] #12 stations
# sane_station_names = return_value["sane_data"]["sane_station_names"] #12 stations

map_data = return_value["map_data"]["map_station_dict"] #3 stations
map_station_names = return_value["map_data"]["map_station_names"] #3 stations
map_data["TELLURIDE 4WNW"], map_data["HERMIT 7 ESE"] = prepare_telluride_hermit(map_data)

start_winter = 1961
end_winter = 2022
x = 10
percentage = 20
include_estimated_precip = True


iterative_average_snowfall_events("1b1", map_data, map_station_names)


#iterative_number_days_with_snow("grid", map_data, map_station_names, end_winter=end_winter)
#iterative_all_functions("grid", map_data, map_station_names, end_winter=end_winter, check_and_all=False)
#iterative_percentage_largest_snowfall_events_average("grid", map_data, map_station_names, end_winter=end_winter, percentage=50)
#one_by_one_all_functions_grouped_by_station(map_data, map_station_names, start_winter, end_winter)





# %%
