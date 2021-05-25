#!/bin/python3

# import
import numpy as np
import h5py as h5
import gdal
import light
import cv2
import griddata
import sys
import matplotlib.pyplot as plt
import matplotlib as mpl
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
    cl = np.linspace(rg[0], rg[1], num=np.size(cc0[:, 0]))

    rgb[:, :, 0] = np.interp(num, cl, cc0[:, 0])
    rgb[:, :, 1] = np.interp(num, cl, cc0[:, 1])
    rgb[:, :, 2] = np.interp(num, cl, cc0[:, 2])

    return rgb
    pass


def v2light(v, vlon, vlat, rg=[-4, 4]):

    infile = './topo.nc'
    f = h5.File(infile, 'r')
    topo = f['topo'][:]
    topo = topo/1000
    topo = topo[0::2, 0::2]
    f.close()

    lon = np.linspace(60, 150, topo.shape[1])
    lat = np.linspace(0, 60, topo.shape[0])
    lon2, lat2 = np.meshgrid(lon, lat)
    v2 = griddata.stb(3, vlat, vlon, v, lat, lon)

    rg = [-4, 4]
    v3 = num2rgb(v2, cc0, rg)

    lt = light.point(lon2, lat2, topo*10, np.array([-1, 1, 1]))
    if True:
        lt[lt < 0] = 0
        lt = lt+0.3
        lt[lt > 1] = 1

    g = 3
    for i in range(0, 0):
        lt = cv2.filter2D(lt, -1, np.ones((g, g))) /\
            cv2.filter2D(np.ones(lt.shape), -1, np.ones((g, g)))

    v4 = v3+0
    v4[:, :, 0] = v3[:, :, 2]*lt
    v4[:, :, 1] = v3[:, :, 1]*lt
    v4[:, :, 2] = v3[:, :, 0]*lt
    return v3, v4


if __name__ == "__main__":

    rgb = ((1, 0, 0), (1, 1, 0), (0, 1, 0), (0, 1, 1), (0, 0, 1))
    cc0 = gen_ccc(rgb, [20, 20, 20, 20])
    ccc = colors.ListedColormap(cc0.tolist(), name='test1')

    infile = './topo.nc'
    f = h5.File(infile, 'r')
    topo = f['topo'][:]
    topo = topo/1000
    topo = topo[0::2, 0::2]
    f.close()

    lon = np.linspace(60, 150, topo.shape[1])
    lat = np.linspace(0, 60, topo.shape[0])
    lon2, lat2 = np.meshgrid(lon, lat)
    topo3, topo4 = v2light(topo, lon2, lat2)

    lonlim = [60, 150]
    latlim = [0, 60]
    outfile = 'test_topo.png'
    fig = plt.figure(figsize=(8, 6), dpi=1600)
    ax = fig.add_subplot(1, 1, 1)
    f = ax.imshow(
        np.flip(topo4, 0), cmap=ccc,
        extent=(lonlim[0], lonlim[1], latlim[0], latlim[1]))
    ax.set_xlim(lonlim)
    ax.set_ylim(latlim)
    cll = np.loadtxt('china+coast.txt')
    ax.plot(cll[:, 0], cll[:, 1], 'k-', linewidth=0.2)

    ax, _ = mpl.colorbar.make_axes(plt.gca(), shrink=0.5)
    cbar = mpl.colorbar.ColorbarBase(
        ax, cmap=ccc, norm=mpl.colors.Normalize(vmin=-110, vmax=50))
    fig.savefig(outfile, dpi=1600)
    plt.close()
    # cv2.imwrite(outfile, (topo4*255).astype(np.int32))
