import os
import sys
import re
import time
import glob
import time_htht as htt


while True:
    ct = time.time()
    year = htt.time2str(ct, 'yyyy')
    ymd = htt.time2str(ct, 'yyyymmdd')
    files = glob.glob(
        './AGRI/L1/FDI/DISK/' + year + '/' + ymd +
        '/FY4A-_AGRI--_N_DISK_1047E_L1-_FDI-_MULT_NOM_*_4000M_V0001.HDF')
    for infile in files:
        rn = '2'
        outfile = re.sub(r'\/AGRI\/', '/figure/', infile)
        outfile = re.sub(r'\.HDF$', '.TIFF', outfile)
        # outfile = re.sub(r'FY4A', 'FY4B', outfile)
        if os.path.exists(outfile):
            continue
        print(outfile)
        outdir = re.sub(r'[^\/]+$', '', outfile)
        if not(os.path.exists(outdir)):
            os.system('mkdir -p '+outdir)
        os.system("python3 ./disk_topo_tb.py "+infile+" "+rn+" "+outfile)
    time.sleep(1)
