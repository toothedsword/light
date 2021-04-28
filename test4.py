#!/bin/python3

# import
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import FY4A_FIG
import time_htht as htt

tcfile = './haishen.dat'
tc = np.loadtxt(tcfile)
tclon = tc[:, 5]
tclat = tc[:, 4]
tctime = tclon*0
for i in range(0, tclon.size):
    tctime[i] = htt.vec2time(tc[i, 0], tc[i, 1], tc[i, 2], tc[i, 3], 0, 0)

t = htt.str2time('20200905000000', 'yyyymmddHHMMSS')
t1 = htt.str2time('20200906000000', 'yyyymmddHHMMSS')

while t <= t1:

# grid figure
# {{{

    tclon1 = np.interp(t, tctime, tclon)
    tclat1 = np.interp(t, tctime, tclat)

    latlim = [-8+tclat1, 8+tclat1]
    lonlim = [-8+tclon1, 8+tclon1]
    print(htt.time2str(t, 'yyyymmdd_HHMMSS'))

    try:
        lon2, lat2, tb2, tb3, tb4, lat_fy4a, lon_fy4a, ccc = \
            FY4A_FIG.get_tb3(t, lonlim, latlim, addlight=True)

        fig = plt.figure(figsize=(20, 12), dpi=100)
        ax = fig.add_subplot(1, 2, 1)
        ax.imshow(np.flip(tb3, 0), extent=(lonlim[0], lonlim[1], latlim[0], latlim[1]))
        plt.title('griddata')
        ax, _ = mpl.colorbar.make_axes(plt.gca(), shrink=0.5)
        cbar = mpl.colorbar.ColorbarBase(
            ax, cmap=ccc, norm=mpl.colors.Normalize(vmin=-110, vmax=50))
# }}}

# light figure
# {{{
        try:
            ax = fig.add_subplot(1, 2, 2)
            f = ax.imshow(np.flip(tb4, 0), cmap=ccc,
                        extent=(lonlim[0], lonlim[1], latlim[0], latlim[1]))
            plt.title('griddata.light')

            ax, _ = mpl.colorbar.make_axes(plt.gca(), shrink=0.5)
            cbar = mpl.colorbar.ColorbarBase(
                ax, cmap=ccc, norm=mpl.colors.Normalize(vmin=-110, vmax=50))
        except:
            pass
        # plt.show()
        fig.savefig(tcfile+'_'+htt.time2str(t, 'yyyymmdd_HHMMSS')+'.png', dpi=200)
    except:
        pass


    t = t+3*3600
# }}}
