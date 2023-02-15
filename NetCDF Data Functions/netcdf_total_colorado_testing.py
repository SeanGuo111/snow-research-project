#import data_preparing as dp

import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
import cartopy.crs as ccrs

import netCDF4 as nc
import xarray as xr

# a function to find the index of the point closest pt (in squared distance) to given lat/lon value.
def get_closest_ij(x_lat: np.ndarray, x_long: np.ndarray, given_lat_pt, given_long_pt):
  """Enter a given coordinate, and this returns a tuple (south_north, west_east) of the dimension values closest to that coordinate."""
  # find squared distance of every point on grid
  dist_sq = (x_lat-given_lat_pt)**2 + (x_long-given_long_pt)**2
  # 1D index of minimum dist_sq element
  minindex_flattened = dist_sq.argmin()
  # Get 2D index for latvals and lonvals arrays from 1D index
  return np.unravel_index(minindex_flattened, x_lat.shape)




dataset_ctrl_2000q4: xr.DataArray = xr.open_dataset("https://rda.ucar.edu/thredds/dodsC/files/g/ds612.0/CTRL/2000/wrf2d_d01_CTRL_SNOW_ACC_NC_200010-200012.nc")
# Another: dataset_pgw_2000q4 = xr.open_dataset("https://rda.ucar.edu/thredds/dodsC/files/g/ds612.0/PGW/2000/wrf2d_d01_PGW_SNOW_ACC_NC_200010-200012.nc")

# Orientation
print(dataset_ctrl_2000q4.info)


# Colorado bounds: -109.046667 W, -102.046667 W, 37 N, 41 N
# Top left corner: (south_north 556, west_east 452) corresponds to (XLAT 40.987, XLONG -109.045). Both slightly inside colorado.
# Bottom right corner: (south_north 435, west_east 591) corresponds to (XLAT 36.990, XLONG -102.036). Both slightly outside colorado.

# Data retrieved using: 
x_lat = dataset_ctrl_2000q4["XLAT"]
x_long = dataset_ctrl_2000q4["XLONG"]
return_val_tl = get_closest_ij(x_lat.data, x_long.data, 37, -102.0467)


# sel for value selection, isel for index selection
dataset_colorado = dataset_ctrl_2000q4.sel(south_north=slice(435,556), west_east=slice(452,591))
print(dataset_colorado.info)

dataarray_snow = dataset_colorado["SNOW_ACC_NC"]

dataarray_snow_24hr = dataarray_snow.sel(Time = "2000-12-25")
dataarray_sum_24hr = np.sum(dataarray_snow_24hr, axis=0)
np_snow_24hr = dataarray_snow_24hr.data
np_sum_24hr = dataarray_sum_24hr.data

print("\n\n\n")
print(f"Specific Data Shape: {np_snow_24hr.shape}")
print(f"24hr Sum Shape: {np_sum_24hr.shape}")
print(f"Total Colorado Snow on December 25, 2000, all 24 hours: {np.sum(np_snow_24hr)} mm")


# Map

ax = plt.axes(projection=ccrs.LambertConformal())
ax.coastlines() 
dataarray_sum_24hr.plot()
plt.show()

