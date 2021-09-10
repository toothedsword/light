import numpy as np
import h5py as h5
import gdal
from netCDF4 import Dataset
from numpy import dtype
import re


def Data_Cal(NOMChannel, CALChannel):
    CALChannel = np.insert(CALChannel, 0, 0)
    NOMChannel[NOMChannel > 4096] = 0
    TB = CALChannel[NOMChannel]
    return TB


infile = '/home/leon/Downloads/cma2loc_2021-8-10_16.25.57/FY4A-_AGRI--_N_REGC_1047E_L1-_FDI-_MULT_NOM_20210720083000_20210720083417_4000M_V0001.HDF'
infile = './FY4A-_AGRI--_N_REGC_1047E_L1-_FDI-_MULT_NOM_20210720003000_20210720003417_4000M_V0001.HDF'

f = h5.File(infile, 'r')
Channel = 12

NOMChannel = f['NOMChannel%s' % (Channel)][:]
CALChannel = f['CALChannel%s' % (Channel)][:]
bln = f.attrs[u'Begin Line Number'][0]
eln = f.attrs[u'End Line Number'][0]
bpn = f.attrs[u'Begin Pixel Number'][0]
epn = f.attrs[u'End Pixel Number'][0]
print('bln=', bln)
tb = Data_Cal(NOMChannel, CALChannel)
f.close()
tb[np.where(tb < 50)] = np.nan

lat_fy4a = gdal.Open('./lut4k_1.tif').\
    ReadAsArray(0, 0, 2748, 2748)  # 纬度数据
lon_fy4a = gdal.Open('./lut4k_2.tif').\
    ReadAsArray(0, 0, 2748, 2748)  # 经度数据

tb0 = lon_fy4a*0-100
tb0[bln:eln+1, bpn:epn+1] = tb
tb = tb0


# open a netCDF file to write
outfile = re.sub(r'.*\/','',infile)
outfile = re.sub('HDF$','NC',outfile)
ncout = Dataset(outfile, 'w', format='NETCDF4')


if True:
    id = (lat_fy4a > 10) & (lat_fy4a < 50) & (lon_fy4a > 100) & (lon_fy4a < 140)
    lat_fy4a = lat_fy4a[id]
    lon_fy4a = lon_fy4a[id]
    tb = tb[id]

    # define axis size
    ncout.createDimension('x', lat_fy4a.shape[0])

    # create variable array
    vout = ncout.createVariable('tb', dtype('double').char, ('x'))
    vout.long_name = '11微米亮温'
    vout.units = 'K'
    vout[:] = tb[:]

    # create variable array
    vout1 = ncout.createVariable('lon', dtype('double').char, ('x'))
    vout1.long_name = 'Longitude'
    vout1.units = 'degree'
    vout1[:] = lon_fy4a[:]

    # create variable array
    vout2 = ncout.createVariable('lat', dtype('double').char, ('x'))
    vout2.long_name = 'Latitude'
    vout2.units = 'degree'
    vout2[:] = lat_fy4a[:]

    # close files
    ncout.close()
    exit()

# define axis size
ncout.createDimension('x', lat_fy4a.shape[0])
ncout.createDimension('y', lon_fy4a.shape[0])

# create variable array
vout = ncout.createVariable('tb', dtype('double').char, ('x', 'y'))
vout.long_name = '11微米亮温'
vout.units = 'K'
vout[:] = tb[:]

# create variable array
vout1 = ncout.createVariable('lon', dtype('double').char, ('x', 'y'))
vout1.long_name = 'Longitude'
vout1.units = 'degree'
vout1[:] = lon_fy4a[:]

# create variable array
vout2 = ncout.createVariable('lat', dtype('double').char, ('x', 'y'))
vout2.long_name = 'Latitude'
vout2.units = 'degree'
vout2[:] = lat_fy4a[:]

# close files
ncout.close()
