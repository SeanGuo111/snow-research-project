import xarray as xr
import numpy as np
import pandas as pd


"""
Xarray: reading data-------------------------------------

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

Xarray: indexing-------------------------------------


Dataset/DataArray/DaskArray.isel(dim1=index1, dim2=index2, ...) returns a Dataset/DataArray/DaskArray found at the specified indices of dimensions/coordinates.
Dataset/DataArray/DaskArray.sel(dim1=label1, dim2=label2, ...) returns a Dataset/DataArray/DaskArray or a value if a single point, found at the specified labels, or values, of coordinates.
    Note: .sel() and .isel() cannot be used for writing DataArrays.

DataArray[index1, index2, ...] returns a DataArray with indexed selecting, but the order of the dimensions must be known
    Can also use this with DaskArray
DataArray.loc[index1, index2, ...] returns a DataArray with labeled selecting, but the order of the dimensions must be known

 An example: time_dim = [1/1, 1/2, 1/3, 1/22], numpy array stored in a DataArray called meteorology_data
    The following 4 methods return equivalent numpy arrays:
    meteorology_data.isel(time_dim = 2)
    meteorology_data.sel(time_dim = 1/3)
    meteorology_data[2]
    meteorology_data[1/3]

Remark: almost all xarray functions work with DaskArrays. 
    As such, you should keep DaskArrays stored inside DataArrays, as getting their "raw" np/dask form would require loading them into memory


Xarray: tips -------------------------------------    

Best practice to select and read data would probably be to index DataArrays and then access the data with .values.

"""

#test = xr.open_dataset("https://rda.ucar.edu/thredds/dodsC/files/g/ds612.0/PGW/2005/wrf2d_d01_PGW_SNOW_ACC_NC_200501-200503.nc?SNOW_ACC_NC[0:24:2159][435:556][452:591],Times[0:24:2159]")
#print(test.info)

time = pd.date_range("2000-01-01", freq="6H", periods=365 * 4)

ds = xr.Dataset({"foo": ("time", np.arange(365 * 4)), "time": time})
print(ds)