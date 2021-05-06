import os
import sys


rn = sys.argv[1]

filepath = './AGRI/L1/FDI/DISK/2019/20190304/' + \
   'FY4A-_AGRI--_N_DISK_1047E_L1-_FDI-_MULT_NOM_' + \
   '20190304040000_20190304041459_4000M_V0001.HDF'

os.system("python3 disk.py "+filepath+" "+rn)
