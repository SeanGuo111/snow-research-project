import netCDF4 as nc
import xarray as xr

"""
NetCDF Structure:
Dimensions and variables are both dictionaries. 

1. Dimensions are axes of the data 
2. Data variables are variables dependent on the dimensions
3. Coordinates are data variables with the same name as dimensions
    You can have multidimensional coordinates: XLAT and XLONG, for example, represent physical and not logical coordinates
    Dimensions are just name/numbers while coordinates are vectors
    Essentially, Dimensions are names of the axes, coordinates are the tick labels
4. Attributes: ancillary/metadata

Dask reading:
Dataset.load() converts all variables to eager dataarrays
    Eager dataarray memory is always available, lazy dask memory is available on-request
    Can be slow, as is converting everything
DaskArray.values returns a variable's temporary numpy array
np.asarray(DaskArray) returns variable's explicitly converted numpy array



"""

# NetCDF4 Library Testing:
# snow_acc_control_2000q4 = nc.Dataset("https://rda.ucar.edu/thredds/dodsC/files/g/ds612.0/CTRL/2000/wrf2d_d01_CTRL_SNOW_ACC_NC_200010-200012.nc")
# snow_acc_warm_2000q4 = nc.Dataset("https://rda.ucar.edu/thredds/dodsC/files/g/ds612.0/PGW/2000/wrf2d_d01_PGW_SNOW_ACC_NC_200010-200012.nc")

# print("CTRL: -------------")
# print(snow_acc_control_2000q4)
# print("\n\n\n")
# print("WARM DIMS: -------------")
# print(snow_acc_warm_2000q4.dimensions)
# print("\n\n\n")
# print("WARM VARS: -------------")
# print(snow_acc_warm_2000q4.variables)
# print("\n\n\n")

# Xarray Testing:
test = xr.open_dataset("https://rda.ucar.edu/thredds/dodsC/files/g/ds612.0/PGW/2005/wrf2d_d01_PGW_SNOW_ACC_NC_200501-200503.nc?SNOW_ACC_NC[0:24:2159][435:556][452:591],Times[0:24:2159]")
print(test.info)