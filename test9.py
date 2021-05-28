#!/bin/python3
"""
突出地形和突出低温
卡阈值突出显示
"""

# import
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import FY4A_FIG
import time_htht as htt
import os
import gc
import re
import sys
import glob


tcname = sys.argv[1]
ft = sys.argv[2]
cll = np.loadtxt('china+coast.txt')
tcfile = './' + tcname + '.dat'
tc = np.loadtxt(tcfile)
tclon = tc[:, 5]
tclat = tc[:, 4]
tctime = tclon*0
for i in range(0, tclon.size):
    tctime[i] = htt.vec2time(tc[i, 0], tc[i, 1], tc[i, 2], tc[i, 3], 0, 0)

t = np.min(tctime)
t1 = np.max(tctime)

while t <= t1:

    # grid figure
    # {{{

    tclon1 = np.interp(t, tctime, tclon)
    tclat1 = np.interp(t, tctime, tclat)

    os.system('mkdir -p ./figure/' + ft + '/')
    figname = './figure/' + ft + '/' + tcfile + '_' + ft + '_' +\
        htt.time2str(t, 'yyyymmdd_HHMMSS')
    print('----------------------------------')
    print(figname)
    if re.search('big', figname):
        latlim = [-20+tclat1, 20+tclat1]
        lonlim = [-20+tclon1, 20+tclon1]
    if re.search('mid', figname):
        latlim = [-15+tclat1, 15+tclat1]
        lonlim = [-15+tclon1, 15+tclon1]
    if re.search('small', figname):
        latlim = [-10+tclat1, 10+tclat1]
        lonlim = [-10+tclon1, 10+tclon1]
    print(htt.time2str(t, 'yyyymmdd_HHMMSS'))
    gc.collect()
    fignames = glob.glob(figname+'*.png')
    if len(fignames) > 0:
        t = t+1*60
        continue

    try:
        lighttype = 'tb'
        if re.search('_topo_', figname):
            lighttype = 'topo'
        if re.search('_topocth_', figname):
            lighttype = 'cth'
        lon2, lat2, tb2, tb3, tb4, lat_fy4a, lon_fy4a, ccc = \
            FY4A_FIG.get_tb3(t, lonlim, latlim, addlight=True,
                             lighttype=lighttype, ctype='swap',
                             tbrg=[-400, -37], miss=40)

        pn = np.sum(tb2 > 50)/np.sum(lon2 > -360)*100
        spn = str(int(pn))
        fig = plt.figure(figsize=(8, 6), dpi=100)
        ax = fig.add_subplot(1, 1, 1)
        f = ax.imshow(
            np.flip(tb4, 0), cmap=ccc,
            extent=(lonlim[0], lonlim[1], latlim[0], latlim[1]))
        plt.title(htt.time2str(t, 'yyyy/mm/dd HH:MM:SS'))
        # ax.plot(tclon, tclat, 'r-+', linewidth=0.5)
        # ax.plot(tclon1, tclat1, 'g+', linewidth=0.5, markersize=20)
        ax.set_xlim(lonlim)
        ax.set_ylim(latlim)
        # ax.plot(cll[:, 0], cll[:, 1], 'k-', linewidth=0.5)

        ax, _ = mpl.colorbar.make_axes(plt.gca(), shrink=0.5)
        cbar = mpl.colorbar.ColorbarBase(
            ax, cmap=ccc, norm=mpl.colors.Normalize(vmin=-110, vmax=50))
        figname1 = figname+'.'+spn+'.png'
        fig.savefig(figname1, dpi=200)
        plt.close()

    except Exception as ex:
        print(ex)
    else:
        print('succeed')

    t = t+1*60
    # }}}
