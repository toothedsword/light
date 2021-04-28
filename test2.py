#!/bin/python3

# import
import numpy as np
import h5py as h5
import matplotlib.pyplot as plt
import time
import gdal
import light
import cv2
import griddata


def gen_ccc(rgb, ns):
    # {{{
    ccc = np.zeros((sum(ns), 3), dtype=float)
    i0 = 0
    for i in range(0, len(ns)):
        i1 = i0+ns[i]
        for j in range(0, 3):
            if ns[i] > 1:
                print(i1)
                ccc[i0:i1, j] = np.linspace(rgb[i][j], rgb[i+1][j], ns[i])
        i0 = i1
    return ccc
# }}}


# get ccc
# {{{
rgb = ((0.2, 0.2, 0), (1, 1, 0), (0.5, 0, 0.5), (1, 0, 1), (1, 0.7, 1),
       (1, 1, 1), (0, 0, 0), (1, 0, 0),
       (1, 1, 0), (0, 1, 0), (0, 1, 1), (0, 0, 0))
ns = [40, 0, 10, 10, 0, 20, 20, 20, 20, 40, 140]
ch8 = gen_ccc(rgb, ns)

rgb = ((0, 0, 0), (0, 0, 1), (0.5, 0, 0.5), (1, 0, 1), (1, 0.7, 1),
       (1, 1, 1), (0, 0, 0), (1, 0, 0),
       (1, 1, 0), (0, 1, 0), (0, 1, 1), (0, 0, 0))
ns = [40, 0, 10, 10, 0, 20, 20, 20, 20, 40, 140]
th8 = gen_ccc(rgb, ns)
# }}}


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


# imshow
# {{{
tb[np.where(tb < 50)] = np.nan

latlim = [-23, -7]
lonlim = [66, 83]
# latlim = [-28, -2]
# lonlim = [61, 88]
lat_gd = np.linspace(latlim[0], latlim[1], num=2000)  # (latlim[1]-latlim[0])*200)
lon_gd = np.linspace(lonlim[0], lonlim[1], num=2500)  # (lonlim[1]-lonlim[0])*200)
sn = 200

time_start = time.time()
id = np.where((tb > 0) & (lon_fy4a > -190) & (lat_fy4a > -100))
if False:
    tb2 = griddata.simple(sn, lat_fy4a[id], lon_fy4a[id],
                            tb[id], lat_gd, lon_gd)
else:
    tb2 = griddata.stb(sn, np.flip(lat_fy4a, 0),
                         np.flip(lon_fy4a, 0),
                         np.flip(tb, 0), lat_gd, lon_gd)
time_end = time.time()
print('time cost', time_end - time_start, 's')
tb2[np.where(tb2 < 10)] = np.nan
tb2[np.where(tb2 < 100)] = 100
tb2[np.where(tb2 > 330)] = 330

ccc = np.array(
    [[1, 0, 0], [1, 1, 0], [0, 1, 0], [0, 1, 1], [0, 0, 1], [1, 0, 1]
     ])
rg = [-110+273.15, 50+273.15]
rg = [-100+273.15, 40+273.15]
# rg = [190, 320]
tb3 = num2rgb(tb2, ch8, rg)

fig = plt.figure(figsize=(20, 12), dpi=100)
ax = fig.add_subplot(1, 2, 1)
ax.imshow(np.flip(tb3, 0), extent=(lonlim[0], lonlim[1], latlim[0], latlim[1]))
plt.title('griddata.simple')
# }}}


# light
# {{{
ax = fig.add_subplot(1, 2, 2)

lon2, lat2 = np.meshgrid(lon_gd, lat_gd)
print(lon2)
lt = light.point(lon2, lat2, 1-tb2/20/100*20, np.array([-1, 1, 1]))
if True:
    lt[lt < 0] = 0
    lt = lt+0.3
    lt[lt > 1] = 1

print(lt)
g = 5
for i in range(0, 3):
    lt = cv2.filter2D(lt, -1, np.ones((g, g))) /\
         cv2.filter2D(np.ones(lt.shape), -1, np.ones((g, g)))

if True:
    tb3[:, :, 0] = tb3[:, :, 0]*lt
    tb3[:, :, 1] = tb3[:, :, 1]*lt
    tb3[:, :, 2] = tb3[:, :, 2]*lt

f = ax.imshow(np.flip(tb3, 0), cmap='jet', extent=(lonlim[0], lonlim[1], latlim[0], latlim[1]))
plt.title('griddata.light')
# plt.colorbar(f)
# fig.savefig('test.png', dpi=600)
# }}}

if False:
    ax = fig.add_subplot(2, 2, 3)
    f = ax.pcolor(lon2, lat2, tb_gd2)
    plt.colorbar(f)

plt.show()

