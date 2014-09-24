'''
Calculate the HAB index for the year from mean along-shore winds
at Port Aransas.
'''

import numpy as np
from noaa_winds import *
import pdb
import netCDF4 as netCDF
import matplotlib.pyplot as plt

# get wind from noaa
wind = retrieve_noaa_winds('ptat2')

# get time from data
t = wind.getfield(datetime)

# get u and v
u = wind.getfield(np.float64,8)
v = wind.getfield(np.float64,16)

# marcus' coastline angle is 50 degrees
theta = -50*pi/180

# rotate u and v
along = u*np.cos(theta)-v*np.sin(theta)
across = u*np.sin(theta)+v*np.cos(theta)

# years = np.array([2004,2007,2008,2010,2005,2006,2009,2011])
years = np.arange(1996,2015)

alongmean = np.ones(len(years))*np.nan
acrossmean = np.ones(len(years))*np.nan
for i,year in enumerate(years):
	ind = (t>=datetime(year,9,1,0))*(t<=datetime(year,10,1,0))
	# pdb.set_trace()
	# calculate mean just for september for each year
	alongmean[i] = along[ind].mean()
	acrossmean[i] = across[ind].mean()

# indices for hab/non-hab years
habyears = np.array([[0,1,3,4,9,10,13,15,16,17]])
nhabyears = np.array([[2,5,6,7,8,11,12,14]])

fig = plt.figure()
ax = fig.add_subplot(111)
ax.plot(years, alongmean, 'go', ms=10)
ax.plot(years[habyears], alongmean[habyears], 'ro', ms=10)
ax.plot(years[nhabyears], alongmean[nhabyears], 'ko', ms=10)
ax.set_xlim(1995,2015)
ax.set_ylabel('mean along-shore wind')
ax.set_xlabel('year')
fig.savefig('hab-index.pdf', bbox_inches='tight')
plt.show()

# if __name__ == "__main__":
#     run()    
