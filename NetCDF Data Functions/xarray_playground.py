import xarray as xr
import numpy as np
import pandas as pd
import random
import string


"""
Xarray: structure--------------------------------------------------------------------------
DataArrays are built of 4 components:
    Data variables: NetCDF4-like variables based off of any number of dimensions

    Dimensions: simply names for the dimensional axes which act as a basises to data variables and both kinds of coordinates. Can be thought of as a list like [0,1,2,3,...,*length-1*] (?)
        Index selecting done by DataArray.isel()

    Dimension coordinates: ancillary data variables with the same name as a dimension, acting as a tick labeller for that dimension. Marked with stars when printing the DataArray
        Known in CF terminology as coordinate variables
        Example: "Time" may be a dimension, with a corresponding dimension coordinate "Time" containing a list of dates
        Label selecting done by DataArray.sel()
        Variables can be turned into coordinates via .rename() and .set_coords(), non-dimension -> dimension coordinate can be converted using .swap_dims()

    Non-dimension coordinates: ancillary data variables with no name relationship to a dimension, and do not correspond to any dimension.
        Known in CF terminology as auxiliary coordinate variables
        Example: "south_north" and "west_east" may both be dimensions, with a corresponding non dimension coordinate "latitude" dependent on both
        Selecting variables by non-dimension coordinates cannot be done (make sure to convert to dimension coordinates, check for *)


    Full info, especially on the coordinates section, at https://docs.xarray.dev/en/stable/user-guide/data-structures.html

    
Datasets are collections of possibly multiple DataArrays

Xarray: reading data--------------------------------------------------------------------------

DataArrays store data in the form of plain-old numpy arrays, or dask arrays-- which are muliple numpy arrays combined.
    DaskArrays are created when NetCDF files are imported using open_mfdataset()

DataArray reading:
DataArray.data returns the DataArray's data as an array, keeping the underlying data type preserved.
    Returns a numpy array if utilizing numpy, or, probably not so ideally, a dask array if utilizing dask.
DataArray.values returns the DataArray's data as a numpy array, regardless of underlying data type.
    Can be slow

DaskArray reading:
DaskArray.compute() returns a DaskArray's data as a numpy array, similarly to DataArray.values
    Note that DataArray.data.values can work for DataArray -> DaskArray -> numpy array
Dataset.load() converts all variables to eager Numpy arrays
    Can be very slow
np.asarray(DaskArray) returns variable's explicitly converted numpy array

Xarray: indexing--------------------------------------------------------------------------


Dataset/DataArray/DaskArray.isel(dim1=index1, dim2=index2, ...) returns a new Dataset/DataArray/DaskArray
    found at the given indices of the given DIMENSIONS.
Dataset/DataArray/DaskArray.sel(dim1=label1, dim2=label2, ...) returns a new Dataset/DataArray/DaskArray 
    found at the given labels, or values, of the corresponding DIMENSION COORDINATES to the given dimensions (which have the same name as coordinates).
        From xarray docs: "In label-based indexing, the element position i is automatically looked-up from the coordinate values." https://xarray.pydata.org/en/v0.10.3/indexing.html
    !! If there are no corresponding dimension coordinates to a given dimension, and it is given an integer "label", it will behave like .isel(), indexing by position for the given label
        In other words, .sel() is identical to .isel() if there is no corresponding dimension coordinate variable

    Note: .sel() and .isel() cannot be used for writing DataArrays.

DataArray[index1, index2, ...] returns a DataArray with indexed selecting, but the order of the dimensions must be known
    Can also use this with DaskArray
DataArray.loc[index1, index2, ...] returns a DataArray with labeled selecting, but the order of the dimensions must be known

 An example: time_dim = 4, time_dim (coordinate) = ["a", "b", "c", "d"], data variable called meteorology_data(time_dim)
    The following 4 methods return equivalent numpy arrays:
    meteorology_data.isel(time_dim = 1)
    meteorology_data.sel(time_dim = "b")
    meteorology_data[1]
    meteorology_data.loc[1/3]

Remark: almost all xarray functions work with DaskArrays. 
    As such, you should keep DaskArrays stored inside DataArrays, as getting their "raw" np/dask form would require loading them into memory


Xarray: tips -------------------------------------    

Best practice to select and read data would probably be to index DataArrays and then access the data with .values.

"""

#test = xr.open_dataset("https://rda.ucar.edu/thredds/dodsC/files/g/ds612.0/PGW/2005/wrf2d_d01_PGW_SNOW_ACC_NC_200501-200503.nc?SNOW_ACC_NC[0:24:2159][435:556][452:591],Times[0:24:2159]")
#print(test.info)




all_ctrl_data = xr.Dataset(data_vars={"SNOW_ACC_NC": (["Time", "south_north", "west_east"], np.ones((240, 97, 158)))},
                           coords={"Time": range(240)})
print(all_ctrl_data)
print()

coarsened_snow_data = all_ctrl_data.SNOW_ACC_NC.coarsen(Time=24, boundary="exact").sum().data
certain_dates = all_ctrl_data.drop("SNOW_ACC_NC").isel(Time=np.arange(0,240,24))
print(coarsened_snow_data)
print()
print(certain_dates)
certain_dates = certain_dates.assign(SNOW_ACC_NC=(["Time", "south_north", "west_east"], coarsened_snow_data))
print()
print(certain_dates)

# for current_iteration in range(iterations):
#     left_index = (current_iteration * 24) + 1
#     right_index = left_index + 23
#     selection_range = list(range(left_index, right_index))
    
#     appended_23_hours = all_ctrl_data.isel(Time=selection_range).sum(dim="Time")
#     removed_23_hour_temp_sum = all_ctrl_data.drop_isel(Time=selection_range)
