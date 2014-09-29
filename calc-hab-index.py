'''
Calculate the HAB index for the year from mean along-shore winds
at Port Aransas.
'''

import numpy as np
from noaa_winds import *
import pdb
import netCDF4 as netCDF
import matplotlib.pyplot as plt
import pandas

# Run September or April wind index
wcase = 'April' # 'September' or 'April'

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

# This is the HAB index
alongmean = np.ones(len(years))*np.nan
# Trying out some other statistics too
alongwinmean = np.ones(len(years))*np.nan
alongvar = np.ones(len(years))*np.nan
alongmax = np.ones(len(years))*np.nan
alongmed = np.ones(len(years))*np.nan
alongcsmax = np.ones(len(years))*np.nan #cumsum max
acrossmean = np.ones(len(years))*np.nan
acrossvar = np.ones(len(years))*np.nan
for i,year in enumerate(years):

    # calculate mean just for 1 month for each year
    if wcase == 'April':
        ind = (t>=datetime(year,4,1,0))*(t<=datetime(year,5,1,0))
    elif wcase == 'September':
        ind = (t>=datetime(year,9,1,0))*(t<=datetime(year,10,1,0))

    df = pandas.DataFrame(along[ind])
    win = pandas.rolling_sum(df, window=72)#, win_type='boxcar')
    alongwinmean[i] = win.min()

    alongmax[i] = abs(along[ind]).max()
    alongcsmax[i] = np.cumsum(along[ind]).min()
    alongmed[i] = np.median(along[ind])
    alongmean[i] = along[ind].mean()
    alongvar[i] = np.var(along[ind])
    acrossmean[i] = across[ind].mean()
    acrossvar[i] = np.var(across[ind])

# indices for hab/non-hab years
habyears = np.array([[0,1,3,4,9,10,13,15,16]])
nhabyears = np.array([[2,5,6,7,8,11,12,14,17]])

# Mean
fig = plt.figure()
ax = fig.add_subplot(111)
ax.plot(years, alongmean, 'go', ms=10)
ax.plot(years[habyears], alongmean[habyears], 'ro', ms=10)
ax.plot(years[nhabyears], alongmean[nhabyears], 'ko', ms=10)
ax.set_xlim(1995,2015)
if wcase == 'April':
    ax.set_ylabel('Mean April along-shore wind [ms$^{-1}$]', fontsize=14)
elif wcase == 'September':
    ax.set_ylabel('Mean September along-shore wind [ms$^{-1}$]', fontsize=14)
ax.set_xlabel('Year', fontsize=14)
if wcase == 'April':
    fig.savefig('hab-index-april.pdf', bbox_inches='tight')
elif wcase == 'September':
    fig.savefig('hab-index-september.pdf', bbox_inches='tight')
plt.show()


# # Along Variance
# fig = plt.figure()
# ax = fig.add_subplot(111)
# ax.plot(years, alongvar, 'go', ms=10)
# ax.plot(years[habyears], alongvar[habyears], 'ro', ms=10)
# ax.plot(years[nhabyears], alongvar[nhabyears], 'ko', ms=10)
# ax.set_xlim(1995,2015)
# ax.set_ylabel('along-shore wind variance')
# ax.set_xlabel('year')
# fig.savefig('hab-var-along.pdf', bbox_inches='tight')
# plt.show()


# # Across Variance
# fig = plt.figure()
# ax = fig.add_subplot(111)
# ax.plot(years, acrossvar, 'go', ms=10)
# ax.plot(years[habyears], acrossvar[habyears], 'ro', ms=10)
# ax.plot(years[nhabyears], acrossvar[nhabyears], 'ko', ms=10)
# ax.set_xlim(1995,2015)
# ax.set_ylabel('across-shore wind variance')
# ax.set_xlabel('year')
# fig.savefig('hab-var-across.pdf', bbox_inches='tight')
# plt.show()


# # Along Max
# fig = plt.figure()
# ax = fig.add_subplot(111)
# ax.plot(years, alongmax, 'go', ms=10)
# ax.plot(years[habyears], alongmax[habyears], 'ro', ms=10)
# ax.plot(years[nhabyears], alongmax[nhabyears], 'ko', ms=10)
# ax.set_xlim(1995,2015)
# ax.set_ylabel('along-shore wind max')
# ax.set_xlabel('year')
# fig.savefig('hab-max-along.pdf', bbox_inches='tight')
# plt.show()


# # Along median
# fig = plt.figure()
# ax = fig.add_subplot(111)
# ax.plot(years, alongmed, 'go', ms=10)
# ax.plot(years[habyears], alongmed[habyears], 'ro', ms=10)
# ax.plot(years[nhabyears], alongmed[nhabyears], 'ko', ms=10)
# ax.set_xlim(1995,2015)
# ax.set_ylabel('along-shore wind median')
# ax.set_xlabel('year')
# fig.savefig('hab-med-along.pdf', bbox_inches='tight')
# plt.show()


# # Along Cumsum Max
# fig = plt.figure()
# ax = fig.add_subplot(111)
# ax.plot(years, alongcsmax, 'go', ms=10)
# ax.plot(years[habyears], alongcsmax[habyears], 'ro', ms=10)
# ax.plot(years[nhabyears], alongcsmax[nhabyears], 'ko', ms=10)
# ax.set_xlim(1995,2015)
# ax.set_ylabel('along-shore wind cumsum max')
# ax.set_xlabel('year')
# fig.savefig('hab-csmax-along.pdf', bbox_inches='tight')
# plt.show()


# # Along win mean
# fig = plt.figure()
# ax = fig.add_subplot(111)
# ax.plot(years, alongwinmean, 'go', ms=10)
# ax.plot(years[habyears], alongwinmean[habyears], 'ro', ms=10)
# ax.plot(years[nhabyears], alongwinmean[nhabyears], 'ko', ms=10)
# ax.set_xlim(1995,2015)
# ax.set_ylabel('along-shore wind window mean')
# ax.set_xlabel('year')
# fig.savefig('hab-winmean.pdf', bbox_inches='tight')
# plt.show()


# if __name__ == "__main__":
#     run()    
