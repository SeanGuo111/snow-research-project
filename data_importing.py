import pandas as pd
import netCDF4 as nc

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
