import netCDF4 as nc

"""
NetCDF Structure-------------------------------------

Dimensions and variables are both dictionaries. 

1. Dimensions are axes of the data 
2. Data variables are variables dependent on the dimensions
3. Coordinates are data variables with the same name as dimensions
    You can have multidimensional coordinates: XLAT and XLONG, for example, represent physical and not logical coordinates
    Dimensions are just name/numbers while coordinates are vectors
    Essentially, Dimensions are names of the axes, coordinates are the tick labels
4. Attributes: ancillary/metadata
"""

snow_acc_control_2000q4 = nc.Dataset("https://rda.ucar.edu/thredds/dodsC/files/g/ds612.0/CTRL/2000/wrf2d_d01_CTRL_SNOW_ACC_NC_200010-200012.nc")
snow_acc_warm_2000q4 = nc.Dataset("https://rda.ucar.edu/thredds/dodsC/files/g/ds612.0/PGW/2000/wrf2d_d01_PGW_SNOW_ACC_NC_200010-200012.nc")

print("CTRL: -------------")
print(snow_acc_control_2000q4)
print("\n\n\n")
print("WARM DIMS: -------------")
print(snow_acc_warm_2000q4.dimensions)
print("\n\n\n")
print("WARM VARS: -------------")
print(snow_acc_warm_2000q4.variables)
print("\n\n\n")