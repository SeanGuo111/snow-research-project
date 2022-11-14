import data_preparing as dp
import real_data_functions as func
import pandas as pd

station_metadata = dp.import_from_source("Colorado Station Metadata.txt")

# Elevation condition: between 2500 and 4000 (inclusive).
# This filters to stations with above 2500 m, but not with greater than 4000 m stations, which may just be measured in feet.
# Longitude condition: left of 38.824378, which filters to about left of Colorado Springs.

lower_bound = 3000
upper_bound = 4000
longitude_bound = -104.802046
candidates = station_metadata[(station_metadata["elev"] >= lower_bound) & (station_metadata["elev"] <= upper_bound) & (station_metadata["lon"] < longitude_bound)]

print(candidates)
print()
print(f"Amount: {len(candidates)}")