# This can be tested later, as a luxury

# Resolve the latest GFS dataset
import metpy
from siphon.catalog import TDSCatalog

# Set up access via NCSS
gfs_catalog = ('http://thredds.ucar.edu/thredds/catalog/grib/NCEP/GFS/'
               'Global_0p5deg/catalog.xml?dataset=grib/NCEP/GFS/Global_0p5deg/Best')
cat = TDSCatalog(gfs_catalog)
ncss = cat.datasets[0].subset()

https://rda.ucar.edu/thredds/ncss/grid/files/g/ds612.0/PGW/2000/wrf2d_d01_PGW_SNOW_ACC_NC_200010-200012.nc?var=SNOW_ACC_NC&north=57.935&west=-139.094&east=-56.906&south=18.115&horizStride=1&time_start=2000-10-01T00:00:00Z&time_end=2000-12-31T23:00:00Z&&&accept=netcdf4-classic
