
import urllib
import urllib2
import re
import gzip
import os
from datetime import datetime
from math import sin, cos, pi
import glob
import pdb

import numpy as np
import pylab

def retrieve_noaa_winds(station_id, data_type='hourly'):
    """Read NOAA winds from web site or file

    Rob's file, adjust by Kristen
    
    Parameters
    ----------
    station_id : string
        The id of the station, like 'burl1' or '42040'
    data_type : ('hourly' or 'h', 'continuous' or 'c')
        The type of data to collect.  Continuous winds are every 10 min.
    
    Returns
    -------
    noaa_wind : ndarray
        The NOAA wind object array contains the date keys:
            dates       : Dates of wind observations
            u           : (EW) wind component
            v           : (NS) wind component.
            direction   : Direction of wind []
            speed       : Wind speed [m/s]
    
    """

    # Get data, historical and through almost present day
    if data_type[0].lower() == 'c':
        # historical data
        url_root_his = 'http://www.ndbc.noaa.gov/data/historical/cwind/'
        url_root_new = 'http://www.ndbc.noaa.gov/data/cwind/'
    else:
        # historical data
        url_root_his = 'http://www.ndbc.noaa.gov/data/historical/stdmet/'
        url_root_new = 'http://www.ndbc.noaa.gov/data/stdmet/'
    mons = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug',
            'Sep', 'Oct', 'Nov', 'Dec']
    url_root_recent = 'http://www.ndbc.noaa.gov/data/realtime2/'
    url_roots = []
    url_roots.append(url_root_his)
    for mon in mons:
        url_roots.append(url_root_new + mon + '/')
    url_roots.append(url_root_recent)
    
    p = re.compile(station_id + '\w*\.txt\.gz', re.IGNORECASE)
    noaa_files = []
    for url_root in url_roots:
        # if 'realtime' in url_root:
        #     pdb.set_trace()
        lines = urllib2.urlopen(url_root).readlines()
        for line in lines:
            m = p.search(line)
            if m:
                # pdb.set_trace()
                noaa_file = m.group()
                noaa_files.append(noaa_file)
                if not noaa_file in os.listdir('.'):
                # if not os.path.exists(noaa_file):
                    print ' ### Downloading ', url_root + noaa_file
                    urllib.urlretrieve(url_root + noaa_file, noaa_file)
                else:
                    print ' ### %s already exists. ' % noaa_file
            else: # if txt.gz doesn't exist, check for just .txt
                ptxt = re.compile(station_id + '\w*\.txt', re.IGNORECASE)
                m = ptxt.search(line)
                if m:
                    # pdb.set_trace()
                    noaa_file = m.group()
                    noaa_files.append(noaa_file)
                    if not noaa_file in os.listdir('.'):
                    # if not os.path.exists(noaa_file):
                        print ' ### Downloading ', url_root + noaa_file
                        temp_fname, headers = urllib.urlretrieve(url_root + noaa_file, noaa_file)
                        # resave file to a new name
                        save_fname = url_root.split('/')[-2] + '_' + temp_fname
                        # pdb.set_trace()
                        os.system('mv ' + temp_fname + ' ' + save_fname)
                        noaa_files.pop(-1) # get rid of old file name
                        noaa_files.append(save_fname) # add on new file name
                    else:
                        print ' ### %s already exists. ' % noaa_file

    # pdb.set_trace()
    # Process wind data (read straight from gzipped file)
    wind_data =[]
    for noaa_file in noaa_files:
        print ' ... processing ', noaa_file
        # pdb.set_trace()
        if '.gz' in noaa_file:
            f = gzip.open(noaa_file)
        else:
            f = open(noaa_file)
        line = f.readline()
        if line[0] == '#':
            line = line[1:]
        dataline = line.split()
        if 'YYYY' in dataline:
            yr_idx = dataline.index('YYYY')
        else:
            yr_idx = dataline.index('YY')
        mo_idx = dataline.index('MM')
        da_idx = dataline.index('DD')
        hr_idx = dataline.index('hh')
        if 'mm' in dataline:
            mn_idx = dataline.index('mm')
        else:
            mn_idx = None
        if 'SPD' in dataline:
            speed_idx = dataline.index('SPD')
        else:
            speed_idx = dataline.index('WSPD')
        if 'WDIR' in dataline:
            dir_idx = dataline.index('WDIR')
        elif 'DIR' in dataline:
            dir_idx = dataline.index('DIR')            
        else:
            dir_idx = dataline.index('WD')
        for line in f.readlines():
            if line[0] == '#': continue
            data = line.split()
            if len(data) == 0:
                continue
            yr = int(data[yr_idx])
            if yr < 1900:
                yr = yr+1900
            mo = int(data[mo_idx])
            da = int(data[da_idx])
            hr = int(data[hr_idx])
            if mn_idx is None:
                date = datetime(yr, mo, da, hr)
            else:
                mn = int(data[mn_idx])
                date = datetime(yr, mo, da, hr, mn)
            
            # if 'realtime2' in noaa_file and data[dir_idx]=='MM':
            #     pdb.set_trace()
            if not data[dir_idx] == 'MM': # if =='MM' don't want line
                direction = float(data[dir_idx])
                speed = float(data[speed_idx])
                u = -1.0 * speed * sin(direction*pi/180.0)  # convert to Oceanographic convention
                v = -1.0 * speed * cos(direction*pi/180.0)
                
                if speed != 99.0:
                    wind_data.append( (date, u, v, direction, speed) )
    
    wind_data =  np.array( wind_data, 
                    dtype=[('date','O'),
                           ('u','double'), ('v','double'), 
                           ('direction', 'double'), ('speed', 'double')])
    
    wind_data.sort(order='date')
    ud = np.unique(wind_data['date'])
    idx = wind_data['date'].searchsorted(ud)
    
    return wind_data[idx]


if __name__ == '__main__':
    noaa_42007c = retrieve_noaa_winds('42007', 'c')
    np.save('noaa_42007c', noaa_42007c)
    noaa_42007h = retrieve_noaa_winds('42007', 'h')
    np.save('noaa_42007h', noaa_42007h)

    noaa_burl1c = retrieve_noaa_winds('burl1', 'c')
    np.save('noaa_burl1c', noaa_burl1c)
    noaa_burl1h = retrieve_noaa_winds('burl1', 'h')
    np.save('noaa_burl1h', noaa_burl1h)

    noaa_42040c = retrieve_noaa_winds('42040', 'c')
    np.save('noaa_42040c', noaa_42040c)
    noaa_42040h = retrieve_noaa_winds('42040', 'h')
    np.save('noaa_42040h', noaa_42040h)

