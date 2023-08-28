import numpy as np
import pandas as pd
from matplotlib import animation as anim
from matplotlib import pyplot as plt
import cartopy.crs as ccrs

import netCDF4 as nc
import xarray as xr

#%% Utility Functions
def get_closest_south_north_west_east(XLAT, XLONG, given_lat_pt, given_long_pt):
    """Enter a given coordinate (lat, long), as well as the WRF's exact lat/long variables as DataArrays.\nThis function returns a tuple (south_north, west_east) of the dimension values closest to that coordinate."""
    
    # find squared distance of every point on grid
    dist_sq = (XLAT-given_lat_pt)**2 + (XLONG-given_long_pt)**2
    
    # 1D index of minimum dist_sq element
    minindex_flattened = dist_sq.argmin()
    
    # Get 2D index for latvals and longvals arrays from 1D index
    return np.unravel_index(minindex_flattened, XLAT.shape)


def get_closest_latitude_longitude(XLAT, XLONG, south_north_value, west_east_value):
    """Enter a given south_north and west_east values, as well as the WRF's exact lat/long variables as DataArrays.\nThis function returns a tuple (XLAT, XLONG) of the corresponding exact geographical coordinates."""
    
    # sel necessary due to indices/values not aligned
    latitude_pt = XLAT[south_north_value, west_east_value]
    longitude_pt = XLONG[south_north_value, west_east_value]

    return (latitude_pt, longitude_pt)


def verify_colorado_coordinate_bounds(data):
    """Outputs information for the bottom-left (southwest) and top-right (northeast) corners of the colorado coordinate bounds."""

    XLAT = data.XLAT.values
    XLONG = data.XLONG.values

    bottom_left = get_closest_south_north_west_east(XLAT, XLONG, 37, -109.046667)
    print(f"Bottom-left south-north/west-east indices: {bottom_left}")
    bottom_left_coord_tuple = get_closest_latitude_longitude(XLAT, XLONG, bottom_left[0], bottom_left[1])
    print(f"Bottom-left coords: {bottom_left_coord_tuple}")

    top_right = get_closest_south_north_west_east(XLAT, XLONG, 41, -102.046667)
    print(f"Top-right south-north/west-east indices: {top_right}")
    top_right_coord_tuple = get_closest_latitude_longitude(XLAT, XLONG, top_right[0], top_right[1])
    print(f"Top-right coords: {top_right_coord_tuple}")

def get_index_from_date(year, start_month):
    """Get index for a file in the urllist from a date range"""

    # Starts at 0 for 2000-10-12, 1 for 2001-01-03, 51 for 2013-07-09
    index = (year-2001)*4 + 1
    index += (start_month - 1)/3
    return int(index)


def get_wrf_dataset(set_type: str, subset_time_start = 0, subset_time_end = -1, subset_every_24_hr: bool = True, subset_colorado_area: bool = True, 
                    include_timestrs: bool = True, include_xlat_xlong: bool = True) -> xr.Dataset:
    """Retrieves list of all WRF simulation urls.\nset_type: 'CTRL' or 'PGW'\nevery_24_hr sets the function sets to function to subset to every 24 hrs of the dataset, at each midnight."""
    
    url_list = []
    num_hrs_list = [2159, 2183, 2207, 2207]
    
    url_start = f"https://thredds.rda.ucar.edu/thredds/dodsC/files/g/ds612.0/{set_type}/"
    every_24_hr_time_constraint = ""
    colorado_constraint = ""
    
    # Configure subsets
    if subset_every_24_hr:
        every_24_hr_time_constraint = ":24"
    if subset_colorado_area:
        colorado_constraint = "[448:544][439:596]"
    else:
        colorado_constraint = "[0:1014][0:1358]"

    # Date range list setting
    date_range_list = ["200010-200012"]
    for year in range(2001, 2013): # missing data in PGW 200501-200503
        for quarter in range(0, 4): 
            start_month = str((3*quarter) + 1)
            end_month = str((3*quarter) + 3)
            if start_month != "10":
                start_month = "0" + start_month
                end_month = "0" + end_month

            date_range = f"{year}{start_month}-{year}{end_month}"
            date_range_list.append(date_range)
    date_range_list.append("201301-201303")
    date_range_list.append("201304-201306")
    date_range_list.append("201307-201309")
    date_range_list.remove("200501-200503")    
    
    # Adding urls based on date range list
    for date_range in date_range_list:
        year = int(date_range[0:4])
        quarter = int((int(date_range[4:6]) - 1)/3)
        
        current_url = url_start
        current_url += f"{year}/wrf2d_d01_{set_type}_SNOW_ACC_NC_"
        
        # Hours
        number_hrs = num_hrs_list[quarter]
        if (year % 4 == 0 and quarter == 0):
            number_hrs = 2183
        
        current_url += f"{date_range}.nc?SNOW_ACC_NC[0{every_24_hr_time_constraint}:{number_hrs}]{colorado_constraint}"
        
        if (include_timestrs):
            current_url += f",Times[0{every_24_hr_time_constraint}:{number_hrs}]"

        if (include_xlat_xlong):
            current_url += f",XLAT{colorado_constraint}"
            current_url += f",XLONG{colorado_constraint}"
        
        url_list.append(current_url)


    dataset: xr.Dataset = xr.open_mfdataset(url_list, concat_dim="Time", combine="nested")

    if (subset_time_end == -1):
        subset_time_end = len(dataset.Time)
    return dataset.isel(Time=slice(subset_time_start, subset_time_end))


#%% Importing

all_ctrl_data = get_wrf_dataset(set_type="CTRL", subset_every_24_hr=False, subset_colorado_area=True, include_timestrs=True, include_xlat_xlong=True)

print("Baseline: ====================================")
print(all_ctrl_data.info)
print("\n")
# all_pgw_data = get_wrf_dataset(set_type="PGW", subset_every_24_hr=True, subset_colorado_area=True, include_timestrs=True, include_xlat_xlong=True)
# print(all_pgw_data.info)

snow_da: xr.DataArray = all_ctrl_data["SNOW_ACC_NC"]
print("Snow DataArray: ====================================")
print(snow_da)
print("\n")

print("Comparing before/after coarsen: ====================================")
original_values = snow_da.isel(Time=np.arange(72,96)).values
print(f"Before type: {type(original_values)}")
print(f"Before shape: {original_values.shape}")
print(f"Before #nonzero: {np.count_nonzero(original_values)}")
print(f"Before overall sum: {np.sum(original_values)}")
print(f"Before first element: {np.sum(original_values[:,24,24])}")


coarsened_snow_summed: xr.DataArray = snow_da.coarsen(Time=24, boundary="exact").sum() # This lines messed. When fixed, condense with below line
coarsened_snow_summed_data = coarsened_snow_summed.data 

coarsened_values = coarsened_snow_summed.isel(Time=3).values
print(f"After type: {type(coarsened_values)}")
print(f"After shape: {coarsened_values.shape}")
print(f"After #nonzero: {np.count_nonzero(coarsened_values)}")
print(f"After overall sum: {np.sum(coarsened_values)}")
print(f"After first element: {coarsened_values[24,24]}")

print("\n")

time_length = all_ctrl_data.dims["Time"]
rest_of_data = all_ctrl_data.drop("SNOW_ACC_NC").isel(Time=np.arange(0,time_length,24))
all_ctrl_data = rest_of_data.assign(SNOW_ACC_NC=(["Time", "south_north", "west_east"], coarsened_snow_summed_data))
print("New Array: ====================================")
print(all_ctrl_data.info)
print("\n")

all_ctrl_data = all_ctrl_data.rename({"Times": "Time"}).swap_dims({"Time": "Time"}) #renames Times variable and sets it as a dimension coordinate to the dimension"Time"
                                                                                    # the swap_dims({"Time": "Time"}) changes the dimension "Time", represented by the key
                                                                                    # , to be named and associated with the coordinate "Time", represented by the value
                                                                                    # Do this after coarsening process, since coarsening of the S64 timestrs will throw an error
ctrl_times: np.ndarray = all_ctrl_data["Time"].values # will need a .values() to unpack-- AFTER your specific, requested elements are selected for
ctrl_snow_da: xr.DataArray = all_ctrl_data["SNOW_ACC_NC"] # will need a .values() to unpack-- AFTER your specific, requested elements are selected for


print("Sanity check for times. ========================")
ctrl_time_da: np.ndarray = ctrl_snow_da["Time"] 
ctrl_time_da = ctrl_time_da.values
print(ctrl_time_da[0])
print(ctrl_time_da[1552])
print(ctrl_time_da[1553])
print(ctrl_time_da[-1])
print("\n")

print("Sanity check for coords. ========================")
verify_colorado_coordinate_bounds(all_ctrl_data)

# test = ctrl_snow.isel(Time=0).values
# print(np.count_nonzero(test))

#%% Testing and Mapping

# plt.figure(figsize=(14, 6))
# ax = plt.axes(projection=ccrs.PlateCarree())
# ax.set_global()
# ctrl_snow_sample.plot.pcolormesh(
#     ax=ax, transform=ccrs.PlateCarree(), x="XLAT", y="XLONG", add_colorbar=True
# )
# ax.coastlines()
# ax.set_ylim([0,90])
# plt.show()


# Setup the initial plot
# fig = plt.figure()
# ax = plt.axes(projection=ccrs.LambertConformal())
# extent = [-109.046667, -102.046667, 37, 41]
# ax.set_extent(extent, ccrs.PlateCarree())
# ax.coastlines()

# # Set up levels etc in this call. 
# image = ctrl_snow.sel(Time = 0).plot.imshow(ax=ax, transform=ccrs.PlateCarree(), animated=True)

# def update(t):
#     # Update the plot for a specific time
#     print(t)
#     ax.set_title(ctrl_times.sel(Time=t).values)
#     image.set_array(ctrl_snow.sel(Time=t).values)
#     return image

# # Run the animation, applying `update()` for each of the times in the variable
# animation = anim.FuncAnimation(fig, update, frames=ctrl_snow.Time.values, interval=200, blit=False)
# plt.show()
