import pandas as pd
import numpy as np
from datetime import date, datetime

import netCDF4 as nc

#%% IMPORTING --------------------------------------------------------------------------------------------------------------------------
def import_from_source(file_name: str):
    """Imports a single source. If csv txt file, as a pandas Dataframe. If .nc file, as a netCDF4 dataset. Include filetype in name."""
    
    if (file_name[-3:] == "txt"):
        directory_path = "C:\\Users\\swguo\\VSCode Projects\\Snow Research\\Real Data\\"
        data: pd.DataFrame = pd.read_csv(directory_path + file_name, comment="#")
        return data
    elif (file_name[-2:] == "nc"):
        directory_path = "C:\\Users\\swguo\\VSCode Projects\\Snow Research\\"
        data = nc.Dataset(directory_path + file_name)
        return data

    return "Bad File Type"


def import_all_rd(all_data: bool, sane_data: bool, map_data: bool):
    """Imports massive real data file. Returns a dictionary of each 'sane' station, and an array of unique station names."""

    all_rd_raw: pd.DataFrame = import_from_source("All RD.txt")
    all_rd_raw["station_name"] = all_rd_raw["station_name"].astype('string')
    
    all_station_names:np.ndarray = np.array(all_rd_raw["station_name"].unique())
    all_station_names = np.delete(all_station_names, np.where(all_station_names=="FRASER"))

    sane_station_names = ["Colorado - Colorado Drainage Basin Climate Division","TELLURIDE 4WNW","LA VETA PASS","HERMIT 7 ESE","GRAND LAKE 6 SSW",
                    "WOLF CREEK PASS 1 E","RUXTON PARK","MEREDITH","RIO GRANDE RSVR","LEMON DAM","VAIL","HOURGLASS RSVR"]
    map_station_names = ["Colorado - Colorado Drainage Basin Climate Division","TELLURIDE 4WNW","HERMIT 7 ESE","RUXTON PARK"]
    list = {}

    # Setup all data
    if all_data:
        all_dict = {station : pd.DataFrame() for station in all_station_names}
        for station in all_dict.keys():
            current_station = all_rd_raw[:][all_rd_raw["station_name"] == station]
            all_dict[station] = format_iowa_real_data(current_station, include_estimated_M_temp=True, include_estimated_M_precip=True)

        list["all_data"] = {"all_station_dict": all_dict, "all_station_names": all_station_names}

    # Setup sane data
    if sane_data:
        sane_dict = {station : pd.DataFrame() for station in sane_station_names}
        for station in sane_dict.keys():
            current_station = all_rd_raw[:][all_rd_raw["station_name"] == station]
            sane_dict[station] = format_iowa_real_data(current_station, include_estimated_M_temp=True, include_estimated_M_precip=True)

        list["sane_data"] = {"sane_station_dict": sane_dict, "sane_station_names": sane_station_names}
    

    # Setup map data
    if map_data:
        map_dict = {station : pd.DataFrame() for station in map_station_names}
        for station in map_dict.keys():
            current_station = all_rd_raw[:][all_rd_raw["station_name"] == station]
            map_dict[station] = format_iowa_real_data(current_station, include_estimated_M_temp=True, include_estimated_M_precip=True)

        list["map_data"] = {"map_station_dict": map_dict, "map_station_names": map_station_names}
    
    
    return list


# Shouldn't need this at the moment.
# def import_all_data():
#     """Imports all data, returned as a dictionary"""
#     data_dict = {}

#     breck_file_name = "Breckenridge RD.txt"
#     data_dict["breck_data"] = import_from_source(breck_file_name)

#     leadville_file_name = "Leadville 2SW RD.txt"
#     data_dict["leadville_data"] = import_from_source(leadville_file_name)

#     telluride_file_name = "Telluride RD.txt"
#     data_dict["telluride_data"] = import_from_source(telluride_file_name)

#     constants_file_name = "RALconus4km_wrf_constants.nc"
#     data_dict["constants"] = import_from_source(constants_file_name)

#     snow_acc_control_2000q4_file_name = "wrf2d_d01_CTRL_SNOW_ACC_NC_200010-200012.nc"
#     data_dict["snow_acc_control_2000q4"] = import_from_source(snow_acc_control_2000q4_file_name)

#     return data_dict

#%% FORMATTING --------------------------------------------------------------------------------------------------------------------------
def date_to_winter(date: datetime):
    current_year = date.year
    if (date.month <= 6):
        return f"{current_year - 1}-{current_year}"
    else:
        return f"{current_year}-{current_year + 1}"


def format_iowa_real_data(data: pd.DataFrame, include_estimated_M_temp: bool = True, include_estimated_M_precip: bool = True):
    """Returns the formatted real_data. Disregards all data less than 0.01 as inaccuracy. Missing flags automatically are casted to True (estimated)."""
    """Boolean variables to indicate whether or not to include data whose flag was true or missing. If not included, the data is denoted as Nan."""
    """Index is the year of the END of the winter season; for example, 1948 would represent the winter of 1947-1948."""
   
     # Flag correct dtypes, technically still object dtype, but the values are all bool.
    data["temp_estimated"] = flag_to_bool(data["temp_estimated"])
    data["precip_estimated"] = flag_to_bool(data["precip_estimated"])

    # Replace rest of the missing values
    data.replace({"M": np.nan}, inplace=True)

    # Station correct dtypes
    data["station"]: pd.Series = data["station"].astype("string")
    data["station_name"]: pd.Series = data["station_name"].astype("string")

    # Date, Year, Month, correct dtypes. Date to index, not dropped.
    data["day"] = pd.to_datetime(data["day"])
    data.rename({"day": "date"}, axis="columns", inplace=True)
    data.set_index("date", drop=False, inplace=True)
    data["year"] = data["date"].dt.year.astype('int32')
    data["month"] = data["date"].dt.month.astype('int32')

    # Winter: format is winter of "year-nextyear". Winter_year is the year representing the END of that winter.
    winter_column = pd.Series(dtype="string")
    winter_column = data["date"].apply(date_to_winter)
    data["winter_label"] = winter_column
    data["winter_year"] = data["winter_label"].str.slice(5, 10).astype('int32')

    # Snow -> float64
    # "int32" is int, "int64" is long, "int" lets python decide
    data["snow"] = data["snow"].astype('float64')

    # Replace less than 0.01 with nothing, Temps and Precip only where estimated = False
    data["snow"] = np.where((data["snow"] > 0) & (data["snow"] < 0.01), np.nan, data["snow"])
    data["precip"] = np.where((data["precip"] > 0) & (data["precip"] < 0.01), np.nan, data["precip"])

    if not include_estimated_M_precip:
        data["precip"] = np.where(data["precip_estimated"] == False, data["precip"], np.nan)

    if not include_estimated_M_temp:
        data["highc"] = np.where(data["temp_estimated"] == False, data["highc"], np.nan)
        data["lowc"] = np.where(data["temp_estimated"] == False, data["lowc"], np.nan)

    return data

def flag_to_bool(input: pd.Series):
    """Converts series of flags with Ms and T/Fs into a boolean series."""
    input = input.astype("string")
    input.replace({"M": "True"}, inplace=True)
    bool_flag = pd.Series(True, index=input.index)
    bool_flag = np.where(input == "True", True, False)
    return bool_flag