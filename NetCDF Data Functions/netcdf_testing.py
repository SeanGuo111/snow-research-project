#import data_preparing as dp

import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
import netCDF4 as nc
import xarray as xr

# With nc:
#snow_acc_control_2000q4 = nc.Dataset("https://rda.ucar.edu/thredds/dodsC/files/g/ds612.0/CTRL/2000/wrf2d_d01_CTRL_SNOW_ACC_NC_200010-200012.nc")
#snow_acc_warm_2000q4 = nc.Dataset("https://rda.ucar.edu/thredds/dodsC/files/g/ds612.0/PGW/2000/wrf2d_d01_PGW_SNOW_ACC_NC_200010-200012.nc")
snow_acc_control_2000q4 = xr.open_dataset("https://rda.ucar.edu/thredds/dodsC/files/g/ds612.0/CTRL/2000/wrf2d_d01_CTRL_SNOW_ACC_NC_200010-200012.nc")
snow_acc_warm_2000q4 = xr.open_dataset("https://rda.ucar.edu/thredds/dodsC/files/g/ds612.0/PGW/2000/wrf2d_d01_PGW_SNOW_ACC_NC_200010-200012.nc")

print("CTRL: -------------")
print(snow_acc_control_2000q4)
# print("\n\n\n")
# print("WARM DIMS: -------------")
# print(snow_acc_warm_2000q4.dimensions)
# print("\n\n\n")
# print("WARM VARS: -------------")
# print(snow_acc_warm_2000q4.variables)
# print("\n\n\n")


# XARRAY (update this into data_importing.py)

# Data: print(xr_snow_acc_control_2000q4["SNOW_ACC_NC"].data)
# print("\n\n\n\n\n")
# specific_data = xr_snow_acc_control_2000q4["SNOW_ACC_NC"].isel(Time = 100).data
# print(f"Data (as np array): {specific_data}")
# print(f"Nonzeros: {np.count_nonzero(specific_data)}")
# print()
# xr_snow_acc_control_2000q4_coords = xr_snow_acc_control_2000q4.coords.get("XLONG")


