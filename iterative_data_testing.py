import data_preparing as dp
import real_data_functions as func
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
import numpy as np

def one_by_one_all_snowfall(all_data, station_names, start_winter = None, end_winter = None):
    for current_station_name in station_names:
        current_station = all_data[current_station_name]
        func.all_snowfall(current_station, show=False)
        
        if start_winter != None and end_winter != None:
            plt.xlim(start_winter,end_winter)

        plt.show()

def one_by_one_all_functions(all_data, station_names, start_winter = None, end_winter = None):
    for current_station_name in station_names:

        current_station = all_data[current_station_name]
        if (start_winter == None):
            start_winter = func.get_start_end_winter_years(current_station)[0]
        if (end_winter == None):
            end_winter = func.get_start_end_winter_years(current_station)[1]

        func.all_functions(current_station, start_winter, end_winter)


def grid_all_snowfall(all_data, station_names, start_winter = None, end_winter = None):
    plt.subplots_adjust(hspace=0.5, wspace=0.5)
    plt.suptitle("All Snowfall Data of 16 Colorado Stations")
    graph_counter = 1

    for current_station_name in station_names:
        current_station = all_data[current_station_name]
        
        plt.subplot(4, 4, graph_counter)
        func.all_snowfall(current_station, show=False)
        plt.title(current_station_name)
        
        if start_winter != None and end_winter != None:
            plt.xlim(start_winter,end_winter)

        graph_counter += 1

    plt.show()

def grid_average_temperature(all_data, station_names, start_winter = None, end_winter = None):
    fig, axs = plt.subplots(3,4)
    # ndarray if one of two subplots() parameters > 1
    axs = axs.flatten()

    plt.subplots_adjust(hspace=0.5, wspace=0.5)
    plt.suptitle("Average Temperature of 16 Colorado Stations")
    graph_counter = 0

    for current_station_name in station_names:

        current_station = all_data[current_station_name]
        if (start_winter == None):
            start_winter = func.get_start_end_winter_years(current_station)[0]
        if (end_winter == None):
            end_winter = func.get_start_end_winter_years(current_station)[1]

        current_axs = axs[graph_counter]
        plt.sca(current_axs) # only possible after axs flattened 2D -> 1D
    
        dict = func.average_temperature(current_station, start_winter, end_winter, show=False)
        plt.title(current_station_name)
        plt.text(0.3,0.08, f"p={dict['p-value']}; tc={dict['total change']}", horizontalalignment='center', verticalalignment='center', transform=current_axs.transAxes)

        graph_counter += 1

    plt.show()


station_metadata = dp.import_from_source("Colorado Station Metadata.txt")
return_value = dp.import_all_rd()
all_station_names = return_value["station_names"] #12 stations
all_data = return_value["data"]
map_station_names = ["Colorado - Colorado Drainage Basin Climate Division","TELLURIDE 4WNW","HERMIT 7 ESE","WOLF CREEK PASS 1 E","RUXTON PARK"] #5 stations on 1960-1993
map_data = {}
for name in map_station_names:
    map_data[name] = all_data[name]

start_winter = 1960
end_winter = 1993

one_by_one_all_snowfall(map_data, map_station_names)
one_by_one_all_functions(map_data, map_station_names)
grid_all_snowfall(map_data, map_station_names)
grid_average_temperature(map_data, map_station_names)
