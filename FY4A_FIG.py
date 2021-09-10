#!/bin/python3

# import
import numpy as np
import h5py as h5
import gdal
import light
import cv2
import griddata
import re
import time_htht as htt
import glob
from matplotlib import colors


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


def get_tb3(dtime, lonlim, latlim, addlight=True,
            lon_gd='', lat_gd='',
            lat_fy4a='./lut4k_1.tif',
            lon_fy4a='./lut4k_2.tif',
            file_re_path='./AGRI/L1/FDI/*/yyyy/yyyymmdd/' +
            'FY4A-_AGRI--_N_*_1047E_L1-_FDI-_MULT_NOM_' +
            'yyyymmddHHMM??_*_4000M_V0001.HDF',
            filepath=-1, lighttype='tb', ctype='ch8',
            tbrg=[-300, 400], miss=-999):

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
    rg = [-110+273.15, 50+100+273.15]
    if ctype == 'swap':
        rgb = ((1, 1, 1), (0, 0, 0), (1, 0, 0), (1, 1, 0), (0, 1, 0),
            (0, 0, 1), (0, 1, 1), (0.8, 0.8, 0.8), (0.1, 0.1, 0.1))
        ns = [10, 10, 10, 10, 10, 10, 10, 80]
        ch8 = gen_ccc(rgb, ns)
        rg = [-90+273.15, 60+273.15]
    if ctype == 'gray':
        rgb = ((1, 1, 1), (0, 0, 0))
        ns = [200]
        ch8 = gen_ccc(rgb, ns)
        rg = [-90+273.15, 60+273.15]

        pass
    # th8 = gen_ccc(rgb, ns)
    # }}}

    # read in data
    print('read')
    # {{{

    if re.search('str', str(type(filepath))):
        pass
    else:
        filepath = htt.time2str(dtime, file_re_path, num=3)
        print(filepath)
        filepath = glob.glob(filepath)
        filepath = filepath[0]

    f = h5.File(filepath, 'r')
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
    # tb[np.where(tb < tbrg[0]+273.15)] = miss
    # tb[np.where(tb > tbrg[1]+273.15)] = miss
    # }}}

    # griddata
    print('griddata')
    # {{{
    if re.search('str', str(type(lat_fy4a))):
        lat_fy4a = gdal.Open(lat_fy4a).\
            ReadAsArray(0, 0, 2748, 2748)  # 纬度数据
        lon_fy4a = gdal.Open(lon_fy4a).\
            ReadAsArray(0, 0, 2748, 2748)  # 经度数据

    if re.search('str', str(type(lat_gd))):
        lat_gd = np.linspace(latlim[0], latlim[1], num=2000)
    if re.search('str', str(type(lon_gd))):
        lon_gd = np.linspace(lonlim[0], lonlim[1], num=2000)
    sn = 200
    tb0 = lon_fy4a*0-100
    tb0[bln:eln+1, bpn:epn+1] = tb
    tb = tb0

    id = np.where((tb > 0) & (lon_fy4a > -190) & (lat_fy4a > -100))
    if False:
        tb2 = griddata.simple(sn, lat_fy4a[id], lon_fy4a[id],
                              tb[id], lat_gd, lon_gd)
    else:
        tb2 = griddata.stb(sn, np.flip(lat_fy4a, 0),
                           np.flip(lon_fy4a, 0),
                           np.flip(tb, 0), lat_gd, lon_gd)

    tb2[np.where(tb2 < 10)] = np.nan
    # tb2[np.where(tb2 < tbrg[0]+273.15)] = miss
    # tb2[np.where(tb2 > tbrg[1]+273.15)] = miss

    tb3 = num2rgb(tb2, ch8, rg)
    # }}}

    # light
    print('light')
    # {{{
    lon2, lat2 = np.meshgrid(lon_gd, lat_gd)
    tb4 = -1
    if addlight:
        if lighttype == 'tb':
            cth = 1-tb2/20/100*20
        if lighttype == 'topo':
            f = h5.File('./topo_fy4a_4km.nc', 'r')
            topo = f['topo'][:]
            topo = np.flip(topo.T, 0)
            f.close()
            topo = griddata.stb(sn, np.flip(lat_fy4a, 0),
                                np.flip(lon_fy4a, 0),
                                np.flip(topo, 0), lat_gd, lon_gd)
            cth = topo
        if lighttype == 'topocth':
            f = h5.File('./topo_fy4a_4km.nc', 'r')
            topo = f['topo'][:]
            topo = np.flip(topo.T, 0)
            f.close()
            cth_file = re.sub(r'\.HDF', r'.NC', filepath)
            cth_file = re.sub(r'FDI', r'CTH', cth_file)
            cth_file = re.sub(r'L1', r'L2', cth_file)
            cth_file = re.sub(r'\/DISK\/', '/DISK/NOM/', cth_file)
            cth_file = re.sub(r'\/REGC\/', '/REGC/NOM/', cth_file)
            print(cth_file)
            f = h5.File(cth_file, 'r')
            cth = f['CTH'][:]
            cth_bln = f['geospatial_lat_lon_extent'].attrs[u'begin_line_number'][0]
            cth_eln = f['geospatial_lat_lon_extent'].attrs[u'end_line_number'][0]
            cth_bpn = f['geospatial_lat_lon_extent'].attrs[u'begin_pixel_number'][0]
            cth_epn = f['geospatial_lat_lon_extent'].attrs[u'end_pixel_number'][0]
            cth0 = lon_fy4a*0-100
            cth0[cth_bln:cth_eln+1, cth_bpn:cth_epn+1] = cth
            cth = cth0
            f.close()
            topo0 = griddata.stb(sn, np.flip(lat_fy4a, 0),
                                 np.flip(lon_fy4a, 0),
                                 np.flip(topo, 0), lat_gd, lon_gd)
            topo[np.where(cth > 0)] = cth[np.where(cth > 0)]
            topo = griddata.stb(sn, np.flip(lat_fy4a, 0),
                                np.flip(lon_fy4a, 0),
                                np.flip(topo, 0), lat_gd, lon_gd)
            cth = topo
            cth[np.where(tb2 == miss)] = topo0[np.where(tb2 == miss)]

        if lighttype == 'tbtopo':
            cth = 1-tb2/20/100*20
            f = h5.File('./topo_fy4a_4km.nc', 'r')
            topo = f['topo'][:]
            topo = np.flip(topo.T, 0)
            f.close()
            topo0 = griddata.stb(sn, np.flip(lat_fy4a, 0),
                                 np.flip(lon_fy4a, 0),
                                 np.flip(topo, 0), lat_gd, lon_gd)
            topo[np.where(cth > 0)] = cth[np.where(cth > 0)]
            topo = griddata.stb(sn, np.flip(lat_fy4a, 0),
                                np.flip(lon_fy4a, 0),
                                np.flip(topo, 0), lat_gd, lon_gd)
            # cth[np.where(tb2 == miss)] = topo0[np.where(tb2 == miss)]
            idout = np.where((tb2-273.15 < tbrg[0]) | (tb2-273.15 > tbrg[1]))
            cth[idout] = topo0[idout]

        lt = light.point(lon2, lat2, cth, np.array([-1, 1, 1]))
        if True:
            lt[lt < 0] = 0
            lt = lt+0.3
            lt[lt > 1] = 1

        g = 5
        for i in range(0, 3):
            lt = cv2.filter2D(lt, -1, np.ones((g, g))) /\
                cv2.filter2D(np.ones(lt.shape), -1, np.ones((g, g)))

        tb4 = tb3+0
        tb4[:, :, 0] = tb4[:, :, 0]*lt
        tb4[:, :, 1] = tb4[:, :, 1]*lt
        tb4[:, :, 2] = tb4[:, :, 2]*lt
    # }}}

    ccc = colors.ListedColormap(ch8.tolist(), name='test1')
    return lon2, lat2, tb2, tb3, tb4, lat_fy4a, lon_fy4a, ccc
