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
from matplotlib.mlab import find

# Run September or April wind index
wcase = 'September' # 'September' or 'April'

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
years = np.arange(1996, datetime.today().year+1)

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
# These are through 2014
habyears = np.array([[0,1,3,4,9,10,13,15,16, 19]])
nhabyears = np.array([[2,5,6,7,8,11,12,14,17, 18]])

# # Mean
# fig = plt.figure()
# ax = fig.add_subplot(111)
# # Plot means
# ax.plot(years, alongmean, 'o', color='blue', ms=10)
# ax.plot(years[habyears], alongmean[habyears], 'ro', ms=10)
# ax.plot(years[nhabyears], alongmean[nhabyears], 'ko', ms=10)
# ax.set_xlim(1995, datetime.today().year + 1)
# if wcase == 'April':
#     ax.set_ylabel('Mean April along-shore wind [ms$^{-1}$]', fontsize=14)
# elif wcase == 'September':
#     ax.set_ylabel('Mean September along-shore wind [ms$^{-1}$]', fontsize=14)
# ax.set_xlabel('Year', fontsize=14)
# ax.set_title('HAB index')
# # Legend
# ax.text(0.02, 0.12, 'HAB year', color='red', fontsize=14, transform=ax.transAxes)
# ax.text(0.02, 0.07, 'non-HAB year', color='black', fontsize=14, transform=ax.transAxes)
# ax.text(0.02, 0.02, 'This year', color='blue', fontsize=14, transform=ax.transAxes)
# if wcase == 'April':
#     fig.savefig('hab-index-april.pdf', bbox_inches='tight')
# elif wcase == 'September':
#     fig.savefig('hab-index-september.pdf', bbox_inches='tight')
# plt.show()


# Plot showing all of September
# f, axes = plt.subplots(1, years.size, sharey=True)
fig = plt.figure()
ax = fig.add_subplot(111)
for i, year in enumerate(years):

    # calculate direction for each time available for September for each year
    inds = find((t >= datetime(year, 9, 1, 0))*(t < datetime(year, 10, 1, 0)))
    days = []
    [days.append(t[ind].day + t[ind].hour/24.) for ind in inds]
    alongmean[i] = along[inds].mean()

    # HAB years
    if t[inds[0]].year in [1996, 1997, 1999, 2000, 2005, 2006, 2009, 2011, 2012, 2015]:
        color = 'r'
    # non-HAB years
    elif t[inds[0]].year in [1998, 2001, 2002, 2003, 2004, 2007, 2008, 2010, 2013, 2014]:
        color = 'k'
    # for j, ind in enumerate(inds):
        # Plot individual points
    ax.plot(days, along[inds], '-', color=color, lw=3, alpha=0.6)
    # ax.plot(t[inds], along[inds], '-', color='0.2', lw=3, alpha=0.1)
    # Plot means
    # ax.plot([days[0], days[-1]], [alongmean[i], alongmean[i]], '-', color=color, lw=5, alpha=0.7)
    # ax.plot([t[inds][0], t[inds][-1]], [alongmean[i], alongmean[i]], '-', color=color, lw=5, alpha=0.7)

    axes[i].set_xlim(t[inds[0]], t[inds[-1]])


    # ax.plot(years[nhabyears], alongmean[nhabyears], 'ko', ms=10)
    ax.set_xlim(1995, datetime.today().year + 1)
    if wcase == 'April':
        ax.set_ylabel('Mean April along-shore wind [ms$^{-1}$]', fontsize=14)
    elif wcase == 'September':
        ax.set_ylabel('Mean September along-shore wind [ms$^{-1}$]', fontsize=14)
    ax.set_xlabel('Year', fontsize=14)
    ax.set_title('HAB index')
    # Legend
    ax.text(0.02, 0.12, 'HAB year', color='red', fontsize=14, transform=ax.transAxes)
    ax.text(0.02, 0.07, 'non-HAB year', color='black', fontsize=14, transform=ax.transAxes)
    ax.text(0.02, 0.02, 'This year', color='blue', fontsize=14, transform=ax.transAxes)
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
