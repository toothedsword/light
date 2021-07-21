
import griddata
import numpy as np
import gdal
import cv2


lat_fy4a = './lut4k_1.tif',
lon_fy4a = './lut4k_2.tif',
lat_fy4a = gdal.Open(lat_fy4a).\
    ReadAsArray(0, 0, 2748, 2748)  # 纬度数据
lon_fy4a = gdal.Open(lon_fy4a).\
    ReadAsArray(0, 0, 2748, 2748)  # 经度数据

figname = 'in.tiff'
rgb = cv2.imread(figname)
r = rgb[:, :, 0]
g = rgb[:, :, 1]
b = rgb[:, :, 2]

lonlim = [-180, 180]
latlim = [-90, 90]

lat_gd = np.linspace(latlim[0], latlim[1], num=2000)
lon_gd = np.linspace(lonlim[0], lonlim[1], num=2000)

r2 = griddata.stb(3, np.flip(lat_fy4a, 0), np.flip(lon_fy4a, 0),
                  np.flip(r, 0), lat_gd, lon_gd)
g2 = griddata.stb(3, np.flip(lat_fy4a, 0), np.flip(lon_fy4a, 0),
                  np.flip(g, 0), lat_gd, lon_gd)
b2 = griddata.stb(3, np.flip(lat_fy4a, 0), np.flip(lon_fy4a, 0),
                  np.flip(b, 0), lat_gd, lon_gd)
rgb2 = np.stack((r2, g2, b2))
cv2.imwrite(figname+'.grid.tiff', rgb2)
