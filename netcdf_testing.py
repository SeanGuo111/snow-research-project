import data_preparing as dp

import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
import netCDF4 as nc
import xarray as xr 

#constants = dp.import_from_source("RALconus4km_wrf_constants.nc")
#snow_acc_control_2000q4 = dp.import_from_source("wrf2d_d01_CTRL_SNOW_ACC_NC_200010-200012.nc")


# BASIC NETCDF4 PACKAGE
# This shows metadata
#print(snow_acc_control_2000q4)
#print(snow_acc_control_2000q4.dimensions.keys())
#print(snow_acc_control_2000q4.variables.keys())

# Dimensions and variables are both dictionaries. 

# Dimensions are axes of the data 
# Coordinates are variables with the same name as dimensions
# Dimensions are names of the axes, coordinates are the tick labels
# Basically, dimensions are just name/numbers while coordinates are vectors
# Data variables are variables that do not have the same name as dimensions
# Attributes: ancillary/metadata

# Dimensions: Time(2208)*, 24hrs x 92 days, South-north(1015), West_east(1359), XLAT*, XLONG*
#   * = also a coordinate



# XARRAY (update this into data_importing.py)
url = "https://rda.ucar.edu/thredds/dodsC/files/g/ds612.0/CTRL/2001/wrf2d_d01_CTRL_ACLWDNBC_200101-200103.nc"
xr_snow_acc_control_2000q4:xr.Dataset = xr.open_dataset(url)
print(xr_snow_acc_control_2000q4.info)
# Data: print(xr_snow_acc_control_2000q4["SNOW_ACC_NC"].data)
print("\n\n\n\n\n")
specific_data = xr_snow_acc_control_2000q4["SNOW_ACC_NC"].isel(Time = 100).data
print(f"Data (as np array): {specific_data}")
print(f"Nonzeros: {np.count_nonzero(specific_data)}")
print()
xr_snow_acc_control_2000q4_coords = xr_snow_acc_control_2000q4.coords.get("XLONG")

#print(xr_snow_acc_control_2000q4)

# Try opening up and reading XLONG, because it has south-north?