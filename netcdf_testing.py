import data_importing as di

import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
import netCDF4 as nc
import xarray as xr 

all_data = di.import_all_data()
constants = all_data["constants"]
snow_acc_control_2000q4 = all_data["snow_acc_control_2000q4"]

# BASIC NETCDF4 PACKAGE
# This shows metadata
#print(snow_acc_control_2000q4)
# Dimensions and variables are both dictionaries
# Dimensions: Time(2208), 24hrs x 92 days, South-north(1015), West_east(1359), DateStrLen(19) ???
#print(snow_acc_control_2000q4.dimensions.keys())
# Variables: each has which dimension(s) they are a function of in ()
#print(snow_acc_control_2000q4.variables.keys())



# XARRAY (update this into data_importing.py)
xr_snow_acc_control_2000q4:xr.Dataset = xr.open_dataset("C:\\Users\\swguo\\VSCode Projects\\Snow Research\\wrf2d_d01_CTRL_SNOW_ACC_NC_200010-200012.nc")
print(xr_snow_acc_control_2000q4["SNOW_ACC_NC"].data)
xr_snow_acc_control_2000q4_coords = xr_snow_acc_control_2000q4.coords.get("XLONG")
print(xr)
#print(xr_snow_acc_control_2000q4)


# Try opening up and reading XLONG, because it has south-north?