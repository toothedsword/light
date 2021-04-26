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

lat_fy4a = gdal.Open(
    '/home/leon/data/ADS_TCPIE/ADS_QPE/data/source/lut4k_1.tif').\
    ReadAsArray(0, 0, 2748, 2748)  # 纬度数据
lon_fy4a = gdal.Open(
    '/home/leon/data/ADS_TCPIE/ADS_QPE/data/source/lut4k_2.tif').\
    ReadAsArray(0, 0, 2748, 2748)  # 经度数据

filepath = '/home/leon/data/FY4A_new/AGRI/L1/FDI/DISK/2019/20190304/' + \
    'FY4A-_AGRI--_N_DISK_1047E_L1-_FDI-_MULT_NOM_' + \
    '20190304040000_20190304041459_4000M_V0001.HDF'
f = h5.File(filepath, 'r')
Channel = 12

NOMChannel = f['NOMChannel%s' % (Channel)][:]
CALChannel = f['CALChannel%s' % (Channel)][:]
tb = Data_Cal(NOMChannel, CALChannel)
f.close()
# }}}

# imshow total
# {{{
fig = plt.figure(figsize=(14, 7), dpi=100)
ax = fig.add_subplot(1, 2, 1)
tb[np.where(tb < 50)] = np.nan

ccc = np.array(
    [[1,0,0],[1,1,0],[0,1,0],[0,1,1],[0,0,1],[1,0,1]
    ])
rg = [170, 320]
tb3 = num2rgb(tb, ccc, rg)

l = light.point(lon_fy4a, lat_fy4a, tb/20/100*20, np.array([0,1,1]))
# l = cv2.filter2D(l, -1, np.ones((5, 5)))/cv2.filter2D(np.ones(l.shape), -1, np.ones((5, 5)))
l = l/8+1

tb3[:,:,0] = tb3[:,:,0]*l
tb3[:,:,1] = tb3[:,:,1]*l
tb3[:,:,2] = tb3[:,:,2]*l

plt.imshow(tb3, cmap='jet')
#plt.colorbar()
plt.title('disk')

lat_gd = np.linspace(-80, 80, 2800)
lon_gd = np.linspace(20, 180, 3000)
sn = 3
lat_gd = np.linspace(-27, -7, 1600)
lon_gd = np.linspace(57, 87, 2000)
sn = 200

time_start = time.time()
id = np.where((tb > 0) & (lon_fy4a > -190) & (lat_fy4a > -100))
tb_gd = griddata.simple(sn, lon_fy4a[id], lat_fy4a[id],
                        tb[id], lon_gd, lat_gd)
time_end = time.time()
print('time cost', time_end - time_start, 's')
tb_gd2 = tb_gd
tb_gd2[np.where(tb_gd2 < 10)] = np.nan
tb_gd2[np.where(tb_gd2 < 100)] = 100
tb_gd2[np.where(tb_gd2 > 330)] = 330
ax = fig.add_subplot(1, 2, 2)

tb2 = np.flip(tb_gd2.transpose(), 0)
lon2, lat2 = np.meshgrid(lon_gd, lat_gd)
l = light.point(lon2, lat2, tb2/20/100*200, np.array([-1,-1,1]))
l = 1-l/8
for i in range(0,1):
    l = cv2.filter2D(l, -1, np.ones((5, 5)))/cv2.filter2D(np.ones(l.shape), -1, np.ones((5, 5)))
ccc = np.array(
    [[1,0,0],[1,1,0],[0,1,0],[0,1,1],[0,0,1],[1,0,1]
    ])
rg = [190, 320]
tb3 = num2rgb(tb2, ccc, rg)
if True:
    tb3[:,:,0] = tb3[:,:,0]*l
    tb3[:,:,1] = tb3[:,:,1]*l
    tb3[:,:,2] = tb3[:,:,2]*l

ax.imshow(tb3, cmap='jet')
plt.title('griddata.simple')
# plt.colorbar()
plt.show()

# }}}
