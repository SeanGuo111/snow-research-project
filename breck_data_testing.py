from datetime import date, datetime
from xml.sax.handler import DTDHandler
from xmlrpc.client import DateTime
import data_preparing as dp
import real_data_functions as func

from cmath import nan
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
#from sklearn.linear_model


# IMPORT DATA ---------------------------------------------------------
breck_data = dp.import_from_source("Breckenridge Iowa Dataset.txt")

# PREPARE DATA ---------------------------------------------------------
breck_data = dp.format_iowa_real_data(breck_data, include_estimated_M_temp=True, include_estimated_M_precip=False)
print(breck_data)

# DO STUFF ----------------------------------------------------
# precip "cut" from 8/26/1913, snow "cut" from 8/31/1913
# First "good" from 7/1/1947
# First full winter from 1948
start_winter = 1948
end_winter = 2020
include_estimated_precip = False

func.all_functions(breck_data, start_winter, end_winter, swr_include_estimated_precip=include_estimated_precip)