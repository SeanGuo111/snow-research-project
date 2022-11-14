import data_preparing as dp
import real_data_functions as func
import pandas as pd

station_metadata = dp.import_from_source("Colorado Station Metadata.txt")

# Elevation condition: between 2500 and 4000 (inclusive). 
# This should filter to stations with above 2500 m, but not with greater than 4000 m stations, which may just be measured in feet.
lower_bound = 2500
upper_bound = 4000
candidates = station_metadata[(station_metadata["elev"] >= 2500) & (station_metadata["elev"] <= 4000)]

print(candidates)
print()
print(f"Amount: {len(candidates)}")