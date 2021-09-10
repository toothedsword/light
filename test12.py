#!/bin/python3
"""
利用地形和云高作为阴影
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



lighttype = 'topo'
lon2, lat2, tb2, tb3, tb4, lat_fy4a, lon_fy4a, ccc = \
    FY4A_FIG.get_tb3(t, lonlim, latlim, addlight=True,
                        lighttype=lighttype, ctype='topo',
                        tbrg=[-400, -37], miss=40)

pn = np.sum(tb2 > 50)/np.sum(lon2 > -360)*100
spn = str(int(pn))
fig = plt.figure(figsize=(8, 6), dpi=100)
ax = fig.add_subplot(1, 1, 1)
f = ax.imshow(
    np.flip(tb4, 0), cmap=ccc,
    extent=(lonlim[0], lonlim[1], latlim[0], latlim[1]))
plt.title(htt.time2str(t, 'yyyy/mm/dd HH:MM:SS'))
ax.set_xlim(lonlim)
ax.set_ylim(latlim)

ax, _ = mpl.colorbar.make_axes(plt.gca(), shrink=0.5)
cbar = mpl.colorbar.ColorbarBase(
    ax, cmap=ccc, norm=mpl.colors.Normalize(vmin=-110, vmax=50))
figname1 = figname+'.'+spn+'.png'
fig.savefig(figname1, dpi=200)
plt.close()

