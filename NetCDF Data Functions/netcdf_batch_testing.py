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


def get_url_list(set_name: str, every_24_hr: bool = True, include_timestrs: bool = True):
    """Retrieves list of all WRF simulation urls."""
    """set_name: 'CTRL' or 'PGW'"""
    """every_24_hr sets the function sets to function to subset to every 24 hrs of the dataset, at each midnight. """
    """include_timestrs sets the function to include another data variable which gives a formatted date. """
    
    ctrl_url_list = []
    num_hrs_list = [2159, 2183, 2207, 2207]
    
    url_start = f"https://rda.ucar.edu/thredds/dodsC/files/g/ds612.0/{set_name}/"
    every_24_hr_time_constraint = ""
    if every_24_hr:
        every_24_hr_time_constraint = ":24"

    # Date range list setting
    date_range_list = ["200504-200506", "200507-200509", "200510-200512"]
    for year in range(2006, 2013): # missing data in PGW 200501-200503
        for quarter in range(0, 4): 
            start_month = str((3*quarter) + 1)
            end_month = str((3*quarter) + 3)
            if start_month != "10":
                start_month = "0" + start_month
                end_month = "0" + end_month

            date_range = f"{year}{start_month}-{year}{end_month}"
            date_range_list.append(date_range)
    date_range_list.append("201301-201303")
    date_range_list.append("201304-201306")
    date_range_list.append("201307-201309")    
    
    for date_range in date_range_list:
        year = int(date_range[0:4])
        quarter = int((int(date_range[4:6]) - 1)/3)
        
        current_url = url_start
        current_url += f"{year}/wrf2d_d01_{set_name}_SNOW_ACC_NC_"

        # Hours
        number_hrs = num_hrs_list[quarter]
        if (year % 4 == 0 and quarter == 0):
            number_hrs = 2183
        
        current_url += f"{date_range}.nc?SNOW_ACC_NC[0{every_24_hr_time_constraint}:{number_hrs}][435:556][452:591]"
        
        if (include_timestrs):
            current_url += f",Times[0{every_24_hr_time_constraint}:{number_hrs}]"
        
        ctrl_url_list.append(current_url)

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
ctrl_url_list = get_url_list(set_name="CTRL")
all_ctrl_data: xr.Dataset = xr.open_mfdataset(ctrl_url_list, concat_dim="Time", combine="nested")
print(all_ctrl_data.info)

pgw_url_list = get_url_list(set_name="PGW")
all_pgw_data: xr.Dataset = xr.open_mfdataset(pgw_url_list, concat_dim="Time", combine="nested")
print(all_pgw_data.info)

# Mapping
# ax = plt.axes(projection=ccrs.LambertConformal())
# ax.coastlines() 
# test = dataset_ctrl_2000q4_subsetted["SNOW_ACC_NC"].sel(Time=1000)
# print(test.shape)
# test.plot()
# plt.show()