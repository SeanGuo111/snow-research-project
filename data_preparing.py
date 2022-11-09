import pandas as pd
import numpy as np
from datetime import date, datetime

import netCDF4 as nc

# IMPORTING --------------------------------------------------------------------------------------------------------------------------
def import_from_source(file_name: str, file_type: str):
    """Imports a single source. If csv txt file, as a pandas Dataframe. If .nc file, as a netCDF4 dataset."""
    
    directory_path = "C:\\Users\\swguo\\VSCode Projects\\Snow Research\\"
    if (file_type == "txt"):
        data: pd.DataFrame = pd.read_csv(directory_path + file_name, comment="#")
        return data
    elif (file_type == "nc"):
        data = nc.Dataset(directory_path + file_name)
        return data



def import_all_data():
    """Imports all data, returned as a dictionary"""
    data_dict = {}

    breck_file_name = "Breckenridge Iowa Dataset.txt"
    data_dict["breck_data"] = import_from_source(breck_file_name, "txt")

    leadville_file_name = "Leadville 2SW Iowa Dataset.txt"
    data_dict["leadville_data"] = import_from_source(leadville_file_name, "txt")

    constants_file_name = "RALconus4km_wrf_constants.nc"
    data_dict["constants"] = import_from_source(constants_file_name, "nc")

    snow_acc_control_2000q4_file_name = "wrf2d_d01_CTRL_SNOW_ACC_NC_200010-200012.nc"
    data_dict["snow_acc_control_2000q4"] = import_from_source(snow_acc_control_2000q4_file_name, "nc")

    return data_dict

# FORMATTING --------------------------------------------------------------------------------------------------------------------------
def date_to_winter(date: datetime):
    current_year = date.year
    if (date.month <= 6):
        return f"{current_year - 1}-{current_year}"
    else:
        return f"{current_year}-{current_year + 1}"


def format_iowa_real_data(data: pd.DataFrame, include_estimated_M_temp: bool = False, include_estimated_M_precip: bool = False):
    """Returns the formatted real_data. Disregards all data less than 0.01 as inaccuracy."""
    """Boolean variables to indicate whether or not to include data whose flag was true or missing."""
    """Index is the year of the END of the winter season; for example, 1948 would represent the winter of 1947-1948."""
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
    