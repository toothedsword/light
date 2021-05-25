import os
import sys
import re


rn = sys.argv[1]
infile = './AGRI/L1/FDI/DISK/2019/20190304/' + \
   'FY4A-_AGRI--_N_DISK_1047E_L1-_FDI-_MULT_NOM_' + \
   '20190304040000_20190304041459_4000M_V0001.HDF'
infile = 'FY4A-_AGRI--_N_DISK_1047E_L1-_FDI-_MULT_NOM_' + \
   '20190304040000_20190304041459_4000M_V0001.HDF'
outfile = re.sub(r'.*\/', '', infile)
outfile = re.sub(r'\.HDF$', '.TIFF', outfile)

# os.system("python3 ./disk.py "+infile+" "+rn+" "+outfile)
os.system("python3 ./disk_topo_cth.py "+infile+" "+rn+" "+outfile)# {{{}}}
