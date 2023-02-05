import data_preparing as dp

import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
import netCDF4 as nc
import xarray as xr 


# Dimensions: Time(2208)*, 24hrs x 92 days, South-north(1015), West_east(1359), XLAT*, XLONG*
#   * = also a coordinate

#snow_acc_control_2000q4 = nc.Dataset("C:\\Users\\swguo\\VSCode Projects\\Snow Research\\NetCDF Data\\wrf2d_d01_CTRL_SNOW_ACC_NC_200010-200012.nc")
snow_acc_control_2000q4 = nc.Dataset("https://rda.ucar.edu/thredds/dodsC/files/g/ds612.0/PGW/2001/wrf2d_d01_CTRL_SNOW_ACC_NC_200101-200103.nc")
snow_acc_warm_2000q4 = nc.Dataset("https://rda.ucar.edu/thredds/dodsC/files/g/ds612.0/PGW/2001/wrf2d_d01_PGW_SNOW_ACC_NC_200101-200103.nc")
print(snow_acc_control_2000q4)
print(snow_acc_warm_2000q4)


# XARRAY (update this into data_importing.py)
# url = "https://rda.ucar.edu/thredds/dodsC/files/g/ds612.0/CTRL/2001/wrf2d_d01_CTRL_ACLWDNBC_200101-200103.nc"
# xr_snow_acc_control_2000q4:xr.Dataset = xr.open_dataset(url)
# print(xr_snow_acc_control_2000q4.info)
# Data: print(xr_snow_acc_control_2000q4["SNOW_ACC_NC"].data)

# print("\n\n\n\n\n")
# specific_data = xr_snow_acc_control_2000q4["SNOW_ACC_NC"].isel(Time = 100).data
# print(f"Data (as np array): {specific_data}")
# print(f"Nonzeros: {np.count_nonzero(specific_data)}")
# print()
# xr_snow_acc_control_2000q4_coords = xr_snow_acc_control_2000q4.coords.get("XLONG")


# Try opening up and reading XLONG, because it has south-north?