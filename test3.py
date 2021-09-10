#!/bin/python3

# import
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import FY4A_FIG
import time_htht as htt

# grid figure
# {{{
latlim = [-23, -7]
lonlim = [66, 83]

lon2, lat2, tb2, tb3, tb4, lat_fy4a, lon_fy4a, ccc = \
    FY4A_FIG.get_tb3(htt.str2time('20210722000000', 'yyyymmddHHMMSS'),
                     lonlim, latlim, addlight=True)

fig = plt.figure(figsize=(20, 12), dpi=100)
ax = fig.add_subplot(1, 2, 1)
ax.imshow(np.flip(tb2, 0), extent=(lonlim[0], lonlim[1], latlim[0], latlim[1]))
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
plt.show()
# }}}
