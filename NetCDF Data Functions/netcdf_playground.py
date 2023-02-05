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