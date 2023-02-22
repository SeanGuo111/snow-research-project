import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
import cartopy.crs as ccrs

import netCDF4 as nc
import xarray as xr

#%% Utility Functions
def get_closest_ij(x_lat: np.ndarray, x_long: np.ndarray, given_lat_pt, given_long_pt):
    """Enter a given coordinate (lat, lon), and this returns a tuple (south_north, west_east) of the dimension values closest to that coordinate."""
    
    # find squared distance of every point on grid
    dist_sq = (x_lat-given_lat_pt)**2 + (x_long-given_long_pt)**2
    
    # 1D index of minimum dist_sq element
    minindex_flattened = dist_sq.argmin()
    
    # Get 2D index for latvals and lonvals arrays from 1D index
    return np.unravel_index(minindex_flattened, x_lat.shape)


def get_ctrl_url_list(include_timestrs: bool = False):
    """Retrieves list of all CTRL urls."""
    url_start = "https://rda.ucar.edu/thredds/dodsC/files/g/ds612.0/CTRL/"
    url_timestr_constraint = ",Times[0:24:2207]"
    # Set this up later

    # Starts with year 2000 anomaly as it only has 10-12
    ctrl_url_list = ["https://rda.ucar.edu/thredds/dodsC/files/g/ds612.0/CTRL/2000/wrf2d_d01_CTRL_SNOW_ACC_NC_200010-200012.nc?SNOW_ACC_NC[0:24:2207][435:556][452:591],Times[0:24:2207]"]
    
    
    # Excludes 2000 and 2013 anomalies
    for year in range(2001, 2013):
        current_url = url_start
        current_url += f"{year}/"

        
        # For leap year
        if (year % 4 == 0):
            ctrl_url_list.append(current_url + f"wrf2d_d01_CTRL_SNOW_ACC_NC_{year}01-{year}03.nc?SNOW_ACC_NC[0:24:2183][435:556][452:591],Times[0:24:2183]")
        else:
            ctrl_url_list.append(current_url + f"wrf2d_d01_CTRL_SNOW_ACC_NC_{year}01-{year}03.nc?SNOW_ACC_NC[0:24:2159][435:556][452:591],Times[0:24:2159]")

        ctrl_url_list.append(current_url + f"wrf2d_d01_CTRL_SNOW_ACC_NC_{year}04-{year}06.nc?SNOW_ACC_NC[0:24:2183][435:556][452:591],Times[0:24:2183]")
        ctrl_url_list.append(current_url + f"wrf2d_d01_CTRL_SNOW_ACC_NC_{year}07-{year}09.nc?SNOW_ACC_NC[0:24:2207][435:556][452:591],Times[0:24:2207]")
        ctrl_url_list.append(current_url + f"wrf2d_d01_CTRL_SNOW_ACC_NC_{year}10-{year}12.nc?SNOW_ACC_NC[0:24:2207][435:556][452:591],Times[0:24:2207]")


    # 2013 anomaly (all excluding 10-12)
    ctrl_url_list.append("https://rda.ucar.edu/thredds/dodsC/files/g/ds612.0/CTRL/2013/wrf2d_d01_CTRL_SNOW_ACC_NC_201301-201303.nc?SNOW_ACC_NC[0:24:2159][435:556][452:591],Times[0:24:2159]")
    ctrl_url_list.append("https://rda.ucar.edu/thredds/dodsC/files/g/ds612.0/CTRL/2013/wrf2d_d01_CTRL_SNOW_ACC_NC_201304-201306.nc?SNOW_ACC_NC[0:24:2183][435:556][452:591],Times[0:24:2183]")
    ctrl_url_list.append("https://rda.ucar.edu/thredds/dodsC/files/g/ds612.0/CTRL/2013/wrf2d_d01_CTRL_SNOW_ACC_NC_201307-201309.nc?SNOW_ACC_NC[0:24:2207][435:556][452:591],Times[0:24:2207]")
    return ctrl_url_list

def get_index_from_date(year, start_month):
    """Get index for a file in the urllist from a date range"""

    # Starts at 0 for 2000-10-12, 1 for 2001-01-03, 51 for 2013-07-09
    index = (year-2001)*4 + 1
    index += (int(start_month[0:2]) - 1)/3
    return int(index)

#%% Testing

# Single URL : https://rda.ucar.edu/thredds/dodsC/files/g/ds612.0/CTRL/2000/wrf2d_d01_CTRL_SNOW_ACC_NC_200010-200012.nc?SNOW_ACC_NC[0:2207][435:556][452:591]
# One dataset:
# dataset_ctrl_2000q4_subsetted: xr.DataArray = xr.open_dataset("https://rda.ucar.edu/thredds/dodsC/files/g/ds612.0/CTRL/2000/wrf2d_d01_CTRL_SNOW_ACC_NC_200010-200012.nc?SNOW_ACC_NC[0:24:2207][435:556][452:591]")
# print(dataset_ctrl_2000q4_subsetted.info)

# Complete data
ctrl_url_list = get_ctrl_url_list()
all_data: xr.Dataset = xr.open_mfdataset(ctrl_url_list, concat_dim="Time", combine="nested")
print(all_data.info)



# Mapping
# ax = plt.axes(projection=ccrs.LambertConformal())
# ax.coastlines() 
# test = dataset_ctrl_2000q4_subsetted["SNOW_ACC_NC"].sel(Time=1000)
# print(test.shape)
# test.plot()
# plt.show()