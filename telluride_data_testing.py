import data_preparing as dp
import real_data_functions as func

# IMPORT DATA ---------------------------------------------------------
data_dict = dp.import_all_data()
telluride_data = data_dict["telluride_data"]

# PREPARE DATA ---------------------------------------------------------
telluride_data = dp.format_iowa_real_data(telluride_data, include_estimated_M_temp=True, include_estimated_M_precip=True)
print(telluride_data)

# DO STUFF ----------------------------------------------------
# Gap until 6/1/1911
# First full winter year: 1912
# Another gap from 12/1/2008
# Last full winter year: 2008
start_winter = 1912
end_winter = 2008

#func.all_precip(telluride_data)

#func.all_snowfall(telluride_data)

func.average_temperature(telluride_data, start_winter, end_winter)

func.largest_and_average_snowfall_events(telluride_data, start_winter, end_winter)

func.season_total_snow_water_ratio(telluride_data, start_winter, end_winter, include_estimated_precip = True)

x = 10
func.x_largest_snowfall_events_average(telluride_data, start_winter, end_winter, x)

max_percentile = 20
func.percentage_largest_snowfall_events_average(telluride_data, start_winter, end_winter, max_percentile)

func.average_days_with_snow(telluride_data, start_winter, end_winter)