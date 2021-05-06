#!/bin/python3

# import
import numpy as np
import h5py as h5
import matplotlib.pyplot as plt
import time
import os
import gdal
import light
import cv2
import griddata
from scipy import interpolate
import sys


def gen_ccc(rgb, ns):
    # {{{
    ccc = np.zeros((sum(ns), 3), dtype=float)
    i0 = 0
    for i in range(0, len(ns)):
        i1 = i0+ns[i]
        for j in range(0, 3):
            if ns[i] > 1:
                ccc[i0:i1, j] = np.linspace(rgb[i][j], rgb[i+1][j], ns[i])
        i0 = i1
    return ccc
# }}}


rgb = ((0.2, 0.2, 0), (1, 1, 0), (0.5, 0, 0.5), (1, 0, 1), (1, 0.7, 1),
        (1, 1, 1), (0, 0, 0), (1, 0, 0),
        (1, 1, 0), (0, 1, 0), (0, 1, 1), (0, 0, 0))
ns = [40, 0, 10, 10, 0, 20, 20, 20, 20, 40, 140]
ch8 = gen_ccc(rgb, ns)


# read in data
# {{{
def Data_Cal(NOMChannel, CALChannel):
    CALChannel = np.insert(CALChannel, 0, 0)
    NOMChannel[NOMChannel > 4096] = 0
    TB = CALChannel[NOMChannel]
    return TB


def num2rgb(num, ccc, rg):
    t = num.shape
    rgb = np.zeros([t[0], t[1], 3])
    cl = np.linspace(rg[0], rg[1], num=np.size(ccc[:, 0]))

    rgb[:, :, 0] = np.interp(num, cl, ccc[:, 0])
    rgb[:, :, 1] = np.interp(num, cl, ccc[:, 1])
    rgb[:, :, 2] = np.interp(num, cl, ccc[:, 2])

    return rgb
    pass


filepath = sys.argv[1]
rn = int(sys.argv[2])

lat_fy4a = gdal.Open(
    './lut4k_1.tif').\
    ReadAsArray(0, 0, 2748, 2748)  # 纬度数据
lon_fy4a = gdal.Open(
    './lut4k_2.tif').\
    ReadAsArray(0, 0, 2748, 2748)  # 经度数据

# filepath = './AGRI/L1/FDI/DISK/2019/20190304/' + \
#    'FY4A-_AGRI--_N_DISK_1047E_L1-_FDI-_MULT_NOM_' + \
#    '20190304040000_20190304041459_4000M_V0001.HDF'
f = h5.File(filepath, 'r')
Channel = 12

NOMChannel = f['NOMChannel%s' % (Channel)][:]
CALChannel = f['CALChannel%s' % (Channel)][:]
tb = Data_Cal(NOMChannel, CALChannel)
f.close()
# }}}
tb[np.where(tb < 50)] = np.nan
print(tb.dtype)

plt.imshow(tb)
plt.colorbar()
plt.show()


if False:
    tb = cv2.resize(tb.astype(np.double), (2748*2, 2748*2))
    lon_fy4a = cv2.resize(lon_fy4a.astype(np.double), (2748*2, 2748*2))
    lat_fy4a = cv2.resize(lat_fy4a.astype(np.double), (2748*2, 2748*2))
    print(tb.shape)


if True:
    x4 = np.linspace(0,10,num=2748)
    y4 = np.linspace(0,10,num=2748)
    x42, y42 = np.meshgrid(x4, y4)
    xo = np.linspace(0,10,num=2748*rn)
    yo = np.linspace(0,10,num=2748*rn)
    id = np.where((tb > 0) & (lon_fy4a > -190) & (lat_fy4a > -100))
    sn = 4
    tb = griddata.stb(sn, x42, y42, tb, xo, yo).transpose()
    lon_fy4a = griddata.stb(sn, x42, y42, lon_fy4a, xo, yo)
    lat_fy4a = griddata.stb(sn, x42, y42, lat_fy4a, xo, yo)

plt.imshow(tb)
plt.colorbar()
plt.show()

# imshow total
# {{{
fig = plt.figure(figsize=(14, 7), dpi=100)
ax = fig.add_subplot(1, 2, 1)
tb[np.where(tb < 50)] = np.nan

rg = [-110+273.15, 50+273.15]
tb3 = num2rgb(tb, ch8, rg)

lt = light.point(lon_fy4a, lat_fy4a, 1-tb/20/100*100, np.array([-1,1,1]))

if True:
    lt[lt < 0] = 0
    lt = lt+0.3
    lt[lt > 1] = 1

g = 3
for i in range(0, 2):
    lt = cv2.filter2D(lt, -1, np.ones((g, g))) /\
        cv2.filter2D(np.ones(lt.shape), -1, np.ones((g, g)))

tb4 = tb3+0
tb4[:, :, 0] = tb3[:, :, 2]*lt
tb4[:, :, 1] = tb3[:, :, 1]*lt
tb4[:, :, 2] = tb3[:, :, 0]*lt

cv2.imwrite('disk.tiff', (tb4*255).astype(np.int32))
# }}}
