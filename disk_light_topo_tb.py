#!/bin/python3

# import
import numpy as np
import h5py as h5
import gdal
import light
import cv2
import griddata
import sys
import re
import common
import os
import time
import traceback


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


if True:
    rgb = ((0.5, 0.2, 0), (0.9, 1, 0.8), (0, 1, 0))
    rgb = ((1, 1, 1), (0.8, 0.8, 0.8), (0.5, 0.5, 0.5))
    ns = [50, 50]
    tcc = gen_ccc(rgb, ns)

if False:
    rgb = ((0.2, 0.2, 0), (1, 1, 0), (0.5, 0, 0.5), (1, 0, 1), (1, 0.7, 1),
           (1, 1, 1), (0, 0, 0), (1, 0, 0),
           (1, 1, 0), (0, 1, 0), (0, 1, 1), (0, 0, 0))
    ns = [40, 0, 10, 10, 0, 20, 20, 20, 20, 40, 140]
    ch8 = gen_ccc(rgb, ns)

if True:
    rgb = ((0.2, 0.2, 0), (1, 1, 0), (0.5, 0, 0.5), (1, 0, 1), (1, 0.7, 1),
           (1, 1, 1), (0, 0, 0), (1, 0, 0),
           (1, 1, 0), (0, 1, 0), (0, 1, 1),
           (0, 0, 0), (1, 0, 0), (0, 1, 1), (0, 1, 0))
    ns = [40, 0, 10, 10, 0, 20, 20, 20, 20, 40, 140, 100, 50, 50]
    ch8 = gen_ccc(rgb, ns)

if False:
    rgb = ((1, 1, 1), (0, 0, 0), (1, 0, 0), (1, 1, 0), (0, 1, 0),
           (0, 0, 1), (0, 1, 1), (0.8, 0.8, 0.8), (0.1, 0.1, 0.1))
    ns = [10, 10, 10, 10, 10, 10, 10, 80]
    ch8 = gen_ccc(rgb, ns)


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


def gen_disk_light_topo_tb(infile, rn, outfile, cth_file, log_file, json_file):
    # {{{
    common.write_log(log_file, 'START disk_light_topo_tb')
    lat_fy4a = gdal.Open(
        './lut4k_1.tif').\
        ReadAsArray(0, 0, 2748, 2748)  # 纬度数据
    lon_fy4a = gdal.Open(
        './lut4k_2.tif').\
        ReadAsArray(0, 0, 2748, 2748)  # 经度数据
    
    f = h5.File(infile, 'r')
    Channel = 12
    NOMChannel = f['NOMChannel%s' % (Channel)][:]
    CALChannel = f['CALChannel%s' % (Channel)][:]
    tb = Data_Cal(NOMChannel, CALChannel)
    f.close()
    
    if False:
        cth_file = re.sub(r'\.HDF', r'.NC', infile)
        cth_file = re.sub(r'FDI', r'CTH', cth_file)
        cth_file = re.sub(r'L1', r'L2', cth_file)
        cth_file = re.sub(r'\/DISK\/', '/DISK/NOM/', cth_file)
    f = h5.File(cth_file, 'r')
    cth = f['CTH'][:]
    f.close()
    
    f = h5.File('topo_fy4a_4km.nc', 'r')
    topo = f['topo'][:]
    topo = np.flip(topo.T, 0)
    f.close()
    
    
    # tb[np.where(tb < 50)] = np.nan
    print(tb.dtype)
    # tb[np.where(cth < 0)] = tb[np.where(cth < 0)]+100
    
    if False:
        tb = cv2.resize(tb.astype(np.double), (2748*2, 2748*2))
        lon_fy4a = cv2.resize(lon_fy4a.astype(np.double), (2748*2, 2748*2))
        lat_fy4a = cv2.resize(lat_fy4a.astype(np.double), (2748*2, 2748*2))
        print(tb.shape)
    
    if True:
        x4 = np.linspace(0, 10, num=2748)
        y4 = np.linspace(0, 10, num=2748)
        x42, y42 = np.meshgrid(x4, y4)
        xo = np.linspace(0, 10, num=2748*rn)
        yo = np.linspace(0, 10, num=2748*rn)
        # id = np.where((tb > 0) & (lon_fy4a > -190) & (lat_fy4a > -100))
        sn = 4
        tb = griddata.stb(sn, x42, y42, tb, xo, yo).transpose()
        topo = griddata.stb(sn, x42, y42, topo, xo, yo).transpose()
        lon_fy4a = griddata.stb(sn, x42, y42, lon_fy4a, xo, yo)
        lat_fy4a = griddata.stb(sn, x42, y42, lat_fy4a, xo, yo)
        cth = griddata.stb(sn, x42, y42, cth, xo, yo).transpose()
    
    topo[np.where(cth > 0)] = cth[np.where(cth > 0)]
    topo = topo/1000
    # cth = 10-tb/20/100*50
    # topo[np.where(tb < -10+273.15)] = cth[np.where(tb < -10+273.15)]
    
    # imshow total
    # tb[np.where(tb < 50)] = np.nan
    rg = [-110+273.15, 50+100+273.15]
    # rg = [-90+273.15, 60+273.15]
    tb3 = num2rgb(tb, ch8, rg)
    
    if True:
        tb_nocloud = tb
        tb3_nocloud = num2rgb(tb_nocloud, tcc, [-50+273.15, 20+273.15])
        r = tb3[:,:,0]
        g = tb3[:,:,1]
        b = tb3[:,:,2]
        rn = tb3_nocloud[:,:,0]
        gn = tb3_nocloud[:,:,1]
        bn = tb3_nocloud[:,:,2]
        rn[np.where(cth > 0)] = r[np.where(cth > 0)] 
        gn[np.where(cth > 0)] = g[np.where(cth > 0)] 
        bn[np.where(cth > 0)] = b[np.where(cth > 0)] 
        # tb3[np.where(tb3_nocloud > 0)] = tb3_nocloud[np.where(tb3_nocloud > 0)]
        tb3[:,:,0] = rn
        tb3[:,:,1] = gn
        tb3[:,:,2] = bn
        # tb3 = tb3_nocloud
        print(tb3.shape)
        print(cth.shape)
    
    lt = light.point(lon_fy4a, lat_fy4a, topo, np.array([-1, 1, 1]))
    if True:
        lt[lt < 0] = 0
        lt = lt+0.3
        lt[lt > 1] = 1
    
    g = 3
    for i in range(0, 2):
        lt = cv2.filter2D(lt, -1, np.ones((g, g))) /\
            cv2.filter2D(np.ones(lt.shape), -1, np.ones((g, g)))
    
    tb4 = tb3+0
    # lt = lt*0+1
    tb4[:, :, 0] = tb3[:, :, 2]*lt
    tb4[:, :, 1] = tb3[:, :, 1]*lt
    tb4[:, :, 2] = tb3[:, :, 0]*lt
    cv2.imwrite(outfile, (tb4*255).astype(np.int32))
    common.write_log(log_file, 'FINISH disk_light_topo_tb')
    out_info = common.OutInfo(json_file)
    out_info.update_file_info(outfile, 'LIGHT', 'R')
    return out_info
    # }}}
    
if __name__ == '__main__':

    # read in data
    
    infile = sys.argv[1]
    cth_file = sys.argv[2]
    rn = int(sys.argv[3])
    output_dir = sys.argv[4]
    json_file = sys.argv[5]
    log_file = sys.argv[6]
    
    
    # 接口参数
    print('******************************************************')
    print('fy4_4000M,', infile)
    print('CTH_file,', cth_file)
    print('output_dir,', output_dir)
    print('json_file,', json_file)
    print('log_file,', log_file)
    tmp = re.search('FY4A-_AGRI--_N_(....)', infile)
    reg = tmp.group(1)

    tmp = re.search(r'(\d{4})(\d{2})(\d{2})(\d{6})_(\d{14})', infile)
    syear = tmp.group(1)
    smonth = tmp.group(2)
    sdom = tmp.group(3)
    shms = tmp.group(4)
    setime = tmp.group(5)

    out_file = output_dir+'/AGRI/L3/'+reg+'/HHMM/LIGHT-/NOM/' + \
            syear+'/'+syear+smonth+sdom+'/FY4A-_AGRI--_N_DISK_1047E_L3_LIGHT-_MULT_NOM_'+syear+smonth+sdom+shms+'_'+setime+'_'+str(int(4/rn))+'000M_HHMM_ADS_V0001.TIFF'
    out_path = re.sub(r'[^\/]+$','',out_file)
    if os.path.exists(out_path):
        pass
    else:
        os.system('mkdir -p ' + out_path)

    try:
        common.write_log(log_file, 'run FRDE')
        t1 = time.process_time()
        out_info = gen_disk_light_topo_tb(infile, rn, out_file, 
                   cth_file, log_file, json_file)
    except Exception as inst:
        # msg = ' '.join(['Fire_Detection:', str(inst.args)])
        msg = traceback.format_exc()  # 捕捉异常消息
        out_info = common.OutInfo(json_file)
        out_info.update('1', msg)
        common.write_log(log_file, msg)
    finally:
        t2 = time.process_time()
        lapse_time = t2 - t1
        msg = ' '.join(['program run', str(round(lapse_time, 2)), 'seconds'])
        common.write_log(log_file, msg)
        out_info.write_json()
