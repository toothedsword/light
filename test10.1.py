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
import h5py as h5


infile = '/home/leon/src/light/cma2loc_2021-5-28_16.53.52/FY4A-_AGRI--_N_REGC_1047E_L2-_CTH-_MULT_NOM_20201028225336_20201028225753_4000M_V0001.NC'

f = h5.File(infile, 'r')
bln = f.attrs[u'Begin Line Number'][0]

f.close()
