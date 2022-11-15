import data_preparing as dp
import real_data_functions as func
import pandas as pd
import matplotlib.pyplot as plt

def average_temperature_subplots():
    pass

station_metadata = dp.import_from_source("Colorado Station Metadata.txt")

# Elevation condition: between 2500 and 4000 (inclusive).
# This filters to stations with above 2500 m, but not with greater than 4000 m stations, which may just be measured in feet.
# Longitude condition: left of 38.824378, which filters to about left of Colorado Springs.

lower_bound = 2500
upper_bound = 4000
longitude_bound = -104.802046
start_date_bound = 2000
candidates = station_metadata[(station_metadata["elev"] >= lower_bound) & (station_metadata["elev"] <= upper_bound) & (station_metadata["lon"] < longitude_bound) & (pd.to_datetime(station_metadata["begints"]).dt.year < start_date_bound)]

return_value = dp.import_all_rd()
all_data = return_value["data"]
station_names = return_value["station_names"]

#breck_data = all_data["BRECKENRIDGE"]
#print(breck_data)

for station in station_names:
    current_station = all_data[station]
    start_winter = current_station["winter_year"].iloc[0]
    end_winter = current_station["winter_year"].iloc[len(current_station)-1] - 1
    func.all_snowfall(current_station)

    # plt.clf()
    # stats_dict = func.average_temperature(current_station, start_winter, end_winter, show = False)
    # if (stats_dict["slope"] >= 0):
    #     plt.show()


